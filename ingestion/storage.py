"""Backend de stockage du lac de donnees.

Responsabilite unique : abstraire le support physique de stockage
(systeme de fichiers local, plus tard S3 / MinIO) derriere une interface
commune. Le reste du code (`lake.py`) ne sait jamais ou sont reellement
ecrits les octets.

Cette abstraction est la cle de la portabilite vers MinIO/S3 en S7 :
seul ce fichier change, le pipeline reste identique.
"""
from pathlib import Path
from typing import Iterable, Protocol


class Storage(Protocol):
    """Interface commune des backends de stockage.

    Une 'key' est un chemin logique de type 'france_travail/2026/05/27/M1805_0000-0149.json'.
    Le backend traduit cette key en chemin physique (fichier, objet S3, etc.).
    """

    def write(self, key: str, content: bytes) -> None: ...
    def read(self, key: str) -> bytes: ...
    def exists(self, key: str) -> bool: ...
    def list_prefix(self, prefix: str) -> Iterable[str]: ...


class FilesystemStorage:
    """Backend systeme de fichiers local.

    Les keys sont des chemins relatifs sous `root`. Les dossiers
    intermediaires sont crees a la demande.
    """

    def __init__(self, root):
        self.root = Path(root)

    def _path(self, key: str) -> Path:
        # Normalise les separateurs : la key utilise toujours '/', mais sous
        # Windows on doit construire un Path natif.
        parts = key.split("/")
        return self.root.joinpath(*parts)

    def write(self, key: str, content: bytes) -> None:
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def read(self, key: str) -> bytes:
        return self._path(key).read_bytes()

    def exists(self, key: str) -> bool:
        return self._path(key).exists()

    def list_prefix(self, prefix: str) -> Iterable[str]:
        base = self._path(prefix) if prefix else self.root
        if not base.exists():
            return []
        keys = []
        for path in base.rglob("*"):
            if path.is_file():
                rel = path.relative_to(self.root).as_posix()
                keys.append(rel)
        return sorted(keys)


# Note pour S7 : ajouter ici une classe S3Storage(endpoint, bucket, ...)
# qui implemente la meme interface en s'appuyant sur boto3 ou minio-py.
# Aucun autre fichier du projet ne devra changer.
