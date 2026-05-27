"""Operations sur le lac de donnees brut.

Responsabilite unique : ecrire et lire des reponses brutes de l'API
sous une convention de nommage et de partitionnement stables.

Convention de partitionnement :
    <source>/<annee>/<mois>/<jour>/<codeROME>_<rangeStart>-<rangeEnd>.json

Un fichier = la reponse exacte d'un appel API (un code ROME, une page
de pagination). Immutable : une nouvelle execution ecrit de nouveaux
fichiers, ne reecrit jamais le passe.

Ce module ne connait pas le backend (fichiers, S3) : il manipule un
objet `storage` qui respecte le Protocol defini dans `storage.py`.
"""
import json
from datetime import date


def _day_prefix(source: str, day: date) -> str:
    """Prefixe d'une journee de collecte pour une source."""
    return f"{source}/{day:%Y}/{day:%m}/{day:%d}"


def _filename(code_rome: str, range_start: int, range_end: int) -> str:
    """Nom de fichier encodant le code ROME et la plage de pagination."""
    return f"{code_rome}_{range_start:04d}-{range_end:04d}.json"


def build_key(source: str, code_rome: str, range_start: int, range_end: int, day=None) -> str:
    """Construit la key complete d'un fichier de reponse brute."""
    day = day or date.today()
    return f"{_day_prefix(source, day)}/{_filename(code_rome, range_start, range_end)}"


def write_response(storage, source, code_rome, range_start, range_end, payload, day=None):
    """Ecrit une reponse brute d'API dans le lac.

    Retourne la key (chemin logique) du fichier ecrit.
    """
    key = build_key(source, code_rome, range_start, range_end, day)
    content = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    storage.write(key, content)
    return key


def iter_responses(storage, source, day=None):
    """Itere sur les fichiers de reponse d'une journee de collecte.

    Yields (key, payload) pour chaque reponse JSON, dans l'ordre des keys.
    Saute les fichiers de service comme '_manifest.json' (reserves pour
    une future evolution).
    """
    day = day or date.today()
    prefix = _day_prefix(source, day)
    for key in storage.list_prefix(prefix):
        filename = key.rsplit("/", 1)[-1]
        if not filename.endswith(".json") or filename.startswith("_"):
            continue
        payload = json.loads(storage.read(key).decode("utf-8"))
        yield key, payload
