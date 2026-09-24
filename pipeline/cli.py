"""Point d'entree de la Pipeline V5. Deterministe, stdlib seule.

  python -m pipeline.cli all            pipeline complete
  python -m pipeline.cli canon          canon + decisions + contradictions
  python -m pipeline.cli manifests      catalogues + graphe + manifests
  python -m pipeline.cli prompts        prompts contextualises d'exemple
  python -m pipeline.cli blender        inspection + rapport de compatibilite
  python -m pipeline.cli validate       toutes les familles de validateurs
  python -m pipeline.cli verify-bin     re-verification des binaires stockes
  python -m pipeline.cli simulate       simulation des profils de joueur
  python -m pipeline.cli compile        compilation runtime
  python -m pipeline.cli report         tous les rapports
"""
from __future__ import annotations
import sys
from . import __version__
from .util import ROOT, write_json


def _state(framework_path=None):
    from .canon import build as canon_build
    from .catalogs import build as catalogs_build
    from .graph import build as graph_build
    from .manifests import build as manifests_build
    from .ontology import build as ontology_build
    canon = canon_build()
    catalogs = catalogs_build(canon)
    graph = graph_build(catalogs)
    manifests = manifests_build(canon, catalogs, graph)
    return canon, ontology_build(), catalogs, graph, manifests


def cmd_canon():
    from .canon import write as cw
    from .contradictions import write as ctw
    from .decisions import write as dw
    from .palette import write as pw
    canon, h = cw(); dec, _ = dw(); con, _ = ctw(); pw()
    print(f"canon          : {len(canon['entries'])} entrees CANONICAL (sha {h[:12]})")
    print(f"decisions      : {dec['decision_count']} "
          f"({', '.join(f'{k}={len(v)}' for k, v in dec['by_status'].items())})")
    print(f"contradictions : {con['total']} (bloquantes: {len(con['blocking'])})")
    for c in con["items"]:
        if c["status"] == "BLOCKED":
            print(f"  BLOCKED  {c['id']}: {c['detail'][:78]}")
    return 0


def cmd_manifests():
    from .catalogs import write as caw
    from .graph import write as gw
    from .manifests import write as mw
    from .ontology import write as ow
    from .schemas import write as sw
    canon, ontology, catalogs, graph, manifests = _state()
    ow(); sw(); caw(canon); gw(catalogs); mw(canon, catalogs, graph)
    print(f"ontologie      : {len(ontology['entity_types'])} types, "
          f"{len(ontology['not_applicable'])} non applicables")
    print(f"graphe         : {graph['node_count']} noeuds, {graph['edge_count']} aretes")
    for k in ("assets", "animations", "maps", "objets", "placement", "pnj"):
        print(f"manifest {k:<12}: {manifests[k]['count']}")
    for fam, meta in manifests["blocked_families"].items():
        print(f"  BLOCKED  {fam} <- {meta['blocked_by']}")
    return 0


def cmd_prompts():
    from .prompts import generate_examples
    canon, ontology, catalogs, graph, manifests = _state()
    w = generate_examples(canon=canon, ontology=ontology, graph=graph,
                          catalogs=catalogs, manifests=manifests)
    for k, v in w.items():
        print(f"prompt {k:<12}: {v}")
    return 0


def cmd_blender(framework_path=None):
    from .blender_adapter import compatibility_report, inspect
    insp = inspect(framework_path)
    rep = compatibility_report(framework_path)
    print(f"framework      : {rep['verdict']}")
    if rep["verdict"] == "BLOCKED":
        print(f"  chemin manquant : {insp['missing_path']}")
        for opt in insp["remediation"]["fix_options"]:
            print(f"  remede {opt['order']} ({opt['how']}): "
                  f"{opt.get('command_posix') or opt.get('file')}")
        return 2
    print(f"  chemin   : {insp['path']}")
    print(f"  entrees  : {insp['entry_scripts']}")
    print(f"  builders : {len(insp['builders'])}")
    return 0


def cmd_validate(framework_path=None):
    from .validators import run_all
    canon, ontology, catalogs, graph, manifests = _state()
    rep = run_all(canon=canon, catalogs=catalogs, graph=graph, manifests=manifests,
                  framework_path=framework_path)
    print(f"validation     : {rep['family_count']} familles, "
          f"{rep['error_total']} erreurs, {rep['warning_total']} avertissements")
    for f in rep["families"]:
        for e in f["errors"]:
            print(f"  ERREUR [{f['family']}] {e['code']}: {e['detail'][:70]}")
    return 0 if rep["ok"] else 1


def cmd_lifecycle():
    from .lifecycle import load, summary
    s = summary()
    print(f"cycle de vie   : {s['tracked']} assets suivis — {s['distribution']}")
    for aid, e in sorted(load()["assets"].items()):
        print(f"  {e['status']:<15} {aid}")
    return 0


