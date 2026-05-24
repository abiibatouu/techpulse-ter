"""Point d'entree de l'ingestion France Travail.

Responsabilite unique : orchestrer le pipeline. Ce module enchaine les
etapes (jeton -> offres -> connexion -> stockage) en s'appuyant sur les
modules france_travail_client et db. Il ne contient aucune logique metier.

Lancement, depuis la racine du projet :
    python ingestion/run_france_travail.py
"""
from dotenv import load_dotenv

import france_travail_client
import db


def main():
    load_dotenv()
    token = france_travail_client.get_access_token()
    offres = france_travail_client.fetch_offres(token)
    conn = db.get_connection()
    db.store_offres(offres, conn)
    print("offres stockees avec succes")
    conn.close()


if __name__ == "__main__":
    main()
