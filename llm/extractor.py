"""Extraction LLM des informations structurees depuis une offre.

Responsabilite unique : orchestrer l'extraction - appeler les prompts,
appeler Mistral, nettoyer et valider le JSON retourne.
Ce module ne connait ni la base de donnees, ni l'orchestration generale.
"""
import json
import prompts
import mistral_client


def _clean_json(raw):
    """Enleve les balises markdown autour du JSON."""
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()


# Valeurs autorisees pour les champs contraints (colonnes VARCHAR(20)).
SENIORITES = {"junior", "confirmé", "senior", "non précisé"}
CONTRATS = {"CDI", "CDD", "Stage", "Freelance", "non précisé"}


def _to_int_or_none(valeur):
    """Convertit en entier, ou None si ce n'est pas un entier valide.

    Indispensable car le LLM renvoie parfois du texte ('hybride',
    'non précisé') dans des champs censes etre numeriques.
    """
    try:
        return int(valeur)
    except (TypeError, ValueError):
        return None


def _normalize(data):
    """Valide et type la sortie du LLM avant insertion en base.

    Ne fait jamais confiance au LLM : toute valeur hors-format est
    ramenee a une valeur sure ('non précisé' ou None), ce qui evite
    les erreurs de type cote PostgreSQL.
    """
    seniorite = data.get("seniorite")
    type_contrat = data.get("type_contrat")
    return {
        "competences": data.get("competences") or [],
        "seniorite": seniorite if seniorite in SENIORITES else "non précisé",
        "salaire_min": _to_int_or_none(data.get("salaire_min")),
        "salaire_max": _to_int_or_none(data.get("salaire_max")),
        "jours_teletravail": _to_int_or_none(data.get("jours_teletravail")),
        "type_contrat": type_contrat if type_contrat in CONTRATS else "non précisé",
        "mention_ia": bool(data.get("mention_ia")),
    }


def extract_from_description(description, client):
    user_prompt = prompts.build_extraction_prompt(description)
    raw = mistral_client.call_llm(client, prompts.SYSTEM_PROMPT, user_prompt)
    try:
        return _normalize(json.loads(_clean_json(raw)))
    except json.JSONDecodeError:
        raise ValueError(f"Réponse du LLM n'est pas un JSON valide : {raw}")