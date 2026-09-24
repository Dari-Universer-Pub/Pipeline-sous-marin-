"""Graphe du monde + detection de connectivite.

Une relation technique ne suffit pas a declarer une entite utile: le graphe
mesure aussi degre, profondeur causale et nombre de systemes touches.
"""
from __future__ import annotations
from collections import deque
from .ontology import RELATION_TYPES
from .util import ROOT, write_json


def build(catalogs) -> dict:
    nodes, edges = {}, []

    def node(nid, kind, **kw):
        nodes[nid] = {"id": nid, "kind": kind, **kw}

    def edge(a, t, b, status="DERIVED"):
        edges.append({"from": a, "type": t, "to": b, "status": status})

    for e in catalogs["zones"]["entries"]:
        node(e["id"], "zone", role=e["role"], status=e["status"])
    for e in catalogs["systemes_vitaux"]["entries"]:
        node(e["id"], "vessel_system", status=e["status"])
    for e in catalogs["artefacts"]["entries"]:
        node(e["id"], "artifact", status=e["status"])
    for e in catalogs["equipage"]["entries"]:
        node(e["id"], "crew", status=e["status"])
    for e in catalogs["actions"]["entries"]:
        node(e["id"], "action", status=e["status"])

    base = "zone_le_vitrail_noire"
    for z in catalogs["zones"]["entries"]:
        if z["id"] != base:
            edge(base, "connects_to", z["id"], "DERIVED")
            edge(z["id"], "connects_to", base, "DERIVED")
            edge(z["id"], "damages", "systeme_coque", "DERIVED")

    for a in catalogs["actions"]["entries"]:
        if a["affects"]:
            edge(a["id"], "requires", a["affects"], "DERIVED")
    for art in catalogs["artefacts"]["entries"]:
        if art["acts_on"]:
            edge(art["id"], "repairs", art["acts_on"], "CANONICAL")
        edge(art["id"], "requires", art["gameplay_verb"], "DERIVED")
        edge(art["id"], "located_in", base, "DERIVED")
    for s in catalogs["systemes_vitaux"]["entries"]:
        if "batterie" in s["consumes"]:
            edge(s["id"], "consumes", "systeme_batterie", "DERIVED")
    for c in catalogs["equipage"]["entries"]:
        edge(c["id"], "located_in", base, "CANONICAL")
    # Canon: Mara est responsable des systemes du sous-marin.
    for s in catalogs["systemes_vitaux"]["entries"]:
        edge("equipage_mara", "knows", s["id"], "CANONICAL")

    edges = [e for e in edges if e["from"] in nodes and e["to"] in nodes]
    edges.sort(key=lambda e: (e["from"], e["type"], e["to"]))
    return {"graph_version": "1.0.0", "node_count": len(nodes), "edge_count": len(edges),
            "nodes": dict(sorted(nodes.items())), "edges": edges}


def _adj(g, directed=False):
    a = {n: set() for n in g["nodes"]}
    for e in g["edges"]:
        a[e["from"]].add(e["to"])
        if not directed:
            a[e["to"]].add(e["from"])
    return a


def _depth(g, start):
    """Profondeur causale: plus longue distance atteinte en BFS depuis start."""
    a, seen, d, q = _adj(g, directed=True), {start}, 0, deque([(start, 0)])
    while q:
        n, k = q.popleft()
        d = max(d, k)
        for m in sorted(a.get(n, ())):
            if m not in seen:
                seen.add(m)
                q.append((m, k + 1))
    return d, len(seen)


def analyse(g) -> dict:
    a = _adj(g)
    out_deg, in_deg = {n: 0 for n in g["nodes"]}, {n: 0 for n in g["nodes"]}
    for e in g["edges"]:
        out_deg[e["from"]] += 1
        in_deg[e["to"]] += 1

    orphans = sorted(n for n in g["nodes"] if not a[n])
    sinks = sorted(n for n in g["nodes"] if out_deg[n] == 0 and in_deg[n] > 0)
    sources = sorted(n for n in g["nodes"] if in_deg[n] == 0 and out_deg[n] > 0)

    # connexite (non orientee)
    comps, unseen = [], set(g["nodes"])
    while unseen:
        s = min(unseen)
        seen, q = {s}, deque([s])
        while q:
            n = q.popleft()
            for m in a[n]:
                if m not in seen:
                    seen.add(m)
                    q.append(m)
        comps.append(sorted(seen))
        unseen -= seen

    metrics = {}
    for n in sorted(g["nodes"]):
        d, reach = _depth(g, n)
        touched = {g["nodes"][m]["kind"] for m in a[n]}
        metrics[n] = {"degree": len(a[n]), "in": in_deg[n], "out": out_deg[n],
                      "causal_depth": d, "reachable": reach,
                      "systems_touched": sorted(touched)}

    # Une entite est "faiblement utile" si elle n'a qu'une relation technique.
    weak = sorted(n for n, m in metrics.items()
                  if m["degree"] <= 1 or len(m["systems_touched"]) <= 1)

    return {"orphans": orphans, "sinks": sinks, "sources": sources,
            "component_count": len(comps),
            "components": comps if len(comps) > 1 else [],
            "connected": len(comps) == 1,
            "weakly_useful": weak, "metrics": metrics}


def write(catalogs, gpath=ROOT / "GRAPH" / "world_graph.json",
          apath=ROOT / "GRAPH" / "connectivity.json"):
    g = build(catalogs)
    a = analyse(g)
    write_json(gpath, g)
    write_json(apath, a)
    return g, a
