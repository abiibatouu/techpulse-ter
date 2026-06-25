# TechPulse — CLAUDE.md
> Fichier lu automatiquement par Claude Code à chaque session.
> Il décrit le projet, l'état d'avancement, les règles de travail et les conventions à respecter.

---

## 1. Présentation du projet

**TechPulse** est un observatoire de l'emploi tech alimenté par un pipeline de données automatisé.
Il collecte des offres d'emploi via l'API France Travail, les enrichit via un LLM (Mistral),
normalise les compétences extraites, et les expose dans un dashboard Streamlit.

- **Encadrant** : Jérémy GROS (jeremy.gros@naos.com)
- **Durée** : 8 semaines (4 mai → 26 juin 2026) — Soutenance semaine du 29 juin
- **Stack** : Python, PostgreSQL, Mistral API, RapidFuzz, Streamlit, Docker

---

## 2. Structure du projet

```
techpulse/
├── ingestion/
│   ├── config.py                  # Codes ROME tech (famille M18) + chemin lac
│   ├── db.py                      # Connexion PostgreSQL + insertion offres
│   ├── france_travail_client.py   # Client OAuth2 + pagination API France Travail
│   ├── lake.py                    # Lecture/écriture lac de données brutes
│   ├── storage.py                 # Abstraction FilesystemStorage (futur S3)
│   ├── run_france_travail.py      # Point d'entrée : Extract→Lac→DB
│   └── schema.sql                 # Schéma PostgreSQL des 4 tables
├── llm/
│   ├── extractor.py               # Orchestre l'extraction : prompt → Mistral → JSON
│   ├── mistral_client.py          # Client HTTP Mistral (get_client, call_llm)
│   ├── prompts.py                 # SYSTEM_PROMPT + build_extraction_prompt()
│   └── run_llm.py                 # Point d'entrée : offres sans LLM → offres_llm
├── taxonomy/
│   ├── taxonomy.py                # Dictionnaire TAXONOMY {compétence: catégorie}
│   ├── normalize.py               # Matching RapidFuzz contre TAXONOMY (seuil 80)
│   ├── enrich_llm.py              # Classifie via Mistral les compétences non matchées
│   └── run_taxonomy.py            # Point d'entrée : offres_llm → competences_normalisees
├── dashboard/                     # Interface Streamlit (à créer)
├── data/raw/                      # Lac de données brutes (NON versionné)
├── docs/
│   └── journal_claude.md          # Journal pédagogique (écrit par Claude Code)
├── .env                           # Variables d'environnement (NON versionné)
├── docker-compose.yml             # À créer en S7
└── CLAUDE.md                      # Ce fichier
```

---

## 3. Schéma de base de données

```sql
sources                    -- 'france_travail', 'wttj'
offres                     -- offres brutes (id, intitule, description, lieu, salaire, raw_json)
offres_llm                 -- extraction LLM par offre (competences JSON, seniorite, salaire_min/max,
                           --   jours_teletravail, type_contrat, mention_ia)
competences_normalisees    -- une ligne par (offre_id, competence_brute) avec
                           --   competence_canonique, categorie, score_similarite
```

**Relations** : `offres_llm.offre_id → offres.id` | `competences_normalisees.offre_id → offres.id`

**Note** : `offres.raw_json` est redondant avec le lac — sera retiré en S7.

---

## 4. Flux de données complet

```
API France Travail
      │  (france_travail_client.py : OAuth2 + pagination)
      ▼
  Lac brut (data/raw/)
      │  (lake.py + storage.py : fichiers JSON par date/ROME)
      ▼
  Table offres (PostgreSQL)
      │  (db.py : ON CONFLICT DO NOTHING)
      ▼
  Pipeline LLM (llm/)
      │  extractor.py appelle prompts.py + mistral_client.py
      │  → JSON : competences, seniorite, salaire, teletravail, mention_ia
      ▼
  Table offres_llm (PostgreSQL)
      │
      ▼
  Pipeline Taxonomie (taxonomy/)
      │  normalize.py : RapidFuzz contre TAXONOMY (seuil 80)
      │  enrich_llm.py : Mistral pour les compétences non matchées
      ▼
  Table competences_normalisees (PostgreSQL)
      │
      ▼
  Dashboard Streamlit (dashboard/)
```

---

## 5. Variables d'environnement (.env)

```env
FRANCE_TRAVAIL_CLIENT_ID=...
FRANCE_TRAVAIL_CLIENT_SECRET=...
DB_HOST=localhost
DB_PORT=5432
DB_NAME=techpulse
DB_USER=...
DB_PASSWORD=...
MISTRAL_API_KEY=...
```

---

## 6. État d'avancement détaillé

### ✅ Terminé et fonctionnel

