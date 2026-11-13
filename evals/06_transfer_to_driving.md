# Section VI: four-driver calibration and transfer evaluation

Updated 2026-11-13. The median-offset benchmark uses **322 verified scenes from 21 recordings, four drivers and five dates**. All four drivers are among the 11 controlled-study participants. P8 retains his existing participant code.

## Results used in the manuscript

Median / P90 angular error in degrees, averaged over held-out driving folds:

| Calibration | P1 | P2 | P6 | P8 |
|---|---:|---:|---:|---:|
| Uncorrected | 3.96 / 4.63 | 1.48 / 2.20 | 6.35 / 8.14 | 2.08 / 3.15 |
| Pooled chessboards | 0.88 / 1.62 | 1.40 / 2.19 | 1.80 / 3.77 | 1.46 / 2.43 |
| In-situ 20% | 0.76 / 1.61 | 0.83 / 1.63 | 1.61 / 3.95 | 0.82 / 1.87 |

In-situ calibration improves the median relative to pooled chessboards for all four drivers. P6's P90 remains higher with the in-situ offset (3.95 versus 3.77 degrees). Five random references beat the pooled chessboard offset for every participant on average; one already does so for P2 and P8. These are within-benchmark results, not population-wide or future-session guarantees.

Paired mean scene-error reductions relative to pooled chessboards, with 95% scene-bootstrap intervals: P1 **0.07 [0.02, 0.11]**, P2 **0.58 [0.47, 0.68]**, P6 **0.23 [0.16, 0.30]**, P8 **0.56 [0.36, 0.74]** degrees. These are scene-level statistics, distinct from weighted sample-error quantiles in the figure and tables.

## Computation preserved

- Canonical gaze tables, detections and annotations were read only. Existing completed benchmark outputs were copied into `data/06_four_drivers/offset/`, with original protocols and hashes. Large CSVs are gzip-compressed losslessly. No synthetic illustration values are used.
- Driving eligibility: a Player-validated scene with at least two finite, metric-valid samples; no central trimming. Scene offsets are componentwise medians of gaze minus target (+right/+up; azimuth wrapped to [-180, 180)).
- Fit `MedianOffset` to calibration-scene offsets, with one vote per scene. Chessboard calibration likewise pools individual corner offsets from complete boards, using the central 60% of each static fixation. It does not average board-level correction models.
- Driving folds: existing seed-42 shuffled KFold over sorted scene IDs, one block for calibration and the other four for testing. Calibration scenes per fold: P1 15–16, P2 14–15, P6 29, P8 5. The test scenes match between calibration sources.
- Chessboard calibration uses the existing GroupKFold by recording and all complete boards in its training pool. Average only available estimates within each driving fold, then the five driving folds equally. The source-fold count and complete-board eligibility are preserved; no missing estimate is invented or treated as zero. The transfer protocol records the independent recomputation of P6/P8 and retention of P1/P2 rows.
- Score spherical gaze-to-target errors with equal recording weight, equal scene weight within each recording, and equal sample weight within each scene. Median/P90 invert the weighted empirical CDF. Report equal means of split scores, not quantiles over pooled splits or medians of scene medians.
- Random k references: preserve the saved participant-specific seeds and 20 draws per fold; average draws within fold, then folds equally. Plot lines only at available k values (P8: 1–5). Shaded ranges describe fold means, not individual draw variation or confidence intervals.
- Scene-level tests retain the existing paired Wilcoxon tests, Holm correction within participant and research question, and 2,000-resample seed-42 bootstrap of the mean scene difference. Scenes are averaged over their held-out appearances before comparisons.

## Independent recording and day transfer

Retain the manuscript's existing minimum of five verified fixations per calibration source; shorter recordings remain test targets. Calibrate one whole recording and test all others. For actual day transfer, pool one day's scenes and test the other day in both directions. No pseudo-days or artificial recording segments are used.

| Split | P1 | P2 | P6 | P8 |
|---|---:|---:|---:|---:|
| Random 20% scenes | 0.76 | 0.83 | 1.61 | 0.82 |
| Across recordings | 0.84 | 0.89 | 1.79 | — |
| Across actual days | 1.17 | 0.91 | 1.72 | — |

All 14 eligible recording splits improve (P1: 7, P2: 3, P6: 4). All six day-transfer directions improve. P6's dates are November 4 and 11: 114 and 31 scenes; corrected day-transfer scores are 1.80 and 1.64 degrees. P1's day comparison includes factory recalibration. Different rows have different held-out sets and calibration budgets; their score differences are descriptive, not paired transfer penalties.

`runs/driving_recordings/summary.csv` averages all source recordings, including sources below the five-scene minimum. Consequently, use the filtered `scores.csv` rows, not its unfiltered recording summary. Filtering reproduces the original P1/P2 values (0.84/0.89), while extending P6 to four actual recordings. Exact splits, counts and summaries are exported to `data/06_recording_day_transfer_*.csv`; the manuscript table is generated as `figures/tab_recording_transfer.tex`.

## Audit and reproduction

`data/06_four_driver_audit.py` reuses the existing Horuspy loaders, splitter, median estimator, spherical scorer and category aggregation. It verifies the 322 driving units and 90,239 samples, 114 distinct source-file hashes, and all recorded implementation hashes. It reproduces **2,510 raw/median-offset scores**, checks the saved split identities against `make_splits`, verifies zero train/test overlap and matched held-out scenes across calibration sources, checks all **3,843 driving calibration selections** against their training pools, and reproduces all **68 category summaries**. Results are recorded in `data/06_four_drivers/verification.json`.

