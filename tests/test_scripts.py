"""Tests for the deterministic scripts: jobkit (incl. the ATS checker), render-art (check-only) and generate-image.

Run: python3 -m unittest discover -s tests -v
Each script is driven through its CLI, as a skill would. Standard library only; no Chrome, no network.
"""
import copy
import json
import importlib.util
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOBKIT = ROOT / "plugins/jobsearch-in-a-box/scripts/jobkit.py"
RENDER = ROOT / "plugins/designer-in-a-box/scripts/render-art.py"
GENERATE = ROOT / "plugins/designer-in-a-box/scripts/generate-image.py"
GATE = ROOT / "plugins/dev-in-a-box/scripts/qualitygate.py"
EXAMPLE_SPEC = ROOT / "plugins/designer-in-a-box/examples/art-spec.json"


_spec = importlib.util.spec_from_file_location("jobkit", JOBKIT)
jobkit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(jobkit)
ats_report = jobkit.ats_report


def run(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)


def _tiny_pdf(text):
    """One-page PDF using a Type0-free simple font with a ToUnicode CMap, so extractors return `text` verbatim."""
    codes = sorted({c for c in text})
    mapping = {c: i + 1 for i, c in enumerate(codes)}
    hexcodes = "".join(f"{mapping[c]:02X}" for c in text)
    bf = "\n".join(f"<{mapping[c]:02X}> <{ord(c):04X}>" for c in codes)
    cmap = ("/CIDInit /ProcSet findresource begin 12 dict begin begincmap /CMapName /Adobe-Identity-UCS def /CMapType 2 def "
            "1 begincodespacerange <00> <FF> endcodespacerange "
            f"{len(codes)} beginbfchar\n{bf}\nendbfchar endcmap CMapName currentdict /CMap defineresource pop end end").encode()
    stream = f"BT /F1 12 Tf 50 700 Td <{hexcodes}> Tj ET".encode()
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(stream) + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /TrueType /BaseFont /Helvetica /FirstChar 0 /LastChar 255 /ToUnicode 6 0 R >>",
        b"<< /Length %d >>\nstream\n" % len(cmap) + cmap + b"\nendstream",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for n, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % n + body + b"\nendobj\n"
    xref = len(out)
    out += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objs) + 1)
    out += b"".join(b"%010d 00000 n \n" % o for o in offsets)
    return out + b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF" % (len(objs) + 1, xref)


class TempDirCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = pathlib.Path(self._tmp.name)

    def write(self, name, data):
        path = self.tmp / name
        path.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
        return path


class JobkitTest(TempDirCase):
    def test_band_edges(self):
        for score, label in [(0, "Poor fit"), (40, "Poor fit"), (60, "Possible fit"), (75, "Good fit"), (90, "Excellent fit"), (100, "Excellent fit")]:
            with self.subTest(score=score):
                self.assertEqual(run(JOBKIT, "band", score).stdout.strip(), label)

    def test_years_counts_overlapping_roles_once(self):
        roles = self.write("roles.json", [{"start": "2018-01", "end": "2020-01"}, {"start": "2019-01", "end": "2021-01"}])
        out = run(JOBKIT, "years", roles, "--today", "2026-01")
        self.assertEqual(json.loads(out.stdout), {"months": 36, "years": 3})

    def test_years_open_role_runs_to_today(self):
        roles = self.write("roles.json", [{"start": "2025-01"}])
        out = run(JOBKIT, "years", roles, "--today", "2026-01")
        self.assertEqual(json.loads(out.stdout)["months"], 12)

    def test_guard_flags_a_number_no_source_backs(self):
        draft = self.write("draft.txt", "Led a team of 12 at Acme.")
        source = self.write("source.txt", "I led 5 engineers at Acme.")
        out = run(JOBKIT, "guard", "--draft", draft, "--source", source)
        self.assertEqual(out.returncode, 2)
        self.assertEqual(json.loads(out.stdout)["unverified"], ["12"])

    def test_guard_passes_a_backed_draft(self):
        text = self.write("same.txt", "I led 5 engineers at Acme.")
        out = run(JOBKIT, "guard", "--draft", text, "--source", text)
        self.assertEqual(out.returncode, 0)
        self.assertEqual(json.loads(out.stdout)["unverified"], [])

    def test_dedupe_drops_repeats_within_a_batch_and_against_seen(self):
        posting = {"company": "Acme", "title": "Backend Engineer", "place": "Remote"}
        postings = self.write("postings.json", [
            posting,
            {"company": "ACME ", "title": "backend  engineer", "place": "remote"},  # same job, different casing
            {"company": "Globex", "title": "SRE", "place": "Lisbon"},
        ])
        fresh = json.loads(run(JOBKIT, "dedupe", postings).stdout)["fresh"]
        self.assertEqual([p["company"] for p in fresh], ["Acme", "Globex"])
        seen = self.write("seen.json", ["globex|sre|lisbon"])
        fresh = json.loads(run(JOBKIT, "dedupe", postings, "--seen", seen).stdout)["fresh"]
        self.assertEqual([p["company"] for p in fresh], ["Acme"])


