"""Accès aux données pour le dashboard.

Responsabilité unique : exécuter les requêtes SQL et retourner des DataFrames.
Ce module ne sait rien de Streamlit, ni de Plotly.
Toute la logique de filtrage SQL est ici — l'interface ne construit jamais de SQL.

Pourquoi SQLAlchemy plutôt que psycopg2 brut ?
→ pandas.read_sql_query() est optimisé pour SQLAlchemy et émet un warning sinon.
→ SQLAlchemy gère aussi mieux le pool de connexions.
→ Les paramètres nommés (:region) sont plus lisibles que les %s positionnels.
"""

import os
import pandas as pd
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Connexion (psycopg2 — cohérent avec ingestion/db.py)
# ---------------------------------------------------------------------------

def get_connection():
    """Ouvre une connexion PostgreSQL depuis les variables d'environnement."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def _query(sql: str, params: dict | None = None) -> pd.DataFrame:
    """Exécute une requête psycopg2 et retourne un DataFrame sans warning pandas.

    Pourquoi ne pas utiliser pd.read_sql_query() ?
    → pandas émet un warning quand on lui passe une connexion psycopg2 brute
      (il préfère SQLAlchemy). Pour l'éviter sans changer de librairie, on
      récupère les données via cursor.fetchall() et on construit le DataFrame
      manuellement à partir de cursor.description (qui donne les noms de colonnes).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            colonnes = [desc[0] for desc in cur.description]
            lignes = cur.fetchall()
        return pd.DataFrame(lignes, columns=colonnes)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Construction dynamique des filtres WHERE
# ---------------------------------------------------------------------------

def _build_where(
    region: str | None,
    seniorite: str | None,
    metier: str | None = None,
) -> tuple[str, dict]:
    """Construit la clause WHERE et le dict de paramètres correspondant.

    Retourne (clause_sql, params_dict).
    Exemple : ("WHERE o.lieu_libelle = :region", {"region": "Paris"})

    Principe Open/Closed : pour ajouter un filtre, on étend ici uniquement.
    """
    conditions = []
    params: dict = {}

    if region:
        conditions.append("o.lieu_libelle = %(region)s")
        params["region"] = region

    if seniorite:
        conditions.append("ol.seniorite = %(seniorite)s")
        params["seniorite"] = seniorite

    if metier:
        conditions.append("o.code_rome = %(metier)s")
        params["metier"] = metier

    where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
    return where, params


# ---------------------------------------------------------------------------
# Valeurs de filtres (pour peupler les selectbox)
# ---------------------------------------------------------------------------

def get_regions() -> list[str]:
    """Retourne les 50 régions les plus fréquentes."""
    df = _query("""
        SELECT lieu_libelle, COUNT(*) AS nb
        FROM offres
        WHERE lieu_libelle IS NOT NULL
        GROUP BY lieu_libelle
        ORDER BY nb DESC
        LIMIT 50
    """)
    return df["lieu_libelle"].tolist()


def get_seniorites() -> list[str]:
    """Retourne les niveaux de séniorité distincts."""
    df = _query("""
        SELECT DISTINCT seniorite
        FROM offres_llm
        WHERE seniorite IS NOT NULL
        ORDER BY seniorite
    """)
    return df["seniorite"].tolist()


def get_categories() -> list[str]:
    """Retourne les catégories de compétences disponibles."""
    df = _query("""
        SELECT DISTINCT categorie
        FROM competences_normalisees
        WHERE categorie IS NOT NULL
        ORDER BY categorie
    """)
    return df["categorie"].tolist()


def get_metiers() -> list[tuple[str, str]]:
    """Retourne les métiers du périmètre : (code_rome, libellé représentatif).

    On regroupe par CODE et non par libellé : France Travail renvoie plusieurs
    variantes de libellé pour un même code ROME (ex : "-DSI-" vs "(DSI)"), alors
    que le code, lui, est stable. Le plus fréquent d'abord.
    """
    df = _query("""
        SELECT code_rome, MIN(libelle_rome) AS libelle, COUNT(*) AS nb
        FROM offres
        WHERE code_rome IS NOT NULL
        GROUP BY code_rome
        ORDER BY nb DESC
    """)
    return list(zip(df["code_rome"], df["libelle"]))


# ---------------------------------------------------------------------------
# Requêtes principales
# ---------------------------------------------------------------------------

def get_top_competences(
    region: str | None = None,
    seniorite: str | None = None,
    categorie: str | None = None,
    top_n: int = 20,
    metier: str | None = None,
) -> pd.DataFrame:
    """Top N compétences par nombre d'offres.

    Colonnes : competence_canonique, categorie, nb_offres.
    """
    where, params = _build_where(region, seniorite, metier)

    # Exclure les competences non matchees (canonique NULL) : elles formaient
    # une fausse ligne "None" qui dominait le classement et le tableau.
    connector = "AND" if where else "WHERE"
    where += f" {connector} cn.competence_canonique IS NOT NULL"

    if categorie:
        where += " AND cn.categorie = %(categorie)s"
        params["categorie"] = categorie

    params["top_n"] = top_n

    sql = f"""
        SELECT
            cn.competence_canonique,
            cn.categorie,
            COUNT(DISTINCT cn.offre_id) AS nb_offres
        FROM competences_normalisees cn
        JOIN offres o ON o.id = cn.offre_id
        JOIN offres_llm ol ON ol.offre_id = cn.offre_id
        {where}
        GROUP BY cn.competence_canonique, cn.categorie
        ORDER BY nb_offres DESC
        LIMIT %(top_n)s
    """
    return _query(sql, params)


