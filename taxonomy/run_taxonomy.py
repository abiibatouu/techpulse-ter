"""Point d'entree de la normalisation des competences.

Responsabilite unique : orchestrer la normalisation - lire les
competences brutes depuis offres_llm, appeler le normaliseur,
stocker les resultats dans competences_normalisees.
"""
import os
import json
from dotenv import load_dotenv
import psycopg2
import normalize


def get_competences_a_normaliser(conn):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT offre_id, competences
        FROM offres_llm
        WHERE competences IS NOT NULL
    """)
    return cursor.fetchall()


def store_competence(conn, offre_id, competence_brute, resultat):
    cursor = conn.cursor()
    if resultat is None:
        competence_canonique = None
        categorie = None
        score = None
    else:
        competence_canonique, categorie, score = resultat

    cursor.execute("""
        INSERT INTO competences_normalisees (
            offre_id, competence_brute, competence_canonique,
            categorie, score_similarite
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT DO NOTHING
    """, (offre_id, competence_brute, competence_canonique, categorie, score))
    conn.commit()


def main():
    load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    rows = get_competences_a_normaliser(conn)
    print(f"{len(rows)} offres a normaliser")

    total_comp = 0
    total_matchees = 0

    for offre_id, competences_json in rows:
        if isinstance(competences_json, list):
            competences = competences_json
        else:
            competences = json.loads(competences_json)
        for comp_brute in competences:
            resultat = normalize.normaliser(comp_brute)
            store_competence(conn, offre_id, comp_brute, resultat)
            total_comp += 1
            if resultat:
                total_matchees += 1

    print(f"Total : {total_comp} competences traitees, {total_matchees} matchees")
    conn.close()


if __name__ == "__main__":
    main()