Run the audit with Horuspy `src` and `scripts/offset_benchmark` on `PYTHONPATH`, and `DATA_ROOT=/home/william/data`. All dataset and Horuspy mounts should be read-only. Regenerate the offset figure, transfer table and flat exports with:

```bash
python scripts/make_section6.py
```

The default reads the four-driver snapshot and regenerates the offset figure, recording/day table and detailed model table. Use `--offset-only` to regenerate only the offset outputs.

## Detailed models updated on the full benchmark

The existing `transfer_regression`, `linear_runtime`, `ridge_20` and `ridge_80` specifications were rerun with the participant list expanded to P1/P2/P6/P8. Seed, folds, models, features, regularization strengths and sample rules are unchanged. Exact specifications are in `data/06_four_drivers/specs/`, with run protocols, scores and split identities under `offset/runs/`. The original 266-scene model runs remain under `data/06_current_driving/` for historical provenance.

Cells below are median / P90 error in degrees. These generate `figures/tab_transfer_models.tex`.

| Fitted on | Correction | P1 | P2 | P6 | P8 |
|---|---|---:|---:|---:|---:|
| Chessboards | median offset | 0.88 / 1.62 | 1.40 / 2.19 | 1.80 / 3.77 | 1.46 / 2.43 |
| Chessboards | linear, position | 1.17 / 1.84 | 1.30 / 2.16 | 1.95 / 4.10 | 2.83 / 3.68 |
| Chessboards | linear, position + pupil | 1.08 / 1.75 | 1.49 / 2.38 | 2.03 / 4.15 | 6.16 / 7.38 |
| In-situ 20% | median offset | 0.76 / 1.61 | 0.83 / 1.63 | 1.61 / 3.95 | 0.82 / 1.87 |
| In-situ 20% | linear, position | 0.87 / 1.77 | 0.89 / 1.78 | 1.61 / 3.63 | 0.86 / 1.77 |
| In-situ 20% | linear, position + pupil | 0.87 / 1.81 | 0.89 / 1.78 | 1.64 / 3.65 | 0.92 / 1.80 |
| In-situ 20% | linear, position + velocity | 0.85 / 1.76 | 0.86 / 1.66 | 1.53 / 3.16 | 0.78 / 1.66 |

The linear model retains the same median-offset base and learns standardized feature terms from at most 60 evenly spaced samples per calibration unit. It is fitted to the residual target-minus-shifted-gaze directions; the fitted intercept is subtracted from predictions, preserving the median base as the constant term. Ridge uses the same estimator with alpha 100. Calibration uses only the selected training units.

Runtime velocity uses the latest preceding gaze sample at least 100 ms earlier, with the existing as-of tolerance (resulting time differences 100–150 ms). Azimuth differences are wrapped. The existing runtime loader retains samples with finite gaze, velocity and inverse distance, even for the position/velocity variant that does not use distance. Its scene offsets are recomputed on this retained sample set. This filter is preserved rather than adjusted after seeing results. Feature-matched raw and median baselines are evaluated with every runtime run.

The results support the existing interpretation: chessboard-trained position/pupil terms do not provide a consistent transfer benefit. Driving-trained velocity terms help P6 and P8, while the simple median offset has the lowest mean median error for P1 and P2 among the reported linear variants. P6 improves both median and P90 in **5/5 folds**, P8 in **4/5 folds** (P90 improves in all five). No population-level inference is made from those overlapping folds. Ridge and distance variants are retained in the saved runs and exports, rather than selected post hoc for the main table. Ridge situation summaries were regenerated with the existing `analyze_ridge.py` so they do not retain the old recording pool.

## Model verification and dataset commit

The independent model audit verified **268 source-file hashes**, all recorded implementation hashes, exact saved split identities and zero train/test overlap. All **90,239 driving samples in 322 scenes** pass the unchanged runtime feature filter, so the velocity comparison also uses the exact same samples as the principal benchmark. Median baselines reproduce the previously audited offset results. All P1/P2 summary metrics reproduce their earlier runs unchanged. All four run summaries were recomputed from their scores, and **108 raw/model scores** were independently refitted and rescored, covering each participant, protocol and model. Fold-wise velocity improvements were checked against each matched median baseline.

Evidence is saved in `data/06_four_drivers/model_verification.json`; the exact audit script is `data/06_model_audit.py`. The audit ran with dataset and Horuspy read-only, using `/scratch` for candidate runs, temporary input caches and the report. No audit script, log, cache, temporary result directory or generated plot was installed in the dataset. Only the 30 final CSV/protocol files belonging to the four model runs were promoted to their canonical evaluation directories. Losslessly compressed split/selection/unit-error copies and exact specs are retained in the paper repository for reproducibility.

Dataset commit: **`660b6f5`** (`660b6f552224bd2ff9374613e44fa24570628f1c`). It contains 46 reviewed CSV/JSON files: final gaze-accuracy results and the related benchmark/catalog/association updates. Only the three new driving catalog rows were staged; five unrelated catalog additions and other pre-existing changes remain uncommitted. The committed file set and installed output hashes were checked after the commit.

The refreshed manuscript compiles to **six main-text pages plus one reference page**, with no undefined citations/references or overfull boxes. The existing underfull controlled-observation cell remains. The four-driver table and transfer results were inspected at paper scale.
