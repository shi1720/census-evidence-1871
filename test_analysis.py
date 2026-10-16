"""Checks against independently transcribed printed totals and source assertions."""

import unittest
from fractions import Fraction
from analyze import load_institutions, share, summarize, completion_sensitivity


class SourceChecks(unittest.TestCase):
    def setUp(self):
        self.rows = load_institutions()

    def test_row_arithmetic(self):
        self.assertEqual(len(self.rows), 12)
        for r in self.rows:
            with self.subTest(r["institution"]):
                self.assertEqual(r["from_birth"] + r["others"], r["total"])

    def test_column_totals(self):
        self.assertEqual(
            tuple(
                sum(r[k] for r in self.rows) for k in ("from_birth", "others", "total")
            ),
            (665, 389, 1054),
        )

    def test_printed_rounded_share(self):
        self.assertEqual(round(float(100 * share(self.rows))), 63)

    def test_complement_does_not_make_diagnosis(self):
        # 37% reproduces the rounded complement; its interpretation is a historical claim.
        self.assertEqual(round(100 * 389 / 1054), 37)
        s = completion_sensitivity()
        self.assertEqual(s[0]["upper_pct"], s[0]["lower_pct"])
        self.assertEqual(s[-1]["upper_pct"], 100)
        self.assertTrue(all(a["upper_pct"] <= b["upper_pct"] for a, b in zip(s, s[1:])))

    def test_1881_published_correction(self):
        r = summarize(self.rows)["correction_1881"]
        self.assertEqual(r["corrected"], 14874)
        self.assertEqual(r["added"], 1579)
        self.assertEqual(8043 + 6831, r["corrected"])

    def test_age_pattern(self):
        a = summarize(self.rows)["age_rate_changes_1871_to_1881"]
        self.assertEqual([r["difference"] for r in a], [-4, -35, -62, -18, 44, 23, 124])

    def test_institution_extremes(self):
        rates = {
            r["institution"]: Fraction(r["from_birth"], r["total"]) for r in self.rows
        }
        self.assertEqual(max(rates, key=rates.get), "Brighton Institution")
        self.assertEqual(
            min(rates, key=rates.get), "Northern Counties Institution (Newcastle)"
        )

    def test_leave_one_out_by_subtraction(self):
        for i, r in enumerate(self.rows):
            self.assertEqual(
                share(self.rows[:i] + self.rows[i + 1 :]),
                Fraction(665 - r["from_birth"], 1054 - r["total"]),
            )


if __name__ == "__main__":
    unittest.main()
