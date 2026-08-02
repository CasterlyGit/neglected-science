# Structural Atlas

## Final verdict

**LIMITED SUPPORT — NO NEW TARGET TRIO**

Different fields in this seed set share recurring research-design failures: reused measurements, mismatched units, shifting calibration, evidence-table reconciliation, and missing usable data. This does not show that the fields share a scientific mechanism, and it does not yet produce three new interview-ready targets.

## Case map

| Domain | Structural pattern | Plain-language finding | Status |
| --- | --- | --- | --- |
| evolutionary biology | measurement-reuse | A striking pattern became much weaker when the starting measurement and later change were separated. | historical-demonstration |
| wildlife disease ecology | unit-mismatch | The data can test whether the association follows the same animal, but cannot by itself prove why it does. | gated |
| global-change evidence synthesis | provenance-reconciliation | A conclusion may change because researchers built the evidence table differently, not because the underlying experiments changed. | gated |
| battery diagnostics | calibration-shift | A diagnostic method can look accurate until the reference curve changes with the thing being diagnosed. | excluded |
| plant disease management | data-closure, unit-mismatch | The question may be important, but the public table is too compressed to test it properly. | excluded |
| materials fatigue engineering | unit-mismatch, data-closure | A persuasive validation question cannot be checked until the actual public files can be acquired. | deferred |
| experimental evolution | measurement-reuse | This is a promising independent check of whether a cross-environment pattern survives when its starting measurement is not reused. | gated |
| field ecosystem experiment | unit-mismatch | The field experiment is useful only if repeated plots, years, and outcomes are kept distinct rather than treated as interchangeable observations. | gated |
| materials fatigue engineering | scale-translation | A shared fatigue curve does not mean the same mechanism survives when the specimen scale changes. | gated |

## What this does and does not mean

- The atlas describes evidence-supported similarities in research design, not a universal theory or a shared mechanism across domains.
- Next gate: Add only new checksum-acquirable paper–data cases that can fill a documented structural gap; then rerun the closed-evidence factory. Do not promote a case merely because it resembles another domain.

## Evidence locations

- `struct-ecoli-assay-blocks`: https://doi.org/10.1098/rspb.2022.1292 (Methods: competition assays; Results: shallow-history analysis); https://doi.org/10.1534/genetics.114.169870 (Abstract and equations 3–4); data: https://doi.org/10.5061/dryad.4f4qrfjfs (Official archive manifest and verified raw files).
- `struct-bighorn-within-between`: https://doi.org/10.1098/rspb.2024.0636 (Methods: energetic-cost GLMMs; Discussion and Conclusions); https://doi.org/10.1111/ele.13160 (Abstract and recommendations); data: https://doi.org/10.5061/dryad.6wwpzgn44 (energeticcostsdata_20240514.csv headers and inspected rows).
- `struct-mesi-reconciliation`: https://doi.org/10.1111/gcb.16585 (Sections 2.3 and 3.2; Table 1); https://doi.org/10.5194/egusphere-egu26-15935 (EGU 2026 conference abstract); data: https://zenodo.org/records/10423853 (mesi_main.csv headers and inspected rows).
- `struct-battery-ocv-shift`: https://doi.org/10.1149/1945-7111/ad6938 (Aged-cell analysis; Summary and Conclusions); data: https://zenodo.org/records/13142016 (Experimental CSV files, condition-specific OCV curves, and MATLAB inventory).
- `struct-vineyard-aggregation`: https://doi.org/10.1002/ps.8140 (Methods and reported epidemic-by-treatment analysis); data: https://zenodo.org/records/15101430 (NT_UCSC_BCA_DiseaseSeverity.csv and Readme.txt).
- `struct-magdrift-access`: https://doi.org/10.1038/s41467-026-70290-w (Fatigue-life evaluation method); data: https://doi.org/10.5061/dryad.1rn8pk13t (Official file metadata and failed content retrieval receipt).
- `struct-tetrahymena-correlated-response`: https://doi.org/10.5061/dryad.vx0k6djzb (Abstract; README file description); data: https://doi.org/10.5061/dryad.vx0k6djzb (Dryad file inventory and README, lines 25–62).
- `struct-tundra-warming-plots`: https://doi.org/10.5061/dryad.9ghx3ffxx (Dataset description and abstract); data: https://doi.org/10.5061/dryad.9ghx3ffxx (Dryad dataset description).
- `struct-alloy-scale-translation`: https://doi.org/10.5061/dryad.vq83bk48n (Abstract; README file structure and methods); data: https://doi.org/10.5061/dryad.vq83bk48n (Dryad file inventory and README, lines 35–149).
