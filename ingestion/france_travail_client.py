"""Client de l'API France Travail.

Responsabilite unique : parler a l'API France Travail (authentification
OAuth2, recuperation des offres, pagination). Ce module ne connait ni
la base de donnees, ni le lac, ni l'orchestration du pipeline.

Contraintes de l'API (cf. conception_lac_de_donnees.md, sec. 2) :
  - une page = 150 resultats maximum
  - debut de range : 0 a 1000
  - fin de range : <= 1149
  - donc : 1150 resultats maximum par recherche
  - le total reel est donne par l'en-tete HTTP `Content-Range`
"""
import os
import time

import requests

OAUTH_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"

PAGE_SIZE = 150          # nombre max de resultats par page
MAX_RANGE_END = 1149     # fin maximum (donc 1150 resultats par recherche au max)
COURTESY_SLEEP_SEC = 0.5 # pause entre 2 appels API


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
    response = requests.post(OAUTH_URL, params=params, data=data, timeout=30)
    response.raise_for_status()
    return response.json()["access_token"]


def _parse_content_range(header):
    """Extrait le total d'une en-tete Content-Range ('offres start-end/total').

    Retourne None si l'en-tete est absente ou mal formee.
    """
    if not header:
        return None
    try:
        return int(header.rsplit("/", 1)[-1])
    except (ValueError, IndexError):
        return None


def fetch_page(token, code_rome, range_start, range_end,
               min_creation_date=None, max_creation_date=None):
    """Recupere une page de resultats pour un code ROME.

    Retourne (payload_json, total_results_or_None).

    Statuts HTTP attendus :
      - 200 : reponse complete (rare pour une recherche large)
      - 206 : Partial Content (cas normal de pagination)
      - 204 : No Content (aucun resultat)
    """
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/json",
    }
    params = {
        "codeROME": code_rome,
        "range": f"{range_start}-{range_end}",
    }
    if min_creation_date:
        params["minCreationDate"] = min_creation_date
    if max_creation_date:
        params["maxCreationDate"] = max_creation_date

    response = requests.get(SEARCH_URL, headers=headers, params=params, timeout=60)

    if response.status_code == 204:
        return {"resultats": []}, 0

    if response.status_code not in (200, 206):
        response.raise_for_status()

    total = _parse_content_range(response.headers.get("Content-Range"))
    return response.json(), total


def paginate(token, code_rome, min_creation_date=None, max_creation_date=None):
    """Itere sur toutes les pages d'une recherche.

    Yields (range_start, range_end, payload, total_annonce).

    Plafond dur de l'API : 1150 resultats par recherche. Si la
    recherche depasse ce plafond, l'appelant doit sous-decouper la
    recherche (par fenetre de dates, par departement, etc.).
    """
    range_start = 0
    while True:
        range_end = min(range_start + PAGE_SIZE - 1, MAX_RANGE_END)
        payload, total = fetch_page(
            token, code_rome, range_start, range_end,
            min_creation_date=min_creation_date,
            max_creation_date=max_creation_date,
        )
        yield range_start, range_end, payload, total

        # Conditions d'arret :
        #   - on a depasse le total annonce
        #   - on a atteint le plafond dur de l'API
        #   - on n'a recu aucun resultat (cas 204)
        if total is None or range_end >= total - 1 or range_end >= MAX_RANGE_END:
            break
        if not payload.get("resultats"):
            break

        range_start = range_end + 1
        time.sleep(COURTESY_SLEEP_SEC)
