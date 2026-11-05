"""Tests for the deterministic scripts: jobkit, render-art (check-only) and generate-image.

Run: python3 -m unittest discover -s tests -v
Each script is driven through its CLI, as a skill would. Standard library only; no Chrome, no network.
"""
import copy
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
JOBKIT = ROOT / "plugins/jobsearch-in-a-box/scripts/jobkit.py"
RENDER = ROOT / "plugins/designer-in-a-box/scripts/render-art.py"
GENERATE = ROOT / "plugins/designer-in-a-box/scripts/generate-image.py"
EXAMPLE_SPEC = ROOT / "plugins/designer-in-a-box/examples/art-spec.json"


def run(script, *args):
    return subprocess.run([sys.executable, str(script), *map(str, args)], capture_output=True, text=True)


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


if __name__ == "__main__":
    unittest.main()
