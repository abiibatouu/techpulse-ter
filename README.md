# TechPulse - Observatoire de l'emploi tech × IA

Pipeline d'ingestion et analyse d'offres d'emploi tech en France via IA.

## Déploiement Docker (une commande)

Tout le projet (PostgreSQL + dashboard Streamlit) démarre avec une seule commande :

```bash
cp .env.example .env
# Remplir les variables : credentials API France Travail, clé Mistral, DB

docker compose up --build
```

- Dashboard Streamlit : http://localhost:8501
- pgAdmin : http://localhost:5050
- Le schéma PostgreSQL est créé automatiquement au premier démarrage (via `ingestion/schema.sql`).

### Alimenter la base (pipeline) via Docker

La base démarre vide. Les trois étapes du pipeline se lancent dans le conteneur applicatif :

```bash
docker compose run --rm dashboard python ingestion/run_france_travail.py --mode backfill
docker compose run --rm dashboard python llm/run_llm.py
docker compose run --rm dashboard python taxonomy/run_taxonomy.py
```

## Installation locale (sans Docker)

### Prérequis
- Python 3.9+
- PostgreSQL 14+

```bash
cp .env.example .env       # remplir les credentials
pip install -r requirements.txt
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

### Extraction LLM puis taxonomie

```bash
python llm/run_llm.py                 # extrait competences/salaire/... via Mistral -> offres_llm
python llm/run_llm.py --limit 10      # mode test sur 10 offres
python taxonomy/run_taxonomy.py       # normalise les competences -> competences_normalisees
```

### Lancer le dashboard en local

```bash
streamlit run dashboard/app.py
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
llm/                          → Extraction par LLM Mistral (S3)
taxonomy/                     → Normalisation des compétences (S4)
dashboard/                    → Dashboard Streamlit (S5-6)
data/raw/                     → lac (non versionné, cf .gitignore)
Dockerfile / docker-compose.yml → déploiement (PostgreSQL + dashboard)
```

## Timeline

S1-S2 Ingestion → S3 LLM → S4 Taxonomie → S5-6 Dashboard → S7 DevOps → S8 Soutenance