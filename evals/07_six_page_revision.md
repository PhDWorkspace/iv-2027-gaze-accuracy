# Six main-text pages plus references: revision record

**Date:** 2026-11-06. **Requested target:** six pages for the main paper, with references additional. This supersedes the initial interpretation of six pages including references.

## Compiled result

- The baseline, after fixing an unclosed introduction list and enabling T1 encoding for accented bibliography names, compiled to eight physical pages; the main text extended onto page seven.
- The revised paper compiles to **six main-text pages plus one reference page**: seven physical pages in total. A page break separates the references.
- The compiled draft is `main.pdf` in the paper root (an ignored build artifact). The standard IEEEtran conference class, text size, columns, margins and figure widths are preserved. No font-size or margin reduction was used to meet the target.
- All seven pages were inspected visually. There are no undefined citations or references. A pre-existing 1.29 pt table-width warning and an underfull controlled-observation table cell remain visually minor; the table and text are legible.

## Editorial changes

The argument remains **real-driving measurement → controlled investigation → correction during driving**. Most savings come from repeated introduction contributions and conclusion summaries. The Related Work and experimental results are retained rather than compressed into metric lists.

- The introduction keeps the driving-supervision motivation, reference gap, three research questions and three contributions. It no longer repeats the full pipeline or the correction results later given in Results.
- Section IV removes prose that repeats the example-scene caption, gives the participant coverage in one sentence, and defines the bias/error ratio consistently with its implementation. Its ending directly motivates the controlled study.
- Section V shortens repeated study-design/protocol descriptions, identifies P2 as the wearer in the 1.41° → 0.87° controlled example, and makes the connection between learnable bias and useful correction explicit.
- The conclusion synthesises the three stages, retains the value of the acquisition workflow, and scopes the evidence to three participants, declared fixations and daytime driving. Downstream supervision benefits remain future work. Unsupported claims about evaluated task-suitability flags were removed from the conclusion.

TeXcount, including the abstract and excluding bibliography, venue-macro definitions and text embedded in figures:

| Category | Before | After |
|---|---:|---:|
| Prose | 4,028 | 3,591 |
| Headings | 83 | 83 |
| Captions/table text | 249 | 229 |
| Total counted text | 4,360 | 3,903 |

Prose was reduced by approximately 11%, while adding focused methodological evidence.

## Evidence added for the second review

1. **Reference footprint.** The annotated target boxes have median angular diagonal **1.28°**, P90 **2.60°**, across all 266 scenes. Existing calibrated pixel-to-ray and spherical-angle functions are reused. Each scene contributes its median extent over frames referenced by its metric-valid gaze samples. This is an annotated footprint, not a validated bound on annotation error or proof of exact centre fixation. See `data/04_target_angular_extent.py`, `.csv`, and `_summary.json`, and the new reference-size section in `04_driving_dataset.md`.
2. **Second review coverage.** The owner confirmed 200 target assignments received a second review. Formal inter-annotator agreement was not measured; no agreement statistic or blind-review protocol is inferred from that count.
3. **Current population.** The main comparison still uses all 266 scenes from 18 recordings, including both Stefan recordings. The new compact breakdown is P1 79 scenes / 10 recordings, P2 73 / 6, and P6 114 / 2.
4. **Paired uncertainty.** Section VI reports paired mean scene-error reductions relative to pooled chessboard calibration, with 95% scene-bootstrap intervals: P1 **0.07° [0.02, 0.11]**, P2 **0.58° [0.47, 0.68]**, P6 **0.20° [0.13, 0.27]**. These come from the existing `06_driving_scene_tests.csv`; they are means of scene-error differences, distinct from the recording-weighted sample medians in Table II. Scene errors are averaged over their test folds before paired testing. These describe variation within the observed benchmark, not population-level uncertainty across independent drivers or recording sessions.
5. **Error tails.** The manuscript explicitly retains P6's P90 exception: the in-situ median offset gives **4.29°**, versus **3.97°** for the chessboard offset. The velocity model improves P6's median/P90 to **1.35° / 3.58°**, in four of five folds.

## Remaining evidence boundary

Exact human fixation location and formal inter-annotator agreement are not independently measured. Public data/code release arrangements have not been supplied. No release commitment or new causal explanation for the calibration-source difference was invented.

## Validation and reproduction

- Full pdfLaTeX/BibTeX compilation through `latexmk`, using the standard IEEEtran class. The local TeX image needed the `multirow` and `ieeetran` packages.
- `bash scripts/sync_bib.sh --check`: both bibliography copies are in sync.
- All new footprint rows are finite and positive, cover 266 unique eligible scenes, and reproduce the reported quantiles. The summary records input/code hashes.
- The figure/model results from the previous current-data evaluation are unchanged; historical one-recording P6 values were not reintroduced.
- No canonical dataset files were written. The pre-existing `scripts/make_section4.py` edit and untracked figure/task files remain outside this revision.

Compile with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Reproduce the footprint summary with Horuspy `src` on `PYTHONPATH` and the dataset mounted read-only at `/data` (or set `DATA_ROOT`):

```bash
python evals/data/04_target_angular_extent.py
```
