"""Verification BINAIRE des assets livres. Bibliotheque standard uniquement.

Un fichier image qui existe n'est PAS automatiquement un asset conforme.
Le nom du fichier et son extension ne font jamais foi: le format est
determine par les octets magiques.

Codes d'erreur (contractuels):
  asset.file_missing     fichier absent, illisible, ou hors du dossier de livraison
  asset.file_format      octets magiques non reconnus / incoherents
  asset.file_corrupt     CRC de chunk PNG invalide, segments JPEG invalides, troncature
  asset.file_hash        SHA-256 reel != SHA-256 declare
  asset.file_dimensions  dimensions reelles != dimensions du manifest
  asset.file_palette     PLTE contient des couleurs hors de la palette imposee
  asset.file_too_large   taille > borne (defaut 8 Mio)
"""
from __future__ import annotations
import struct, zlib
from pathlib import Path
from .util import sha256_bytes, is_within

MAX_BYTES = 8 * 1024 * 1024  # 8 Mio
PNG_SIG = b"\x89PNG\r\n\x1a\n"

# SOF0..SOF15 hors marqueurs non-SOF (DHT=C4, JPG=C8, DAC=CC)
_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
        0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


class BinaryError(Exception):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail = code, detail


# ---------------------------------------------------------------- PNG

def _parse_png(data: bytes) -> dict:
    """Parcourt tous les chunks, verifie chaque CRC-32. Retourne les metadonnees."""
    if len(data) < 8 or data[:8] != PNG_SIG:
        raise BinaryError("asset.file_format", "signature PNG absente")
    pos, info, order = 8, {"format": "png", "palette": None}, []
    seen_ihdr = seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise BinaryError("asset.file_corrupt", f"en-tete de chunk tronque a l'offset {pos}")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            raise BinaryError("asset.file_corrupt",
                              f"chunk {ctype.decode('latin1')} tronque "
                              f"(annonce {length} octets, offset {pos})")
        payload = data[pos + 8:pos + 8 + length]
        (declared_crc,) = struct.unpack(">I", data[pos + 8 + length:end])
        actual_crc = zlib.crc32(ctype + payload) & 0xFFFFFFFF
        if declared_crc != actual_crc:
            raise BinaryError("asset.file_corrupt",
                              f"CRC invalide sur le chunk {ctype.decode('latin1')} "
                              f"(declare {declared_crc:08x}, calcule {actual_crc:08x})")
        order.append(ctype)
        if ctype == b"IHDR":
            if length != 13:
                raise BinaryError("asset.file_corrupt", f"IHDR de longueur {length}, attendu 13")
            w, h, depth, color = struct.unpack(">IIBB", payload[:10])
            if w == 0 or h == 0:
                raise BinaryError("asset.file_corrupt", f"dimensions nulles {w}x{h}")
            info.update(width=w, height=h, bit_depth=depth, color_type=color)
            seen_ihdr = True
        elif ctype == b"PLTE":
            if length % 3 or length == 0:
                raise BinaryError("asset.file_corrupt", f"PLTE de longueur {length} (non multiple de 3)")
            info["palette"] = [tuple(payload[i:i + 3]) for i in range(0, length, 3)]
        elif ctype == b"IEND":
            seen_iend = True
        pos = end
    if not seen_ihdr:
        raise BinaryError("asset.file_corrupt", "chunk IHDR absent")
    if not seen_iend:
        raise BinaryError("asset.file_corrupt", "chunk IEND absent (fichier tronque)")
    if order[0] != b"IHDR":
        raise BinaryError("asset.file_corrupt", "IHDR n'est pas le premier chunk")
    if info.get("color_type") == 3 and info["palette"] is None:
        raise BinaryError("asset.file_corrupt", "PNG indexe (color_type 3) sans chunk PLTE")
    info["indexed"] = info.get("color_type") == 3
    info["has_alpha"] = info.get("color_type") in (4, 6) or b"tRNS" in order
    return info


# --------------------------------------------------------------- JPEG