def cmd_advance(asset_id=None, status=None):
    """Fait avancer un asset d'EXACTEMENT une etape. Aucun saut possible."""
    from .lifecycle import record
    if not asset_id or not status:
        print("usage: python -m pipeline.cli advance <asset_id> <statut>")
        return 64
    try:
        e = record(asset_id, status.upper())
    except ValueError as err:
        print(f"REFUSE: {err}")
        return 1
    print(f"{asset_id}: {e['history'][-1]['from']} -> {e['status']}")
    return 0


def cmd_verify_bin():
    from .assets_bin import reverify_all
    rv = reverify_all()
    print(f"binaires       : {rv['checked']} verifies, {len(rv['errors'])} erreurs")
    for e in rv["errors"]:
        print(f"  ERREUR {e['code']}: {e['detail']}")
    return 0 if rv["ok"] else 1


def cmd_simulate():
    from .simulate import run_all
    rep = run_all()
    print(f"simulation     : {rep['profile_count']} profils, "
          f"{len(rep['survivors'])} survivants, {len(rep['failures'])} echecs")
    return 0


def cmd_compile():
    from .compile_runtime import compile_all, verify_no_runtime_dependency
    canon, ontology, catalogs, graph, manifests = _state()
    art, h = compile_all(canon=canon, catalogs=catalogs, graph=graph, manifests=manifests)
    v = verify_no_runtime_dependency(art)
    print(f"runtime        : RUNTIME/runtime_data.json (sha {h[:12]})")
    print(f"  sans LLM     : {not art['requires_llm']}")
    print(f"  sans Blender : {not art['requires_blender']}")
    print(f"  liaisons asset: {art['asset_bindings_count']}")
    for e in v["errors"]:
        print(f"  ERREUR {e['code']}: {e['detail']}")
    return 0 if v["ok"] else 1


def cmd_report(framework_path=None):
    from .reports import write_all
    from .validators import run_all
    canon, ontology, catalogs, graph, manifests = _state()
    val = run_all(canon=canon, catalogs=catalogs, graph=graph, manifests=manifests,
                  framework_path=framework_path)
    out, _ = write_all(canon=canon, catalogs=catalogs, manifests=manifests,
                       graph=graph, validation=val)
    print(f"maturite       : {out['maturity']['complete']}/{out['maturity']['total']} "
          f"ART_GREEN — {out['maturity']['distribution']}")
    print(f"manquants      : {out['missing']['total']}")
    print(f"isoles         : orphelins={len(out['isolated']['orphans'])}, "
          f"faibles={len(out['isolated']['weakly_useful'])}")
    print(f"decisions ouv. : {out['open_decisions']['total']}")
    print(f"tracabilite    : {out['traceability']['row_count']} lignes")
    return 0


def cmd_all(framework_path=None):
    print(f"=== Pipeline V5 — Abyssal Glass (v{__version__}) ===")
    codes = []
    for name, fn in [("CANON", cmd_canon), ("MANIFESTS", cmd_manifests),
                     ("PROMPTS", cmd_prompts),
                     ("BLENDER", lambda: cmd_blender(framework_path)),
                     ("VALIDATION", lambda: cmd_validate(framework_path)),
                     ("BINAIRES", cmd_verify_bin), ("CYCLE_DE_VIE", cmd_lifecycle),
                     ("SIMULATION", cmd_simulate),
                     ("COMPILATION", cmd_compile),
                     ("RAPPORTS", lambda: cmd_report(framework_path))]:
        print(f"\n--- {name} ---")
        codes.append((name, fn()))
    blocked = [n for n, c in codes if c == 2]
    failed = [n for n, c in codes if c == 1]
    print("\n=== BILAN ===")
    print(f"etapes bloquees : {blocked or 'aucune'}")
    print(f"etapes en echec : {failed or 'aucune'}")
    write_json(ROOT / "REPORTS" / "run_summary.json",
               {"version": __version__, "steps": dict(codes),
                "blocked": blocked, "failed": failed})
    return 1 if failed else (2 if blocked else 0)


COMMANDS = {"all": cmd_all, "canon": cmd_canon, "manifests": cmd_manifests,
            "prompts": cmd_prompts, "blender": cmd_blender, "validate": cmd_validate,
            "verify-bin": cmd_verify_bin, "simulate": cmd_simulate,
            "compile": cmd_compile, "report": cmd_report,
            "advance": cmd_advance, "lifecycle": cmd_lifecycle}


def main(argv=None):
    argv = list(argv if argv is not None else sys.argv[1:])
    cmd = argv[0] if argv else "all"
    if cmd in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    if cmd not in COMMANDS:
        print(f"commande inconnue: {cmd}\n{__doc__}")
        return 64
    fn = COMMANDS[cmd]
    if cmd == "advance":
        return fn(*argv[1:3])
    fp = argv[1] if len(argv) > 1 else None
    return fn(fp) if cmd in ("all", "blender", "validate", "report") else fn()


if __name__ == "__main__":
    raise SystemExit(main())
