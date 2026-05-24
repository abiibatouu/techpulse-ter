"""Acces a la base de donnees PostgreSQL.

Responsabilite unique : gerer la connexion a PostgreSQL et le stockage des
offres. Ce module ne connait rien de l'API France Travail.
"""
import os
import json

import psycopg2


def get_connection():
    """Ouvre une connexion PostgreSQL a partir des variables d'environnement."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def store_offres(offres, conn):
    """Insere les offres dans la table 'offres'.

    Les offres dont l'id existe deja sont ignorees (ON CONFLICT DO NOTHING).
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM sources WHERE nom = %s", ("france_travail",))
    source_id = cursor.fetchone()[0]
    for offre in offres["resultats"]:
        id = offre.get("id")
        intitule = offre.get("intitule")
        description = offre.get("description")
        date_creation = offre.get("dateCreation")
        lieu_libelle = offre.get("lieuTravail", {}).get("libelle")
        code_postal = offre.get("lieuTravail", {}).get("codePostal")
        entreprise_nom = offre.get("entreprise", {}).get("nom")
        type_contrat = offre.get("typeContrat")
        salaire_libelle = offre.get("salaire", {}).get("libelle")
        raw_json = json.dumps(offre)
        cursor.execute("""
            INSERT INTO offres (id, source_id, intitule, description, date_creation, lieu_libelle, code_postal, entreprise_nom, type_contrat, salaire_libelle, raw_json)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (id, source_id, intitule, description, date_creation, lieu_libelle, code_postal, entreprise_nom, type_contrat, salaire_libelle, raw_json))
    conn.commit()
