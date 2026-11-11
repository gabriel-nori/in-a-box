#!/usr/bin/env python3
"""Deterministic quality gate for dev-in-a-box. Standard library only, no network.

  qualitygate.py crap  --files F [F ...] --coverage COVERAGE.json [--max N]   CRAP per Python function (exit 2 if any is over the limit)
  qualitygate.py dupes --files F [F ...] [--max R] [--min-nodes N]            near-duplicate Python functions by structural similarity (exit 2 if any pair is over)
  qualitygate.py gate  --files F [F ...] [--coverage C.json] [--mutation-score R] [--config quality.json]
                                                                              all checks, one verdict: pass (0), fail (2) or not-measured (3)

CRAP = CC^2 * (1 - coverage)^3 + CC, per function. COVERAGE.json is the output of `coverage json`.
Only Python is measured here. Any other file is reported as not measured, never as passed.
Config (JSON): {"crap_max": 10, "dup_max": 0.8, "dup_min_nodes": 30, "mutation_min": 0.8}. Flags override it.

Everything here follows a fixed model, so it is code and not a model's judgement.
"""
import argparse
import ast
import difflib
import itertools
import json
import pathlib
import sys

DEFAULTS = {"crap_max": 10.0, "dup_max": 0.8, "dup_min_nodes": 30, "mutation_min": 0.8}
BRANCHES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp, ast.comprehension)
FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef)


def complexity(fn):
    """McCabe complexity of one function; nested functions count on their own."""
    total, stack = 1, list(ast.iter_child_nodes(fn))
    while stack:
        node = stack.pop()
        if isinstance(node, FUNCTIONS + (ast.Lambda, ast.ClassDef)):
            continue
        if isinstance(node, BRANCHES):
            total += 1 + (len(node.ifs) if isinstance(node, ast.comprehension) else 0)
        elif isinstance(node, ast.BoolOp):
            total += len(node.values) - 1
        elif hasattr(ast, "match_case") and isinstance(node, ast.match_case):
            total += 1
        stack.extend(ast.iter_child_nodes(node))
    return total


def crap_score(cc, coverage):
    return cc * cc * (1 - coverage) ** 3 + cc


def functions_of(path):
    tree = ast.parse(pathlib.Path(path).read_text(encoding="utf-8"), filename=str(path))
    return [n for n in ast.walk(tree) if isinstance(n, FUNCTIONS)]


def coverage_for(report, path):
    """The executed and missing line sets of `path` in a coverage.py JSON report, matched by path suffix."""
    want = pathlib.PurePath(path).as_posix()
    for name, data in report.get("files", {}).items():
        got = pathlib.PurePath(name).as_posix()
        if want == got or want.endswith("/" + got) or got.endswith("/" + want):
            return set(data.get("executed_lines", [])), set(data.get("missing_lines", []))
    return None


def crap_check(files, report, limit):
    findings, unmeasured = [], []
    for path in files:
        lines = coverage_for(report, path)
        if lines is None:
            unmeasured.append(f"{path}: no entry in the coverage report")
            continue
        done, missing = lines
        for fn in functions_of(path):
            span = range(fn.lineno, fn.end_lineno + 1)
            hit, miss = sum(1 for n in span if n in done), sum(1 for n in span if n in missing)
            cov = hit / (hit + miss) if hit + miss else 1.0
            cc = complexity(fn)
            findings.append({"file": str(path), "function": fn.name, "line": fn.lineno, "cc": cc,
                             "coverage": round(cov, 3), "crap": round(crap_score(cc, cov), 2)})
    over = [f for f in findings if f["crap"] > limit]
    return {"name": "crap", "limit": limit, "status": "fail" if over else "not-measured" if unmeasured and not findings else "pass",
            "findings": sorted(over, key=lambda f: -f["crap"]), "functions": len(findings), "unmeasured": unmeasured}


def shape(fn):
    return [type(n).__name__ for n in ast.walk(fn)]


def dupes_check(files, limit, min_nodes):
    shapes = [(str(p), fn, shape(fn)) for p in files for fn in functions_of(p)]
    shapes = [s for s in shapes if len(s[2]) >= min_nodes]
    findings = []
    for (pa, fa, sa), (pb, fb, sb) in itertools.combinations(shapes, 2):
        ratio = difflib.SequenceMatcher(None, sa, sb, autojunk=False).ratio()
        if ratio >= limit:
            findings.append({"a": f"{pa}:{fa.lineno} {fa.name}", "b": f"{pb}:{fb.lineno} {fb.name}", "similarity": round(ratio, 3)})
    return {"name": "dupes", "limit": limit, "status": "fail" if findings else "pass",
            "findings": sorted(findings, key=lambda f: -f["similarity"]), "functions": len(shapes), "unmeasured": []}


def mutation_check(score, floor):
    if score is None:
        return {"name": "mutation", "limit": floor, "status": "not-measured", "findings": [], "unmeasured": ["no mutation score given"]}
    status = "pass" if score >= floor else "fail"
    return {"name": "mutation", "limit": floor, "status": status, "score": score,
            "findings": [] if status == "pass" else [{"score": score, "floor": floor}], "unmeasured": []}


def split_files(files):
    python = [f for f in files if str(f).endswith(".py")]
    return python, [str(f) for f in files if not str(f).endswith(".py")]


def verdict(checks, other):
    states = {c["status"] for c in checks}
    if "fail" in states:
        return "fail"
    return "not-measured" if "not-measured" in states or other else "pass"


def load_config(path, args):
    cfg = dict(DEFAULTS)
    if path:
        cfg.update(json.loads(pathlib.Path(path).read_text(encoding="utf-8")))
    for key, value in (("crap_max", args.max_crap), ("dup_max", args.max_dup), ("dup_min_nodes", args.min_nodes),
                       ("mutation_min", args.mutation_min)):
        if value is not None:
            cfg[key] = value
    return cfg


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["crap", "dupes", "gate"])
    ap.add_argument("--files", nargs="+", required=True)
    ap.add_argument("--coverage")
    ap.add_argument("--mutation-score", type=float)
    ap.add_argument("--config")
    ap.add_argument("--max", type=float, dest="max_any")
    ap.add_argument("--min-nodes", type=int)
    ap.add_argument("--max-crap", type=float)
    ap.add_argument("--max-dup", type=float)
    ap.add_argument("--mutation-min", type=float)
    args = ap.parse_args(argv)
    if args.max_any is not None:
        args.max_crap = args.max_crap if args.command != "crap" else args.max_any
        args.max_dup = args.max_dup if args.command != "dupes" else args.max_any
    cfg = load_config(args.config, args)
    python, other = split_files(args.files)
    checks = []
    if args.command in ("crap", "gate"):
        if args.coverage:
            report = json.loads(pathlib.Path(args.coverage).read_text(encoding="utf-8"))
            checks.append(crap_check(python, report, cfg["crap_max"]))
        else:
            checks.append({"name": "crap", "limit": cfg["crap_max"], "status": "not-measured", "findings": [],
                           "unmeasured": ["no coverage report given"]})
    if args.command in ("dupes", "gate"):
        checks.append(dupes_check(python, cfg["dup_max"], cfg["dup_min_nodes"]))
    if args.command == "gate":
        checks.append(mutation_check(args.mutation_score, cfg["mutation_min"]))
    result = {"verdict": verdict(checks, other), "checks": checks,
              "not_measured_files": [{"file": f, "reason": "language not measured natively"} for f in other]}
    print(json.dumps(result, indent=2))
    return {"pass": 0, "fail": 2, "not-measured": 3}[result["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
