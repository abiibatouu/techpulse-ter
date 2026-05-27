"""Configuration du perimetre TechPulse.

Responsabilite unique : centraliser les parametres metier (codes ROME du
perimetre tech, chemin du lac) pour qu'ils soient versionnes et faciles
a faire evoluer.

La liste exacte des codes ROME RESTE A VALIDER avec l'encadrant a partir
du referentiel ROME 4.0 officiel. La liste ci-dessous est un point de
depart raisonnable couvrant la famille M18 (Informatique et
telecommunications).
"""

# Famille M18 - Informatique et telecommunications (ROME 4.0).
# A confirmer avec l'encadrant.
ROME_CODES_TECH = [
    "M1801",  # Administration de systemes d'information
    "M1802",  # Conseil et maitrise d'ouvrage en systemes d'information
    "M1803",  # Direction des systemes d'information
    "M1805",  # Etudes et developpement informatique (le plus large - dev, data)
    "M1806",  # Conseil et MOA en systemes d'information / etudes
    "M1810",  # Production et exploitation de systemes d'information
]

# Racine du lac de donnees brutes. Cree automatiquement au besoin.
# A ne PAS versionner (cf. .gitignore).
LAKE_ROOT = "data/raw"
