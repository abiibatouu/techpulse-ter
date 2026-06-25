import os
from dotenv import load_dotenv
import psycopg2
import extractor
import mistral_client
import json
import sys

def get_offres_sans_llm(conn, limit=None):
    cursor = conn.cursor()
    query = """
        SELECT o.id, o.description 
        FROM offres o
        LEFT JOIN offres_llm llm ON o.id = llm.offre_id
        WHERE llm.offre_id IS NULL
        AND o.description IS NOT NULL
    """
    if limit:
        query += f" LIMIT {int(limit)}"
    cursor.execute(query)
    return cursor.fetchall()
def store_llm_result(conn, offre_id, result):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO offres_llm (
            offre_id, competences, seniorite, salaire_min,
            salaire_max, jours_teletravail, type_contrat, mention_ia
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (offre_id) DO NOTHING
    """, (
        offre_id,
        json.dumps(result.get("competences", []), ensure_ascii=False),
        result.get("seniorite"),
        result.get("salaire_min"),
        result.get("salaire_max"),
        result.get("jours_teletravail"),
        result.get("type_contrat"),
        result.get("mention_ia"),
    ))
    conn.commit()
    
def main():
    load_dotenv()
    
    # Parser les arguments
    limit = None
    if "--limit" in sys.argv:
        idx = sys.argv.index("--limit")
        if idx + 1 < len(sys.argv):
            limit = int(sys.argv[idx + 1])
    
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    client = mistral_client.get_client()
    offres = get_offres_sans_llm(conn, limit=limit)
    print(f"{len(offres)} offres a traiter (limit={limit})")
    
    for idx, (offre_id, description) in enumerate(offres, 1):
        try:
            result = extractor.extract_from_description(description, client)
            store_llm_result(conn, offre_id, result)
            print(f"[{idx}/{len(offres)}] OK : {offre_id}")
        except Exception as e:
            conn.rollback()
            print(f"[{idx}/{len(offres)}] ERREUR {offre_id} : {e}")
if __name__ == "__main__":
    main()