def get_repartition_categories(
    region: str | None = None,
    seniorite: str | None = None,
    metier: str | None = None,
) -> pd.DataFrame:
    """Nombre d'offres par catégorie de compétence.

    Colonnes : categorie, nb_offres.
    """
    where, params = _build_where(region, seniorite, metier)

    sql = f"""
        SELECT
            cn.categorie,
            COUNT(DISTINCT cn.offre_id) AS nb_offres
        FROM competences_normalisees cn
        JOIN offres o ON o.id = cn.offre_id
        JOIN offres_llm ol ON ol.offre_id = cn.offre_id
        {where}
        GROUP BY cn.categorie
        ORDER BY nb_offres DESC
    """
    return _query(sql, params)


def get_salaire_par_competence(
    region: str | None = None,
    metier: str | None = None,
    top_n: int = 12,
) -> pd.DataFrame:
    """Salaire moyen min/max pour les compétences les mieux rémunérées.

    Répond à : 'Quelles compétences sont associées aux meilleurs salaires ?'
    Colonnes : competence_canonique, categorie, salaire_min_moyen, salaire_max_moyen, nb_offres.
    """
    conditions = ["ol.salaire_min IS NOT NULL", "ol.salaire_max IS NOT NULL"]
    params: dict = {}

    if region:
        conditions.append("o.lieu_libelle = %(region)s")
        params["region"] = region
    if metier:
        conditions.append("o.code_rome = %(metier)s")
        params["metier"] = metier

    where = "WHERE " + " AND ".join(conditions)
    params["top_n"] = top_n

    sql = f"""
        SELECT
            cn.competence_canonique,
            cn.categorie,
            ROUND(AVG(ol.salaire_min)) AS salaire_min_moyen,
            ROUND(AVG(ol.salaire_max)) AS salaire_max_moyen,
            COUNT(DISTINCT cn.offre_id) AS nb_offres
        FROM competences_normalisees cn
        JOIN offres o  ON o.id = cn.offre_id
        JOIN offres_llm ol ON ol.offre_id = cn.offre_id
        {where}
        GROUP BY cn.competence_canonique, cn.categorie
        HAVING COUNT(DISTINCT cn.offre_id) >= 3
        ORDER BY salaire_max_moyen DESC
        LIMIT %(top_n)s
    """
    df = _query(sql, params)
    for col in ["salaire_min_moyen", "salaire_max_moyen"]:
        if col in df.columns:
            df[col] = df[col].astype(float)
    return df


def get_salaire_par_seniorite(
    region: str | None = None,
) -> pd.DataFrame:
    """Salaire moyen min/max par niveau de séniorité.

    Colonnes : seniorite, salaire_min_moyen, salaire_max_moyen, nb_offres.
    """
    conditions = ["ol.salaire_min IS NOT NULL", "ol.salaire_max IS NOT NULL"]
    params: dict = {}

    if region:
        conditions.append("o.lieu_libelle = %(region)s")
        params["region"] = region

    where = "WHERE " + " AND ".join(conditions)

    sql = f"""
        SELECT
            ol.seniorite,
            ROUND(AVG(ol.salaire_min)) AS salaire_min_moyen,
            ROUND(AVG(ol.salaire_max)) AS salaire_max_moyen,
            COUNT(*) AS nb_offres
        FROM offres_llm ol
        JOIN offres o ON o.id = ol.offre_id
        {where}
        GROUP BY ol.seniorite
        ORDER BY salaire_min_moyen DESC
    """
    return _query(sql, params)


def get_evolution_temporelle(
    region: str | None = None,
    seniorite: str | None = None,
) -> pd.DataFrame:
    """Nombre d'offres publiées par semaine.

    Colonnes : semaine, nb_offres.
    """
    where, params = _build_where(region, seniorite)

    sql = f"""
        SELECT
            DATE_TRUNC('week', o.date_creation) AS semaine,
            COUNT(DISTINCT o.id) AS nb_offres
        FROM offres o
        JOIN offres_llm ol ON ol.offre_id = o.id
        {where}
        GROUP BY semaine
        ORDER BY semaine
    """
    return _query(sql, params)


