#!/usr/bin/env python3
"""Turn the generate slots of an art-spec into diffusion requests: generate-image.py <art-spec.json> <out-dir> [--send --provider NAME --authorize HASH]

Default is a dry run: writes <out-dir>/image-requests.json (the whole piece the model would receive) and prints its hash.
Sending is an outward action. It needs --send, --provider and --authorize <hash> where the hash is the one printed for
exactly that file, so approval of one request set never covers another. A provider is a JSON file
(~/.in-a-box/image-providers/<name>.json, or $IN_A_BOX_IMAGE_PROVIDERS/<name>.json) with {"command": [...]}: the command
receives one request as JSON on stdin and prints the path of the PNG it wrote. No provider API is built in.
Writes <out-dir>/art-spec.resolved.json (assets filled in) and <out-dir>/image-assets.json."""
import copy
import hashlib
import json
import os
import pathlib
import re
import subprocess
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
    prov, auth = opt("--provider"), opt("--authorize")
    for v in (prov, auth):
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
    if "--send" not in sys.argv:
        print("dry run: nothing left this machine")
        return
    if not prov or auth != digest:
        sys.exit("refused: --send needs --provider and --authorize with the hash of this exact request set")
    base = [os.environ.get("IN_A_BOX_IMAGE_PROVIDERS"), os.path.expanduser("~/.in-a-box/image-providers")]
    cfg = next((pathlib.Path(b) / f"{prov}.json" for b in base if b and (pathlib.Path(b) / f"{prov}.json").exists()), None)
    if not cfg:
        sys.exit(f"provider '{prov}' not found")
    cmd = json.loads(cfg.read_text(encoding="utf-8"))["command"]
    resolved, assets = copy.deepcopy(spec), []
    for r in reqs:
        body = {k: v for k, v in r.items() if not k.startswith("_")}
        p = subprocess.run(cmd, input=json.dumps(body), capture_output=True, text=True, check=True)
        src = pathlib.Path(p.stdout.strip().splitlines()[-1])
        dst = out / f"{r['slot']}.png"
        dst.write_bytes(src.read_bytes())
        resolved["slides"][r["_slide"] - 1]["image"]["asset"] = str(dst)
        assets.append({"slot": r["slot"], "file": dst.name, "provider": prov, "request_hash": digest})
    (out / "art-spec.resolved.json").write_text(json.dumps(resolved, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "image-assets.json").write_text(json.dumps(assets, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(assets)} image(s); provenance in image-assets.json")


if __name__ == "__main__":
    main()
