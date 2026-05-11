CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO sources (nom) VALUES ('france_travail'), ('wttj')
ON CONFLICT (nom) DO NOTHING;


CREATE TABLE offres (
    id VARCHAR(50) PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    intitule VARCHAR(255) NOT NULL,
    description TEXT,
    date_creation TIMESTAMP NOT NULL,
    lieu_libelle VARCHAR(255),
    code_postal VARCHAR(10),
    entreprise_nom VARCHAR(255),
    type_contrat VARCHAR(50),
    salaire_libelle VARCHAR(100),
    raw_json JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_offres_source ON offres(source_id);
CREATE INDEX idx_offres_date ON offres(date_creation DESC);

