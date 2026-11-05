#!/usr/bin/env python3
"""Deterministic helpers for jobsearch-in-a-box. Standard library only, no network.

  jobkit.py guard  --draft FILE --source FILE [--source FILE ...]   facts in the draft that no source backs (exit 2 if any)
  jobkit.py years  ROLES.json [--today YYYY-MM]                     years of experience, overlapping roles counted once
  jobkit.py band   SCORE                                            the fit band for a 0-100 score
  jobkit.py dedupe POSTINGS.json [--seen SEEN.json]                 postings not seen before, same job twice counted once
  jobkit.py normalize FILE                                          text with ligatures, soft hyphens and zero-width marks repaired
  jobkit.py ats (--text F | --pdf F | --docx F) [--keywords K.json] [--source-text F] [--filename NAME] [--min-coverage N]
                                                                    can an applicant tracking system read this resume, and does it carry the posting's backed terms (exit 2 on a parse error)

Everything here follows a fixed model, so it is code and not a model's judgement.
"""
import argparse
import datetime
import json
import re
import sys
import shutil
import subprocess
import unicodedata
import zipfile
import xml.etree.ElementTree as ET

NUMBER_WORDS = {w: n for n, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}
NUMBER_WORDS.update({"thirty": 30, "forty": 40, "fifty": 50, "hundred": 100})
CALENDAR = set("""january february march april may june july august september october november december
jan feb mar apr jun jul aug sep sept oct nov dec monday tuesday wednesday thursday friday saturday sunday""".split())
NOT_NAMES = {"i", "i'm", "i've", "i'd", "i'll", "ok"}
CREDENTIAL = re.compile(r"\b(certified|certification|certificate|licensed|license|accredited|chartered)\b", re.I)
NUMBER = re.compile(r"(?<![\w])(\d{1,3}(?:[,.  ]\d{3})+|\d+(?:[.,]\d+)?)\s*([km])?%?(?![\w])", re.I)
WORD = re.compile(r"[\w][\w&'+#.-]*", re.U)
CAPITAL = re.compile(r"[A-ZÀ-Ý][\w&'+#-]*", re.U)


def number_value(digits, suffix):
    grouped = re.fullmatch(r"\d{1,3}(?:[,.  ]\d{3})+", digits)
    value = float(re.sub(r"\D", "", digits)) if grouped else float(digits.replace(",", "."))
    return value * {"k": 1_000, "m": 1_000_000}.get((suffix or "").lower(), 1)


def numbers_in(text):
    found = [(m.group(0).strip(), number_value(m.group(1), m.group(2))) for m in NUMBER.finditer(text)]
    found += [(w, NUMBER_WORDS[w.lower()]) for w in re.findall(r"\b[a-z]+\b", text, re.I) if w.lower() in NUMBER_WORDS]
    return found


def sentence_starts(text):
    starts = {0}
    for m in re.finditer(r"(?:[.!?:;][\"')]?\s+|\n)\s*(?:[-*•]\s+)?(?=\S)", text.rstrip()):
        starts.add(m.end())
    return starts


def unverified(text, sources):
    """Names, acronyms, numbers and credentials in `text` that the sources do not contain, in order, once each."""
    haystack = "\n".join(sources).lower()
    words = {w.rstrip(".'").lower() for w in WORD.findall(haystack)}
    numbers = {v for _, v in numbers_in(haystack)}
    flags = []

    def flag(value):
        if value not in flags:
            flags.append(value)

    starts = sentence_starts(text)
    for m in CAPITAL.finditer(text):
        word = re.sub(r"['’]s$", "", m.group(0)).strip("-'")
        low = word.lower()
        acronym = sum(c.isupper() for c in word) >= 2
        if m.start() in starts and not acronym:
            continue
        if low in NOT_NAMES or low in CALENDAR or low in words or low in haystack:
            continue
        flag(word)
    for raw, value in numbers_in(text):
        if value in numbers or (raw.isalpha() and value <= 2):
            continue
        flag(raw)
    for m in CREDENTIAL.finditer(text):
        if m.group(1).lower()[:7] not in haystack:
            flag(m.group(1))
    return flags


