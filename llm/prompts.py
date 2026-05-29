"""Prompts pour l'extraction LLM.

Responsabilite unique : construire les messages envoyes au LLM.
Ce module ne connait ni Mistral, ni la base de donnees.
"""

SYSTEM_PROMPT = """Tu es un assistant spécialisé en analyse d'offres d'emploi tech.
Tu extrais des informations structurées depuis une fiche de poste.
Tu réponds UNIQUEMENT en JSON valide, sans texte avant ni après."""
def build_extraction_prompt(description):
    return f"""Analyse cette offre d'emploi et extrais les informations suivantes en JSON :

{{
  "competences": ["liste", "des", "competences", "techniques"],
  "seniorite": "junior | confirmé | senior | non précisé",
  "salaire_min": null,
  "salaire_max": null,
  "jours_teletravail": null,
  "type_contrat": "CDI | CDD | Stage | Freelance | non précisé",
  "mention_ia": true
}}

Fiche de poste :
{description}"""