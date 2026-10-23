"""Calibration tests: human fixtures must PASS, slop fixtures must be FLAGGED. Run: python3 -m unittest discover tests"""
import os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import ink  # noqa: E402

FIX = os.path.join(HERE, "fixtures")


def score(name):
    return ink.run(open(os.path.join(FIX, name), encoding="utf-8").read())


class Calibration(unittest.TestCase):
    def test_human_pass(self):
        for f in ("human_fr.txt", "human_en.txt"):
            r = score(f)
            self.assertEqual(r["verdict"], "PASS", f"{f}: {r['overall']}")

    def test_slop_flagged(self):
        for f in ("slop_fr.txt", "slop_en.txt"):
            r = score(f)
            self.assertEqual(r["verdict"], "FLAGGED", f"{f}: {r['overall']}")

    def test_lang_detection(self):
        self.assertEqual(score("human_fr.txt")["lang"], "fr")
        self.assertEqual(score("human_en.txt")["lang"], "en")

    def test_clean_removes_fingerprints(self):
        dirty = "Voici\u200b un test \u2014 avec \u201cguillemets\u201d et \U0001D5EF\U0001D5FC\U0001D5F9\U0001D5F1."
        out, _ = ink.clean(dirty, "fr")
        self.assertNotIn("\u200b", out)
        self.assertNotIn("\u2014", out)
        self.assertIn("bold", out)

    def test_inflections(self):
        r = ink.run("Des produits robustes et des équipes qui fosters. Et vous, qu'en pensez-vous ?", "fr")
        self.assertIn("robuste", r["slop_terms"])
        self.assertIn("qu'en pensez-vous", r["slop_terms"])


class ProfileCliches(unittest.TestCase):
    def test_about_cliche_flagged(self):
        r = ink.run("Product Manager with a proven track record of success in the tech industry. I have a deep understanding of agile.", "en")
        self.assertIn("proven track record", r["slop_terms"])
        self.assertNotEqual(r["verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
