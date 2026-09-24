"""Generateur de prompts specialises + injecteur automatique de contexte.

Aucun prompt n'est isole: chacun recoit canon, ontologie, graphe, manifest,
fiche fonctionnelle, relations entrantes/sortantes, contraintes visuelles,
validations, sortie attendue, outil de production et chemin de sortie.

Modes:
  by_id       - un asset independant
  by_family   - elements visuellement interdependants (tilesets, terrains, anomalies)
  by_sequence - une sequence animee
"""
from __future__ import annotations
from .util import ROOT, write_json, jdump

RESPONSE_CONTRACT = {
    "format": "JSON strict, UTF-8, une seule racine objet",
    "required_fields": ["asset_id", "entity_id", "status", "width", "height",
                        "format", "variants", "directions"],
    "binary_fields": {
        "file": "chemin du binaire livre, OBLIGATOIREMENT sous ASSETS_IN/<famille>/",
        "file_sha256": "empreinte SHA-256 reelle du binaire livre (64 hex minuscules)"},
    "binary_rule": "Sans 'file' et 'file_sha256', la reponse reste une SPECIFICATION "
                   "valide (binaire attendu plus tard). Avec ces champs, toute "
                   "non-conformite binaire entraine le REJET.",
    "on_missing_information": "Retourner {\"status\": \"BLOCKED\", \"missing\": [...]} "
                              "et NE RIEN INVENTER.",
    "forbidden": ["inventer un fait narratif", "inventer un nom hors canon",
                  "redimensionner apres rendu", "livrer hors palette imposee",
                  "presenter un placeholder comme contenu final"],
    "error_codes": ["asset.file_missing", "asset.file_corrupt", "asset.file_hash",
                    "asset.file_dimensions", "asset.file_palette",
                    "asset.file_too_large", "asset.file_format"],
}


def _relations(graph, entity_id):
    inc = [e for e in graph["edges"] if e["to"] == entity_id]
    out = [e for e in graph["edges"] if e["from"] == entity_id]
    return {"incoming": inc, "outgoing": out,
            "degree": len(inc) + len(out)}


def inject_context(*, canon, ontology, graph, manifest_entry, catalogs,
                   entity_id, correction_strategy=None) -> dict:
    """Injecteur automatique de contexte. Jamais appele manuellement par l'IA cible."""
    fiche = None
    for block in catalogs.values():
        if isinstance(block, dict) and "entries" in block:
            for e in block["entries"]:
                if e.get("id") == entity_id:
                    fiche = e
                    break
    return {
        "canon": {"world_name": canon["world_name"], "vessel_name": canon["vessel_name"],
                  "player_name": canon["player_name"],
                  "immutable_rules": [r["text"] for r in canon["immutable_rules"]],
                  "naming_rule": canon["naming_rule"]["text"],
                  "forbidden": canon["forbidden"],
                  "declared_open": [o["text"] for o in canon["declared_open"]]},
        "ontology": {"entity_types": sorted(ontology["entity_types"]),
                     "relation_types": sorted(ontology["relation_types"]),
                     "not_applicable": sorted(ontology["not_applicable"])},
        "functional_sheet": fiche or {"warning": "aucune fiche fonctionnelle trouvee"},
        "graph_relations": _relations(graph, entity_id),
        "manifest": manifest_entry,
        "visual_constraints": {
            "engine": "Godot 4", "tile": 16, "scaling": "entiere",
            "style": manifest_entry.get("style"),
            "palette_size": len(manifest_entry.get("palette", [])),
            "view": "vue unique depuis l'interieur du sous-marin"},
        "expected_output": {
            "tool": manifest_entry.get("producer", "framework_blender"),
            "output_dir": manifest_entry.get("output_rules", {}).get("dir"),
            "filename": manifest_entry.get("output_rules", {}).get("filename"),
            "format": manifest_entry.get("format")},
        "validations": manifest_entry.get("validations", []),
        "response_contract": RESPONSE_CONTRACT,
        "correction_strategy": correction_strategy or
            "En cas de rejet, corriger UNIQUEMENT le champ signale par le code "
            "d'erreur et relivrer. Ne jamais redessiner un binaire deja accepte.",
        "production_status": manifest_entry.get("status", "PLANNED"),
    }


