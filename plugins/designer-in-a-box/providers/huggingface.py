#!/usr/bin/env python3
"""Hugging Face diffusion adapter for generate-image.py: reads one request as JSON on stdin, writes an image, prints its path.
Also lists what exists: `huggingface.py spaces` prints the text-to-image Gradio Spaces that are running on free hardware (public metadata, starts no GPU job).

It uses a Space, a Gradio app that wraps a diffusion model, over its public HTTP API (POST /gradio_api/call/<endpoint>, then stream the event).
The Space is chosen with $HF_SPACE (owner/name; default: the first running Space of `spaces`). The endpoint is $HF_ENDPOINT (default generate).
Parameters are read from the Space's own /gradio_api/info: prompt, negative_prompt, size (the smallest offered for the aspect), steps (the lowest the slider allows,
or $HF_STEPS), seed. The Space is a third party's server: the prompt reaches it.
Key: $HF_TOKEN, else ~/.in-a-box/secrets/huggingface.key; a ZeroGPU Space spends the account's daily GPU quota."""
import json
import os
import pathlib
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://huggingface.co/api"
ENDPOINT = os.environ.get("HF_ENDPOINT", "generate").lstrip("/")


def key():
    k = os.environ.get("HF_TOKEN")
    f = pathlib.Path.home() / ".in-a-box" / "secrets" / "huggingface.key"
    return k or (f.read_text().strip() if f.exists() else "")


def call(url, token="", data=None, timeout=30):
    h = {"User-Agent": "in-a-box"}
    if data is not None:
        h["Content-Type"] = "application/json"
    if token:
        h["Authorization"] = f"Bearer {token}"
    return urllib.request.urlopen(
        urllib.request.Request(url, data=None if data is None else json.dumps(data).encode(), headers=h), timeout=timeout)


def get_json(url, token=""):
    try:
        with call(url, token) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"huggingface: {url.split('?')[0]} answered {e.code}")


def info(space):
    d = get_json(f"{API}/spaces/{space}")
    rt = d.get("runtime") or {}
    hw = (rt.get("hardware") or {}).get("current") or ""
    return {"id": d.get("id", space), "host": d.get("host", ""), "hardware": hw, "likes": d.get("likes", 0),
            "ready": rt.get("stage") == "RUNNING" and d.get("sdk") == "gradio", "free": hw.startswith(("zero", "cpu"))}


def spaces(limit=12):
    q = urllib.parse.urlencode({"filter": "text-to-image", "sdk": "gradio", "sort": "likes", "limit": limit * 3})
    rows = [info(s["id"]) for s in get_json(f"{API}/spaces?{q}")]
    return sorted((r for r in rows if r["ready"] and r["free"]), key=lambda r: -r["likes"])[:limit]


def smallest_for(choices, aspect):
    sizes = [(int(m[1]), int(m[2]), str(c)) for c in choices if (m := re.search(r"(\d{2,5})\s*[x×]\s*(\d{2,5})", str(c)))]
    if not sizes:
        return ""
    m = re.fullmatch(r"(\d+(?:\.\d+)?):(\d+(?:\.\d+)?)", aspect or "")
    want = float(m[1]) / float(m[2]) if m else None
    if want is None:
        return min(sizes, key=lambda s: s[0] * s[1])[2]
    best = min(abs(w / h - want) / want for w, h, _ in sizes)
    return min((s for s in sizes if abs(s[0] / s[1] - want) / want <= best + 0.05), key=lambda s: s[0] * s[1])[2]


def parameters(host, token):
    ep = (get_json(f"{host}/gradio_api/info", token).get("named_endpoints") or {}).get("/" + ENDPOINT)
    if not ep:
        sys.exit(f"huggingface: the Space has no endpoint /{ENDPOINT}")
    params = ep["parameters"]
    cfg = get_json(f"{host}/config", token)
    comps = {c["id"]: c.get("props") or {} for c in cfg.get("components", [])}
    dep = next((d for d in cfg.get("dependencies", []) if d.get("api_name") == ENDPOINT), {})
    return params, dict(zip((p["parameter_name"] for p in params), (comps.get(i, {}) for i in dep.get("inputs", []))))


def run(host, data, token, timeout=300):
    try:
        with call(f"{host}/gradio_api/call/{ENDPOINT}", token, {"data": data}) as r:
            event_id = json.load(r)["event_id"]
        event = ""
        with call(f"{host}/gradio_api/call/{ENDPOINT}/{event_id}", token, timeout=timeout) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").rstrip("\n")
                if line.startswith("event:"):
                    event = line[6:].strip()
                elif line.startswith("data:") and event in ("complete", "error"):
                    if event == "error":
                        sys.exit(f"huggingface: the Space reported an error: {line[5:].strip()[:300]}")
                    return json.loads(line[5:])
    except urllib.error.HTTPError as e:
        sys.exit(f"huggingface: the Space answered {e.code}: {e.read().decode(errors='replace')[:300]}")
    sys.exit("huggingface: the Space ended without an image")


def main():
    if sys.argv[1:] == ["spaces"]:
        print(json.dumps(spaces(), indent=2))
        return
    r = json.load(sys.stdin)
    token = key()
    if not token:
        sys.exit("huggingface: no token; set HF_TOKEN or write ~/.in-a-box/secrets/huggingface.key (the anonymous GPU quota is tiny)")
    space = os.environ.get("HF_SPACE") or (spaces(1) or [{}])[0].get("id")
    if not space:
        sys.exit("huggingface: no running free text-to-image Space found; set HF_SPACE")
    host = info(space)["host"]
    params, props = parameters(host, token)
    names = {p["parameter_name"] for p in params}
    values = {"prompt": r["prompt"] + (f". Style: {r['style']}" if r.get("style") else ""),
              "negative_prompt": r.get("negative", "")}
    if "size" in names:
        values["size"] = smallest_for([c[0] if isinstance(c, list) else c for c in props["size"].get("choices", [])], r.get("aspect"))
    if "steps" in names:
        lo = props["steps"].get("minimum")
        values["steps"] = int(os.environ.get("HF_STEPS") or lo or 20)
    if "seed" in names:
        values["seed"], values["randomize_seed"] = int(r.get("seed", 0)), "seed" not in r
    data = [values.get(p["parameter_name"], p.get("parameter_default")) for p in params]
    out = run(host, data, token)
    img = next((x for x in out if isinstance(x, dict) and (x.get("url") or x.get("path"))), None)
    if not img:
        sys.exit("huggingface: the Space answered without an image")
    url = img.get("url") or f"{host}/gradio_api/file={img['path']}"
    with call(url, token if (urllib.parse.urlparse(url).hostname or "").endswith(".hf.space") else "", timeout=60) as resp:
        body = resp.read()
    ext = pathlib.Path(urllib.parse.urlparse(url).path).suffix.lower()
    dest = pathlib.Path(tempfile.mkdtemp(prefix="hf-img-")) / f"{r.get('slot', 'image')}{ext if ext in ('.png', '.jpg', '.jpeg', '.webp') else '.png'}"
    dest.write_bytes(body)
    print(f"space {space}", file=sys.stderr)
    print(dest)


if __name__ == "__main__":
    main()
