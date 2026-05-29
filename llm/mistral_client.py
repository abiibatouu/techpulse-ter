"""Client de l'API Mistral.

Responsabilite unique : envoyer des prompts a Mistral et retourner la reponse brute.
Ce module ne connait ni le contenu des prompts, ni la base de donnees, ni les offres.
"""
import os
import requests

MODEL = "mistral-small-latest"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"


def get_client():
    return os.getenv("MISTRAL_API_KEY")


def call_llm(client, system_prompt, user_prompt):
    headers = {
        "Authorization": "Bearer " + client,
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }
    response = requests.post(MISTRAL_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]