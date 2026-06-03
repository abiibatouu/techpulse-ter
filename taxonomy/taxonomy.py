"""Taxonomie des competences tech.

Responsabilite unique : definir la liste de reference des competences
canoniques et leur categorie. Ce module ne connait ni la base de
donnees, ni l'algorithme de normalisation.
"""

TAXONOMY = {
    # Classiques
    "Python":       "classique",
    "SQL":          "classique",
    "ETL":          "classique",
    "Power BI":     "classique",
    "Tableau":      "classique",
    "Excel":        "classique",
    "Java":         "classique",
    "Git":          "classique",
    "Docker":       "classique",
    "Linux":        "classique",
    "JavaScript":       "classique",
    "Angular":          "classique",
    "C#":               "classique",
    "Windows":          "classique",
    "Windows Server":   "classique",
    "Active Directory": "classique",
    "CI/CD":            "classique",
    "Gestion de projet":"classique",
    "Cybersecurite":    "classique",
    "Documentation technique": "classique",
    "Veille technologique":    "classique",

    # IA / LLM
    "LangChain":    "ia_llm",
    "RAG":          "ia_llm",
    "Ollama":       "ia_llm",
    "Mistral":      "ia_llm",
    "OpenAI":       "ia_llm",
    "ChatGPT":      "ia_llm",
    "Prompt engineering": "ia_llm",
    "Intelligence artificielle": "ia_llm",
    "ChatGPT":          "ia_llm",

    # Emergentes
    "dbt":          "emergente",
    "DuckDB":       "emergente",
    "Prefect":      "emergente",
    "Airflow":      "emergente",
    "Spark":        "emergente",
    "Kafka":        "emergente",
    "Kubernetes":   "emergente",

    # Soft skills
    "Communication":    "soft_skill",
    "Autonomie":        "soft_skill",
    "Travail en equipe":"soft_skill",
    "Rigueur":          "soft_skill",
    "Conduite du changement":   "soft_skill",
    "Amelioration continue":    "soft_skill",
    "Formation utilisateurs":   "soft_skill",
}