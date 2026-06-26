"""Systeme de design TechPulse — palette bleu/indigo + mode sombre."""

# ---------------------------------------------------------------------------
# Palette de couleurs (charts Plotly)
# ---------------------------------------------------------------------------

COULEURS = {
    "classique":  "#5B7FEF",
    "ia_llm":     "#1E3A8A",
    "emergente":  "#818CF8",
    "soft_skill": "#F9A8A8",
}

LABELS_CATEGORIES = {
    "classique":  "Classique",
    "ia_llm":     "IA / LLM",
    "emergente":  "Emergente",
    "soft_skill": "Soft Skill",
}

COULEURS_ZONES = {
    "Paris":              "#5B7FEF",
    "Full remote":        "#818CF8",
    "Villes secondaires": "#38BDF8",
}

# ---------------------------------------------------------------------------
# Layouts Plotly (clair et sombre)
# ---------------------------------------------------------------------------

PLOTLY_LAYOUT_LIGHT = dict(
    template="simple_white",
    font=dict(
        family="'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif",
        size=13, color="#5A6270",
    ),
    paper_bgcolor="#FFFFFF",
    plot_bgcolor="#FFFFFF",
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(bgcolor="rgba(255,255,255,0)", bordercolor="rgba(0,0,0,0)", borderwidth=0),
    xaxis=dict(gridcolor="#EEF2FF", linecolor="#D6E4FF", tickfont=dict(size=11, color="#8898AA")),
    yaxis=dict(gridcolor="#EEF2FF", linecolor="#D6E4FF", tickfont=dict(size=11, color="#8898AA")),
    title=dict(
        font=dict(size=14, color="#1E2848", family="'Inter', 'Segoe UI', Arial, sans-serif"),
        x=0, xanchor="left", pad=dict(l=8),
    ),
    hoverlabel=dict(
        bgcolor="white", bordercolor="#D6E4FF",
        font=dict(size=12, family="'Inter', 'Segoe UI', Arial, sans-serif", color="#1E2848"),
    ),
)

PLOTLY_LAYOUT_DARK = dict(
    template="simple_white",
    font=dict(
        family="'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif",
        size=13, color="#94A3B8",
    ),
    paper_bgcolor="#131C38",
    plot_bgcolor="#131C38",
    margin=dict(l=16, r=16, t=48, b=16),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(0,0,0,0)", borderwidth=0),
    xaxis=dict(gridcolor="rgba(91,127,239,0.1)", linecolor="rgba(91,127,239,0.2)", tickfont=dict(size=11, color="#64748B")),
    yaxis=dict(gridcolor="rgba(91,127,239,0.1)", linecolor="rgba(91,127,239,0.2)", tickfont=dict(size=11, color="#64748B")),
    title=dict(
        font=dict(size=14, color="#E2E8F0", family="'Inter', 'Segoe UI', Arial, sans-serif"),
        x=0, xanchor="left", pad=dict(l=8),
    ),
    hoverlabel=dict(
        bgcolor="#1A2340", bordercolor="rgba(91,127,239,0.3)",
        font=dict(size=12, family="'Inter', 'Segoe UI', Arial, sans-serif", color="#E2E8F0"),
    ),
)

# Alias backward-compat pour charts.py
PLOTLY_LAYOUT = PLOTLY_LAYOUT_LIGHT


def get_plotly_layout(dark: bool = False) -> dict:
    return PLOTLY_LAYOUT_DARK if dark else PLOTLY_LAYOUT_LIGHT


# ---------------------------------------------------------------------------
# CSS — variables clair
# ---------------------------------------------------------------------------

