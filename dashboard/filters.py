"""Composants de filtrage de la sidebar Streamlit.

Responsabilité unique : rendre les widgets de filtre et retourner les valeurs
choisies par l'utilisateur. Ne connaît ni SQL, ni Plotly.
"""

import streamlit as st
from style import html_sidebar_header, html_sidebar_footer


def render_filters(regions: list[str], seniorites: list[str], categories: list[str]) -> dict:
    """Affiche les filtres dans la sidebar et retourne les valeurs sélectionnées.

    Retourne un dict :
        { "region", "seniorite", "categorie", "top_n" }
    """
    st.sidebar.markdown(html_sidebar_header(), unsafe_allow_html=True)

    region_choice = st.sidebar.selectbox(
        "Région",
        ["Toutes les régions"] + regions,
        label_visibility="visible",
    )
    region = None if region_choice == "Toutes les régions" else region_choice

    seniorite_choice = st.sidebar.selectbox(
        "Séniorité",
        ["Toutes les séniorités"] + seniorites,
    )
    seniorite = None if seniorite_choice == "Toutes les séniorités" else seniorite_choice

    categorie_choice = st.sidebar.selectbox(
        "Catégorie",
        ["Toutes les catégories"] + categories,
    )
    categorie = None if categorie_choice == "Toutes les catégories" else categorie_choice

    top_n = st.sidebar.slider("Top N compétences", min_value=5, max_value=40, value=20, step=5)

    st.sidebar.markdown(html_sidebar_footer(), unsafe_allow_html=True)

    return {
        "region":    region,
        "seniorite": seniorite,
        "categorie": categorie,
        "top_n":     top_n,
    }
