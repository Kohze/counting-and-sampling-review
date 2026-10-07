# Source evidence

The complete bibliography is in `../main.tex`. This folder supplies a
per-entry evidence ledger tied to that source's SHA-256 and byte count.

`citation-evidence.json` retains all 39 cited sources, their bibliographic
metadata, source categories, primary URLs and locators, cited roles, restrictions,
and access qualifications. `citation-evidence.csv` is a concise inspection view
of the same entries.

The classifications distinguish:
- 22 published scholarly works;
- 4 external versioned research preprints;
- 6 research manuscripts in the OpenAI release;
- 6 repository documentation records and 1 software documentation record.

This gives 32 research works, including 26 scholarly works independent of
the release. These counts describe the cited collection, rather than a claim
of completeness for the field.

Identity and scope evidence comes from original publishers, author-hosted texts
or publication records, versioned arXiv metadata/content, official software
documentation, and the release pinned to commit
`adc7f1241b42e322a6451854ab7e4b4c146bf78a`.
Preprints retain their source status. The evidence concerns the statements
used in this review; full source-proof certification is a separate undertaking.
The JSON records relevant source-access qualifications.

`release-recommended-citations.bib` preserves the release's six recommended
citation records. Its keys differ from the local short keys in `main.tex`;
it is provided as source evidence and is not required for the LaTeX build.
The manuscript itself uses pinned repository links.

Third-party manuscript files are available through the recorded primary URLs
and are not included here.
