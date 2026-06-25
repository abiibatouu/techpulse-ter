"""Système de design TechPulse.

Responsabilité unique : définir les styles CSS et les composants HTML réutilisables.
Aucune logique métier, aucune requête SQL ici.
"""

# ---------------------------------------------------------------------------
# Palette de couleurs — cohérente dans tout le dashboard
# ---------------------------------------------------------------------------

COULEURS = {
    "classique":  "#3B82F6",   # bleu
    "ia_llm":     "#F59E0B",   # ambre
    "emergente":  "#10B981",   # vert émeraude
    "soft_skill": "#8B5CF6",   # violet
}

LABELS_CATEGORIES = {
    "classique":  "Classique",
    "ia_llm":     "IA / LLM",
    "emergente":  "Émergente",
    "soft_skill": "Soft Skill",
}

COULEURS_ZONES = {
    "Paris":              "#EF4444",
    "Full remote":        "#10B981",
    "Villes secondaires": "#6366F1",
}

# Thème Plotly appliqué à tous les graphiques
PLOTLY_LAYOUT = dict(
    font=dict(
        family="'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif",
        size=13,
        color="#374151",
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#E5E7EB",
        borderwidth=1,
    ),
    xaxis=dict(
        gridcolor="#F3F4F6",
        linecolor="#E5E7EB",
        tickfont=dict(size=12),
    ),
    yaxis=dict(
        gridcolor="#F3F4F6",
        linecolor="#E5E7EB",
        tickfont=dict(size=12),
    ),
    title=dict(
        font=dict(size=15, color="#111827", family="Inter, sans-serif"),
        x=0,
        xanchor="left",
    ),
    hoverlabel=dict(
        bgcolor="white",
        bordercolor="#E5E7EB",
        font=dict(size=13, family="Inter, sans-serif"),
    ),
)


# ---------------------------------------------------------------------------
# CSS global injecté via st.markdown()
# ---------------------------------------------------------------------------

CSS = """
<style>
/* ── Police système — charge instantanément, pas de dépendance réseau ── */
/* Segoe UI sur Windows, SF Pro sur Mac, Roboto sur Android/Linux        */
:root {
    --font: 'Segoe UI', -apple-system, BlinkMacSystemFont,
            'Helvetica Neue', Arial, sans-serif;
}

/* ── Reset & base ─────────────────────────────────────────── */
html, body, [class*="css"], .stMarkdown, .stText, button, input, select {
    font-family: var(--font) !important;
}

.main .block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1280px;
}

/* ── Header principal ─────────────────────────────────────── */
.tp-header {
    background: linear-gradient(135deg, #1B2A4A 0%, #2563EB 100%);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.75rem;
    color: white;
}
.tp-header h1 {
    margin: 0 0 0.35rem 0;
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: white;
}
.tp-header p {
    margin: 0;
    font-size: 0.95rem;
    color: rgba(255,255,255,0.75);
    font-weight: 400;
}
.tp-header-meta {
    margin-top: 1rem;
    display: flex;
    gap: 1.5rem;
}
.tp-badge {
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.78rem;
    color: rgba(255,255,255,0.9);
    font-weight: 500;
}

/* ── Cartes KPI ───────────────────────────────────────────── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.75rem;
}
.kpi-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s ease;
}
.kpi-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #2563EB);
    border-radius: 10px 10px 0 0;
}
.kpi-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6B7280;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #111827;
    line-height: 1;
    margin-bottom: 0.25rem;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #9CA3AF;
}

/* ── Séparateur de section ────────────────────────────────── */
.tp-section {
    margin: 1.5rem 0 0.75rem 0;
}
.tp-section-title {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #9CA3AF;
    margin-bottom: 0.75rem;
}

/* ── Conteneur graphique ──────────────────────────────────── */
.chart-card {
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.25rem;
    margin-bottom: 1rem;
}

/* ── Onglets ──────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: white;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    padding: 0.25rem;
    margin-bottom: 1.25rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    padding: 0.5rem 1.25rem;
    font-size: 0.85rem;
    font-weight: 500;
    color: #6B7280;
    border: none;
    background: transparent;
}
.stTabs [aria-selected="true"] {
    background: #EFF6FF !important;
    color: #2563EB !important;
    font-weight: 600;
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none;
}
.stTabs [data-baseweb="tab-border"] {
    display: none;
}

/* ── Sidebar ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #F9FAFB;
    border-right: 1px solid #E5E7EB;
}
[data-testid="stSidebar"] .block-container {
    padding-top: 1.5rem;
}
.sidebar-title {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #6B7280;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #E5E7EB;
}
.sidebar-footer {
    font-size: 0.72rem;
    color: #9CA3AF;
    line-height: 1.6;
    border-top: 1px solid #E5E7EB;
    padding-top: 0.75rem;
    margin-top: 1rem;
}

/* ── Masquer les éléments Streamlit par défaut ────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMetric"] { display: none; }  /* on utilise nos propres cartes */

/* ── Scrollbar fine ───────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #F3F4F6; }
::-webkit-scrollbar-thumb { background: #D1D5DB; border-radius: 3px; }
</style>
"""


# ---------------------------------------------------------------------------
# Composants HTML
# ---------------------------------------------------------------------------

def html_header(nb_offres: int, date_maj: str = "Juin 2026") -> str:
    return f"""
    <div class="tp-header">
        <h1>TechPulse</h1>
        <p>Observatoire de l'emploi tech &mdash;
           Sur quelles technologies se former pour être compétitif en 2026&nbsp;?</p>
        <div class="tp-header-meta">
            <span class="tp-badge">API France Travail</span>
            <span class="tp-badge">LLM Mistral</span>
            <span class="tp-badge">{nb_offres:,} offres analysées</span>
            <span class="tp-badge">Mise à jour : {date_maj}</span>
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
    <div class="kpi-grid">
        <div class="kpi-card" style="--accent: #2563EB;">
            <div class="kpi-label">Offres analysées</div>
            <div class="kpi-value">{nb_offres:,}</div>
            <div class="kpi-sub">offres d'emploi tech</div>
        </div>
        <div class="kpi-card" style="--accent: #10B981;">
            <div class="kpi-label">Compétences distinctes</div>
            <div class="kpi-value">{nb_competences:,}</div>
            <div class="kpi-sub">compétences canoniques</div>
        </div>
        <div class="kpi-card" style="--accent: #F59E0B;">
            <div class="kpi-label">Présence de l'IA</div>
            <div class="kpi-value">{pct_ia}&thinsp;%</div>
            <div class="kpi-sub">des offres mentionnent l'IA</div>
        </div>
        <div class="kpi-card" style="--accent: #8B5CF6;">
            <div class="kpi-label">Télétravail moyen</div>
            <div class="kpi-value">{teletravail:.1f}</div>
            <div class="kpi-sub">jours par semaine</div>
        </div>
    </div>
    """


def html_section(titre: str) -> str:
    return f"""
    <div class="tp-section">
        <div class="tp-section-title">{titre}</div>
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
        TechPulse &mdash; Master SID AMU 2026
    </div>
    """
