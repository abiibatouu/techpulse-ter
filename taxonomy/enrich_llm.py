"""Enrichissement automatique de la taxonomie par LLM.

Responsabilite unique : classer automatiquement les competences
frequentes non matchees en utilisant Mistral.
Ce module ne connait pas la base de donnees directement - 
il recoit une liste de competences et retourne leur categorie.
"""
import psycopg2
import os
import sys
sys.path.append("..")
from dotenv import load_dotenv
import llm.mistral_client as mistral_client


def get_competences_frequentes(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT competence_brute
        FROM competences_normalisees
        WHERE competence_canonique IS NULL
        GROUP BY competence_brute
        HAVING COUNT(*) > 10
        ORDER BY COUNT(*) DESC
    """)
    return [row[0] for row in cursor.fetchall()]


def classifier_competence(client, competence):
    """Demande a Mistral de classer une competence dans une categorie."""
    prompt = f"""Classe cette competence technique dans UNE SEULE categorie.
Reponds UNIQUEMENT avec un de ces mots : classique, ia_llm, emergente, soft_skill, hors_scope

- classique : SQL, Python, Java, Docker, Git, outils BI, bases de donnees...
- ia_llm : LangChain, RAG, Ollama, prompt engineering, LLM, IA generative...
- emergente : dbt, DuckDB, Prefect, Airflow, Spark, Kafka, Kubernetes...
- soft_skill : communication, gestion de projet, anglais, management...
- hors_scope : trop generique, non technique, ou hors domaine tech

Competence : {competence}
Categorie :"""

    reponse = mistral_client.call_llm(client, "", prompt)
    reponse = reponse.strip().lower()

    categories_valides = ["classique", "ia_llm", "emergente", "soft_skill", "hors_scope"]
    if reponse in categories_valides:
        return reponse
    return None


def main():
    load_dotenv()

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    competences = get_competences_frequentes(conn)
    conn.close()
    print(f"{len(competences)} competences a classifier")

    client = mistral_client.get_client()

    nouvelles_entrees = {}
    for comp in competences:
        categorie = classifier_competence(client, comp)
        if categorie and categorie != "hors_scope":
            nouvelles_entrees[comp] = categorie
            print(f"OK : {comp} -> {categorie}")
        else:
            print(f"HORS SCOPE : {comp}")

    print(f"\n{len(nouvelles_entrees)} nouvelles competences classifiees")
    print("\nA ajouter dans taxonomy.py :")
    for comp, cat in nouvelles_entrees.items():
        print(f'    "{comp}": "{cat}",')


if __name__ == "__main__":
    main()