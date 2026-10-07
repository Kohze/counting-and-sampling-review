# Scientific outputs and finite domains

- `table-reduction-audit.json`: exact summary printed by
  `reproduce/table_reduction_audit.py`.
- `table-reduction-instances.csv`: all 6,885 inputs in that exhaustive domain,
  including infeasible inputs. Columns give row margins, column margins,
  row-major capacities, and the common feasible count checked by both
  enumeration descriptions.
- `bisection-law-audit.json`: complete exact reports from
  `reproduce/bisection_law_audit.py`, including every returned table/failure
  probability, total variation, and the corresponding bound.
- `bisection-law-summary.csv`: one row for each of the nine toy-counter cases.
  Fields absent for the empty input are blank.
- `bisection-output-laws.csv`: each output with positive probability for each
  nonempty case. `output_kind=failure` has blank table coordinates. An empty
  original feasible set has its status in the JSON/summary and no probability
  law row.
- `independent-3x3-audit.json`: summary printed by
  `reproduce/independent_3x3_audit.py`.
- `independent-3x3-instances.csv`: all 100 seeded input/count rows. The two
  additional control counts are in the JSON.
- `data-provenance.json`: source-script/data hashes, generated-file hashes,
  arithmetic, and finite-domain descriptions.

Margins and coordinates are nonnegative integers. CSV matrices use row-major
order and one-based column labels. Exact rational values use `numerator/denominator`;
the JSON of the first audit follows Python Fraction's shorter formatting for
integer values. A blank coin-bit value denotes the ideal rational branch choice,
rather than a bounded-bit implementation.

To verify all outputs and source-citation identities:
`python -B reproduce/verify_repo.py`.

To regenerate the six derived files:
`python -B reproduce/export_data.py --write`.
The exporter uses the original audit functions and exact saved bisection report.
