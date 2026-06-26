"""Composants de filtrage de la sidebar Streamlit.

Responsabilité unique : rendre les widgets de filtre et retourner les valeurs
choisies par l'utilisateur. Ne connaît ni SQL, ni Plotly.
"""

import streamlit as st
from style import html_sidebar_header, html_sidebar_footer, html_legend


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

    # Libellés courts lisibles par code ROME (remplace les libellés bruts tronqués)
    LABELS_ROME = {
        "M1801": "M1801 — Administration SI",
        "M1802": "M1802 — Conseil & MOA en SI",
        "M1803": "M1803 — Direction SI (DSI)",
        "M1805": "M1805 — Études & dev (data, dev, IA)",
        "M1806": "M1806 — Conseil et MOA",
        "M1810": "M1810 — Production & exploitation SI",
    }
    label_vers_code = {
        LABELS_ROME.get(code, f"{code} — {libelle[:35]}"): code
        for code, libelle in metiers
    }
    metier_choice = st.sidebar.selectbox(
        "Métier (ROME)",
        ["Tous les métiers"] + list(label_vers_code.keys()),
    )
    metier = label_vers_code.get(metier_choice)

    st.sidebar.markdown('<div class="sb-section">Localisation</div>', unsafe_allow_html=True)

    region_choice = st.sidebar.selectbox(
        "Région",
        ["Toutes les régions"] + regions,
        label_visibility="visible",
    )
    region = None if region_choice == "Toutes les régions" else region_choice

    st.sidebar.markdown('<div class="sb-section">Profil</div>', unsafe_allow_html=True)

    seniorite_choice = st.sidebar.selectbox(
        "Séniorité",
        ["Toutes les séniorités"] + seniorites,
    )
    seniorite = None if seniorite_choice == "Toutes les séniorités" else seniorite_choice

    categorie_choice = st.sidebar.selectbox(
        "Catégorie de compétence",
        ["Toutes les catégories"] + categories,
    )
    categorie = None if categorie_choice == "Toutes les catégories" else categorie_choice

    st.sidebar.markdown('<div class="sb-section">Affichage</div>', unsafe_allow_html=True)

    top_n = st.sidebar.slider("Top N compétences", min_value=5, max_value=40, value=20, step=5)

    st.sidebar.markdown('<div class="sb-section">Légende</div>', unsafe_allow_html=True)
    st.sidebar.markdown(html_legend(), unsafe_allow_html=True)

    st.sidebar.markdown(html_sidebar_footer(), unsafe_allow_html=True)

    return {
        "region":    region,
        "seniorite": seniorite,
        "categorie": categorie,
        "metier":    metier,
        "top_n":     top_n,
    }
