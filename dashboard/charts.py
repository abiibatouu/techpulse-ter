"""Visualisations Plotly pour le dashboard TechPulse.

Responsabilité unique : transformer des DataFrames en figures Plotly.
Toutes les figures partagent le même thème défini dans style.py.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from style import (
    COULEURS, LABELS_CATEGORIES, COULEURS_ZONES, PLOTLY_LAYOUT,
    ENCRE, ACCENT, GRIS, GRIS_CLAIR, GRIS_FORT,
)


def _apply_theme(fig: go.Figure, height: int = 400) -> go.Figure:
    """Applique le thème commun à toutes les figures."""
    fig.update_layout(height=height, **PLOTLY_LAYOUT)
    return fig


def _label(cat: str) -> str:
    return LABELS_CATEGORIES.get(cat, cat)


# ---------------------------------------------------------------------------
# Onglet 1 : Top compétences
# ---------------------------------------------------------------------------

def chart_top_competences(df: pd.DataFrame) -> go.Figure:
    """Barres horizontales : top compétences par nombre d'offres."""
    if df.empty:
        return _vide("Aucune compétence trouvée avec ces filtres.")

    df = df.copy().sort_values("nb_offres", ascending=True)
    df["label_cat"] = df["categorie"].map(_label)

    fig = px.bar(
        df,
        x="nb_offres",
        y="competence_canonique",
        color="categorie",
        color_discrete_map=COULEURS,
        orientation="h",
        text="nb_offres",
        labels={
            "nb_offres": "Offres",
            "competence_canonique": "",
            "categorie": "Catégorie",
        },
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#6B7280"),
        marker_line_width=0,
    )
    fig.update_layout(
        title="Compétences les plus demandées",
        showlegend=True,
        legend=dict(
            title=None,
            orientation="h",
            yanchor="bottom", y=1.02,
            xanchor="right", x=1,
        ),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        # Force le tri par valeur (sinon le coloriage par categorie regroupe
        # les barres par couleur au lieu de les classer par nombre d'offres).
        yaxis=dict(showgrid=False, categoryorder="total ascending"),
        bargap=0.35,
    )
    return _apply_theme(fig, height=max(380, len(df) * 30))


def chart_repartition_categories(df: pd.DataFrame) -> go.Figure:
    """Donut : répartition par catégorie."""
    if df.empty:
        return _vide("Aucune donnée disponible.")

    df = df.copy().dropna(subset=["categorie"])   # élimine les catégories NULL
    df["label"] = df["categorie"].map(_label)

    fig = go.Figure(go.Pie(
        labels=df["label"],
        values=df["nb_offres"],
        hole=0.55,
        marker=dict(
            colors=[COULEURS.get(c, GRIS) for c in df["categorie"]],
            line=dict(color="white", width=2),
        ),
        textinfo="percent",
        textfont=dict(size=12),
        hovertemplate="<b>%{label}</b><br>%{value} offres (%{percent})<extra></extra>",
    ))
    # On affiche le NOMBRE DE CATEGORIES, pas une somme d'offres : un meme
    # offre peut appartenir a plusieurs categories, donc sommer les parts
    # double-compterait et donnerait un total > nb d'offres reelles.
    fig.add_annotation(
        text=f"<b>{len(df)}</b><br><span style='font-size:10px;color:#9CA3AF'>catégories</span>",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="#111827"),
        align="center",
    )
    fig.update_layout(
        title="Répartition par catégorie",
        showlegend=True,
        legend=dict(
            orientation="v",
            xanchor="left", x=1.02,
            yanchor="middle", y=0.5,
        ),
    )
    return _apply_theme(fig, height=320)


