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


def extract_from_description(description, client):
    user_prompt = prompts.build_extraction_prompt(description)
    raw = mistral_client.call_llm(client, prompts.SYSTEM_PROMPT, user_prompt)
    try:
        return json.loads(_clean_json(raw))
    except json.JSONDecodeError:
        raise ValueError(f"Réponse du LLM n'est pas un JSON valide : {raw}")