GOOD_CV = """Ana Souza
ana.souza@example.com | +55 11 91234-5678 | linkedin.com/in/anasouza

RESUMO PROFISSIONAL
Engenheira de dados com experiência em pipelines ETL, Python e SQL, focada em confiabilidade e eficiência de fluxos.

EXPERIÊNCIA PROFISSIONAL
Engenheira de Dados | Acme Ltda | 03/2021 - presente
- Construiu pipelines ETL em Python e Airflow para ingestão diária de dados de vendas.
- Modelou tabelas analíticas em SQL e documentou contratos de dados com o time de produto.
- Reduziu falhas de carga ao adicionar testes automatizados e alertas de qualidade de dados.
Principais tecnologias: Python, Airflow, SQL, PostgreSQL, Docker
Analista de Dados | Globex S.A. | 01/2018 - 02/2021
- Criou relatórios em SQL para as áreas financeira e comercial e automatizou conciliações semanais.
- Padronizou consultas e dicionário de dados usados por quatro equipes de negócio.
- Apoiou migração de planilhas para banco relacional com validação por amostragem.
Principais tecnologias: SQL, Excel, Power BI

FORMAÇÃO ACADÊMICA
Bacharelado em Sistemas de Informação, Universidade Exemplo, 2013 - 2017

HABILIDADES
Linguagens: Python, SQL
Dados: ETL, Airflow, PostgreSQL, Power BI
Ferramentas: Docker, Git
""" + "\n".join(f"- Atividade complementar {i} de rotina com entrega documentada e revisada pelo time." for i in range(12))

KEYWORDS = [
    {"term": "Python", "status": "covered", "must": True},
    {"term": "ETL", "status": "covered", "must": True},
    {"term": "Airflow", "status": "covered", "must": False},
    {"term": "Kubernetes", "status": "gap", "must": True},
    {"term": "Spark", "status": "gap", "must": False},
    {"term": "Power BI", "status": "partial", "must": False, "aliases": ["PowerBI"]},
]

