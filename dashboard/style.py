"""Système de design TechPulse, style suisse / international.

Responsabilité unique : définir les styles CSS et les composants HTML réutilisables.
Aucune logique métier, aucune requête SQL ici.

Principes : monochrome « encre » + un seul accent (rouge signal), filets fins
plutôt que cartes, coins droits, typographie Helvetica, beaucoup de blanc.
Pas de dégradé, pas de pilule, pas de palette arc-en-ciel.
"""

# ---------------------------------------------------------------------------
# Palette : monochrome « encre » + un unique accent
# ---------------------------------------------------------------------------

ENCRE      = "#141414"   # quasi-noir : texte et série de données principale
GRIS_FORT  = "#5A5A5A"
GRIS       = "#8C8C8C"
GRIS_CLAIR = "#C2C2C2"
FILET      = "#E4E4E4"   # filets (hairlines)
ACCENT     = "#E2231A"   # rouge signal, réservé à l'emphase (IA, sélection)

# Couleurs par catégorie : tout en encre/gris, l'IA seule en accent.
# Choix éditorial : le rouge fait ressortir la donnée « IA », qui est le sujet
# du tableau de bord.
COULEURS = {
    "classique":  ENCRE,
    "ia_llm":     ACCENT,
    "emergente":  GRIS,
    "soft_skill": GRIS_CLAIR,
}

LABELS_CATEGORIES = {
    "classique":  "Classique",
    "ia_llm":     "IA / LLM",
    "emergente":  "Émergente",
    "soft_skill": "Soft Skill",
}

COULEURS_ZONES = {
    "Paris":              ENCRE,
    "Full remote":        ACCENT,
    "Villes secondaires": GRIS,
}

# Thème Plotly appliqué à tous les graphiques
_FONT = "'Helvetica Neue', Helvetica, Arial, sans-serif"

PLOTLY_LAYOUT = dict(
    font=dict(family=_FONT, size=13, color=ENCRE),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=8, r=8, t=52, b=8),
    colorway=[ENCRE, ACCENT, GRIS, GRIS_CLAIR],
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(0,0,0,0)",
        borderwidth=0,
        font=dict(size=12, color=GRIS_FORT),
    ),
    xaxis=dict(
        gridcolor=FILET,
        linecolor=ENCRE,
        zerolinecolor=FILET,
        tickfont=dict(size=11, color=GRIS_FORT),
    ),
    yaxis=dict(
        gridcolor=FILET,
        linecolor=ENCRE,
        zerolinecolor=FILET,
        tickfont=dict(size=11, color=GRIS_FORT),
    ),
    title=dict(
        font=dict(size=14, color=ENCRE, family=_FONT),
        x=0, xanchor="left", y=0.97,
    ),
    hoverlabel=dict(
        bgcolor=ENCRE,
        bordercolor=ENCRE,
        font=dict(size=12, color="white", family=_FONT),
    ),
)


# ---------------------------------------------------------------------------
# CSS global injecté via st.markdown()
# ---------------------------------------------------------------------------