_CSS_VARS_LIGHT = """
:root {
    --bg:             #EEF2FF;
    --card:           #FFFFFF;
    --sidebar:        #F5F8FF;
    --accent:         #5B7FEF;
    --t1:             #1E2848;
    --t2:             #5A6270;
    --t3:             #8898AA;
    --border:         #D6E4FF;
    --sh:             0 2px 12px rgba(59,91,219,0.07), 0 1px 3px rgba(0,0,0,0.04);
    --sh-md:          0 6px 24px rgba(59,91,219,0.11), 0 2px 6px rgba(0,0,0,0.05);
    --sh-hover:       0 10px 32px rgba(59,91,219,0.14), 0 4px 8px rgba(0,0,0,0.06);
    --tab-active-bg:  #EEF2FF;
    --tab-desc-bg:    #F0F4FF;
    --badge-acc-bg:   #EEF2FF;
    --scrollbar:      #C7D6FF;
    --logo-glow:      rgba(91,127,239,0.35);
    --logo-glow-hi:   rgba(91,127,239,0.65);
}
"""

# ---------------------------------------------------------------------------
# CSS — variables sombre
# ---------------------------------------------------------------------------

_CSS_VARS_DARK = """
:root {
    --bg:             #0B1027;
    --card:           #131C38;
    --sidebar:        #0D1526;
    --accent:         #7B9BF5;
    --t1:             #E2E8F0;
    --t2:             #94A3B8;
    --t3:             #64748B;
    --border:         rgba(91,127,239,0.2);
    --sh:             0 2px 12px rgba(0,0,0,0.35), 0 1px 3px rgba(0,0,0,0.25);
    --sh-md:          0 6px 24px rgba(0,0,0,0.45), 0 2px 6px rgba(0,0,0,0.3);
    --sh-hover:       0 10px 32px rgba(0,0,0,0.55), 0 4px 8px rgba(0,0,0,0.35);
    --tab-active-bg:  rgba(91,127,239,0.18);
    --tab-desc-bg:    rgba(91,127,239,0.09);
    --badge-acc-bg:   rgba(91,127,239,0.12);
    --scrollbar:      rgba(91,127,239,0.3);
    --logo-glow:      rgba(91,127,239,0.45);
    --logo-glow-hi:   rgba(91,127,239,0.8);
}
"""

# ---------------------------------------------------------------------------
# CSS — structure commune (utilise les variables CSS)
# ---------------------------------------------------------------------------