**ingestion/**
- `france_travail_client.py` : OAuth2 client_credentials, pagination par Content-Range, plafond 1150
- `lake.py` : écriture/lecture avec convention `source/année/mois/jour/ROME_start-end.json`
- `storage.py` : Protocol Python + FilesystemStorage (extensible vers S3)
- `db.py` : connexion via env vars, `store_offres()` idempotente
- `config.py` : 6 codes ROME famille M18, chemin `data/raw`
- `run_france_travail.py` : modes `backfill` / `quotidien` / `--skip-extract`
- `schema.sql` : 4 tables créées avec contraintes

**llm/**
- `prompts.py` : SYSTEM_PROMPT + `build_extraction_prompt()` avec template JSON
- `mistral_client.py` : `get_client()` (retourne API key), `call_llm()` via HTTP
- `extractor.py` : `extract_from_description()` + nettoyage balises markdown + validation JSON
- `run_llm.py` : récupère offres sans LLM, appelle extractor, stocke dans offres_llm

**taxonomy/**
- `taxonomy.py` : ~80 compétences canoniques en 4 catégories (classique/ia_llm/emergente/soft_skill)
- `normalize.py` : `normaliser()` via RapidFuzz `token_sort_ratio`, seuil 80
- `run_taxonomy.py` : lit offres_llm, normalise chaque compétence brute, stocke résultats
- `enrich_llm.py` : classe via Mistral les compétences fréquentes non matchées (> 10 occurrences)

### ❌ À faire
- `dashboard/` : interface Streamlit (S5-S6)
- Analyses SQL temporelles et géographiques (S5)
- Scraping WTTJ via Playwright (S7, optionnel)
- `docker-compose.yml` (S7)
- Orchestration Prefect (S7)
- Remplacer `FilesystemStorage` par `S3Storage` (S7)
- Retirer `raw_json` de la table `offres` (S7)

---

## 7. Commandes utiles

```bash
# Ingestion
cd ingestion
python run_france_travail.py --mode quotidien
python run_france_travail.py --mode backfill
python run_france_travail.py --skip-extract   # recharge lac → DB seulement

# Pipeline LLM
cd llm
python run_llm.py

# Taxonomie
cd taxonomy
python run_taxonomy.py          # normalisation RapidFuzz
python enrich_llm.py            # enrichissement Mistral des non-matchées

# Dashboard (à créer)
streamlit run dashboard/app.py

# Init base de données
psql -U $DB_USER -d $DB_NAME -f ingestion/schema.sql
```

---

## 8. Conventions de code

- **Langue** : docstrings et commentaires en **français**, noms de variables/fonctions en **anglais**
- **Responsabilité unique** : chaque module a une seule responsabilité (pattern déjà en place)
- **`run_*.py`** : orchestration uniquement, zéro logique métier
- **Idempotence** : toute insertion DB utilise `ON CONFLICT DO NOTHING`
- **Pas de credentials en dur** : toujours via `os.getenv()` + `python-dotenv`
- **Imports relatifs** : dans `taxonomy/`, utiliser `sys.path.append("..")` pour accéder à `llm/`
- **Pas de `sudo`** sans demander explicitement
- **Validation LLM** : toujours tester sur un échantillon de 50 offres avant de lancer sur toute la base

---

## 🎓 RÈGLE PÉDAGOGIQUE — OBLIGATOIRE À CHAQUE MODIFICATION

> **À chaque fois que tu modifies ou crées un fichier, tu DOIS écrire dans `docs/journal_claude.md`.**

Utilise ce format exact :

```markdown
## [DATE] — [nom_du_fichier.py]

### Ce que j'ai fait
- Description courte et concrète de la modification

### Pourquoi
- La raison technique ou métier qui justifie ce choix

### Comment ça marche (pour apprendre)
- Explication pédagogique du concept utilisé
- Exemple concret si utile

### Ce qu'il faut retenir
- Point clé 1
- Point clé 2 (max 3 points)
```

**Ce journal est destiné à l'étudiant pour apprendre. Sois clair, vulgarise sans simplifier.**
Ne saute jamais cette étape, même pour une modification mineure.

---

## 9. Points d'attention importants

- **Plafond API France Travail** : 1150 résultats max par recherche. Si `total_annonce > 1150`,
  il faut sous-découper par fenêtre de dates (non encore implémenté — voir `run_france_travail.py`)
- **Coût LLM Mistral** : ne jamais lancer sur toute la base sans valider un échantillon d'abord
- **Le lac est immutable** : on n'écrase jamais un fichier existant, on écrit toujours de nouveaux fichiers
- **`data/raw/`** est dans `.gitignore` — ne pas versionner les données brutes
- **`enrich_llm.py`** génère du texte à copier dans `taxonomy.py` — l'ajout est manuel (contrôle qualité)

---

## 10. Prochaine tâche prioritaire

Créer le **dashboard Streamlit** (`dashboard/app.py`) pour répondre à la question :
> « Sur quelles technologies se former pour être compétitif en 2026 ? »

Filtres attendus : métier, région, séniorité.
Données sources : tables `competences_normalisees` + `offres` + `offres_llm`.
