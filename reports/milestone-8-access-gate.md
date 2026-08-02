# Milestone 8 access gate — E. coli source files

Status: gated on 2026-08-02. No baseline, novel analysis, validation, final-holdout evaluation, or scientific result was run.

## Required evidence

The preregistration names `data_set-full.anc.txt` and `data_set-full.ev.change.txt` from Dryad DOI 10.5061/dryad.4f4qrfjfs. Dryad's public version-file manifest (`/api/v2/versions/195459/files`, retrieved 2026-08-02) lists them with respectively SHA-256 `cca2444865e9f823882447a4b31cbe7c28b0227d4ab3f30b20aa0fd3471c57bb` and `11e2233ebe5d4b2560d475359f2682484bebc51d6d3ff0a38ebef6a3b02b9ed8`.

## Bounded access attempts

The documented public API archive and individual-file download routes returned HTTP 401. The legacy public file-stream route returned HTTP 403. A bounded search found no author-provided raw-data mirror. The linked Zenodo record (DOI 10.5281/zenodo.6795996) provides the original R Markdown analysis, but not input tables; the publisher Figshare collection (DOI 10.6084/m9.figshare.c.6179392) provides only supplementary tables and figures.

Those artifacts are insufficient substitutes for the raw observations. Reconstructing results from figures, relying on unverified copies, or treating metadata as data would violate the research contract.

## Reopen condition

Reopen only after an owner-authorized, public, checksum-verifiable source is available. Then reproduce the published-style baseline with blocks 1–2, freeze the validated implementation after block 3, and run block 4 exactly once under the preregistration.
