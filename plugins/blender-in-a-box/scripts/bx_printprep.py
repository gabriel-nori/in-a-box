"""
bx_printprep: the blender-print-prep pipeline in one headless run.

  blender -b --factory-startup --python-exit-code 1 --python bx_printprep.py -- \
          --import part.stl --out-dir work/ [--no-repair] [--merge 1e-5] [--max-hole 0]

Import a model, gate it with the print profile, repair what failed, gate again, export
the STL in millimetres and re-import it to compare. The input file is never written.
Writes <out-dir>/<stem>_print.stl and <out-dir>/<stem>_report.json. When the final gate
still fails nothing is exported (--force-export overrides) and the exit code is 2. Edges
shared by 3+ faces are reported, never guessed at: fixing them changes the geometry.
"""
import json
import os
import sys

import bmesh
import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)
import bx_audit  # noqa: E402
import bx_export  # noqa: E402


def repair(objs, merge=None, max_hole=0):
    """Merge near-duplicate verts, drop degenerate and loose geometry, fill open borders
    (max_hole sides, 0 = any size), make the winding consistent. Returns counts per object.
    Edges shared by 3+ faces are not touched: they need a human decision."""
    done = {}
    for o in objs:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        diag = max(o.dimensions) or 1.0
        dist = merge if merge is not None else diag * 1e-6
        n0 = len(bm.verts)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
        bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=dist)
        bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context="VERTS")
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        border = [e for e in bm.edges if e.is_boundary]
        filled = 0
        if border:
            r = bmesh.ops.holes_fill(bm, edges=border, sides=max_hole)
            filled = len(r["faces"])
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        done[o.name] = {"verts_merged": n0 - len(bm.verts), "holes_filled": filled,
                        "faces": len(bm.faces)}
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()
    return done


def run(src, out_dir, do_repair=True, merge=None, max_hole=0, force_export=False):
    stem = os.path.splitext(os.path.basename(src))[0]
    os.makedirs(out_dir, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bx_export._op(bx_export.IMPORTERS[os.path.splitext(src)[1].lower()])(filepath=src)
    names = [o.name for o in bpy.context.scene.objects if o.type == "MESH"]
    rep = {"source": src, "parts": len(names)}
    first = bx_audit.deliverable(names, profile="print")
    rep["gate_before"] = {"pass": first["pass"], "errors": first["errors"], "warnings": first["warnings"]}
    final = first
    if do_repair and not first["pass"]:
        rep["repairs"] = repair([bpy.data.objects[n] for n in names], merge, max_hole)
        final = bx_audit.deliverable(names, profile="print")
        rep["gate_after"] = {"pass": final["pass"], "errors": final["errors"], "warnings": final["warnings"]}
    rep["pass"] = final["pass"]
    if final["pass"] or force_export:
        out = os.path.join(out_dir, stem + "_print.stl")
        before = bx_export.inspect_scene()
        rep["export"] = bx_export.export(out, "print")["bytes"]
        rep["round_trip_diffs"] = bx_export.compare(
            before, bx_export.inspect_file(out), bx_export.CARRIES["print"], scale=bx_export.SCALE.get("print", 1.0))
    else:
        rep["export"] = "skipped: the gate fails"
    with open(os.path.join(out_dir, stem + "_report.json"), "w") as f:
        json.dump(rep, f, indent=1, default=str)
    return rep


def _cli():
    import argparse
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="bx_printprep.py")
    ap.add_argument("--import", dest="source", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--no-repair", action="store_true")
    ap.add_argument("--merge", type=float, help="weld distance (default 1e-6 of the size)")
    ap.add_argument("--max-hole", type=int, default=0, help="largest hole to fill, in sides (0 = any)")
    ap.add_argument("--force-export", action="store_true", help="write the STL even if the gate fails")
    a = ap.parse_args(argv)
    r = run(a.source, a.out_dir, not a.no_repair, a.merge, a.max_hole, a.force_export)
    print(json.dumps(r, indent=1, default=str))
    sys.exit(0 if r["pass"] else 2)


if __name__ == "__main__":
    _cli()
