#!/usr/bin/env python3
"""Gemini image adapter for generate-image.py: reads one request as JSON on stdin, writes a PNG, prints its path.

Endpoint, model ids and the response_format field come from the Gemini API image-generation page
(aistudio.google.com/docs/image-generation, read 2026-11-02). That page documents no seed and no raw response sample,
so the seed is not sent and the image is found by walking the response for a content block {"type": "image", "data": b64}.
Key: $GEMINI_API_KEY, else ~/.in-a-box/secrets/gemini.key. Model: $GEMINI_IMAGE_MODEL (default gemini-3.1-flash-image).
$GEMINI_BASE_URL exists so tests can point at a local server. Every generated image carries a SynthID watermark."""
import base64
import json
import os
import pathlib
import sys
import tempfile
import urllib.error
import urllib.request

BASE = os.environ.get("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com")
MODEL = os.environ.get("GEMINI_IMAGE_MODEL", "gemini-3.1-flash-image")


def key():
    k = os.environ.get("GEMINI_API_KEY")
    f = pathlib.Path.home() / ".in-a-box" / "secrets" / "gemini.key"
    k = k or (f.read_text().strip() if f.exists() else "")
    if not k:
        sys.exit("gemini: no key; set GEMINI_API_KEY or write ~/.in-a-box/secrets/gemini.key")
    return k


def prompt_of(r):
    parts = [r["prompt"]]
    if r.get("style"):
        parts.append(f"Style: {r['style']}.")
    if r.get("text_in_image") is False:
        parts.append("The image contains no text, letters, numbers, logos or watermarks.")
    if r.get("negative"):
        parts.append(f"Avoid: {r['negative']}.")
    return " ".join(parts)


def find_image(node):
    if isinstance(node, dict):
        if node.get("type") == "image" and isinstance(node.get("data"), str):
            return node["data"]
        node = list(node.values())
    if isinstance(node, list):
        for v in node:
            found = find_image(v)
            if found:
                return found
    return None


def main():
    r = json.load(sys.stdin)
    body = {"model": MODEL, "input": prompt_of(r), "response_format": {"type": "image"}}
    if r.get("aspect"):
        body["response_format"]["aspect_ratio"] = r["aspect"]
    req = urllib.request.Request(
        f"{BASE}/v1beta/interactions", data=json.dumps(body).encode(), method="POST",
        headers={"x-goog-api-key": key(), "Content-Type": "application/json", "Api-Revision": "2026-05-20"})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"gemini: HTTP {e.code}: {e.read().decode(errors='replace')[:500]}")
    b64 = find_image(data)
    if not b64:
        sys.exit("gemini: response carried no image block (blocked or unexpected shape)")
    out = pathlib.Path(tempfile.mkdtemp(prefix="gemini-img-")) / f"{r.get('slot', 'image')}.png"
    out.write_bytes(base64.b64decode(b64))
    print(out)


if __name__ == "__main__":
    main()
