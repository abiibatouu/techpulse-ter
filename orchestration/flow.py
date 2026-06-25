"""Orchestration Prefect du pipeline TechPulse.

Responsabilite unique : enchainer les 3 etapes du pipeline dans l'ordre et
permettre de les planifier automatiquement (ex : une collecte quotidienne).

  ingestion  ->  extraction LLM  ->  (reset) taxonomie

Chaque etape reutilise les scripts existants (lances en sous-processus), de
sorte que l'orchestrateur ne duplique aucune logique metier : il se contente
de les ordonner, de les reessayer en cas d'echec et de tracer les logs.

Usage :
    # Un seul run, tout de suite (collecte incrementale du jour) :
    python orchestration/flow.py

    # Un run en mode chargement complet :
    python orchestration/flow.py --mode backfill

    # Planifier le pipeline tous les jours a 06h00 (laisser le process tourner) :
    python orchestration/flow.py --serve
"""
import argparse
import os
import subprocess
import sys

import psycopg2
from dotenv import load_dotenv
from prefect import flow, task, get_run_logger

# Racine du projet (un cran au-dessus de ce fichier) : les scripts s'executent
# depuis la pour que leurs imports relatifs fonctionnent comme en lancement manuel.
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _run_script(args: list[str]) -> str:
    """Lance un script Python du projet depuis la racine et remonte ses logs.

    Leve une exception si le script renvoie un code de sortie non nul, ce qui
    fait echouer la task Prefect (et declenche les retries eventuels).
    """
    logger = get_run_logger()
    logger.info("Execution : python %s", " ".join(args))
    res = subprocess.run(
        [sys.executable, *args],
        cwd=RACINE,
        capture_output=True,
        text=True,
    )
    if res.stdout:
        logger.info(res.stdout.strip())
    if res.returncode != 0:
        logger.error(res.stderr.strip())
        raise RuntimeError(f"Echec de : python {' '.join(args)}")
    return res.stdout


@task(name="Ingestion France Travail", retries=2, retry_delay_seconds=60)
def ingestion(mode: str = "quotidien") -> None:
    """Etape 1 : API France Travail -> lac -> PostgreSQL."""
    _run_script(["ingestion/run_france_travail.py", "--mode", mode])


@task(name="Extraction LLM", retries=1, retry_delay_seconds=120)
def extraction_llm() -> None:
    """Etape 2 : offres non traitees -> Mistral -> table offres_llm."""
    _run_script(["llm/run_llm.py"])


@task(name="Reset taxonomie")
def reset_taxonomie() -> None:
    """Vide competences_normalisees avant recalcul.

    Necessaire car la table n'est pas idempotente (cle primaire SERIAL) :
    relancer la normalisation sans vider dupliquerait toutes les lignes.
    """
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    try:
        with conn, conn.cursor() as cur:
            cur.execute("TRUNCATE competences_normalisees")
    finally:
        conn.close()


@task(name="Taxonomie")
def taxonomie() -> None:
    """Etape 3 : normalisation des competences -> competences_normalisees."""
    _run_script(["taxonomy/run_taxonomy.py"])


@flow(name="techpulse-pipeline")
def pipeline(mode: str = "quotidien") -> None:
    """Pipeline complet TechPulse, etapes executees en sequence.

    Les appels directs (sans .submit) sont bloquants : chaque etape attend
    la precedente, ce qui garantit l'ordre ingestion -> LLM -> taxonomie.
    """
    ingestion(mode)
    extraction_llm()
    reset_taxonomie()
    taxonomie()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode", choices=["backfill", "quotidien"], default="quotidien",
        help="Mode de collecte (defaut : quotidien).",
    )
    parser.add_argument(
        "--serve", action="store_true",
        help="Planifier le pipeline tous les jours a 06h00 (laisser tourner).",
    )
    args = parser.parse_args()

    if args.serve:
        # Cree un deploiement planifie ; le pipeline s'execute selon le cron
        # tant que ce process reste actif. Cron "0 6 * * *" = tous les jours a 6h.
        pipeline.serve(name="techpulse-quotidien", cron="0 6 * * *")
    else:
        pipeline(mode=args.mode)
