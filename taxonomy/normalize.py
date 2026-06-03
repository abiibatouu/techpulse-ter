"""Normalisation des competences extraites par le LLM.

Responsabilite unique : trouver la competence canonique la plus proche
dans la taxonomie pour une competence brute donnee.
Ce module ne connait ni la base de donnees, ni les offres.
"""
from rapidfuzz import process, fuzz
import taxonomy
SEUIL_SIMILARITE = 80  # score minimum pour accepter une correspondance (sur 100)


def normaliser(competence_brute):
    """Trouve la competence canonique la plus proche dans la taxonomie.
    
    Retourne (competence_canonique, categorie, score) ou None si aucune
    correspondance n'est assez proche.
    """
    candidats = list(taxonomy.TAXONOMY.keys())
    
    resultat = process.extractOne(
        competence_brute,
        candidats,
        scorer=fuzz.token_sort_ratio
    )
    
    if resultat is None or resultat[1] < SEUIL_SIMILARITE:
        return None
    
    competence_canonique = resultat[0]
    categorie = taxonomy.TAXONOMY[competence_canonique]
    score = resultat[1]
    
    return competence_canonique, categorie, score