_CSS_COMMON = """
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes logoPulse {
    0%, 100% { filter: drop-shadow(0 2px 6px var(--logo-glow)); }
    50%       { filter: drop-shadow(0 2px 14px var(--logo-glow-hi)); }
}

html, body, [class*="css"], .stMarkdown, .stText,
button, input, select, textarea {
    font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif !important;
}
.stApp { background: var(--bg) !important; }
.main  { background: var(--bg) !important; }
.main .block-container {
    padding-top: 1.75rem;
    padding-bottom: 3rem;
    max-width: 1360px;
}

/* SIDEBAR */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div:first-child {
    background: var(--sidebar) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] div.stMarkdown p {
    color: var(--t2) !important;
    font-size: 0.8rem !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    transition: border-color 0.18s ease;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:hover {
    border-color: var(--accent) !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] div[class] {
    color: var(--t1) !important;
    background: transparent !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: var(--t3) !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] p  { color: var(--t2) !important; }

/* Toggle mode sombre */
[data-testid="stSidebar"] [data-testid="stToggle"] label { color: var(--t2) !important; }

.sb-top {
    padding-bottom: 1.2rem;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
}
.sb-logo-row { display: flex; align-items: center; gap: 0.75rem; }
.sb-logo-svg { flex-shrink: 0; animation: logoPulse 3s ease-in-out infinite; }

.sb-legend { margin-top: 0.35rem; }
.sb-legend-item {
    display: flex; align-items: center; gap: 0.55rem;
    margin-bottom: 0.42rem; font-size: 0.72rem;
    color: var(--t2) !important; font-weight: 400;
}
.sb-legend-dot { width: 9px; height: 9px; border-radius: 50%; flex-shrink: 0; }

.tab-desc {
    border-left: 3px solid var(--accent);
    background: var(--tab-desc-bg);
    border-radius: 0 8px 8px 0;
    padding: 0.6rem 1rem 0.6rem 0.9rem;
    margin-bottom: 1.2rem;
    font-size: 0.78rem; color: var(--t2); line-height: 1.5;
    animation: fadeIn 0.4s ease both;
}
.sb-project-name {
    font-size: 1rem; font-weight: 800;
    color: var(--t1) !important;
    letter-spacing: -0.02em; line-height: 1.1;
}
.sb-project-uni { font-size: 0.58rem; color: var(--t3) !important; margin-top: 0.1rem; }
.sb-section {
    font-size: 0.55rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.12em; color: var(--t3) !important;
    margin: 1.1rem 0 0.45rem 0;
}
.sb-footer {
    font-size: 0.62rem; color: var(--t3) !important; line-height: 1.9;
    border-top: 1px solid var(--border); padding-top: 0.85rem; margin-top: 2rem;
}

/* KPI */
.kpi-grid {
    display: grid; grid-template-columns: repeat(4, 1fr);
    gap: 1rem; margin-bottom: 1.5rem;
}
.kpi-card {
    background: var(--card); border-radius: 12px;
    border: 1px solid var(--border);
    padding: 1.3rem 1.4rem 1.3rem 1.6rem;
    box-shadow: var(--sh); position: relative; overflow: hidden;
    animation: fadeSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: var(--sh-hover); }
.kpi-card:nth-child(1) { animation-delay: 0.04s; }
.kpi-card:nth-child(2) { animation-delay: 0.09s; }
.kpi-card:nth-child(3) { animation-delay: 0.14s; }
.kpi-card:nth-child(4) { animation-delay: 0.19s; }
.kpi-accent-bar {
    position: absolute; left: 0; top: 0; bottom: 0;
    width: 4px; border-radius: 12px 0 0 12px;
}
.kpi-label {
    font-size: 0.7rem; font-weight: 600; color: var(--t3);
    margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 0.06em;
}
.kpi-value {
    font-size: 2.1rem; font-weight: 800; line-height: 1;
    margin-bottom: 0.3rem; letter-spacing: -0.03em;
}
.kpi-sub { font-size: 0.7rem; color: var(--t3); font-weight: 400; }
.kpi-badge {
    display: inline-block; margin-top: 0.45rem;
    font-size: 0.65rem; font-weight: 600;
    padding: 0.15rem 0.5rem; border-radius: 99px;
}

/* HEADER */
.page-header {
    display: flex; align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 1.5rem; padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    animation: fadeIn 0.4s ease both;
}
.page-title {
    font-size: 1.2rem; font-weight: 800; color: var(--t1);
    letter-spacing: -0.025em; margin: 0 0 0.2rem 0;
}
.page-sub { font-size: 0.76rem; color: var(--t3); margin: 0; }
.page-badges { display: flex; gap: 0.5rem; flex-wrap: wrap; align-items: center; }
.page-badge {
    background: var(--card); border: 1px solid var(--border);
    border-radius: 6px; padding: 0.2rem 0.65rem;
    font-size: 0.7rem; color: var(--t2); font-weight: 500; box-shadow: var(--sh);
}
.page-badge-accent {
    background: var(--badge-acc-bg);
    border-color: var(--border);
    color: var(--accent); font-weight: 600;
}

/* GRAPHIQUES */
[data-testid="stPlotlyChart"] {
    background: var(--card) !important;
    border-radius: 12px !important; border: 1px solid var(--border) !important;
    box-shadow: var(--sh) !important; overflow: hidden;
    margin-bottom: 1rem;
    animation: fadeIn 0.55s ease 0.25s both;
    transition: box-shadow 0.2s ease;
}
[data-testid="stPlotlyChart"]:hover { box-shadow: var(--sh-md) !important; }
[data-testid="stPlotlyChart"] > div { border-radius: 12px !important; }

.tp-section { display: flex; align-items: center; gap: 0.75rem; margin: 1.5rem 0 0.9rem 0; }
.tp-section-title {
    font-size: 0.62rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.1em; color: var(--t3); white-space: nowrap;
}
.tp-section::after { content: ''; flex: 1; height: 1px; background: var(--border); }

/* ONGLETS */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem; background: var(--card); border-radius: 12px;
    padding: 0.3rem; margin-bottom: 1.25rem;
    border: 1px solid var(--border) !important; box-shadow: var(--sh);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; padding: 0.5rem 1.4rem;
    font-size: 0.82rem; font-weight: 500; color: var(--t3);
    border: none; background: transparent;
    transition: color 0.15s ease, background 0.15s ease;
}
.stTabs [aria-selected="true"] {
    background: var(--tab-active-bg) !important;
    color: var(--accent) !important; font-weight: 700;
}
.stTabs [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
    color: var(--t1) !important; background: var(--bg) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

[data-testid="stDataFrame"] {
    border-radius: 10px !important; border: 1px solid var(--border) !important;
    overflow: hidden; box-shadow: var(--sh) !important;
}

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMetric"] { display: none; }

/* Sidebar toujours visible — jamais cachee */
section[data-testid="stSidebar"] {
    transform: translateX(0) !important;
    display: block !important;
    visibility: visible !important;
    min-width: 18rem !important;
}
/* Cacher le bouton de fermeture (non necessaire si sidebar fixe) */
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
}

::-webkit-scrollbar       { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--scrollbar); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent); }
"""


