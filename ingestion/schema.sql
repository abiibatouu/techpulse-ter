CREATE TABLE IF NOT EXISTS sources (
    id   SERIAL PRIMARY KEY,
    nom  VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO sources (nom) VALUES ('france_travail')
ON CONFLICT (nom) DO NOTHING;

INSERT INTO sources (nom) VALUES ('wttj')
ON CONFLICT (nom) DO NOTHING;

CREATE TABLE IF NOT EXISTS offres (
    id              VARCHAR         PRIMARY KEY,
    source_id       INTEGER         REFERENCES sources(id),
    intitule        TEXT,
    description     TEXT,
    date_creation   TIMESTAMP,
    lieu_libelle    TEXT,
    code_postal     VARCHAR(10),
    entreprise_nom  TEXT,
    type_contrat    VARCHAR(20),
    salaire_libelle TEXT,
    code_rome       VARCHAR(10),
    libelle_rome    TEXT,
    date_ingestion  TIMESTAMP       DEFAULT NOW(),
    raw_json        JSONB
);
CREATE TABLE IF NOT EXISTS offres_llm (
    offre_id        VARCHAR     PRIMARY KEY REFERENCES offres(id),
    competences     JSONB,
    seniorite       VARCHAR(20),
    salaire_min     INTEGER,
    salaire_max     INTEGER,
    jours_teletravail INTEGER,
    type_contrat    VARCHAR(20),
    mention_ia      BOOLEAN,
    date_extraction TIMESTAMP   DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS competences_normalisees (
    id              SERIAL PRIMARY KEY,
    offre_id        VARCHAR REFERENCES offres(id),
    competence_brute    TEXT,
    competence_canonique TEXT,
    categorie       VARCHAR(20),
    score_similarite INTEGER,
    date_normalisation TIMESTAMP DEFAULT NOW()
);