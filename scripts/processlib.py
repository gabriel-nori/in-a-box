"""Shared reader for process files (CONVENTIONS section 10)."""
import pathlib
import re

SECTIONS = ["Purpose", "Trigger", "Participants", "Inputs", "Outcomes", "How it is handled",
            "Expectations of the position", "Sources"]
LIST_FIELDS = ("roles", "sources")


def load_process(plugin_dir, path):
    """Return {id,title,scenario,roles,sources,file,body,sections} for a process file."""
    text = pathlib.Path(path).read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta, body = {}, text
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            k, _, v = line.partition(":")
            v = v.strip()
            if k.strip() in LIST_FIELDS:
                v = [x.strip() for x in v.strip("[]").split(",") if x.strip()]
            meta[k.strip()] = v
    return {"id": meta.get("id", ""), "title": meta.get("title", ""), "scenario": meta.get("scenario", ""),
            "roles": meta.get("roles", []), "sources": meta.get("sources", []),
            "file": pathlib.Path(path).relative_to(plugin_dir).as_posix(), "body": body.strip(),
            "sections": re.findall(r"^## (.+)$", body, re.M), "has_meta": bool(m)}
