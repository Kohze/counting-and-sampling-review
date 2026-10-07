"""Export deterministic scientific data for the review's finite audits.

python -B reproduce/export_data.py --check
python -B reproduce/export_data.py --write

The checks use exact integer/Fraction arithmetic in the companion scripts.
"""
import argparse
import contextlib
import csv
import hashlib
import io
import itertools
import json
from pathlib import Path
import random
import runpy

ROOT = Path(__file__).resolve().parents[1]


def json_text(value):
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def csv_text(headers, rows):
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(headers)
    writer.writerows(rows)
    return output.getvalue()


def scientific_files(root=ROOT):
    root = Path(root)
    table = runpy.run_path(str(root / "reproduce/table_reduction_audit.py"),
                          run_name="_table_data")
    table_rows = []
    for flat_caps in itertools.product(range(3), repeat=4):
        caps = (flat_caps[:2], flat_caps[2:])
        for rows in itertools.product(range(5), repeat=2):
            for col0 in range(5):
                cols = (col0, sum(rows) - col0)
                if not 0 <= cols[1] <= 4:
                    continue
                count = table["check_instance"](rows, cols, caps)
                table_rows.append((len(table_rows) + 1, *rows, *cols,
                                   *flat_caps, count))
    assert len(table_rows) == 6885
    assert sum(row[-1] > 0 for row in table_rows) == 1215
    assert max(row[-1] for row in table_rows) == 3

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        three = runpy.run_path(str(root / "reproduce/independent_3x3_audit.py"),
                               run_name="_three_data")
    three_report = json.loads(captured.getvalue())
    rng = random.Random(20261007)
    three_rows = []
    for index in range(100):
        total = rng.randrange(4)
        margins = list(three["compositions"](total, 3))
        rows, cols = rng.choice(margins), rng.choice(margins)
        caps = tuple(rng.choice((0, 1, 2, 2**30 + 1)) for _ in range(9))
        count = three["check"](rows, cols, caps)
        three_rows.append((index + 1, *rows, *cols, *caps, count))
    assert sum(row[-1] > 0 for row in three_rows) == three_report["nonempty"]
    assert max(row[-1] for row in three_rows) == three_report["max_count"]

    bisection = json.loads((root / "results/bisection-law-audit.json")
                           .read_text(encoding="utf-8"))
    columns = ["case", "states", "depth_bound", "relative_tolerance",
               "failure_parameter_per_counter", "coin_bits_per_branch",
               "tv", "tv_bound", "failure_probability", "failure_bound",
               "replacement_tv", "worst_local_tv", "status"]
    summary_rows, law_rows = [], []
    for case in bisection["cases"]:
        summary_rows.append([case.get(key, "") for key in columns])
        for item in case.get("output_law", []):
            state = item["state"]
            law_rows.append([case["case"],
                             "failure" if state == "failure" else "table",
                             *([""] * 4 if state == "failure" else state), item["probability"]])
    out = {
        "table-reduction-instances.csv": csv_text(
            ["case", "r1", "r2", "c1", "c2", "u11", "u12", "u21", "u22",
             "feasible_count"], table_rows),
        "independent-3x3-instances.csv": csv_text(
            ["case", "r1", "r2", "r3", "c1", "c2", "c3",
             "u11", "u12", "u13", "u21", "u22", "u23", "u31", "u32", "u33",
             "feasible_count"], three_rows),
        "independent-3x3-audit.json": json_text(three_report),
        "bisection-law-summary.csv": csv_text(columns, summary_rows),
        "bisection-output-laws.csv": csv_text(
            ["case", "output_kind", "x11", "x12", "x21", "x22",
             "probability"], law_rows),
    }
    provenance = {
        "date": "2026-10-07",
        "generator": "reproduce/export_data.py",
        "arithmetic": "exact integers and fractions.Fraction in source audits",
        "source_scripts": {
            name: hashlib.sha256((root / "reproduce" / name).read_bytes())
                  .hexdigest()
            for name in ["table_reduction_audit.py",
                         "independent_3x3_audit.py",
                         "bisection_law_audit.py"]
        },
        "source_data": {
            "results/bisection-law-audit.json":
                hashlib.sha256((root / "results/bisection-law-audit.json")
                               .read_bytes()).hexdigest()
        },
        "generated_files": {
            name: {"bytes": len(text.encode("utf-8")),
                   "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()}
            for name, text in out.items()
        },
        "finite_domains": {
            "table_reduction": "all 6885 equal-total 2x2 instances; capacities "
                               "0..2 and margins 0..4",
            "independent_3x3": "100 seeded instances with totals 0..3; "
                               "capacities 0,1,2,1073741825",
            "bisection": "nine prescribed rational toy-counter cases; "
                         "complete nonempty output laws include failure mass"
        }
    }
    out["data-provenance.json"] = json_text(provenance)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true",
                      help="compare all derived files with saved data")
    mode.add_argument("--write", action="store_true",
                      help="regenerate only the six derived data files")
    args = parser.parse_args()
    expected = scientific_files()
    if args.write:
        (ROOT / "results").mkdir(exist_ok=True)
        for name, text in expected.items():
            (ROOT / "results" / name).write_bytes(text.encode("utf-8"))
        print("Wrote six derived scientific data files.")
    else:
        for name, text in expected.items():
            actual = (ROOT / "results" / name).read_bytes()
            if actual != text.encode("utf-8"):
                raise AssertionError("Derived data differs: " + name)
        print("All six derived scientific data files match exactly.")


if __name__ == "__main__":
    main()
