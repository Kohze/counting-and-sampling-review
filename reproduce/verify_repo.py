"""Verify the standalone review's exact outputs and citation identities.

Run from any working directory:
    python -B reproduce/verify_repo.py
Uses only the Python standard library and writes no files.
"""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    for script, saved in [
        ("table_reduction_audit.py", "table-reduction-audit.json"),
        ("bisection_law_audit.py", "bisection-law-audit.json"),
        ("independent_3x3_audit.py", "independent-3x3-audit.json"),
    ]:
        completed = subprocess.run(
            [sys.executable, "-B", str(ROOT / "reproduce" / script)],
            cwd=ROOT, text=True, encoding="utf-8", capture_output=True,
            check=True)
        actual = json.loads(completed.stdout)
        expected = json.loads((ROOT / "results" / saved)
                              .read_text(encoding="utf-8"))
        if actual != expected:
            raise AssertionError("Saved output differs: " + saved)
        print("PASS exact saved output:", saved)

    completed = subprocess.run(
        [sys.executable, "-B", str(ROOT / "reproduce/export_data.py"), "--check"],
        cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True)
    print(completed.stdout.strip())

    tex = (ROOT / "main.tex").read_text(encoding="utf-8")
    keys = re.findall(r"\\bibitem\{([^}]+)\}", tex)
    cited = {key.strip()
             for group in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", tex)
             for key in group.split(",")}
    ledger = json.loads((ROOT / "references/citation-evidence.json")
                        .read_text(encoding="utf-8"))
    source_bytes = (ROOT / "main.tex").read_bytes()
    if ledger["source_sha256"] != hashlib.sha256(source_bytes).hexdigest():
        raise AssertionError("Citation ledger source hash differs")
    if ledger["source_bytes"] != len(source_bytes):
        raise AssertionError("Citation ledger source byte count differs")
    ledger_keys = [entry["key"] for entry in ledger["entries"]]
    if len(keys) != 39 or len(set(keys)) != 39:
        raise AssertionError("Expected 39 distinct bibliography entries")
    if keys != ledger_keys or cited != set(keys):
        raise AssertionError("Bibliography, citations and ledger differ")
    if len(ledger["entries"]) != ledger["counts"]["bibliography_entries"]:
        raise AssertionError("Ledger count differs")
    print("PASS bibliography/citation ledger: 39 entries, all cited")
    print("All standalone scientific checks passed.")


if __name__ == "__main__":
    main()
