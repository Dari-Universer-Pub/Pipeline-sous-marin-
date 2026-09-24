"""Generateur de PNG indexes de FIXTURE (stdlib seule).

USAGE STRICTEMENT LIMITE AUX TESTS DE LA PIPELINE.
Ce script ne produit JAMAIS un asset de production: la production visuelle
appartient au framework Blender. Il ne doit jamais servir a remplacer,
redessiner ou reparer un binaire livre manquant ou corrompu.
"""
from __future__ import annotations
import struct, zlib
from pathlib import Path


def _chunk(ctype: bytes, payload: bytes) -> bytes:
    return (struct.pack(">I", len(payload)) + ctype + payload
            + struct.pack(">I", zlib.crc32(ctype + payload) & 0xFFFFFFFF))


def indexed_png(path, width: int, height: int, palette, pixels=None) -> Path:
    """Ecrit un PNG indexe 8 bits. `palette` = liste de (r,g,b), <=256 entrees.

    `pixels` = fonction (x, y) -> index de palette. Defaut: damier deterministe.
    """
    if not 1 <= len(palette) <= 256:
        raise ValueError("palette: 1 a 256 entrees")
    if pixels is None:
        def pixels(x, y):
            return (x // 4 + y // 4) % len(palette)
    raw = bytearray()
    for y in range(height):
        raw.append(0)  # filtre None, rendu deterministe
        for x in range(width):
            raw.append(pixels(x, y) % len(palette))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 3, 0, 0, 0)
    plte = b"".join(bytes(c) for c in palette)
    data = (b"\x89PNG\r\n\x1a\n" + _chunk(b"IHDR", ihdr) + _chunk(b"PLTE", plte)
            + _chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + _chunk(b"IEND", b""))
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
    return p
