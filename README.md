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

```bash
python ingestion/run_france_travail.py
```

Vérifier :
```bash
psql -d techpulse -c "SELECT COUNT(*) FROM offres;"
```

## Architecture

```
ingestion/       → France Travail API + WTTJ scraping
llm/             → Extraction par LLM (S3)
dashboard/       → Streamlit (S5)
```

## Timeline

S1-S2 Ingestion → S3 LLM → S4 Taxonomie → S5-6 Dashboard → S7 DevOps → S8 Soutenance