#!/usr/bin/env python3
"""Render an art-spec to PNG: render-art.py <art-spec.json> <out-dir> [--check-only] [--chrome PATH]

Validates the spec (format, WCAG contrast, minimum font size, character limits, safe zone), builds HTML
from fixed templates and prints each slide with headless Chrome. Writes manifest.json beside the PNGs.
The model writes the spec; this script draws. Exit 1 on any failed check."""
import html
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

FORMATS = {"portrait": (1080, 1350), "square": (1080, 1080), "landscape": (1200, 627), "story": (1080, 1920)}
MIN_FONT, SAFE = 28, 64
LIMITS = {  # layout -> {field: max characters}
    "cover": {"kicker": 40, "title": 90, "subtitle": 90},
    "list": {"title": 50, "item": 70, "items": 5},
    "compare": {"title": 40, "item": 60, "items": 4},
    "numbers": {"title": 40, "label": 40, "number": 8, "items": 3},
    "quote": {"quote": 160, "source": 50},
    "cta": {"title": 70, "body": 120, "action": 50},
}
CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium", "chrome"]


def lum(hexcolor):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def validate(spec):
    errs = []
    if spec.get("format") not in FORMATS:
        errs.append(f"format must be one of {sorted(FORMATS)}")
    t = spec.get("tokens", {})
    for k in ("bg", "fg", "accent"):
        if not (isinstance(t.get(k), str) and len(t[k]) == 7 and t[k].startswith("#")):
            errs.append(f"tokens.{k} must be #rrggbb")
    if not errs:
        if contrast(t["fg"], t["bg"]) < 4.5:
            errs.append(f"fg/bg contrast {contrast(t['fg'], t['bg']):.2f} < 4.5 (WCAG AA)")
        if contrast(t["accent"], t["bg"]) < 3:
            errs.append(f"accent/bg contrast {contrast(t['accent'], t['bg']):.2f} < 3 (WCAG large text)")
    base = t.get("base_font", 36)
    if base < MIN_FONT:
        errs.append(f"tokens.base_font {base} < minimum {MIN_FONT}px")
    if t.get("padding", 90) < SAFE:
        errs.append(f"tokens.padding {t.get('padding')} < safe zone {SAFE}px")
    slides = spec.get("slides") or []
    if not slides:
        errs.append("slides is empty")
    for i, s in enumerate(slides, 1):
        lay = s.get("layout")
        if lay not in LIMITS:
            errs.append(f"slide {i}: unknown layout '{lay}'")
            continue
        lim = LIMITS[lay]
        for f, mx in lim.items():
            if f in ("items",):
                if len(s.get("items", [])) > mx:
                    errs.append(f"slide {i}: more than {mx} items")
            elif f in ("item", "label", "number"):
                continue
            elif len(str(s.get(f, ""))) > mx:
                errs.append(f"slide {i}: {f} over {mx} characters")
        for it in s.get("items", []):
            txt = it if isinstance(it, str) else json.dumps(it, ensure_ascii=False)
            if isinstance(it, str) and len(it) > lim.get("item", 70):
                errs.append(f"slide {i}: item over {lim.get('item', 70)} characters: {txt[:30]}")
            if isinstance(it, dict):
                if len(str(it.get("number", ""))) > lim.get("number", 8):
                    errs.append(f"slide {i}: number over {lim.get('number', 8)} characters")
                if len(str(it.get("label", ""))) > lim.get("label", 40):
                    errs.append(f"slide {i}: label over {lim.get('label', 40)} characters")
        img = s.get("image")
        if img and not (img.get("asset") or img.get("generate")):
            errs.append(f"slide {i}: image needs 'asset' (a file) or 'generate' (a prompt block)")
        if img and img.get("generate") and not img.get("asset"):
            errs.append(f"slide {i}: image '{img.get('slot', '?')}' is a generate slot with no asset yet; run image-generator first")
    return errs


def li(xs):
    return "".join(f"<li>{html.escape(x if isinstance(x, str) else x.get('text', ''))}</li>" for x in xs)