def get_css(dark: bool = False) -> str:
    """Retourne le CSS complet pour le mode clair ou sombre."""
    v = _CSS_VARS_DARK if dark else _CSS_VARS_LIGHT
    return f"<style>{v}{_CSS_COMMON}</style>"


# Alias backward-compat
CSS = get_css(False)


# ---------------------------------------------------------------------------
# Composants HTML
# ---------------------------------------------------------------------------

def html_header(nb_offres: int, date_maj: str = "Juin 2026") -> str:
    return (
        '<div class="page-header">'
        '<div>'
        '<p class="page-title">Comp&eacute;tences tech en France &mdash; March&eacute; de l\'emploi 2026</p>'
        f'<p class="page-sub">Bas&eacute; sur {nb_offres:,} offres &nbsp;&middot;&nbsp; Mistral AI &nbsp;&middot;&nbsp; {date_maj}</p>'
        '</div>'
        '<div class="page-badges">'
        '<span class="page-badge page-badge-accent">Temps r&eacute;el</span>'
        '<span class="page-badge">Famille M18</span>'
        '<span class="page-badge">6 codes ROME</span>'
        '</div>'
        '</div>'
    )


def html_kpi_grid(nb_offres: int, nb_competences: int, pct_ia: int, teletravail: float) -> str:
    return (
        '<div class="kpi-grid">'
        '<div class="kpi-card">'
        '<div class="kpi-accent-bar" style="background:#5B7FEF;"></div>'
        '<div class="kpi-label">Offres analys&eacute;es</div>'
        f'<div class="kpi-value" style="color:#5B7FEF;">{nb_offres:,}</div>'
        '<div class="kpi-sub">offres d\'emploi tech</div>'
        '<div class="kpi-badge" style="background:rgba(91,127,239,0.12);color:#5B7FEF;">Famille M18</div>'
        '</div>'
        '<div class="kpi-card">'
        '<div class="kpi-accent-bar" style="background:#1E3A8A;"></div>'
        '<div class="kpi-label">Comp&eacute;tences distinctes</div>'
        f'<div class="kpi-value" style="color:#5B7FEF;">{nb_competences}</div>'
        '<div class="kpi-sub">comp&eacute;tences canoniques</div>'
        '<div class="kpi-badge" style="background:rgba(30,58,138,0.12);color:#4A7CE0;">76 dans la taxonomie</div>'
        '</div>'
        '<div class="kpi-card">'
        '<div class="kpi-accent-bar" style="background:#818CF8;"></div>'
        '<div class="kpi-label">Pr&eacute;sence de l\'IA</div>'
        f'<div class="kpi-value" style="color:#818CF8;">{pct_ia}&thinsp;%</div>'
        '<div class="kpi-sub">des offres mentionnent l\'IA</div>'
        '<div class="kpi-badge" style="background:rgba(129,140,248,0.12);color:#818CF8;">LLM &middot; RAG &middot; Prompt</div>'
        '</div>'
        '<div class="kpi-card">'
        '<div class="kpi-accent-bar" style="background:#38BDF8;"></div>'
        '<div class="kpi-label">T&eacute;l&eacute;travail moyen</div>'
        f'<div class="kpi-value" style="color:#0EA5E9;">{teletravail:.1f}</div>'
        '<div class="kpi-sub">jours par semaine</div>'
        '<div class="kpi-badge" style="background:rgba(56,189,248,0.12);color:#0EA5E9;">sur 5 j. ouv&eacute;r&eacute;s</div>'
        '</div>'
        '</div>'
    )