def get_ia_vs_classiques(
    region: str | None = None,
    seniorite: str | None = None,
    metier: str | None = None,
) -> pd.DataFrame:
    """Évolution mensuelle : nombre d'offres avec compétences IA vs classiques.

    Répond à : "Est-ce que les compétences IA prennent de la place sur les classiques ?"
    Colonnes : mois, categorie, nb_offres.
    """
    where, params = _build_where(region, seniorite, metier)
    connector = "AND" if where else "WHERE"

    sql = f"""
        SELECT
            DATE_TRUNC('month', o.date_creation)    AS mois,
            cn.categorie,
            COUNT(DISTINCT cn.offre_id)             AS nb_offres
        FROM competences_normalisees cn
        JOIN offres o  ON o.id = cn.offre_id
        JOIN offres_llm ol ON ol.offre_id = cn.offre_id
        {where}
        {connector} cn.categorie IN ('ia_llm', 'classique')
        GROUP BY mois, cn.categorie
        ORDER BY mois
    """
    return _query(sql, params)


def get_correlation_seniorite_ia(
    region: str | None = None,
    metier: str | None = None,
) -> pd.DataFrame:
    """Corrélation séniorité × présence de l'IA dans les offres.

    Répond à : "Les offres senior mentionnent-elles plus l'IA ?"
    Colonnes : seniorite, total_offres, offres_ia, pct_ia.
    """
    conditions = ["ol.seniorite IS NOT NULL"]
    params: dict = {}

    if region:
        conditions.append("o.lieu_libelle = %(region)s")
        params["region"] = region
    if metier:
        conditions.append("o.code_rome = %(metier)s")
        params["metier"] = metier

    where = "WHERE " + " AND ".join(conditions)

    sql = f"""
        SELECT
            ol.seniorite,
            COUNT(*)                                                        AS total_offres,
            SUM(CASE WHEN ol.mention_ia THEN 1 ELSE 0 END)                 AS offres_ia,
            ROUND(100.0 * SUM(CASE WHEN ol.mention_ia THEN 1 ELSE 0 END)
                  / NULLIF(COUNT(*), 0))                                    AS pct_ia
        FROM offres_llm ol
        JOIN offres o ON o.id = ol.offre_id
        {where}
        GROUP BY ol.seniorite
        ORDER BY pct_ia DESC
    """
    return _query(sql, params)


def get_disparites_geo(metier: str | None = None) -> pd.DataFrame:
    """Disparités Paris / villes secondaires / full remote.

    Répond à : "Est-ce que Paris domine toujours le marché tech ?"
    On classe les offres en 3 zones :
      - Paris       : lieu_libelle contient "Paris"
      - Full remote : jours_teletravail >= 5
      - Secondaires : tout le reste
    Colonnes : zone, nb_offres, salaire_median, pct_ia, teletravail_moyen.
    """
    sql = """
        SELECT
            CASE
                WHEN o.lieu_libelle ILIKE '%%Paris%%' THEN 'Paris'
                WHEN ol.jours_teletravail ~ '^[0-9]+$' AND ol.jours_teletravail::numeric >= 5 THEN 'Full remote'
                ELSE 'Villes secondaires'
            END                                                             AS zone,
            COUNT(DISTINCT o.id)                                            AS nb_offres,
            ROUND(AVG(
                CASE WHEN ol.salaire_min IS NOT NULL AND ol.salaire_max IS NOT NULL
                     THEN (ol.salaire_min + ol.salaire_max) / 2.0
                     ELSE NULL END
            ))                                                              AS salaire_median,
            ROUND(100.0 * SUM(CASE WHEN ol.mention_ia THEN 1 ELSE 0 END)
                  / NULLIF(COUNT(*), 0))                                    AS pct_ia,
            ROUND(AVG(CASE WHEN ol.jours_teletravail ~ '^[0-9]+$' THEN ol.jours_teletravail::numeric END)) AS teletravail_moyen
        FROM offres o
        JOIN offres_llm ol ON ol.offre_id = o.id
        GROUP BY zone
        ORDER BY nb_offres DESC
    """
    return _query(sql)


def get_kpis(
    region: str | None = None,
    seniorite: str | None = None,
    metier: str | None = None,
) -> dict:
    """Indicateurs clés : nb offres, nb compétences uniques, % mention IA, télétravail.

    jours_teletravail est un INTEGER (NULL si non numérique, garanti par la
    normalisation dans extractor.py), donc AVG() s'applique directement.
    """
    where, params = _build_where(region, seniorite, metier)

    df = _query(f"""
        SELECT
            COUNT(DISTINCT o.id)                                        AS nb_offres,
            COUNT(DISTINCT cn.competence_canonique)                     AS nb_competences,
            ROUND(100.0 * SUM(CASE WHEN ol.mention_ia THEN 1 ELSE 0 END)
                  / NULLIF(COUNT(*), 0))                                AS pct_ia,
            ROUND(AVG(CASE WHEN ol.jours_teletravail ~ '^[0-9]+$' THEN ol.jours_teletravail::numeric END)) AS teletravail_moyen
        FROM offres o
        JOIN offres_llm ol ON ol.offre_id = o.id
        LEFT JOIN competences_normalisees cn ON cn.offre_id = o.id
        {where}
    """, params)

    row = df.iloc[0]
    return {
        "nb_offres":        int(row["nb_offres"] or 0),
        "nb_competences":   int(row["nb_competences"] or 0),
        "pct_ia":           int(row["pct_ia"] or 0),
        "teletravail_moyen": float(row["teletravail_moyen"] or 0),
    }
