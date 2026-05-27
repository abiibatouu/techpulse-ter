"""Point d'entree de l'ingestion France Travail.

Responsabilite unique : orchestrer le pipeline en deux etapes decouplees.

  Etape 1 - Extract -> Lac  : appelle l'API, ecrit les reponses brutes
                              dans le lac sans aucune transformation.

  Etape 2 - Lac    -> DB    : lit les fichiers du lac d'une journee,
                              parse les offres et les insere dans la
                              table 'offres' de PostgreSQL.

Deux modes de collecte :
  --mode backfill   : chargement initial, capture toutes les offres
                      actives actuellement (1 seule fois au demarrage).
  --mode quotidien  : ne recupere que les offres recentes (defaut).

Le module ne contient aucune logique metier : il enchaine les modules
france_travail_client, lake, storage, db et config.

Lancement, depuis la racine du projet :
    python ingestion/run_france_travail.py --mode quotidien
    python ingestion/run_france_travail.py --mode backfill
    python ingestion/run_france_travail.py --skip-extract  (recharge seulement)
"""
import argparse
from datetime import date, timedelta

from dotenv import load_dotenv

import france_travail_client
import db
import lake
import storage
import config


SOURCE_NOM = "france_travail"
JOURS_QUOTIDIEN = 2   # fenetre de la collecte quotidienne, en jours


def extract_to_lake(storage_, mode):
    """Etape 1 : recupere les offres depuis l'API et les ecrit dans le lac."""
    token = france_travail_client.get_access_token()
    today = date.today()

    min_creation_date = None
    if mode == "quotidien":
        depuis = today - timedelta(days=JOURS_QUOTIDIEN)
        min_creation_date = depuis.strftime("%Y-%m-%dT00:00:00Z")
        print(f"Collecte quotidienne : offres creees depuis {min_creation_date}")
    else:
        print("Backfill : toutes les offres actives actuelles")

    total_fichiers = 0
    for code_rome in config.ROME_CODES_TECH:
        print(f"  ROME {code_rome} ...", end=" ", flush=True)
        nb_pages = 0
        total_annonce = None
        for range_start, range_end, payload, total in france_travail_client.paginate(
            token, code_rome, min_creation_date=min_creation_date,
        ):
            if total_annonce is None:
                total_annonce = total
            lake.write_response(
                storage_, SOURCE_NOM, code_rome,
                range_start, range_end, payload, day=today,
            )
            nb_pages += 1
            total_fichiers += 1
        print(f"{nb_pages} pages, total annonce = {total_annonce}")

        # Alerte si on touche au plafond dur de l'API.
        if total_annonce and total_annonce > 1150:
            print(
                f"    ATTENTION : {total_annonce} offres pour {code_rome}, "
                f"plafond de 1150 atteint. Sous-decoupage par fenetre de "
                f"dates a implementer si besoin."
            )

    print(f"Extraction terminee : {total_fichiers} fichiers ecrits dans le lac.")


def load_to_db(storage_, day=None):
    """Etape 2 : lit les fichiers du lac d'une journee et insere en DB."""
    day = day or date.today()
    conn = db.get_connection()
    try:
        total_offres = 0
        total_inserees = 0
        for key, payload in lake.iter_responses(storage_, SOURCE_NOM, day):
            offres = payload.get("resultats") or []
            nb = db.store_offres(offres, SOURCE_NOM, conn)
            total_offres += len(offres)
            total_inserees += nb
        print(
            f"Chargement DB termine : {total_offres} offres lues, "
            f"{total_inserees} nouvelles inserees (les autres existaient deja)."
        )
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode", choices=["backfill", "quotidien"], default="quotidien",
        help="Mode de collecte (defaut : quotidien).",
    )
    parser.add_argument(
        "--skip-extract", action="store_true",
        help="Ne pas appeler l'API : recharger seulement le lac du jour vers la DB.",
    )
    args = parser.parse_args()

    load_dotenv()
    storage_ = storage.FilesystemStorage(config.LAKE_ROOT)

    if not args.skip_extract:
        print(f"=== Etape 1 : Extract -> Lac (mode = {args.mode}) ===")
        extract_to_lake(storage_, mode=args.mode)

    print("=== Etape 2 : Lac -> DB ===")
    load_to_db(storage_)


if __name__ == "__main__":
    main()
