"""Client de l'API France Travail.

Responsabilite unique : parler a l'API France Travail (authentification
OAuth2 et recuperation des offres). Ce module ne connait ni la base de
donnees, ni l'orchestration du pipeline.
"""
import os

import requests

OAUTH_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"


def get_access_token():
    """Recupere un jeton d'acces OAuth2 (flux client_credentials)."""
    client_id = os.getenv("FRANCE_TRAVAIL_CLIENT_ID")
    client_secret = os.getenv("FRANCE_TRAVAIL_CLIENT_SECRET")
    params = {"realm": "/partenaire"}
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "api_offresdemploiv2 o2dsoffre",
    }
    response = requests.post(OAUTH_URL, params=params, data=data)
    return response.json()["access_token"]


def fetch_offres(token):
    """Interroge l'API et renvoie la reponse JSON brute des offres."""
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
    }
    params = {"motsCles": "data engineer", "range": "0-49"}
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    return response.json()
