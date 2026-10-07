# Approximate Counting and Uniform Sampling: A Critical Review of Matroid Intersections, Contingency Tables, and Graph Switch Chains

Robin Gounder · Vaionex Corporation · 7 October 2026

This repository accompanies a focused narrative review of six recent counting
and sampling manuscripts in the OpenAI mathematics release. It connects their
stated guarantees to established literature through representation-preserving
reductions, worked probability laws, and explicit accuracy and runtime models.

Read [the manuscript PDF](counting-and-sampling-review.pdf) or
[the LaTeX source](main.tex). The complete 39-entry bibliography is embedded in
`main.tex`. The [source-evidence ledger](references/citation-evidence.json)
records bibliographic identities, primary URLs, version dates, cited statements,
and their restrictions.

The scientific reproduction files check the review's bounded-table reduction,
its three-state uniform-versus-Fisher example, and finite output laws for
interval bisection with prescribed rational counter distributions. Their domains
and arithmetic are explicit; they support the worked analysis in the review.

## Repository contents

| Path | Purpose |
| --- | --- |
| `main.tex` | Editable manuscript, including the bibliography and dedicated AI disclosure |
| `counting-and-sampling-review.pdf` | Prepared manuscript PDF |
| `reproduce/` | Three original finite-audit scripts, data exporter, verification command, MIT license |
| `results/` | Saved exact JSON outputs, complete small-instance CSV data, output-law CSVs, data provenance |
| `references/` | Curated citation evidence and recommended release citation records |
| `CITATION.cff` | Author and preferred manuscript citation |
| `LICENSE.md` | Manuscript/data rights and the separate reproduction-code license |

## Reproduce the scientific checks

Use Python 3.8 or later. All scripts use Python's standard library.

From the repository directory:

```sh
python -B reproduce/verify_repo.py
```

The verification command reruns all three original audits, compares their JSON
objects with the saved outputs, regenerates and checks all six derived data
files, and checks that the source bibliography and citation ledger contain the
same 39 references. It writes no files. The script also works from another
working directory when invoked with its absolute path.

Individual audits:

```sh
python -B reproduce/table_reduction_audit.py
python -B reproduce/bisection_law_audit.py
python -B reproduce/independent_3x3_audit.py
python -B reproduce/export_data.py --check
```

Expected scientific checks:

- **2×2 tables:** 6,885 equal-total inputs, 1,215 nonempty instances, maximum
  count 3. Direct table enumeration and all-subset integer-common-base
  enumeration agree. The Fisher probabilities are `1/6, 2/3, 1/6`, at total
  variation distance `1/3` from the uniform law.
- **Interval bisection:** nine prescribed exact/relative-error/failure cases,
  including an empty support and a unique feasible table. The complete finite
  laws retain failure mass and account for fixed-bit branch rounding.
- **3×3 tables:** 100 cases with seed 20261007 and totals 0–3, using capacities
  0, 1, 2, and 1,073,741,825; 71 are nonempty, maximum count 2. Additional
  controls give 6 binary permutation matrices and 2 six-cycle-host matchings.
  Large capacities here accompany small totals; this is a finite representation
  check.

The original scripts print JSON to standard output. The saved JSON is accompanied
by all 6,885 enumerated 2×2 input/count rows and all 100 seeded 3×3 input/count
rows. See [the results guide](results/README.md) for formats.

To regenerate the six derived files explicitly:

```sh
python -B reproduce/export_data.py --write
```

The two original saved JSON outputs are reproduced by their corresponding
audit scripts. The exporter creates the additional 3×3 JSON report and CSVs
and records their hashes in `results/data-provenance.json`.

## Build the manuscript

Install a LaTeX distribution with the packages listed at the start of
`main.tex` (including `amsmath`, `booktabs`, `lmodern`, `xurl`, and
`hyperref`). In the repository directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

This produces `main.pdf`. The second pass resolves references. The bibliography
is self-contained and does not require BibTeX. PDF binary hashes can differ
between builds because of toolchain and metadata differences.

## Sources and scope

The review assesses the release at commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a` and uses a literature cutoff of
7 October 2026. Its evidence matrix distinguishes manuscript statements from
the selected formalization scope described by repository documentation.
The reference ledger includes 22 published scholarly works, 4 external
research preprints, 6 release research preprints, and 7 documentation entries.
See [the reference guide](references/README.md) for the classifications and
access qualifications.

Third-party papers remain available through their primary publishers, author
copies, versioned preprints, or pinned repository links. This repository carries
their citation evidence rather than copies of their manuscripts.

## Citation and licensing

Use [`CITATION.cff`](CITATION.cff) to cite the manuscript and accompanying
artifacts. No DOI is assigned in this repository.

Copyright © 2026 Robin Gounder. The manuscript, repository narrative text, and
data collection retain all rights reserved; publication here provides reading
and inspection access. The original Python reproduction code under
`reproduce/` is licensed under the
[MIT License](reproduce/LICENSE). See [the licensing notice](LICENSE.md)
for the scope of these separate terms.
