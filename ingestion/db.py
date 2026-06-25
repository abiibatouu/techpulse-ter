"""Acces a la base de donnees PostgreSQL.

Responsabilite unique : gerer la connexion a PostgreSQL et le stockage
des offres. Ce module ne connait rien de l'API France Travail ni du lac.
Il recoit deja une liste d'offres (dicts) et les ecrit telles quelles.
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


def _source_id(cursor, source_nom):
    """Recupere l'id d'une source par son nom."""
    cursor.execute("SELECT id FROM sources WHERE nom = %s", (source_nom,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Source inconnue dans la table sources : {source_nom}")
    return row[0]


def store_offres(offres_list, source_nom, conn):
    """Insere une liste d'offres dans la table 'offres'.

    Parametres :
      - offres_list : liste de dicts (un dict = une offre, format API France Travail)
      - source_nom : nom de la source ('france_travail', 'wttj', ...)
      - conn : connexion PostgreSQL ouverte

    Idempotence : les offres dont l'id existe deja sont ignorees
    (ON CONFLICT DO NOTHING).

    Retourne le nombre d'offres effectivement inserees.
    """
    if not offres_list:
        return 0

    cursor = conn.cursor()
    source_id = _source_id(cursor, source_nom)

    nb_inserees = 0
    for offre in offres_list:
        id_ = offre.get("id")
        if not id_:
            continue
        intitule = offre.get("intitule")
        description = offre.get("description")
        date_creation = offre.get("dateCreation")
        lieu = offre.get("lieuTravail") or {}
        lieu_libelle = lieu.get("libelle")
        code_postal = lieu.get("codePostal")
        entreprise = offre.get("entreprise") or {}
        entreprise_nom = entreprise.get("nom")
        type_contrat = offre.get("typeContrat")
        salaire = offre.get("salaire") or {}
        salaire_libelle = salaire.get("libelle")
        # Code metier ROME : sert aux filtres et analyses "par metier".
        code_rome = offre.get("romeCode")
        libelle_rome = offre.get("romeLibelle")
        # raw_json reste pour l'instant : redondant avec le lac, sera retire en S7.
        raw_json = json.dumps(offre, ensure_ascii=False)

        cursor.execute("""
            INSERT INTO offres (
                id, source_id, intitule, description, date_creation,
                lieu_libelle, code_postal, entreprise_nom, type_contrat,
                salaire_libelle, code_rome, libelle_rome, raw_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            id_, source_id, intitule, description, date_creation,
            lieu_libelle, code_postal, entreprise_nom, type_contrat,
            salaire_libelle, code_rome, libelle_rome, raw_json,
        ))
        nb_inserees += cursor.rowcount

    conn.commit()
    return nb_inserees
