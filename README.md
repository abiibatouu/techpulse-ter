# TechPulse - Observatoire de l'emploi tech × IA

Pipeline d'ingestion et analyse d'offres d'emploi tech en France via IA.

## Setup

### Prérequis
- Python 3.9+
- PostgreSQL 14+ (ou Docker)

### Installation

```bash
cp .env.example .env
# Remplir les variables (credentials API + DB)

pip install -r requirements.txt
```

### Lancer PostgreSQL

Docker :
```bash
docker-compose up -d
```

Ou local :
```bash
createdb techpulse
psql -U postgres -d techpulse -f ingestion/schema.sql
```

### Ingestion

Le pipeline est en **deux étapes** (Extract → Lac, puis Lac → DB) et **deux modes** :

```bash
# Chargement initial (1 fois au démarrage) : toutes les offres tech actives
python ingestion/run_france_travail.py --mode backfill

# Collecte quotidienne (à planifier) : ne récupère que les offres récentes
python ingestion/run_france_travail.py --mode quotidien

# Recharger uniquement le lac du jour vers la DB (sans rappeler l'API)
python ingestion/run_france_travail.py --skip-extract
```

Vérifier :
```bash
psql -d techpulse -c "SELECT COUNT(*) FROM offres;"
ls data/raw/france_travail/2026/  # contenu du lac
```

## Architecture

```
ingestion/
  config.py                   → codes ROME du périmètre + chemin du lac
  storage.py                  → backend de stockage (filesystem, plus tard S3/MinIO)
  lake.py                     → opérations sur le lac brut
  france_travail_client.py    → API France Travail (OAuth + pagination)
  db.py                       → écriture des offres en PostgreSQL
  run_france_travail.py       → orchestrateur (extract → lac → DB)
llm/                          → Extraction par LLM (S3)
dashboard/                    → Streamlit (S5)
data/raw/                     → lac (non versionné, cf .gitignore)
```

## Timeline

S1-S2 Ingestion → S3 LLM → S4 Taxonomie → S5-6 Dashboard → S7 DevOps → S8 Soutenance