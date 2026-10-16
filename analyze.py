"""Recompute descriptive results from attributed nineteenth-century tables.

No random samples, trained models, or inferred diagnoses are created here.
Run: python3 analyze.py
"""

from pathlib import Path
import csv, json
from fractions import Fraction

ROOT = Path(__file__).resolve().parent


def load_institutions():
    with (ROOT / "data/institutions_1871.csv").open() as f:
        return [
            dict(
                institution=r["institution"],
                **{k: int(r[k]) for k in ("from_birth", "others", "total")}
            )
            for r in csv.DictReader(f)
        ]


def share(rows):
    return Fraction(sum(r["from_birth"] for r in rows), sum(r["total"] for r in rows))


def summarize(rows):
    b = sum(r["from_birth"] for r in rows)
    o = sum(r["others"] for r in rows)
    n = sum(r["total"] for r in rows)
    loo = [
        {
            "omitted": r["institution"],
            "share_pct": float(100 * share([x for x in rows if x is not r])),
        }
        for r in rows
    ]
    return {
        "institutions": len(rows),
        "from_birth": b,
        "others": o,
        "total": n,
        "pooled_from_birth_pct": float(Fraction(100 * b, n)),
        "pooled_others_pct": float(Fraction(100 * o, n)),
        "institution_shares_pct": {
            r["institution"]: float(Fraction(100 * r["from_birth"], r["total"]))
            for r in rows
        },
        "equal_institution_weight_share_pct": float(
            sum(Fraction(100 * r["from_birth"], r["total"]) for r in rows) / len(rows)
        ),
        "leave_one_institution_out": loo,
        "coverage_diagnostic": {
            "reported_institutional_total": 1122,
            "table_total": n,
            "difference": 1122 - n,
            "table_fraction_pct": 100 * n / 1122,
        },
        "conditional_completion_scenarios_pct": {
            "all_others_acquired_and_68_unmarked_acquired": 100 * b / 1122,
            "all_others_acquired_and_68_unmarked_from_birth": 100
            * (b + 1122 - n)
            / 1122,
            "others_not_assumed_acquired_with_no_other_information_lower": 100
            * b
            / 1122,
            "others_not_assumed_acquired_with_no_other_information_upper": 100.0,
        },
        "correction_1881": {
            "enumerated": 13295,
            "under5_enumerated": 498,
            "under5_estimated": 2077,
            "corrected": 13295 - 498 + 2077,
            "added": 2077 - 498,
            "increase_pct": 100 * (2077 - 498) / 13295,
            "under5_estimate_multiple": 2077 / 498,
        },
        "age_rate_changes_1871_to_1881": load_age_changes(),
    }


def load_age_changes():
    with (ROOT / "data/age_rates.csv").open() as f:
        return [
            {
                "age": r["age_period"],
                "1871": int(r["1871"]),
                "1881": int(r["1881"]),
                "difference": int(r["1881"]) - int(r["1871"]),
                "relative_change_pct": 100 * (int(r["1881"]) / int(r["1871"]) - 1),
            }
            for r in csv.DictReader(f)
        ]


def completion_sensitivity():
    # u is a deliberately varied hypothetical fraction of 'Others' whose onset is unknown.
    # These are identification scenarios, not confidence intervals or observations.
    return [
        {
            "unknown_fraction_of_others": str(u),
            "lower_pct": 100 * 665 / 1054,
            "upper_pct": float(100 * (Fraction(665) + u * 389) / 1054),
        }
        for u in (
            Fraction(0),
            Fraction(1, 4),
            Fraction(1, 2),
            Fraction(3, 4),
            Fraction(1),
        )
    ]


if __name__ == "__main__":
    result = summarize(load_institutions())
    result["others_sensitivity"] = completion_sensitivity()
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "results/results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