TEMPLATES = {
    "by_id": """# PROMPT ASSET — {asset_id}

Tu produis UN asset pour le jeu Abyssal Glass via le framework Blender declare.

## Contexte injecte (ne rien deviner, tout est fourni)
{context}

## Tache
Produire l'asset `{asset_id}` de l'entite `{entity_id}`, famille `{family}`,
en {width}x{height} px, format {fmt}, palette imposee ({palette_size} teintes),
variantes: {variants}, directions: {directions}.

## Regles
- Respecter EXACTEMENT asset_id, entity_id et le chemin de sortie.
- Ne jamais inventer un fait narratif ni un nom hors canon.
- Si une information manque: repondre BLOCKED avec la liste `missing`.
- Un asset rendu n'est PAS termine: il sera importe, verifie en binaire, valide,
  puis teste en contexte runtime.

## Reponse attendue
JSON strict conforme a `response_contract` ci-dessus.
""",
    "by_family": """# PROMPT FAMILLE — {family}

Les elements de cette famille sont VISUELLEMENT INTERDEPENDANTS: ils doivent
etre produits ENSEMBLE et partager grammaire de forme, valeurs et palette.

## Contexte injecte
{context}

## Membres de la famille
{members}

## Regles
- Coherence inter-membres obligatoire (bords, valeurs, epaisseur de trait).
- Les transitions de terrain doivent raccorder sans couture sur 16 px.
- Meme palette imposee pour tous les membres.
- Un membre manquant => BLOCKED pour la famille entiere, pas de livraison partielle
  silencieuse.

## Reponse attendue
JSON strict: un objet racine avec `family` et `assets`: [ ... ] conforme au contrat.
""",
    "by_sequence": """# PROMPT SEQUENCE ANIMEE — {animation_id}

## Contexte injecte
{context}

## Sequence
entite: {entity_id}
etat/action: {state_or_action}
direction: {direction}
frames: {frames}   fps: {fps}   boucle: {loop}
frame d'impact: {impact_frame}
effet logique declenche: {effect}
transitions possibles: {transitions}

## Regles
- L'animation n'est PAS seulement visuelle: la frame d'impact doit coincider
  avec l'instant ou l'effet logique s'applique dans le moteur.
- Le nombre de frames livre doit etre EXACTEMENT {frames}.
- Chaque frame respecte la palette imposee et les dimensions de l'asset source.

## Reponse attendue
JSON strict conforme au contrat, avec `produced_animations` renseigne.
""",
}


def render_by_id(ctx, entry) -> str:
    return TEMPLATES["by_id"].format(
        asset_id=entry["id"], entity_id=entry["entity_id"], family=entry["family"],
        width=entry["width"], height=entry["height"], fmt=entry["format"],
        palette_size=len(entry["palette"]), variants=entry["variants"] or "aucune",
        directions=entry["directions"], context=jdump(ctx))


def render_by_family(ctx, family, members) -> str:
    return TEMPLATES["by_family"].format(
        family=family, context=jdump(ctx),
        members="\n".join(f"- {m['id']} ({m['width']}x{m['height']}, "
                          f"variantes: {m['variants'] or 'aucune'})" for m in members))


def render_by_sequence(ctx, anim) -> str:
    return TEMPLATES["by_sequence"].format(
        animation_id=anim["id"], entity_id=anim["entity_id"],
        state_or_action=anim["state_or_action"], direction=anim["direction"],
        frames=anim["frames"], fps=anim["fps"], loop=anim["loop"],
        impact_frame=anim["impact_frame"], effect=anim["logical_effect"],
        transitions=anim["transitions"] or "aucune", context=jdump(ctx))


def generate_examples(*, canon, ontology, graph, catalogs, manifests,
                      outdir=ROOT / "PROMPTS") -> dict:
    """Genere quelques prompts contextualises d'EXEMPLE (pas de campagne massive)."""
    written = {}
    assets = manifests["assets"]["entries"]
    anims = manifests["animations"]["entries"]

    a = next(x for x in assets if x["family"] == "famille_artefacts")
    ctx = inject_context(canon=canon, ontology=ontology, graph=graph,
                         manifest_entry=a, catalogs=catalogs, entity_id=a["entity_id"])
    p = outdir / "examples" / f"prompt_by_id__{a['id']}.md"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_by_id(ctx, a), encoding="utf-8")
    written["by_id"] = p.relative_to(ROOT).as_posix()

    fam = "famille_fond_abyssal"
    members = [x for x in assets if x["family"] == fam]
    ctx = inject_context(canon=canon, ontology=ontology, graph=graph,
                         manifest_entry=members[0], catalogs=catalogs,
                         entity_id=members[0]["entity_id"])
    p = outdir / "examples" / f"prompt_by_family__{fam}.md"
    p.write_text(render_by_family(ctx, fam, members), encoding="utf-8")
    written["by_family"] = p.relative_to(ROOT).as_posix()

    an = anims[0]
    src = next(x for x in assets if x["id"] == an["assets"][0])
    ctx = inject_context(canon=canon, ontology=ontology, graph=graph,
                         manifest_entry=src, catalogs=catalogs, entity_id=an["entity_id"])
    p = outdir / "examples" / f"prompt_by_sequence__{an['id']}.md"
    p.write_text(render_by_sequence(ctx, an), encoding="utf-8")
    written["by_sequence"] = p.relative_to(ROOT).as_posix()

    for name, tpl in TEMPLATES.items():
        t = outdir / "templates" / f"template_{name}.md"
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(tpl, encoding="utf-8")
    write_json(outdir / "response_contract.json", RESPONSE_CONTRACT)
    return written
