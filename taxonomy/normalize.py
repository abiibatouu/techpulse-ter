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
    
    # token_set_ratio (et non token_sort_ratio) : matche sur l'INTERSECTION
    # des mots, donc retrouve une competence canonique noyee dans une chaine
    # longue. Ex : "Windows Server" dans "Administration systeme (Windows
    # Server 2019/2022, Debian)".
    resultats = process.extract(
        competence_brute,
        candidats,
        scorer=fuzz.token_set_ratio,
        limit=10,
    )

    if not resultats or resultats[0][1] < SEUIL_SIMILARITE:
        return None

    meilleur_score = resultats[0][1]

    # Plusieurs canoniques peuvent etre a egalite : "Windows" ET "Windows
    # Server" scorent tous deux 100 pour la brute "Windows Server", car
    # token_set_ratio ignore les mots en trop. On departage en gardant le
    # candidat le plus FIDELE a la chaine entiere (token_sort_ratio), ce qui
    # privilegie le terme le plus specifique au lieu du plus generique.
    ex_aequo = [cand for cand, score, _ in resultats if score == meilleur_score]
    competence_canonique = max(
        ex_aequo,
        key=lambda cand: fuzz.token_sort_ratio(competence_brute, cand),
    )
    categorie = taxonomy.TAXONOMY[competence_canonique]

    return competence_canonique, categorie, meilleur_score