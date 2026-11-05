#!/usr/bin/env python3
"""Turn the generate slots of an art-spec into image requests, as text: generate-image.py <art-spec.json> <out-dir> [--attach IMAGES-DIR --by NAME]

Knows no image service and calls none. Step 1 writes <out-dir>/image-requests.json (the whole piece a model would
receive), <out-dir>/image-brief.md (the same as plain text to hand to any LLM or image model) and prints the request hash.
Whoever runs the brain gets the images made elsewhere (and owns the approval for that outward step), then
step 2, --attach IMAGES-DIR --by NAME, expects IMAGES-DIR/<slot>.png for every request, copies them in, and writes
<out-dir>/art-spec.resolved.json (assets filled in) and <out-dir>/image-assets.json (slot, maker, request hash)."""
import copy
import hashlib
import json
import pathlib
import re
import sys

ALLOWED = ("slot", "prompt", "negative", "style", "aspect", "seed")
PERSONAL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|\+?\d[\d\s().-]{8,}\d|https?://\S+")
ASPECT = {"portrait": "4:5", "square": "1:1", "landscape": "1.91:1", "story": "9:16"}


def requests(spec):
    out, errs = [], []
    for i, s in enumerate(spec.get("slides", []), 1):
        g = (s.get("image") or {}).get("generate")
        if not g or (s["image"].get("asset")):
            continue
        r = {k: g[k] for k in ALLOWED if k in g}
        r.setdefault("slot", f"slide-{i:02d}")
        r.setdefault("aspect", ASPECT.get(spec.get("format"), "1:1"))
        r["text_in_image"] = False  # copy is typeset by art-renderer; the model must not draw letters
        r["negative"] = (r.get("negative", "") + ", text, letters, watermark, logo").strip(", ")
        if not r.get("prompt"):
            errs.append(f"slide {i}: generate block has no prompt")
        if PERSONAL.search(" ".join(str(v) for v in r.values())):
            errs.append(f"slide {i}: request carries an email, phone number or URL; remove it")
        r["_slide"] = i
        out.append(r)
    return out, errs


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opt = lambda n: sys.argv[sys.argv.index(n) + 1] if n in sys.argv else None
    by, att = opt("--by"), opt("--attach")
    for v in (by, att):
        if v in args:
            args.remove(v)
    if len(args) != 2:
        sys.exit(__doc__)
    spec = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    out = pathlib.Path(args[1])
    out.mkdir(parents=True, exist_ok=True)
    reqs, errs = requests(spec)
    if errs:
        sys.exit("image requests rejected:\n- " + "\n- ".join(errs))
    blob = json.dumps(reqs, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    (out / "image-requests.json").write_text(blob, encoding="utf-8")
    digest = hashlib.sha256(blob.encode()).hexdigest()[:16]
    print(f"{len(reqs)} request(s) written; hash {digest}")
    brief = "\n\n".join(
        f"## {r['slot']} ({r['aspect']})\n{r['prompt']}\nStyle: {r.get('style', '-')}\nAvoid: {r['negative']}\nSeed: {r.get('seed', '-')}\nNo lettering in the image." for r in reqs)
    (out / "image-brief.md").write_text(f"# Image requests, hash {digest}\n\nOne PNG per section, named <slot>.png.\n\n{brief}\n", encoding="utf-8")
    if not att:
        print("requests only: nothing left this machine; hand image-brief.md to an image model, then re-run with --attach")
        return
    if not by:
        sys.exit("--attach needs --by NAME (who made the images), recorded as provenance")
    missing = [r["slot"] for r in reqs if not (pathlib.Path(att) / f"{r['slot']}.png").exists()]
    if missing:
        sys.exit(f"missing images for: {', '.join(missing)}")
    resolved, assets = copy.deepcopy(spec), []
    for r in reqs:
        dst = out / f"{r['slot']}.png"
        dst.write_bytes((pathlib.Path(att) / dst.name).read_bytes())
        resolved["slides"][r["_slide"] - 1]["image"]["asset"] = str(dst)
        assets.append({"slot": r["slot"], "file": dst.name, "provider": by, "request_hash": digest})
    (out / "art-spec.resolved.json").write_text(json.dumps(resolved, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "image-assets.json").write_text(json.dumps(assets, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(assets)} image(s); provenance in image-assets.json")


if __name__ == "__main__":
    main()
