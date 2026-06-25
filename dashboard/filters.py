"""Composants de filtrage de la sidebar Streamlit.

Responsabilité unique : rendre les widgets de filtre et retourner les valeurs
choisies par l'utilisateur. Ne connaît ni SQL, ni Plotly.
"""

import streamlit as st
from style import html_sidebar_header, html_sidebar_footer


def render_filters(
    regions: list[str],
    seniorites: list[str],
    categories: list[str],
    metiers: list[tuple[str, str]] | None = None,
) -> dict:
    """Affiche les filtres dans la sidebar et retourne les valeurs sélectionnées.

    Retourne un dict :
        { "region", "seniorite", "categorie", "metier", "top_n" }
    """
    metiers = metiers or []
    st.sidebar.markdown(html_sidebar_header(), unsafe_allow_html=True)

    # metiers = liste de (code_rome, libellé) : on affiche le libellé, on filtre sur le code.
    label_vers_code = {libelle: code for code, libelle in metiers}
    metier_choice = st.sidebar.selectbox(
        "Métier (ROME)",
        ["Tous les métiers"] + list(label_vers_code.keys()),
    )
    metier = label_vers_code.get(metier_choice)  # None pour "Tous les métiers"

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
        "metier":    metier,
        "top_n":     top_n,
    }
