"""Dashboard TechPulse, point d'entrée Streamlit.

Responsabilité unique : orchestrer database → filters → charts → style.
Aucune logique SQL, aucun graphique, aucun CSS ici.

Lancement : streamlit run dashboard/app.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from database import (
    get_regions, get_seniorites, get_categories, get_metiers, get_kpis,
    get_top_competences, get_repartition_categories,
    get_salaire_par_seniorite, get_salaire_par_competence, get_evolution_temporelle,
    get_ia_vs_classiques, get_correlation_seniorite_ia, get_disparites_geo,
)
from charts import (
    chart_top_competences, chart_repartition_categories,
    chart_salaires, chart_salaire_par_competence, chart_evolution,
    chart_ia_vs_classiques, chart_correlation_seniorite_ia,
    chart_disparites_geo, table_disparites_geo,
)
from filters import render_filters
from style import CSS, html_header, html_kpi_grid, html_section


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="TechPulse, observatoire de l'emploi tech",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Injection du CSS global
st.markdown(CSS, unsafe_allow_html=True)


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
# KPIs
# ---------------------------------------------------------------------------

kpis = get_kpis(region=region, seniorite=seniorite, metier=metier)

# Header avec le nombre d'offres intégré
st.markdown(html_header(kpis["nb_offres"]), unsafe_allow_html=True)

# Cartes KPI custom (on masque les st.metric via CSS)
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


# ── Onglet 1 ────────────────────────────────────────────────────────────────
with tab1:
    col_left, col_right = st.columns([2, 1], gap="medium")

    with col_left:
        df_top = get_top_competences(
            region=region, seniorite=seniorite, categorie=categorie,
            top_n=top_n, metier=metier,
        )
        st.plotly_chart(chart_top_competences(df_top), use_container_width=True, key="top_comp")

    with col_right:
        df_cat = get_repartition_categories(region=region, seniorite=seniorite, metier=metier)
        st.plotly_chart(chart_repartition_categories(df_cat), use_container_width=True, key="repartition_cat")

    st.markdown(html_section("Salaires & activité"), unsafe_allow_html=True)
    col_sal, col_evo = st.columns(2, gap="medium")

    with col_sal:
        df_sal = get_salaire_par_seniorite(region=region)
        st.plotly_chart(chart_salaires(df_sal), use_container_width=True, key="salaires")

    with col_evo:
        df_evo = get_evolution_temporelle(region=region, seniorite=seniorite)
        st.plotly_chart(chart_evolution(df_evo), use_container_width=True, key="evolution")

    st.markdown(html_section("Salaire médian par compétence"), unsafe_allow_html=True)
    st.caption(
        "Quelles compétences sont associées aux salaires les plus élevés ? "
        "Médiane du milieu de fourchette, compétences avec au moins 5 offres salariées."
    )
    df_sal_comp = get_salaire_par_competence(
        region=region, seniorite=seniorite, metier=metier, top_n=top_n
    )
    st.plotly_chart(
        chart_salaire_par_competence(df_sal_comp),
        use_container_width=True, key="salaire_competence",
    )

    with st.expander("Tableau détaillé des compétences"):
        if not df_top.empty:
            st.dataframe(
                df_top.rename(columns={
                    "competence_canonique": "Compétence",
                    "categorie": "Catégorie",
                    "nb_offres": "Offres",
                }),
                use_container_width=True,
                hide_index=True,
            )


# ── Onglet 2 ────────────────────────────────────────────────────────────────
with tab2:
    st.markdown(
        html_section("Évolution mensuelle des compétences IA vs Classiques"),
        unsafe_allow_html=True,
    )
    st.caption(
        "Observe mois par mois si les compétences IA (LangChain, RAG, Mistral…) "
        "progressent par rapport aux compétences classiques (SQL, Python, Java…)."
    )
    df_ia = get_ia_vs_classiques(region=region, seniorite=seniorite)
    st.plotly_chart(chart_ia_vs_classiques(df_ia), use_container_width=True, key="ia_classiques")

    if not df_ia.empty:
        with st.expander("Données brutes"):
            st.dataframe(df_ia, use_container_width=True, hide_index=True)


# ── Onglet 3 ────────────────────────────────────────────────────────────────
with tab3:
    st.markdown(
        html_section("Corrélation séniorité × présence de l'IA"),
        unsafe_allow_html=True,
    )
    st.caption(
        "Pour chaque niveau de séniorité, quel pourcentage des offres mentionne "
        "l'IA dans les missions ? Les profils senior sont-ils plus exposés ?"
    )
    df_corr = get_correlation_seniorite_ia(region=region)
    st.plotly_chart(chart_correlation_seniorite_ia(df_corr), use_container_width=True, key="corr_seniorite")

    if not df_corr.empty:
        st.dataframe(
            df_corr.rename(columns={
                "seniorite":    "Séniorité",
                "total_offres": "Offres totales",
                "offres_ia":    "Dont IA",
                "pct_ia":       "% IA",
            }),
            use_container_width=True,
            hide_index=True,
        )


# ── Onglet 4 ────────────────────────────────────────────────────────────────
with tab4:
    st.markdown(
        html_section("Paris / Villes secondaires / Full remote"),
        unsafe_allow_html=True,
    )
    st.caption(
        "Comparaison du volume d'offres, du salaire médian et de la présence de l'IA "
        "selon la localisation. La taille des bulles représente le nombre d'offres."
    )
    df_geo = get_disparites_geo()
    st.plotly_chart(chart_disparites_geo(df_geo), use_container_width=True, key="geo")

    if not df_geo.empty:
        st.dataframe(
            table_disparites_geo(df_geo),
            use_container_width=True,
            hide_index=True,
        )