def html_section(titre: str) -> str:
    return f'<div class="tp-section"><span class="tp-section-title">{titre}</span></div>'


def html_sidebar_header() -> str:
    logo = (
        '<svg class="sb-logo-svg" width="40" height="40" viewBox="0 0 40 40"'
        ' fill="none" xmlns="http://www.w3.org/2000/svg">'
        '<defs><linearGradient id="tpg" x1="0" y1="0" x2="40" y2="40"'
        ' gradientUnits="userSpaceOnUse">'
        '<stop offset="0%" stop-color="#6B8EF5"/>'
        '<stop offset="100%" stop-color="#2D3B8E"/>'
        '</linearGradient></defs>'
        '<rect width="40" height="40" rx="10" fill="url(#tpg)"/>'
        '<polyline points="4,20 10,20 14,11 17,29 20,13 23,22 27,20 36,20"'
        ' fill="none" stroke="white" stroke-width="2.2"'
        ' stroke-linecap="round" stroke-linejoin="round"/>'
        '</svg>'
    )
    return (
        '<div class="sb-top">'
        '<div class="sb-logo-row">'
        + logo +
        '<div>'
        '<div class="sb-project-name">TechPulse</div>'
        '<div class="sb-project-uni">Aix-Marseille Universit&eacute;</div>'
        '</div>'
        '</div>'
        '</div>'
        '<div class="sb-section">Analyse</div>'
    )


def html_legend() -> str:
    items = [
        ("#5B7FEF", "Classique &mdash; &eacute;tablies"),
        ("#1E3A8A", "IA / LLM &mdash; IA g&eacute;n&eacute;rative"),
        ("#818CF8", "Emergente &mdash; nouveaux outils"),
        ("#F9A8A8", "Soft Skill &mdash; humaines"),
    ]
    html = '<div class="sb-legend">'
    for color, label in items:
        html += (
            '<div class="sb-legend-item">'
            f'<span class="sb-legend-dot" style="background:{color};"></span>'
            f'{label}'
            '</div>'
        )
    html += '</div>'
    return html


def html_tab_desc(text: str) -> str:
    return f'<div class="tab-desc">{text}</div>'


def html_sidebar_footer() -> str:
    return (
        '<div class="sb-footer">'
        'Donn&eacute;es&nbsp;: API France Travail<br>'
        'Extraction&nbsp;: Mistral AI<br>'
        'Master SID &mdash; AMU 2026'
        '</div>'
    )


def html_chart_card(contenu_chart_key: str = "") -> str:
    return '<div class="chart-card">'
