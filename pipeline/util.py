"""Determinisme, hachage, IO JSON stable octet par octet."""
from __future__ import annotations
import hashlib, json, os, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def jdump(obj) -> str:
    """Serialisation JSON deterministe: cles triees, UTF-8, newline final."""
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_json(path, obj) -> str:
    """Ecrit un JSON deterministe. Retourne le SHA-256 du fichier ecrit."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = jdump(obj).encode("utf-8")
    p.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256_file(path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def rel(path) -> str:
    """Chemin relatif a la racine du depot, en separateurs POSIX (portable)."""
    return Path(path).resolve().relative_to(ROOT).as_posix()


def ascii_fold(text: str) -> str:
    """Retire les accents: 'Vitrail Noire' -> 'Vitrail Noire' (ASCII)."""
    return "".join(c for c in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(c))


def is_within(base, candidate) -> bool:
    """Vrai si candidate est contenu dans base (anti traversee de chemin)."""
    base = Path(base).resolve()
    try:
        Path(candidate).resolve().relative_to(base)
        return True
    except ValueError:
        return False