def _parse_jpeg(data: bytes) -> dict:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        raise BinaryError("asset.file_format", "marqueur SOI absent")
    pos = 2
    while pos < len(data):
        if data[pos] != 0xFF:
            raise BinaryError("asset.file_corrupt", f"octet de marqueur attendu a l'offset {pos}")
        while pos < len(data) and data[pos] == 0xFF:
            pos += 1
        if pos >= len(data):
            raise BinaryError("asset.file_corrupt", "flux termine sur un remplissage 0xFF")
        marker = data[pos]; pos += 1
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            continue
        if marker == 0xD9:
            raise BinaryError("asset.file_corrupt", "EOI atteint avant tout segment SOF")
        if pos + 2 > len(data):
            raise BinaryError("asset.file_corrupt", "longueur de segment tronquee")
        (seg_len,) = struct.unpack(">H", data[pos:pos + 2])
        if seg_len < 2 or pos + seg_len > len(data):
            raise BinaryError("asset.file_corrupt",
                              f"segment 0x{marker:02x} invalide (longueur {seg_len})")
        if marker in _SOF:
            if seg_len < 7:
                raise BinaryError("asset.file_corrupt", "segment SOF trop court")
            h, w = struct.unpack(">HH", data[pos + 3:pos + 7])
            if w == 0 or h == 0:
                raise BinaryError("asset.file_corrupt", f"dimensions nulles {w}x{h}")
            return {"format": "jpeg", "width": w, "height": h,
                    "palette": None, "indexed": False, "has_alpha": False}
        pos += seg_len
    raise BinaryError("asset.file_corrupt", "aucun segment SOF trouve")


# ------------------------------------------------------------ API

def sniff(data: bytes) -> str:
    if data[:8] == PNG_SIG:
        return "png"
    if data[:2] == b"\xff\xd8":
        return "jpeg"
    raise BinaryError("asset.file_format",
                      f"octets magiques inconnus: {data[:8].hex()}")


def probe(path) -> dict:
    """Lit un binaire et en extrait les metadonnees reelles. Leve BinaryError."""
    p = Path(path)
    if not p.is_file():
        raise BinaryError("asset.file_missing", f"fichier absent: {p}")
    data = p.read_bytes()
    if len(data) == 0:
        raise BinaryError("asset.file_corrupt", "fichier vide")
    if len(data) > MAX_BYTES:
        raise BinaryError("asset.file_too_large", f"{len(data)} octets > borne {MAX_BYTES}")
    fmt = sniff(data)
    info = _parse_png(data) if fmt == "png" else _parse_jpeg(data)
    info["size_bytes"] = len(data)
    info["sha256"] = sha256_bytes(data)
    return info


def verify(path, *, expected_sha256=None, expected_width=None, expected_height=None,
           allowed_palette=None, expected_format=None, max_bytes=MAX_BYTES,
           delivery_dir=None) -> dict:
    """Verification binaire complete d'un asset livre.

    Retourne {ok, info, errors:[{code, detail}]}. N'ecrit rien, ne repare rien.
    """
    errors, info = [], None
    p = Path(path)
    if delivery_dir is not None and not is_within(delivery_dir, p):
        return {"ok": False, "info": None, "errors": [{
            "code": "asset.file_missing",
            "detail": f"chemin hors du dossier de livraison {delivery_dir}: {p}"}]}
    try:
        info = probe(p)
        if info["size_bytes"] > max_bytes:
            errors.append({"code": "asset.file_too_large",
                           "detail": f"{info['size_bytes']} > {max_bytes}"})
    except BinaryError as e:
        return {"ok": False, "info": None, "errors": [{"code": e.code, "detail": e.detail}]}

    if expected_format and info["format"] != expected_format:
        errors.append({"code": "asset.file_format",
                       "detail": f"format reel {info['format']}, attendu {expected_format}"})
    if expected_sha256 and info["sha256"] != expected_sha256.lower():
        errors.append({"code": "asset.file_hash",
                       "detail": f"reel {info['sha256']}, declare {expected_sha256.lower()}"})
    if expected_width is not None and info["width"] != expected_width:
        errors.append({"code": "asset.file_dimensions",
                       "detail": f"largeur reelle {info['width']}, specifiee {expected_width}"})
    if expected_height is not None and info["height"] != expected_height:
        errors.append({"code": "asset.file_dimensions",
                       "detail": f"hauteur reelle {info['height']}, specifiee {expected_height}"})
    if allowed_palette is not None:
        allowed = {tuple(c) for c in allowed_palette}
        if info["palette"] is None:
            if info["indexed"]:
                errors.append({"code": "asset.file_palette",
                               "detail": "PNG indexe sans PLTE lisible"})
            else:
                errors.append({"code": "asset.file_palette",
                               "detail": "palette imposee mais image non indexee "
                                         "(PLTE absent, palette reelle non verifiable)"})
        else:
            extra = sorted(set(info["palette"]) - allowed)
            if extra:
                errors.append({"code": "asset.file_palette",
                               "detail": f"{len(extra)} couleur(s) hors palette, "
                                         f"ex: {['#%02x%02x%02x' % c for c in extra[:5]]}"})
    return {"ok": not errors, "info": info, "errors": errors}
