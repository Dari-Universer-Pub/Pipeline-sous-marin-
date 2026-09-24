"""Rapports: maturite, elements manquants, isoles, decisions ouvertes, tracabilite."""
from __future__ import annotations
from .assets_bin import load_registry
from .decisions import DECISIONS
from .graph import analyse
from .status import ASSET_LIFECYCLE, ENTITY_MATURITY
from .util import ROOT, write_json


def maturity(catalogs, manifests, graph):
    reg = load_registry()
    rows = []
    for a in manifests["assets"]["entries"]:
        stored = a["id"] in reg["entries"]
        rows.append({"id": a["id"], "kind": "asset", "status": a["status"],
                     "stored_binary": stored,
                     "complete": a["status"] == "ART_GREEN",
                     "next_step": _next(ASSET_LIFECYCLE, a["status"])})
    for an in manifests["animations"]["entries"]:
        rows.append({"id": an["id"], "kind": "animation", "status": an["status"],
                     "stored_binary": False, "complete": an["status"] == "ART_GREEN",
                     "next_step": _next(ASSET_LIFECYCLE, an["status"])})
    dist = {}
    for r in rows:
        dist[r["status"]] = dist.get(r["status"], 0) + 1
    return {"total": len(rows), "distribution": dict(sorted(dist.items())),
            "complete": sum(1 for r in rows if r["complete"]),
            "rule": "Aucun asset n'est termine avant ART_GREEN. Un asset GENERATED "
                    "mais non importe, valide et teste en contexte est INCOMPLET.",
            "rows": sorted(rows, key=lambda r: r["id"])}


def _next(cycle, status):
    if status == "BLOCKED" or status not in cycle:
        return None
    i = cycle.index(status)
    return cycle[i + 1] if i + 1 < len(cycle) else None


def missing(catalogs, manifests, graph):
    items = []
    for name in ("anomalies", "traces", "evenements", "ressources"):
        b = catalogs[name]
        if b["count"] == 0:
            items.append({"what": f"catalogue {name}", "count": 0,
                          "blocked_by": b["blocking_decision"], "reason": b["reason"]})
    for fam, meta in manifests["blocked_families"].items():
        items.append({"what": f"famille d'assets {fam}", "count": 0,
                      "blocked_by": meta["blocked_by"], "reason": meta["reason"]})
    reg = load_registry()
    for a in manifests["assets"]["entries"]:
        if a["id"] not in reg["entries"]:
            items.append({"what": f"binaire de {a['id']}", "count": 0,
                          "blocked_by": "dec_chemin_blender",
                          "reason": "aucun binaire livre: le framework Blender est "
                                    "introuvable; aucun placeholder n'est dessine"})
    return {"total": len(items), "items": items}


def isolated(graph):
    a = analyse(graph)
    return {"orphans": a["orphans"], "sinks": a["sinks"], "sources": a["sources"],
            "weakly_useful": a["weakly_useful"],
            "connected": a["connected"], "component_count": a["component_count"],
            "note": "Une relation technique unique ne suffit pas a declarer une "
                    "entite utile: 'weakly_useful' liste les entites a renforcer."}


def open_decisions():
    rows = [d for d in DECISIONS if d["status"] in ("TO_VALIDATE", "BLOCKED")]
    return {"total": len(rows),
            "owner_decisions": sorted(d["id"] for d in rows if d["status"] == "TO_VALIDATE"),
            "blocked": sorted(d["id"] for d in rows if d["status"] == "BLOCKED"),
            "rows": sorted(rows, key=lambda d: d["id"])}


def traceability(canon, catalogs, manifests, graph, validation):
    """Matrice: chaque type de contenu x chaque etape du contrat."""
    val_ok = {f["family"]: f["ok"] for f in validation["families"]}
    reg = load_registry()
    types = {
        "systemes_vitaux": catalogs["systemes_vitaux"]["count"],
        "zones": catalogs["zones"]["count"],
        "artefacts": catalogs["artefacts"]["count"],
        "equipage": catalogs["equipage"]["count"],
        "actions": catalogs["actions"]["count"],
        "objets": manifests["objets"]["count"],
        "maps": manifests["maps"]["count"],
        "placement": manifests["placement"]["count"],
        "assets": manifests["assets"]["count"],
        "animations": manifests["animations"]["count"],
        "anomalies": 0, "traces": 0, "evenements": 0, "ressources": 0,
    }
    rows = []
    for t, n in sorted(types.items()):
        blocked = n == 0
        rows.append({
            "type": t, "count": n,
            "specified": n > 0,
            "schema_validated": val_ok.get("structurel", False) and n > 0,
            "imported": t == "assets" and len(reg["entries"]) > 0,
            "cataloged": n > 0,
            "graph_connected": val_ok.get("logique", False) and n > 0,
            "compiled": n > 0 and t in ("systemes_vitaux", "zones", "actions", "objets"),
            "runtime_tested": False,
            "status": "BLOCKED" if blocked else "CATALOGED",
            "blocked_by": None if not blocked else "decision ouverte du proprietaire",
        })
    return {"row_count": len(rows),
            "note": "runtime_tested reste False partout: aucune integration Godot n'a "
                    "ete executee dans cette phase (hors perimetre: on livre la "
                    "fabrique, pas le jeu).",
            "rows": rows}


def write_all(*, canon, catalogs, manifests, graph, validation,
              outdir=ROOT / "REPORTS"):
    out = {}
    out["maturity"] = maturity(catalogs, manifests, graph)
    out["missing"] = missing(catalogs, manifests, graph)
    out["isolated"] = isolated(graph)
    out["open_decisions"] = open_decisions()
    out["traceability"] = traceability(canon, catalogs, manifests, graph, validation)
    hashes = {}
    for name, data in out.items():
        hashes[name] = write_json(outdir / f"{name}_report.json", data)
    return out, hashes
