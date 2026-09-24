"""Simulateur abstrait deterministe. Aucun LLM, aucun Blender.

Teste un etat AVANT et APRES chaque action: un simple test d'existence ne
suffit pas. Sert aussi de preuve que le moteur de regles est deterministe.
"""
from __future__ import annotations
import random
from .util import ROOT, write_json

PROFILES = {
    "prudent": ["observer", "reculer", "reparer"],
    "explorateur": ["avancer", "avancer", "observer"],
    "econome": ["eteindre", "avancer", "observer"],
    "ignore_les_signes": ["avancer", "avancer", "avancer"],
    "fuyard": ["avancer", "fuir", "reculer"],
    "specialiste_observation": ["eteindre", "observer", "observer"],
    "opposant": ["reculer", "eteindre", "reculer"],
    "optimiseur": ["eteindre", "avancer", "recuperer"],
}

# Cout par action, en unites de systeme. Valeurs PROPOSED (dec_duree_plongee
# etant TO_VALIDATE, elles servent au test de mecanique, pas a l'equilibrage).
COSTS = {
    "avancer":   {"oxygen": -2, "battery": -3, "depth": +50, "hull": -1},
    "reculer":   {"oxygen": -2, "battery": -3, "depth": -50, "hull": 0},
    "observer":  {"oxygen": -1, "battery": -1, "depth": 0, "hull": 0},
    "eteindre":  {"oxygen": -1, "battery": +2, "depth": 0, "hull": 0},
    "fuir":      {"oxygen": -4, "battery": -8, "depth": -100, "hull": -2},
    "reparer":   {"oxygen": -3, "battery": -2, "depth": 0, "hull": +5},
    "recuperer": {"oxygen": -2, "battery": -1, "depth": 0, "hull": 0},
}


def initial_state():
    return {"oxygen": 100, "battery": 100, "hull": 100, "depth": 0,
            "lights_on": True, "elapsed": 0, "alive": True}


def step(state, action):
    """Applique une action. Retourne (avant, apres, effets constates)."""
    before = dict(state)
    if not state["alive"]:
        return before, dict(state), ["ignore: plongee terminee"]
    c = COSTS[action]
    state["oxygen"] = max(0, min(100, state["oxygen"] + c["oxygen"]))
    state["battery"] = max(0, min(100, state["battery"] + c["battery"]))
    state["hull"] = max(0, min(100, state["hull"] + c["hull"]))
    state["depth"] = max(0, state["depth"] + c["depth"])
    state["elapsed"] += 1
    if action == "eteindre":
        state["lights_on"] = False
    if state["depth"] > 800:                       # pression
        state["hull"] = max(0, state["hull"] - 2)
    if state["hull"] < 40:                         # breche: perte acceleree
        state["oxygen"] = max(0, state["oxygen"] - 2)
    effects = [f"{k}: {before[k]} -> {state[k]}" for k in
               ("oxygen", "battery", "hull", "depth") if before[k] != state[k]]
    for sysname, key in (("systeme_oxygene", "oxygen"), ("systeme_batterie", "battery"),
                         ("systeme_coque", "hull")):
        if state[key] == 0:
            state["alive"] = False
            effects.append(f"ECHEC: {sysname} a zero")
    return before, dict(state), effects


def run_profile(name, seed=20260924, turns=24):
    rng = random.Random(seed)
    loop = PROFILES[name]
    state, trace = initial_state(), []
    for i in range(turns):
        action = loop[i % len(loop)] if rng.random() > 0.15 else rng.choice(loop)
        before, after, effects = step(state, action)
        trace.append({"turn": i, "action": action, "before": before,
                      "after": after, "effects": effects})
        if not state["alive"]:
            break
    return {"profile": name, "seed": seed, "turns_played": len(trace),
            "survived": state["alive"], "final": state,
            "systems_exercised": sorted({e.split(":")[0] for t in trace for e in t["effects"]}),
            "trace": trace}


def run_all(seed=20260924, path=ROOT / "REPORTS" / "simulation_report.json"):
    runs = {name: run_profile(name, seed) for name in sorted(PROFILES)}
    rep = {
        "seed": seed, "profile_count": len(runs),
        "survivors": sorted(n for n, r in runs.items() if r["survived"]),
        "failures": sorted(n for n, r in runs.items() if not r["survived"]),
        "determinism_note": "meme graine => meme trace, verifie par test_reproductibilite",
        "runs": runs,
    }
    write_json(path, rep)
    return rep