# (name, mutation of GOOD_CV, issue code that must appear; None = clean)
ATS_CASES = [
    ("clean", lambda t: t, None),
    ("ligature-fi", lambda t: t.replace("confiabilidade", "conﬁabilidade"), "ligatures"),
    ("ligature-fl", lambda t: t.replace("fluxos", "ﬂuxos"), "ligatures"),
    ("garbled-cid", lambda t: t.replace("Python e SQL", "(cid:12)(cid:45) e SQL", 1), "unmapped-glyphs"),
    ("replacement-char", lambda t: t.replace("Docker", "Doc�er"), "unmapped-glyphs"),
    ("image-only", lambda t: "Ana Souza\nana.souza@example.com\n", "no-selectable-text"),
    ("letter-spaced-name", lambda t: t.replace("Ana Souza", "A n a S o u z a", 1) + "\nS k i l l s e t\n", "letter-spacing"),
    ("two-columns", lambda t: "\n".join(ln + "          Coluna lateral" if ln.strip() else ln for ln in t.splitlines()), "columns"),
    ("no-experience-heading", lambda t: t.replace("EXPERIÊNCIA PROFISSIONAL", "ONDE TRABALHEI"), "missing-experience-heading"),
    ("no-skills-heading", lambda t: t.replace("HABILIDADES", "MEU ARSENAL"), "missing-skills-heading"),
    ("no-dates", lambda t: t.replace("03/2021 - presente", "").replace("01/2018 - 02/2021", "").replace("2013 - 2017", ""), "no-date-ranges"),
    ("no-email", lambda t: t.replace("ana.souza@example.com", "ver no LinkedIn"), "contact-missing"),
    ("fancy-bullets", lambda t: t.replace("\n- ", "\n➤ "), "bullets"),
    ("text-box", lambda t: t, "text-box"),
    ("header-contact", lambda t: t, "contact-in-header"),
    ("table-pipes", lambda t: t + "\n| a | b |\n| c | d |\n| e | f |\n", "table"),
    ("english-clean", lambda t: t.replace("RESUMO PROFISSIONAL", "SUMMARY").replace("EXPERIÊNCIA PROFISSIONAL", "WORK EXPERIENCE")
        .replace("FORMAÇÃO ACADÊMICA", "EDUCATION").replace("HABILIDADES", "SKILLS").replace("presente", "present"), None),
    ("pt-ate-dates-clean", lambda t: t.replace("03/2021 - presente", "março de 2021 até o presente").replace("01/2018 - 02/2021", "janeiro de 2018 até fevereiro de 2021"), None),
    ("intl-phone-clean", lambda t: t.replace("+55 11 91234-5678", "+34 612 345 678"), None),
    ("short-text-resume-clean", lambda t: "\n".join(t.splitlines()[:21]), None),
    ("two-line-heading-clean", lambda t: t.replace("RESUMO PROFISSIONAL", "RESUMO\nPROFISSIONAL"), None),
    ("accented-month-range-clean", lambda t: t.replace("03/2021 - presente", "Março 2021 - Atual"), None),
]
ATS_META = {"text-box": {"textboxes": 1}, "header-contact": {"header_footer_text": "ana.souza@example.com +55 11 91234-5678"}}