def chart_salaires(df: pd.DataFrame) -> go.Figure:
    """Barres groupées : salaire min/max par séniorité."""
    if df.empty:
        return _vide("Pas assez de données salariales.")

    df = df.copy()
    df["salaire_min_moyen"] = df["salaire_min_moyen"].astype(float)
    df["salaire_max_moyen"] = df["salaire_max_moyen"].astype(float)
    df = df.sort_values("salaire_min_moyen", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Min moyen",
        x=df["seniorite"],
        y=df["salaire_min_moyen"],
        marker_color=GRIS_CLAIR,
        marker_line_width=0,
        text=df["salaire_min_moyen"].apply(lambda v: f"{int(v):,} €"),
        textposition="outside",
        textfont=dict(size=11, color="#6B7280"),
    ))
    fig.add_trace(go.Bar(
        name="Max moyen",
        x=df["seniorite"],
        y=df["salaire_max_moyen"],
        marker_color=ENCRE,
        marker_line_width=0,
        text=df["salaire_max_moyen"].apply(lambda v: f"{int(v):,} €"),
        textposition="outside",
        textfont=dict(size=11, color="#6B7280"),
    ))
    fig.update_layout(
        title="Fourchette salariale par séniorité (€/an)",
        barmode="group",
        bargap=0.25,
        bargroupgap=0.05,
        yaxis=dict(showgrid=True, ticksuffix=" €", showticklabels=False),
        xaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return _apply_theme(fig, height=350)


def chart_salaire_par_competence(df: pd.DataFrame) -> go.Figure:
    """Barres horizontales : salaire médian par compétence (les mieux payées en haut)."""
    if df.empty:
        return _vide("Pas assez de données salariales par compétence.")

    df = df.copy().sort_values("salaire_median", ascending=True)
    df["salaire_median"] = df["salaire_median"].astype(float)

    fig = px.bar(
        df,
        x="salaire_median",
        y="competence_canonique",
        color="categorie",
        color_discrete_map=COULEURS,
        orientation="h",
        text=df["salaire_median"].apply(lambda v: f"{int(v):,} €"),
        labels={
            "salaire_median": "Salaire médian (€/an)",
            "competence_canonique": "",
            "categorie": "Catégorie",
        },
    )
    fig.update_traces(
        textposition="outside",
        textfont=dict(size=11, color="#6B7280"),
        marker_line_width=0,
    )
    fig.update_layout(
        title="Salaire médian par compétence (€/an)",
        showlegend=True,
        legend=dict(
            title=None, orientation="h",
            yanchor="bottom", y=1.02, xanchor="right", x=1,
        ),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, categoryorder="total ascending"),
        bargap=0.35,
    )
    return _apply_theme(fig, height=max(380, len(df) * 30))


def chart_evolution(df: pd.DataFrame) -> go.Figure:
    """Aire : volume d'offres par semaine."""
    if df.empty or len(df) < 2:
        return _vide("Pas assez de données temporelles.")

    df = df.copy()
    df["semaine"] = pd.to_datetime(df["semaine"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["semaine"],
        y=df["nb_offres"],
        mode="lines",
        fill="tozeroy",
        line=dict(color=ENCRE, width=2),
        fillcolor="rgba(20,20,20,0.06)",
        hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y} offres<extra></extra>",
    ))
    fig.update_layout(
        title="Volume d'offres par semaine",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True),
    )
    return _apply_theme(fig, height=300)


# ---------------------------------------------------------------------------
# Onglet 2 : IA vs Classiques
# ---------------------------------------------------------------------------