def body(s):
    e = html.escape
    lay = s["layout"]
    if lay == "cover":
        return f'<div class="kick">{e(s.get("kicker", ""))}</div><h1>{e(s["title"])}</h1><p class="acc">{e(s.get("subtitle", ""))}</p>'
    if lay == "list":
        return f'<h2>{e(s["title"])}</h2><ul class="big">{li(s["items"])}</ul>'
    if lay == "compare":
        a, b = s["items"][: len(s["items"]) // 2], s["items"][len(s["items"]) // 2:]
        return (f'<h2>{e(s["title"])}</h2><div class="cols"><div class="card bad"><h3>{e(s.get("left", ""))}</h3><ul>{li(a)}</ul></div>'
                f'<div class="card good"><h3>{e(s.get("right", ""))}</h3><ul>{li(b)}</ul></div></div>')
    if lay == "numbers":
        n = "".join(f'<div class="num"><b>{e(str(i["number"]))}</b><span>{e(i["label"])}</span></div>' for i in s["items"])
        return f'<h2>{e(s["title"])}</h2>{n}'
    if lay == "quote":
        return f'<p class="quote">{e(s["quote"])}</p><p class="src">{e(s.get("source", ""))}</p>'
    return f'<h2>{e(s["title"])}</h2><p class="foot">{e(s.get("body", ""))}</p><p class="cta">{e(s["action"])}</p>'


def page(spec, s, w, h):
    t = spec["tokens"]
    pad, base = t.get("padding", 90), t.get("base_font", 36)
    img = s.get("image") or {}
    bg = f'url("{pathlib.Path(img["asset"]).resolve().as_uri()}")' if img.get("asset") else "none"
    veil = "linear-gradient(rgba(0,0,0,.55),rgba(0,0,0,.55))," if img.get("asset") and img.get("veil", True) else ""
    css = f"""@page{{size:{w}px {h}px;margin:0}}*{{box-sizing:border-box}}html,body{{margin:0}}
body{{width:{w}px;height:{h}px;font-family:{t.get('font', "-apple-system,'Helvetica Neue',Arial,sans-serif")};font-size:{base}px;color:{t['fg']};
background:{veil}{bg} center/cover,{t['bg']};padding:{pad}px;display:flex;flex-direction:column;justify-content:center;overflow:hidden}}
h1{{font-size:{base*2.6:.0f}px;line-height:1.08;margin:0 0 40px;letter-spacing:-2px}}h2{{font-size:{base*2.1:.0f}px;margin:0 0 50px;color:{t['accent']};letter-spacing:-1px}}
h3{{font-size:{base*1.3:.0f}px;margin:0 0 24px}}.acc{{color:{t['accent']};font-size:{base*1.5:.0f}px;font-weight:700;margin:0}}.kick{{letter-spacing:6px;color:{t['accent']};margin-bottom:36px}}
ul{{list-style:none;padding:0;margin:0}}ul.big li{{font-size:{base*1.35:.0f}px;line-height:1.25;margin-bottom:30px;padding-left:56px;position:relative}}ul.big li:before{{content:"→";position:absolute;left:0;color:{t['accent']}}}
.cols{{display:flex;flex-direction:column;gap:32px}}.card{{border-radius:32px;padding:40px;background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.18)}}.good{{border-color:{t['accent']}}}.good h3{{color:{t['accent']}}}
.card li{{font-size:{base}px;line-height:1.3;margin-bottom:14px}}.num{{display:flex;align-items:baseline;gap:30px;margin-bottom:30px}}.num b{{font-size:{base*3.4:.0f}px;color:{t['accent']};min-width:{w*0.38:.0f}px}}
.quote{{font-size:{base*1.6:.0f}px;line-height:1.2;font-weight:700;margin:0 0 36px}}.src,.foot{{font-size:{base}px;line-height:1.4}}.cta{{font-size:{base*1.4:.0f}px;font-weight:700;color:{t['accent']}}}"""
    return f"<!doctype html><html><head><meta charset=utf-8><style>{css}</style></head><body>{body(s)}</body></html>"


def find_chrome(arg):
    for c in ([arg] if arg else []) + CHROME:
        p = c if os.path.isabs(c) and os.path.exists(c) else shutil.which(c)
        if p:
            return p
    sys.exit("Chrome not found; pass --chrome PATH")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    chrome_arg = sys.argv[sys.argv.index("--chrome") + 1] if "--chrome" in sys.argv else None
    if chrome_arg in args:
        args.remove(chrome_arg)
    if len(args) != 2:
        sys.exit(__doc__)
    spec = json.loads(pathlib.Path(args[0]).read_text(encoding="utf-8"))
    errs = validate(spec)
    if errs:
        print("art-spec rejected:\n- " + "\n- ".join(errs))
        sys.exit(1)
    print("art-spec ok")
    if "--check-only" in sys.argv:
        return
    out = pathlib.Path(args[1])
    out.mkdir(parents=True, exist_ok=True)
    w, h = FORMATS[spec["format"]]
    chrome = find_chrome(chrome_arg)
    files = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, s in enumerate(spec["slides"], 1):
            src = pathlib.Path(tmp) / f"s{i}.html"
            src.write_text(page(spec, s, w, h), encoding="utf-8")
            png = out / f"slide-{i:02d}.png"
            subprocess.run([chrome, "--headless=new", "--no-sandbox", "--hide-scrollbars", f"--window-size={w},{h}",
                            f"--screenshot={png}", src.as_uri()], check=True, capture_output=True)
            files.append({"file": png.name, "layout": s["layout"], "width": w, "height": h})
    (out / "manifest.json").write_text(json.dumps({"format": spec["format"], "slides": files}, indent=2) + "\n", encoding="utf-8")
    print(f"rendered {len(files)} slide(s) to {out}")


if __name__ == "__main__":
    main()