def cmd_guard(args):
    draft = open(args.draft, encoding="utf-8").read()
    sources = [open(p, encoding="utf-8").read() for p in args.source]
    flags = unverified(draft, sources)
    print(json.dumps({"unverified": flags, "checked_against": args.source}, indent=2, ensure_ascii=False))
    return 2 if flags else 0


def month(value, today):
    if not value:
        return today
    year, mon = (int(x) for x in value.split("-")[:2])
    return year * 12 + mon - 1


def cmd_years(args):
    today_d = datetime.date.fromisoformat((args.today or datetime.date.today().isoformat()[:7]) + "-01")
    today = today_d.year * 12 + today_d.month - 1
    spans = sorted((month(r["start"], today), month(r.get("end"), today)) for r in json.load(open(args.roles)))
    merged = []
    for start, end in spans:
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    months = sum(end - start for start, end in merged)
    print(json.dumps({"months": months, "years": months // 12}))
    return 0


def band(score):
    return "Excellent fit" if score >= 85 else "Good fit" if score >= 70 else "Possible fit" if score >= 50 else "Poor fit"


def cmd_band(args):
    print(band(max(0, min(100, args.score))))
    return 0


def key(posting):
    norm = lambda s: re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()
    return f"{norm(posting.get('company'))}|{norm(posting.get('title'))}|{norm(posting.get('place'))}"


def cmd_dedupe(args):
    seen = set(json.load(open(args.seen))) if args.seen else set()
    fresh = []
    for posting in json.load(open(args.postings)):
        keys = {key(posting)} | ({posting["url"]} if posting.get("url") else set())
        if keys & seen:
            continue
        seen |= keys
        fresh.append(posting)
    print(json.dumps({"fresh": fresh, "seen": sorted(seen)}, indent=2, ensure_ascii=False))
    return 0


# ---- ATS readability -------------------------------------------------------------------------------------------
LIGATURES = {"ﬀ": "ff", "ﬁ": "fi", "ﬂ": "fl", "ﬃ": "ffi", "ﬄ": "ffl", "ﬅ": "st", "ﬆ": "st"}
INVISIBLE = dict.fromkeys(map(ord, "­​‌‍⁠﻿"), None)
HEADINGS = {
    "summary": "resumo|resumo profissional|sumario|perfil|perfil profissional|objetivo|summary|professional summary|profile|about|resumen|perfil profesional",
    "experience": "experiencia|experiencia profissional|work history|career history|experiencia profesional|experiencias|historico profissional|experience|work experience|professional experience|employment|employment history|experiencia laboral",
    "education": "formacao|formacao academica|formacion academica|academic qualifications|educacao|escolaridade|education|academic background|formacion|educacion",
    "skills": "habilidades|competencias|conhecimentos|habilidades tecnicas|competencias tecnicas|tecnologias|skills|technical skills|core skills|habilidades tecnicas|tecnologias e ferramentas",
}
EXTRA_HEADINGS = "projetos|certificacoes|certificados|idiomas|publicacoes|premios|cursos|projects|certifications|languages|publications|awards|courses|palestras|talks|links"
MONTHS = ("jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez|feb|apr|may|aug|sep|oct|dec|ene|dic|january|february|march|april|june|july|august|september|october|november|december|"
          "janeiro|fevereiro|marco|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro|enero|febrero|marzo|mayo|junio|julio|septiembre|setiembre|octubre|noviembre|diciembre")
NOW = r"atual|atualmente|presente|present|current|now|hoje|actualidad|actual"
DATE_RANGE = re.compile(
    rf"(?:(?:{MONTHS})\.?\s*(?:de\s+)?|(?:0?[1-9]|1[0-2])\s*[/.-]\s*)?(?:19|20)\d\d\s*(?:[-–—]|a|ate|hasta|to|until)\s*"
    rf"(?:(?:(?:{MONTHS})\.?\s*(?:de\s+)?|(?:0?[1-9]|1[0-2])\s*[/.-]\s*)?(?:19|20)\d\d|{NOW})", re.I)
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
PHONE = re.compile(r"(?<![\d@])\+?\d[\d\s().-]{7,}\d(?![\d@])")
FANCY_BULLET = re.compile("[\u27a2\u27a4\u25ba\u25aa\u25a0\u25a1\u25c6\u2756\u2713\u2714\u2605\u2606\u2794\u279c\u2192\u2023\u2043]")
GARBLED = re.compile(r"\(cid:\d+\)|[�-]")
SPACED_LETTERS = re.compile(r"(?<![\w])(?:[^\W\d_]\s){5,}[^\W\d_](?![\w])", re.U)
GAP = re.compile(r"\S(?: {4,}|\t)\S")


def fold(text):
    """Lower-case and accent-free, the way a recruiter's search box matches."""
    return "".join(c for c in unicodedata.normalize("NFD", text.lower()) if not unicodedata.combining(c))


def normalize_text(text):
    for lig, plain in LIGATURES.items():
        text = text.replace(lig, plain)
    return text.translate(INVISIBLE).replace(" ", " ")


def pdf_text(path):
    raw = open(path, "rb").read()
    images = len(re.findall(rb"/Subtype\s*/Image", raw))
    exe = shutil.which("pdftotext")
    if exe:
        done = subprocess.run([exe, "-layout", path, "-"], capture_output=True, text=True)
        if done.returncode:
            raise SystemExit(f"pdftotext failed: {done.stderr.strip() or done.returncode}")
        text = done.stdout
    else:
        try:
            import pypdf
        except ImportError:
            raise SystemExit("ats --pdf needs pdftotext or pypdf; install one, or pass the extracted text with --text")
        reader = pypdf.PdfReader(path)
        text = "\n".join((p.extract_text(extraction_mode="layout") if hasattr(p, "extract_text") else "") or "" for p in reader.pages)
    pages = len(re.findall(rb"/Type\s*/Page(?!s)\b", raw))
    return text, {"pages": pages or None, "images": images}


def docx_text(path):
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    meta = {"tables": 0, "textboxes": 0, "header_footer_text": ""}
    with zipfile.ZipFile(path) as z:
        body = ET.fromstring(z.read("word/document.xml"))
        meta["tables"] = len(list(body.iter(ns + "tbl")))
        meta["textboxes"] = len(list(body.iter(ns + "txbxContent")))
        for name in z.namelist():
            if re.match(r"word/(header|footer)\d*\.xml", name):
                meta["header_footer_text"] += " ".join(t.text or "" for t in ET.fromstring(z.read(name)).iter(ns + "t")) + " "
    lines = ["".join(t.text or "" for t in para.iter(ns + "t")) for para in body.iter(ns + "p")]
    return "\n".join(lines), meta


def find_headings(lines):
    """Index of each recognised heading line -> its section name ('other' for optional ones). Two short lines may form one heading."""
    table = {fold(v): k for k, vs in HEADINGS.items() for v in vs.split("|")}
    table.update({v: "other" for v in EXTRA_HEADINGS.split("|")})
    found, i = {}, 0
    while i < len(lines):
        one = re.sub(r"[\s:]+$", "", fold(lines[i]).strip())
        nxt = next((j for j in range(i + 1, min(i + 4, len(lines))) if lines[j].strip()), None)
        two = re.sub(r"[\s:]+$", "", fold(lines[i] + " " + lines[nxt]).strip()) if nxt is not None else ""
        two = re.sub(r"\s+", " ", two)
        nxt_fold = re.sub(r"[\s:]+$", "", fold(lines[nxt]).strip()) if nxt is not None else ""
        if len(one) <= 40 and one in table:
            found[i] = table[one]
        elif nxt is not None and lines[i].strip() and len(two) <= 40 and two in table and one not in table and nxt_fold not in table:
            found[i] = table[two]
            i = nxt
        i += 1
    return found


def term_found(term_variants, haystack):
    return any(re.search(rf"(?<![\w+#]){re.escape(fold(v))}(?![\w+#])", haystack) for v in term_variants)


def tail_shingles(text, n=5):
    flat = re.sub(r"[\W_]+", "", fold(normalize_text(text)))
    return {flat[i:i + n] for i in range(max(0, len(flat) - n + 1))}


def ats_report(text, meta=None, keywords=None, source_text=None, filename=None):
    meta = meta or {}
    issues = []

    def add(level, code, detail):
        issues.append({"level": level, "code": code, "detail": detail})

    ligs = sorted({c for c in text if c in LIGATURES})
    if ligs:
        add("error", "ligatures", f"{''.join(ligs)} are single glyphs; a keyword search for the plain word misses them (run jobkit normalize on the source and re-export)")
    if GARBLED.search(text):
        add("error", "unmapped-glyphs", "characters without a text mapping ((cid:N), replacement or private-use); the font is not extractable")
    clean = normalize_text(text)
    lines = clean.splitlines()
    nonblank = [ln for ln in lines if ln.strip()]
    words = len(re.findall(r"\w+", clean))
    if words < 60 or (meta.get("images") and words < 150):
        add("error", "no-selectable-text", f"only {words} words extracted; the resume may be an image or scan")
    elif words > 1100 or (meta.get("pages") or 0) > 2:
        add("warn", "too-long", f"{words} words, {meta.get('pages') or '?'} pages; two pages is the working limit")
    if SPACED_LETTERS.search(clean):
        add("error", "letter-spacing", "letters come out separated by spaces; a name or word is split apart")
    gapped = [ln for ln in nonblank if GAP.search(ln)]
    ratio = len(gapped) / len(nonblank) if nonblank else 0
    if len(gapped) >= 5 and ratio >= 0.25:
        add("error", "columns", f"{len(gapped)} of {len(nonblank)} lines have wide internal gaps; a multi-column layout reads out of order")
    elif len(gapped) >= 3 and ratio >= 0.10:
        add("warn", "table-like-alignment", f"{len(gapped)} lines have wide internal gaps; a table or aligned column may be dropped")
    if sum(ln.strip().startswith("|") or ln.strip().endswith("|") for ln in nonblank) >= 3 or meta.get("tables"):
        add("warn", "table", "table rows (lines framed by pipes) or a real table; some systems skip table content")
    if meta.get("textboxes"):
        add("error", "text-box", "text inside text boxes is often not read")
    if meta.get("header_footer_text", "").strip() and (EMAIL.search(meta["header_footer_text"]) or PHONE.search(meta["header_footer_text"])):
        add("error", "contact-in-header", "contact details sit in the page header or footer, which parsers often skip")
    if FANCY_BULLET.search(clean):
        add("warn", "bullets", "decorative bullet glyphs; use a plain hyphen or a standard bullet")
    heads = find_headings(lines)
    names = set(heads.values())
    for need in ("experience", "education", "skills"):
        if need not in names:
            add("error" if need == "experience" else "warn", f"missing-{need}-heading", f"no standard '{need}' section heading found")
    if "summary" not in names:
        add("warn", "missing-summary-heading", "no standard summary heading found")
    if not DATE_RANGE.search(fold(clean)):
        add("error", "no-date-ranges", "no recognisable date range (e.g. 03/2021 - 08/2023, Jan 2020 - presente)")
    top = "\n".join(nonblank[:25])
    if not EMAIL.search(top):
        add("error", "contact-missing", "no email in the first lines of the body")
    if not PHONE.search(top):
        add("warn", "phone-missing", "no phone number in the first lines of the body")
    if filename is not None:
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{2,70}\.(pdf|docx)", filename) or not re.search(r"[A-Za-z0-9]-[A-Za-z0-9]", filename):
            add("warn", "filename", "use Name-Role-Company.pdf: ASCII, no spaces, at least name and role")
    if source_text is not None:
        want, got = tail_shingles(source_text), tail_shingles(clean)
        recall = len(want & got) / len(want) if want else 1.0
        if recall < 0.95:
            add("error", "extraction-loss", f"only {recall:.0%} of the source text survives extraction")

    report = {"issues": issues, "words": words, "sections": sorted(names)}
    errors = sum(i["level"] == "error" for i in issues)
    warns = sum(i["level"] == "warn" for i in issues)
    report["readability"] = max(0, 100 - 25 * errors - 8 * warns)
    report["parse_ok"] = errors == 0
    if keywords is not None:
        hay = fold(clean)
        skills_span = set()
        order = sorted(heads)
        for n, idx in enumerate(order):
            if heads[idx] == "skills":
                skills_span.update(range(idx, order[n + 1] if n + 1 < len(order) else len(lines)))
        outside = fold("\n".join(ln for i, ln in enumerate(lines) if i not in skills_span))
        backed = [k for k in keywords if k["status"] in ("covered", "partial")]
        present, absent, only_skills = [], [], []
        for k in backed:
            variants = [k["term"], *k.get("aliases", [])]
            if not term_found(variants, hay):
                absent.append(k["term"])
            else:
                present.append(k["term"])
                if not term_found(variants, outside):
                    only_skills.append(k["term"])
        report["keywords"] = {
            "coverage": round(100 * len(present) / len(backed), 1) if backed else None,
            "present": present,
            "backed_but_missing": absent,
            "only_in_skills_list": only_skills,
            "gaps_not_claimed": [k["term"] for k in keywords if k["status"] == "gap"],
        }
    return report


def cmd_normalize(args):
    sys.stdout.write(normalize_text(open(args.file, encoding="utf-8").read()))
    return 0


def cmd_ats(args):
    meta = {}
    if args.pdf:
        text, meta = pdf_text(args.pdf)
    elif args.docx:
        text, meta = docx_text(args.docx)
    else:
        text = open(args.text, encoding="utf-8").read()
    keywords = json.load(open(args.keywords, encoding="utf-8")) if args.keywords else None
    source = open(args.source_text, encoding="utf-8").read() if args.source_text else None
    report = ats_report(text, meta, keywords, source, args.filename)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.min_coverage is not None and report.get("keywords", {}).get("coverage") is not None \
            and report["keywords"]["coverage"] < args.min_coverage:
        return 2
    return 0 if report["parse_ok"] else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("guard"); p.add_argument("--draft", required=True); p.add_argument("--source", action="append", required=True); p.set_defaults(fn=cmd_guard)
    p = sub.add_parser("years"); p.add_argument("roles"); p.add_argument("--today"); p.set_defaults(fn=cmd_years)
    p = sub.add_parser("band"); p.add_argument("score", type=int); p.set_defaults(fn=cmd_band)
    p = sub.add_parser("dedupe"); p.add_argument("postings"); p.add_argument("--seen"); p.set_defaults(fn=cmd_dedupe)
    p = sub.add_parser("normalize"); p.add_argument("file"); p.set_defaults(fn=cmd_normalize)
    p = sub.add_parser("ats")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text"); src.add_argument("--pdf"); src.add_argument("--docx")
    p.add_argument("--keywords"); p.add_argument("--source-text"); p.add_argument("--filename"); p.add_argument("--min-coverage", type=float)
    p.set_defaults(fn=cmd_ats)
    args = parser.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
