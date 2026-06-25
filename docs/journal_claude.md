# Journal Claude — TechPulse

> Ce fichier est écrit par Claude Code à chaque modification du projet.
> Son but : t'expliquer ce qui a été fait, pourquoi, et ce que tu dois en retenir.
> Lis-le régulièrement pour apprendre en suivant l'avancement du projet.

---

<!-- Les entrées seront ajoutées ici par Claude Code, de la plus récente à la plus ancienne. -->

---

## 2026-06-25 — dashboard/ (analyses manquantes + onglets)

### Ce que j'ai fait
- Ajouté 3 nouvelles requêtes SQL dans `database.py` :
  - `get_ia_vs_classiques()` : évolution mensuelle IA vs compétences classiques
  - `get_correlation_seniorite_ia()` : % d'offres mentionnant l'IA par niveau de séniorité
  - `get_disparites_geo()` : Paris vs villes secondaires vs full remote
- Ajouté 3 graphiques dans `charts.py` : courbes temporelles, barres horizontales, scatter plot à bulles
- Restructuré `app.py` avec 4 onglets Streamlit pour séparer les angles d'analyse

### Pourquoi
- Ces 3 analyses étaient explicitement demandées dans l'énoncé (objectif 4 du PDF)
- Les onglets évitent un dashboard trop chargé et guident l'utilisateur question par question

### Comment ça marche (pour apprendre)

**Onglets Streamlit :**
```python
tab1, tab2, tab3 = st.tabs(["Nom 1", "Nom 2", "Nom 3"])
with tab1:
    st.write("contenu onglet 1")
```
Chaque `with tab:` délimite le contenu de l'onglet. Simple et efficace.

**Requête géographique avec CASE WHEN :**
```sql
CASE
    WHEN lieu_libelle ILIKE '%Paris%' THEN 'Paris'
    WHEN jours_teletravail::INTEGER >= 5 THEN 'Full remote'
    ELSE 'Villes secondaires'
END AS zone
```
`ILIKE` = comparaison insensible à la casse. `CASE WHEN` crée une colonne calculée à la volée —
on classe les données en catégories directement en SQL, sans post-traitement Python.

**`%%` dans les f-strings SQL avec psycopg2 :**
```python
sql = f"WHERE lieu ILIKE '%%Paris%%'"  # ← %% dans f-string = % littéral
```
Dans un f-string Python, `%` est un caractère spécial pour psycopg2 (début de paramètre `%s`).
Pour avoir un `%` littéral dans le SQL, on écrit `%%`.

**Scatter plot à bulles (px.scatter avec size=) :**
Encode 4 dimensions en un seul graphique :
- X → salaire médian
- Y → % IA
- Taille → nombre d'offres
- Couleur → zone géographique

### Ce qu'il faut retenir
- **`CASE WHEN`** permet de créer des catégories directement en SQL — plus efficace que de le faire en Python après
- **`ILIKE '%%Paris%%'`** : le double `%%` est obligatoire dans les f-strings Python avec psycopg2
- **`st.tabs()`** = façon propre d'organiser un dashboard multi-questions sans surcharger la page

---

## 2026-06-25 — dashboard/ (app.py, database.py, charts.py, filters.py)

### Ce que j'ai fait
- Créé le dashboard Streamlit en 4 fichiers avec séparation stricte des responsabilités
- `database.py` : toutes les requêtes SQL + connexion PostgreSQL
- `charts.py` : toutes les visualisations Plotly (barres, camembert, salaires, évolution)
- `filters.py` : widgets sidebar Streamlit (région, séniorité, catégorie, top N)
- `app.py` : orchestrateur qui connecte les 3 modules ci-dessus, zéro logique métier

### Pourquoi
- La soutenance est dans 4 jours, le dashboard est la pièce visible manquante
- Séparer SQL / graphiques / UI permet de modifier chaque partie sans casser les autres
- Cela applique les principes SOLID, notamment **S** (Single Responsibility) et **O** (Open/Closed)

### Comment ça marche (pour apprendre)

**Architecture en couches :**
```
app.py  →  database.py  (couche données : SQL)
        →  filters.py   (couche UI : widgets Streamlit)
        →  charts.py    (couche présentation : Plotly)
```
Chaque couche ne connaît que ce dont elle a besoin. `charts.py` ne sait pas que les données
viennent de PostgreSQL — il reçoit juste un DataFrame. Si demain on change de base de données,
on ne touche que `database.py`.

**`@st.cache_data(ttl=600)` dans app.py :**
Streamlit re-exécute tout le script à chaque interaction utilisateur. Sans cache, on interrogerait
la DB à chaque clic sur un filtre. `@st.cache_data` mémorise le résultat 600 secondes (10 min).

**`_build_where()` dans database.py :**
Plutôt que de dupliquer la construction de la clause WHERE dans chaque requête, une seule
fonction la fabrique dynamiquement selon les filtres actifs. C'est le principe **DRY** (Don't Repeat Yourself).

**Paramètres SQL via `%s` et non f-strings :**
```python
cursor.execute("WHERE lieu_libelle = %s", (region,))  # ✅ sécurisé
cursor.execute(f"WHERE lieu_libelle = '{region}'")    # ❌ injection SQL possible
```
Les paramètres `%s` sont échappés automatiquement par psycopg2 — protection contre les injections SQL.

### Ce qu'il faut retenir
- **Séparation des responsabilités** = chaque fichier a un rôle unique, le changement est localisé
- **`@st.cache_data`** = indispensable en Streamlit pour éviter des requêtes DB à chaque clic
- **Ne jamais construire du SQL avec des f-strings** sur des valeurs utilisateur (risque injection SQL)
