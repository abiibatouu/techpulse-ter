"""Dashboard TechPulse — Point d'entrée Streamlit."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from database import (
    get_regions, get_seniorites, get_categories, get_metiers, get_kpis,
    get_top_competences, get_repartition_categories,
    get_salaire_par_competence, get_salaire_par_seniorite, get_evolution_temporelle,
    get_ia_vs_classiques, get_correlation_seniorite_ia, get_disparites_geo,
)
from charts import (
    chart_top_competences, chart_repartition_categories,
    chart_salaire_par_competence, chart_salaires, chart_evolution,
    chart_ia_vs_classiques, chart_correlation_seniorite_ia,
    chart_disparites_geo, table_disparites_geo,
)
from filters import render_filters
from style import get_css, html_header, html_kpi_grid, html_section, html_tab_desc


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="TechPulse — Observatoire de l'emploi tech",
    layout="wide",
    initial_sidebar_state="expanded",
)

dark_mode = st.session_state.get("dark_mode", False)
st.markdown(get_css(dark_mode), unsafe_allow_html=True)

# Toggle mode sombre flottant (accessible même si sidebar fermée)
_col_spacer, _col_toggle = st.columns([10, 1])
with _col_toggle:
    st.toggle("🌙", key="dark_mode", help="Mode sombre")


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

@st.cache_data(ttl=600)
def load_filter_options():
    return get_regions(), get_seniorites(), get_categories(), get_metiers()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

regions, seniorites, categories, metiers = load_filter_options()
filtres   = render_filters(regions, seniorites, categories, metiers)
region    = filtres["region"]
seniorite = filtres["seniorite"]
categorie = filtres["categorie"]
metier    = filtres["metier"]
top_n     = filtres["top_n"]


# ---------------------------------------------------------------------------
# En-tête et KPIs
# ---------------------------------------------------------------------------

kpis = get_kpis(region=region, seniorite=seniorite, metier=metier)

st.markdown(html_header(kpis["nb_offres"]), unsafe_allow_html=True)

st.markdown(
    html_kpi_grid(
        kpis["nb_offres"],
        kpis["nb_competences"],
        kpis["pct_ia"],
        kpis["teletravail_moyen"],
    ),
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Onglets
# ---------------------------------------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "Top compétences",
    "IA vs Classiques",
    "Séniorité & IA",
    "Géographie",
])


# ── Onglet 1 — Compétences ──────────────────────────────────────────────────
with tab1:

    st.markdown(html_tab_desc(
        "Quelles compétences reviennent le plus dans les offres tech ? "
        "Utilisez les filtres à gauche pour affiner par région, séniorité ou code ROME. "
        "Les couleurs : bleu indigo = classique, bleu marine = IA/LLM, lavande = émergente, rose = soft skill."
    ), unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1], gap="large")

    with col_left:
        df_top = get_top_competences(
            region=region, seniorite=seniorite, categorie=categorie,
            top_n=top_n, metier=metier,
        )
        st.plotly_chart(chart_top_competences(df_top), key="top_comp", use_container_width=True)

    with col_right:
        df_cat = get_repartition_categories(region=region, seniorite=seniorite, metier=metier)
        st.plotly_chart(chart_repartition_categories(df_cat), key="repartition_cat", use_container_width=True)

    st.markdown(html_section("Salaires par compétence"), unsafe_allow_html=True)

    df_sal_comp = get_salaire_par_competence(region=region, metier=metier)
    st.plotly_chart(chart_salaire_par_competence(df_sal_comp), key="sal_competence", use_container_width=True)

    st.markdown(html_section("Fourchette salariale & volume"), unsafe_allow_html=True)

    col_sal, col_evo = st.columns(2, gap="large")

    with col_sal:
        df_sal = get_salaire_par_seniorite(region=region)
        st.plotly_chart(chart_salaires(df_sal), key="salaires", use_container_width=True)

    with col_evo:
        df_evo = get_evolution_temporelle(region=region, seniorite=seniorite)
        st.plotly_chart(chart_evolution(df_evo), key="evolution", use_container_width=True)

    with st.expander("Tableau détaillé des compétences"):
        if not df_top.empty:
            st.dataframe(
                df_top.rename(columns={
                    "competence_canonique": "Compétence",
                    "categorie":            "Catégorie",
                    "nb_offres":            "Offres",
                }),
                hide_index=True,
                use_container_width=True,
            )


# ── Onglet 2 — IA vs Classiques ─────────────────────────────────────────────
with tab2:

    st.markdown(html_tab_desc(
        "Évolution mensuelle des compétences IA/LLM face aux compétences classiques. "
        "Observez si les outils d'intelligence artificielle gagnent du terrain dans les offres d'emploi tech en France."
    ), unsafe_allow_html=True)

    df_ia = get_ia_vs_classiques(region=region, seniorite=seniorite, metier=metier)
    st.plotly_chart(chart_ia_vs_classiques(df_ia), key="ia_classiques", use_container_width=True)

    if not df_ia.empty:
        with st.expander("Données brutes"):
            st.dataframe(df_ia, hide_index=True, use_container_width=True)


# ── Onglet 3 — Séniorité & IA ───────────────────────────────────────────────
with tab3:

    st.markdown(html_tab_desc(
        "Les offres senior mentionnent-elles plus l'IA ? "
        "Ce graphique montre le pourcentage d'offres citant l'intelligence artificielle pour chaque niveau d'expérience."
    ), unsafe_allow_html=True)

    df_corr = get_correlation_seniorite_ia(region=region, metier=metier)
    st.plotly_chart(chart_correlation_seniorite_ia(df_corr), key="corr_seniorite", use_container_width=True)

    if not df_corr.empty:
        st.dataframe(
            df_corr.rename(columns={
                "seniorite":    "Séniorité",
                "total_offres": "Offres totales",
                "offres_ia":    "Dont IA",
                "pct_ia":       "% IA",
            }),
            hide_index=True,
            use_container_width=True,
        )


# ── Onglet 4 — Géographie ───────────────────────────────────────────────────
with tab4:

    st.markdown(html_tab_desc(
        "Paris domine-t-elle toujours le marché tech ? "
        "Comparez les salaires médians, la présence de l'IA et le télétravail entre Paris, les villes secondaires et le full remote."
    ), unsafe_allow_html=True)

    df_geo = get_disparites_geo()
    st.plotly_chart(chart_disparites_geo(df_geo), key="geo", use_container_width=True)

    if not df_geo.empty:
        st.dataframe(
            table_disparites_geo(df_geo),
            hide_index=True,
            use_container_width=True,
        )