class AtsTest(TempDirCase):
    def ats(self, text, *extra, meta=None):
        path = self.write("cv.txt", text)
        cmd = ["ats", "--text", path, *extra]
        out = run(JOBKIT, *cmd)
        return out, json.loads(out.stdout)

    def test_normalize_repairs_ligatures_and_invisible_marks(self):
        path = self.write("l.txt", "conﬁabilidade eﬃciência ﬂuxos soft­hyphen zero​width")
        out = run(JOBKIT, "normalize", path)
        self.assertEqual(out.stdout, "confiabilidade efficiência fluxos softhyphen zerowidth")

    def test_labeled_corpus_reaches_80_percent_assertiveness(self):
        # Every case is judged by whether its expected code is raised (or no error is raised for clean cases).
        hits, rows = 0, []
        for name, mutate, code in ATS_CASES:
            report = ats_report(mutate(GOOD_CV), ATS_META.get(name))
            codes = {i["code"] for i in report["issues"]}
            ok = (report["parse_ok"] and not codes & {"ligatures", "columns", "unmapped-glyphs"}) if code is None else code in codes
            hits += ok
            rows.append((name, ok, sorted(codes)))
        accuracy = hits / len(ATS_CASES)
        self.assertGreaterEqual(accuracy, 0.8, rows)
        self.assertEqual([r for r in rows if not r[1]], [], "every case should pass, not just 80 percent")

    def test_good_cv_has_no_errors_and_exit_zero(self):
        out, report = self.ats(GOOD_CV)
        self.assertEqual(out.returncode, 0, out.stdout)
        self.assertTrue(report["parse_ok"])
        self.assertEqual(report["readability"], 100)

    def test_parse_error_exits_two(self):
        out, report = self.ats(GOOD_CV.replace("fluxos", "ﬂuxos"))
        self.assertEqual(out.returncode, 2)
        self.assertFalse(report["parse_ok"])

    def test_keywords_report_backed_missing_and_never_suggest_gaps(self):
        kw = self.write("kw.json", KEYWORDS)
        out, report = self.ats(GOOD_CV.replace("Airflow", "Prefect").replace("Power BI", "Tableau"), "--keywords", kw)
        k = report["keywords"]
        self.assertEqual(k["backed_but_missing"], ["Airflow", "Power BI"])
        self.assertEqual(k["gaps_not_claimed"], ["Kubernetes", "Spark"])
        self.assertNotIn("Kubernetes", k["present"] + k["backed_but_missing"])
        self.assertEqual(k["coverage"], 50.0)

    def test_alias_counts_and_accents_fold(self):
        kw = self.write("kw.json", [{"term": "Power BI", "status": "covered", "aliases": ["PowerBI"]},
                                    {"term": "experiencia", "status": "covered"}])
        _, report = self.ats(GOOD_CV.replace("Power BI", "PowerBI"), "--keywords", kw)
        self.assertEqual(report["keywords"]["coverage"], 100.0)

    def test_term_only_in_skills_list_is_flagged(self):
        kw = self.write("kw.json", [{"term": "Git", "status": "covered"}, {"term": "Python", "status": "covered"}])
        _, report = self.ats(GOOD_CV, "--keywords", kw)
        self.assertEqual(report["keywords"]["only_in_skills_list"], ["Git"])

    def test_term_must_be_a_whole_word(self):
        kw = self.write("kw.json", [{"term": "Java", "status": "covered"}, {"term": "SQ", "status": "covered"}])
        _, report = self.ats(GOOD_CV.replace("Python", "JavaScript"), "--keywords", kw)
        self.assertEqual(report["keywords"]["present"], [])

    def test_min_coverage_gate(self):
        kw = self.write("kw.json", KEYWORDS)
        out, _ = self.ats(GOOD_CV.replace("Airflow", "Prefect"), "--keywords", kw, "--min-coverage", "90")
        self.assertEqual(out.returncode, 2)
        out, _ = self.ats(GOOD_CV.replace("Airflow", "Prefect"), "--keywords", kw, "--min-coverage", "50")
        self.assertEqual(out.returncode, 0)

    def test_filename_convention(self):
        _, ok = self.ats(GOOD_CV, "--filename", "Ana-Souza-Data-Engineer-Acme.pdf")
        _, bad = self.ats(GOOD_CV, "--filename", "CV Ana Souza (final) v2.pdf")
        self.assertNotIn("filename", {i["code"] for i in ok["issues"]})
        self.assertIn("filename", {i["code"] for i in bad["issues"]})

    def test_extraction_loss_against_source(self):
        src = self.write("src.txt", GOOD_CV)
        _, report = self.ats(GOOD_CV[: len(GOOD_CV) // 2], "--source-text", src)
        self.assertIn("extraction-loss", {i["code"] for i in report["issues"]})
        _, report = self.ats(GOOD_CV, "--source-text", src)
        self.assertNotIn("extraction-loss", {i["code"] for i in report["issues"]})

    def test_docx_tables_textboxes_and_header_contact(self):
        W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
        paras = "".join(f"<w:p><w:r><w:t>{ln}</w:t></w:r></w:p>" for ln in GOOD_CV.replace("&", "e").splitlines())
        doc = f'<w:document {W}><w:body>{paras}<w:tbl><w:tr><w:tc><w:p><w:r><w:t>x</w:t></w:r></w:p></w:tc></w:tr></w:tbl>' \
              f'<w:p><w:r><w:txbxContent><w:p><w:r><w:t>oculto</w:t></w:r></w:p></w:txbxContent></w:r></w:p></w:body></w:document>'
        header = f'<w:hdr {W}><w:p><w:r><w:t>ana.souza@example.com</w:t></w:r></w:p></w:hdr>'
        path = self.tmp / "cv.docx"
        with zipfile.ZipFile(path, "w") as z:
            z.writestr("word/document.xml", doc)
            z.writestr("word/header1.xml", header)
        out = run(JOBKIT, "ats", "--docx", path)
        codes = {i["code"] for i in json.loads(out.stdout)["issues"]}
        self.assertTrue({"table", "text-box", "contact-in-header"} <= codes, codes)
        self.assertEqual(out.returncode, 2)

    def test_pdf_with_ligature_glyphs_is_caught_when_an_extractor_exists(self):
        try:
            import pypdf  # noqa: F401
        except ImportError:
            if not shutil.which("pdftotext"):
                self.skipTest("no PDF extractor installed")
        # A minimal one-page PDF whose content stream shows the single glyph U+FB01 through a ToUnicode map.
        pdf = _tiny_pdf("Ana Souza ana.souza@example.com conﬁabilidade")
        path = self.tmp / "t.pdf"
        path.write_bytes(pdf)
        out = run(JOBKIT, "ats", "--pdf", path)
        self.assertIn("ligatures", {i["code"] for i in json.loads(out.stdout)["issues"]}, out.stdout + out.stderr)


class RenderArtCheckTest(TempDirCase):
    def spec(self):
        return copy.deepcopy(json.loads(EXAMPLE_SPEC.read_text(encoding="utf-8")))

    def check(self, spec):
        return run(RENDER, self.write("spec.json", spec), self.tmp / "out", "--check-only")

    def test_example_spec_passes(self):
        out = self.check(self.spec())
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("art-spec ok", out.stdout)

    def test_low_contrast_is_rejected(self):
        spec = self.spec()
        spec["tokens"]["fg"] = spec["tokens"]["bg"]
        out = self.check(spec)
        self.assertEqual(out.returncode, 1)
        self.assertIn("contrast", out.stdout + out.stderr)

    def test_unknown_format_is_rejected(self):
        spec = self.spec()
        spec["format"] = "billboard"
        out = self.check(spec)
        self.assertEqual(out.returncode, 1)
        self.assertIn("format", out.stdout + out.stderr)

    def test_overlong_field_is_rejected(self):
        spec = self.spec()
        spec["slides"][0]["title"] = "x" * 200
        self.assertEqual(self.check(spec).returncode, 1)


class GenerateImageTest(TempDirCase):
    def spec_with_slot(self, prompt="A calm abstract gradient of teal and navy"):
        spec = json.loads(EXAMPLE_SPEC.read_text(encoding="utf-8"))
        spec["slides"][0]["image"] = {"generate": {"slot": "hero", "prompt": prompt}}
        return spec

    def test_requests_only_writes_brief_and_hash_and_sends_nothing(self):
        spec = self.write("spec.json", self.spec_with_slot())
        out = run(GENERATE, spec, self.tmp / "g")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("1 request(s) written", out.stdout)
        requests = json.loads((self.tmp / "g/image-requests.json").read_text())
        self.assertEqual(requests[0]["slot"], "hero")
        self.assertIs(requests[0]["text_in_image"], False)
        self.assertIn("watermark", requests[0]["negative"])  # the model must not draw letters or marks

    def test_hash_is_stable_for_the_same_request(self):
        spec = self.write("spec.json", self.spec_with_slot())
        first = run(GENERATE, spec, self.tmp / "a").stdout.split("hash ")[1].split()[0]
        second = run(GENERATE, spec, self.tmp / "b").stdout.split("hash ")[1].split()[0]
        self.assertEqual(first, second)

    def test_request_carrying_personal_data_is_rejected(self):
        spec = self.write("spec.json", self.spec_with_slot("Portrait for jane@example.com, see https://x.test"))
        out = run(GENERATE, spec, self.tmp / "g")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("remove it", out.stderr)

    def test_attach_needs_a_maker_name(self):
        spec = self.write("spec.json", self.spec_with_slot())
        images = self.tmp / "images"
        images.mkdir()
        out = run(GENERATE, spec, self.tmp / "g", "--attach", images)
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("--by", out.stderr)

    def test_attach_with_a_missing_image_fails(self):
        spec = self.write("spec.json", self.spec_with_slot())
        images = self.tmp / "images"
        images.mkdir()
        out = run(GENERATE, spec, self.tmp / "g", "--attach", images, "--by", "tester")
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("hero", out.stderr)

    def test_attach_records_provenance_bound_to_the_request_hash(self):
        spec = self.write("spec.json", self.spec_with_slot())
        images = self.tmp / "images"
        images.mkdir()
        (images / "hero.png").write_bytes(b"\x89PNG fake")
        out = run(GENERATE, spec, self.tmp / "g", "--attach", images, "--by", "tester")
        self.assertEqual(out.returncode, 0, out.stderr)
        digest = out.stdout.split("hash ")[1].split(";")[0].split()[0]
        assets = json.loads((self.tmp / "g/image-assets.json").read_text())
        self.assertEqual(assets, [{"slot": "hero", "file": "hero.png", "provider": "tester", "request_hash": digest}])
        resolved = json.loads((self.tmp / "g/art-spec.resolved.json").read_text())
        self.assertTrue(resolved["slides"][0]["image"]["asset"].endswith("hero.png"))


class QualityGateTest(TempDirCase):
    BRANCHY = ("def f(a, b, c):\n    if a:\n        if b:\n            return 1\n        if c:\n            return 2\n"
               "    for x in a:\n        if x and b or c:\n            return 3\n    return 0\n")
    SIMPLE = "def g(a):\n    return a\n"

    def coverage(self, path, executed, missing):
        return self.write("cov.json", {"files": {str(path): {"executed_lines": executed, "missing_lines": missing}}})

    def test_uncovered_branchy_function_fails_crap(self):
        src = self.write("m.py", self.BRANCHY)
        cov = self.coverage(src, [], list(range(1, 11)))
        out = run(GATE, "crap", "--files", src, "--coverage", cov)
        self.assertEqual(out.returncode, 2, out.stdout)
        found = json.loads(out.stdout)["checks"][0]["findings"][0]
        self.assertEqual(found["function"], "f")
        self.assertGreater(found["crap"], 10)

    def test_fully_covered_function_passes_crap(self):
        src = self.write("m.py", self.BRANCHY)
        cov = self.coverage(src, list(range(1, 11)), [])
        out = run(GATE, "crap", "--files", src, "--coverage", cov, "--max", 100)
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_crap_of_an_uncovered_simple_function_is_two(self):
        src = self.write("m.py", self.SIMPLE)
        cov = self.coverage(src, [], [1, 2])
        check = json.loads(run(GATE, "crap", "--files", src, "--coverage", cov).stdout)["checks"][0]
        self.assertEqual(check["functions"], 1)
        self.assertEqual(check["status"], "pass")
        out = run(GATE, "crap", "--files", src, "--coverage", cov, "--max", 1)
        self.assertEqual(json.loads(out.stdout)["checks"][0]["findings"][0]["crap"], 2.0)

    def test_duplicate_functions_are_flagged(self):
        a = self.write("a.py", self.BRANCHY)
        b = self.write("b.py", self.BRANCHY.replace("def f", "def h"))
        out = run(GATE, "dupes", "--files", a, b, "--min-nodes", 10)
        self.assertEqual(out.returncode, 2, out.stdout)
        self.assertGreaterEqual(json.loads(out.stdout)["checks"][0]["findings"][0]["similarity"], 0.8)

    def test_gate_without_reports_is_not_measured_never_pass(self):
        src = self.write("m.py", self.SIMPLE)
        out = run(GATE, "gate", "--files", src)
        self.assertEqual(out.returncode, 3, out.stdout)
        self.assertEqual(json.loads(out.stdout)["verdict"], "not-measured")

    def test_non_python_file_is_listed_as_not_measured(self):
        py = self.write("m.py", self.SIMPLE)
        kt = self.write("A.kt", "fun a() = 1")
        cov = self.coverage(py, [1, 2], [])
        out = run(GATE, "gate", "--files", py, kt, "--coverage", cov, "--mutation-score", 0.9)
        self.assertEqual(out.returncode, 3, out.stdout)
        self.assertEqual(json.loads(out.stdout)["not_measured_files"][0]["file"], str(kt))

    def test_everything_measured_and_inside_limits_passes(self):
        py = self.write("m.py", self.SIMPLE)
        cov = self.coverage(py, [1, 2], [])
        out = run(GATE, "gate", "--files", py, "--coverage", cov, "--mutation-score", 0.9)
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_mutation_score_below_floor_fails(self):
        py = self.write("m.py", self.SIMPLE)
        cov = self.coverage(py, [1, 2], [])
        out = run(GATE, "gate", "--files", py, "--coverage", cov, "--mutation-score", 0.5)
        self.assertEqual(out.returncode, 2, out.stdout)

    def test_config_overrides_default_limit(self):
        py = self.write("m.py", self.SIMPLE)
        cov = self.coverage(py, [1, 2], [])
        cfg = self.write("q.json", {"mutation_min": 0.95})
        out = run(GATE, "gate", "--files", py, "--coverage", cov, "--mutation-score", 0.9, "--config", cfg)
        self.assertEqual(out.returncode, 2, out.stdout)


if __name__ == "__main__":
    unittest.main()