def chart_ia_vs_classiques(df: pd.DataFrame) -> go.Figure:
    """Courbes : évolution mensuelle IA vs classiques."""
    if df.empty:
        return _vide("Pas assez de données temporelles.")

    df = df.copy()
    df["mois"] = pd.to_datetime(df["mois"])

    fig = go.Figure()
    for cat, color in [("classique", COULEURS["classique"]), ("ia_llm", COULEURS["ia_llm"])]:
        sub = df[df["categorie"] == cat]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["mois"],
            y=sub["nb_offres"],
            name=_label(cat),
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color, line=dict(color="white", width=1.5)),
            hovertemplate=f"<b>{_label(cat)}</b><br>%{{x|%B %Y}}<br>%{{y}} offres<extra></extra>",
        ))
    fig.update_layout(
        title="Compétences IA vs Classiques, évolution mensuelle",
        xaxis=dict(showgrid=False, tickformat="%b %Y"),
        yaxis=dict(showgrid=True),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return _apply_theme(fig, height=380)


# ---------------------------------------------------------------------------
# Onglet 3 : Séniorité & IA
# ---------------------------------------------------------------------------

def chart_correlation_seniorite_ia(df: pd.DataFrame) -> go.Figure:
    """Barres horizontales : % offres IA par séniorité."""
    if df.empty:
        return _vide("Pas de données de séniorité disponibles.")

    df = df.copy()
    df["pct_ia"] = df["pct_ia"].astype(float)
    df = df.sort_values("pct_ia", ascending=True)

    # Dégradé de couleur selon le %
    max_pct = float(df["pct_ia"].max()) or 1.0
    colors = [
        f"rgba(226,35,26,{0.25 + 0.75 * (float(v) / max_pct):.2f})"
        for v in df["pct_ia"]
    ]

    fig = go.Figure(go.Bar(
        x=df["pct_ia"],
        y=df["seniorite"],
        orientation="h",
        marker=dict(color=colors, line=dict(width=0)),
        text=df["pct_ia"].apply(lambda v: f"{int(v)} %"),
        textposition="outside",
        textfont=dict(size=12, color="#374151"),
        customdata=df[["total_offres", "offres_ia"]].values,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "%{x} % des offres mentionnent l'IA<br>"
            "%{customdata[1]} / %{customdata[0]} offres<extra></extra>"
        ),
    ))
    fig.update_layout(
        title="Part des offres mentionnant l'IA, par séniorité",
        xaxis=dict(
            showgrid=False, showticklabels=False,
            range=[0, df["pct_ia"].max() * 1.25],
        ),
        yaxis=dict(showgrid=False),
    )
    return _apply_theme(fig, height=320)


# ---------------------------------------------------------------------------
# Onglet 4 : Géographie
# ---------------------------------------------------------------------------

def chart_disparites_geo(df: pd.DataFrame) -> go.Figure:
    """Bulles : salaire vs % IA par zone géographique."""
    if df.empty:
        return _vide("Pas de données géographiques.")

    df = df.copy().fillna(0)
    for col in ["salaire_median", "pct_ia", "nb_offres", "teletravail_moyen"]:
        if col in df.columns:
            df[col] = df[col].astype(float)

    fig = go.Figure()
    for _, row in df.iterrows():
        zone = row["zone"]
        color = COULEURS_ZONES.get(zone, GRIS)
        fig.add_trace(go.Scatter(
            x=[row["salaire_median"]],
            y=[row["pct_ia"]],
            mode="markers+text",
            name=zone,
            text=[zone],
            textposition="top center",
            textfont=dict(size=12, color="#374151"),
            marker=dict(
                size=max(20, min(80, row["nb_offres"] / 15)),
                color=color,
                opacity=0.85,
                line=dict(color="white", width=2),
            ),
            hovertemplate=(
                f"<b>{zone}</b><br>"
                "Salaire médian : %{x:,.0f} €<br>"
                "% IA : %{y} %<br>"
                f"Offres : {int(row['nb_offres']):,}<extra></extra>"
            ),
        ))
    fig.update_layout(
        title="Disparités géographiques, salaire médian vs présence de l'IA",
        xaxis=dict(title="Salaire médian annuel (€)", tickformat=",.0f", ticksuffix=" €"),
        yaxis=dict(title="% offres mentionnant l'IA", ticksuffix=" %"),
        showlegend=False,
    )
    return _apply_theme(fig, height=420)


def table_disparites_geo(df: pd.DataFrame) -> pd.DataFrame:
    """DataFrame formaté pour st.dataframe()."""
    if df.empty:
        return df
    return df.rename(columns={
        "zone":              "Zone",
        "nb_offres":         "Offres",
        "salaire_median":    "Salaire médian (€)",
        "pct_ia":            "% IA",
        "teletravail_moyen": "Télétravail (j/sem)",
    })


# ---------------------------------------------------------------------------
# Utilitaire
# ---------------------------------------------------------------------------

def _vide(message: str) -> go.Figure:
    """Figure vide avec message centré."""
    fig = go.Figure()
    fig.add_annotation(
        text=message, xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=14, color="#9CA3AF"),
    )
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=280,
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ("xaxis", "yaxis")},
    )
    return fig