CSS = """
<style>
:root {
    --font: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    --ink: #141414;
    --gris-fort: #5A5A5A;
    --gris: #8C8C8C;
    --gris-clair: #C2C2C2;
    --filet: #E4E4E4;
    --accent: #E2231A;
}

/* ── Reset & base ─────────────────────────────────────────── */
html, body, [class*="css"], .stMarkdown, .stText,
button, input, select, textarea {
    font-family: var(--font) !important;
    -webkit-font-smoothing: antialiased;
}
.stApp { background: #FFFFFF; }

.main .block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1180px;
}
/* Signature : court filet rouge en tête de page (repère typographique) */
.main .block-container::before {
    content: "";
    display: block;
    width: 56px;
    height: 3px;
    background: var(--accent);
    margin-bottom: 1.5rem;
}

/* ── Masthead ─────────────────────────────────────────────── */
.tp-masthead {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 2rem;
    padding: 0 0 1rem 0;
    margin: 0 0 1.9rem 0;
    border-bottom: 2px solid var(--ink);
}
.tp-mark {
    margin: 0;
    font-size: 2.6rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    line-height: 1;
    color: var(--ink);
}
.tp-tagline {
    margin: 0.7rem 0 0 0;
    max-width: 48ch;
    font-size: 0.92rem;
    line-height: 1.45;
    font-weight: 400;
    color: var(--gris-fort);
}
.tp-mast-right {
    text-align: right;
    flex-shrink: 0;
    padding-bottom: 0.15rem;
}
.tp-meta-row {
    font-size: 0.74rem;
    line-height: 1.85;
    letter-spacing: 0.04em;
    color: var(--gris);
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}
.tp-meta-row strong { color: var(--ink); font-weight: 700; }

/* ── Bloc KPI : gros chiffres, filets verticaux, zéro carte ── */
.kpi-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    border-top: 1px solid var(--filet);
    border-bottom: 1px solid var(--filet);
    margin: 0 0 2.1rem 0;
}
.kpi-cell {
    padding: 1.15rem 1.5rem 1.25rem 1.5rem;
    border-left: 1px solid var(--filet);
}
.kpi-cell:first-child { border-left: 0; padding-left: 0; }
.kpi-value {
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1;
    color: var(--ink);
    font-variant-numeric: tabular-nums;
}
.kpi-value.is-accent { color: var(--accent); }
.kpi-label {
    margin-top: 0.55rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--ink);
}
.kpi-unit {
    margin-top: 0.1rem;
    font-size: 0.72rem;
    color: var(--gris);
}

/* ── Titre de section : libellé + filet ───────────────────── */
.tp-section {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.1rem 0 1rem 0;
}
.tp-section-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--ink);
    white-space: nowrap;
}
.tp-section::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--filet);
}

/* ── Légendes (st.caption) ────────────────────────────────── */
[data-testid="stCaptionContainer"], .stCaption {
    color: var(--gris-fort) !important;
    font-size: 0.84rem !important;
    line-height: 1.5;
    max-width: 72ch;
}

/* ── Onglets : plats, soulignés ───────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 1.6rem;
    background: transparent;
    border: 0;
    border-bottom: 1px solid var(--filet);
    border-radius: 0;
    padding: 0;
    margin-bottom: 1.5rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    padding: 0.5rem 0 0.8rem 0;
    background: transparent;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--gris-fort);
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: var(--ink) !important;
    font-weight: 700;
    border-bottom: 2px solid var(--accent) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ── Conteneur graphique (sans chrome) ────────────────────── */
.chart-card {
    background: transparent;
    border: 0;
    border-radius: 0;
    padding: 0;
    margin-bottom: 0.5rem;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #FAFAFA;
    border-right: 1px solid var(--filet);
}
[data-testid="stSidebar"] .block-container { padding-top: 2.2rem; }
.sidebar-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: var(--ink);
    margin: 0 0 1.2rem 0;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid var(--ink);
}
.sidebar-footer {
    font-size: 0.72rem;
    line-height: 1.75;
    color: var(--gris);
    border-top: 1px solid var(--filet);
    padding-top: 0.9rem;
    margin-top: 1.5rem;
}

/* ── Widgets : coins droits, filets fins, focus encre ─────── */
[data-baseweb="select"] > div {
    border-radius: 0 !important;
    border-color: var(--filet) !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: var(--ink) !important;
    box-shadow: none !important;
}
[data-testid="stWidgetLabel"] p {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--ink);
}

/* ── Expander & dataframe : coins droits ──────────────────── */
[data-testid="stExpander"] {
    border-color: var(--filet) !important;
    border-radius: 0 !important;
}
[data-testid="stExpander"] summary { border-radius: 0 !important; }

/* ── Masquer les éléments Streamlit par défaut ────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stMetric"] { display: none; }  /* on utilise nos propres cartes */

/* ── Scrollbar fine ───────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--gris-clair); border-radius: 0; }
</style>
"""


# ---------------------------------------------------------------------------
# Composants HTML
# ---------------------------------------------------------------------------

def _n(v: int) -> str:
    """Formate un entier avec une espace insécable comme séparateur (style FR)."""
    return f"{v:,}".replace(",", " ")


def html_header(nb_offres: int, date_maj: str = "Juin 2026") -> str:
    return f"""
    <div class="tp-masthead">
        <div class="tp-mast-left">
            <h1 class="tp-mark">TechPulse</h1>
            <p class="tp-tagline">Observatoire de l'emploi tech,
               sur quelles technologies se former pour rester compétitif en 2026.</p>
        </div>
        <div class="tp-mast-right">
            <div class="tp-meta-row"><strong>{_n(nb_offres)}</strong> offres analysées</div>
            <div class="tp-meta-row">API France Travail &middot; LLM Mistral</div>
            <div class="tp-meta-row">Mise à jour : {date_maj}</div>
        </div>
    </div>
    """


def html_kpi_grid(
    nb_offres: int,
    nb_competences: int,
    pct_ia: int,
    teletravail: float,
) -> str:
    return f"""
    <div class="kpi-row">
        <div class="kpi-cell">
            <div class="kpi-value">{_n(nb_offres)}</div>
            <div class="kpi-label">Offres analysées</div>
            <div class="kpi-unit">offres d'emploi tech</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-value">{_n(nb_competences)}</div>
            <div class="kpi-label">Compétences distinctes</div>
            <div class="kpi-unit">compétences canoniques</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-value is-accent">{pct_ia}&thinsp;%</div>
            <div class="kpi-label">Présence de l'IA</div>
            <div class="kpi-unit">des offres mentionnent l'IA</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-value">{teletravail:.1f}</div>
            <div class="kpi-label">Télétravail moyen</div>
            <div class="kpi-unit">jours par semaine</div>
        </div>
    </div>
    """


def html_section(titre: str) -> str:
    return f"""
    <div class="tp-section">
        <span class="tp-section-title">{titre}</span>
    </div>
    """


def html_chart_card(contenu_chart_key: str = "") -> str:
    return '<div class="chart-card">'


def html_sidebar_header() -> str:
    return '<div class="sidebar-title">Filtres</div>'


def html_sidebar_footer() -> str:
    return """
    <div class="sidebar-footer">
        Données : API France Travail<br>
        Extraction : Mistral AI<br>
        TechPulse, Master SID AMU 2026
    </div>
    """


# Design : style suisse / international, encre + accent rouge, filets, coins droits.
