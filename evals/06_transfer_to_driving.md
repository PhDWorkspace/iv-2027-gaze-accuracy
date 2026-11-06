# Section VI: current calibration and transfer evaluation

**Updated:** 2026-11-06. All current driving comparisons include **266 validated scenes from 18 recordings**, including Stefan’s two actual recordings on November 4 (114 scenes, 23,300 samples). P1 and P2 retain 79 and 73 scenes. Canonical gaze tables and annotations were read only; new outputs are stored in this paper repository.

The previous 245-scene results remain available as [the dated historical evaluation](06_transfer_to_driving_2026-11-05.md). Historical runs under `06_transfer_regression_run/` and `06_linear_runtime_run/` are retained for provenance and are no longer the inputs to the current figure or model table. The historical frozen P6 baseline of 1.41° applies to the first recording only; the current 1.43° baseline uses both recordings.

## Protocol

- Reuse the existing Horuspy loaders, median/linear/ridge models, spherical-error scorer and seed-42 five-fold splits. Each driving fold calibrates on one shuffled scene block (~20%) and tests on the other four. Calibration and test scenes are disjoint.
- Calibration references per fold: P1 15–16; P2 14–15; P6 22–23. Test scenes and recording identities are matched across the compared sources/models. Random scene folds can contain references and tests from the same recordings; independent recording/day transfer is evaluated separately.
- Chessboard transfer pools approximately 80% of each participant’s available controlled recordings per calibration fold. Available recordings with complete boards: P1 125, P2 23, P6 25. The central 60% of each controlled fixation is used. Five calibration folds × five driving test folds give 25 model evaluations; their scores are averaged. In-situ models use five evaluations.
- Fit the median of the calibration fixation offsets, giving each fixation one vote. Score held-out samples with equal total weight per recording, equal fixation weight within recording, and equal sample weight within fixation. Median and P90 are weighted sample-error quantiles, not quantiles of scene medians. Report equal means of split scores.
- Runtime velocity uses the existing causal preceding-100-ms feature and feature-complete samples. Inspect each runtime run’s protocol and scene identities. The runtime median/raw scores match the principal median/raw scores at the reported precision.

## Current main comparison

Cells are median / P90 angular error in degrees. These values generate `figures/tab_transfer_models.tex` and `figures/fig6_transfer.pdf`.

| Source | Correction | P1 | P2 | P6 |
|---|---|---:|---:|---:|
| Pooled chessboards | Uncorrected | 3.96 / 4.63 | 1.48 / 2.20 | 5.97 / 7.91 |
| Pooled chessboards | Median offset | 0.88 / 1.62 | 1.40 / 2.19 | 1.51 / 3.97 |
| Pooled chessboards | Linear, position | 1.17 / 1.84 | 1.30 / 2.16 | 1.53 / 4.00 |
| Pooled chessboards | Linear, position + pupil | 1.08 / 1.75 | 1.50 / 2.38 | 1.64 / 3.96 |
| In-situ (20%) | Median offset | 0.76 / 1.61 | 0.83 / 1.63 | 1.43 / 4.29 |
| In-situ (20%) | Linear, position | 0.87 / 1.77 | 0.89 / 1.78 | 1.40 / 4.45 |
| In-situ (20%) | Linear, position + pupil | 0.87 / 1.81 | 0.89 / 1.78 | 1.38 / 4.39 |
| In-situ (20%) | Linear, position + velocity | 0.85 / 1.76 | 0.86 / 1.66 | 1.35 / 3.58 |

## Interpretation changes

- Sparse in-situ offsets still outperform pooled chessboard offsets on mean held-out median error for all three participants. This compares the available calibration sources; it does not establish a unique causal explanation for their difference.
- P6’s in-situ median is now **1.43°**, versus **1.51°** for pooled chessboard calibration. His P90 remains worse under the in-situ offset (**4.29° vs 3.97°**); a median benefit is not a benefit across the entire error distribution.
- P6’s position-plus-velocity model improves median error to **1.35°** and P90 to **3.58°**, improving both metrics in **4/5 folds**, rather than the historical 5/5 claim. The median offset is therefore not the best median-error model for every participant. P1/P2 retain the strongest median performance with the simple offset among the reported linear variants.
- Chessboard position/pupil models increase P6’s mean median error, but position alone improves it in two of five driving folds. Do not retain the old claim that every fold worsens for both P1 and P6.
- About five random driving references match or beat the pooled chessboard offset for all three participants on average (P6: k=5 gives approximately 1.50°, versus 1.51°). One random reference already beats the chessboard offset for P2. Exact geometric-versus-random comparisons must match available test folds; some geometric layouts are unavailable in some folds. Do not reuse the old unqualified 0.05° bound.
- Recording/day transfer retains the independently checked values in [the fair-transfer report](06_fair_recording_transfer.md): recording medians P1/P2/P6 **0.84° / 0.89° / 1.43°**; real-day medians P1/P2 **1.17° / 0.91°**. P1 includes factory recalibration; P6 has one actual day.

## Scene-level statistical checks

Tests use each held-out scene’s median error, averaged over applicable test folds/calibration models, with the existing Holm correction per participant and research question. These scene-level statistics differ from the recording-weighted sample-quantile scores in the main table.

| Participant | In-situ pooled vs pooled chessboard: mean scene-error difference | Holm p | Scenes |
|---|---:|---:|---:|
| william | -0.068° | 0.00278 | 79 |
| katharina | -0.576° | 9.91e-11 | 73 |
| stefan | -0.199° | 7.78e-07 | 114 |

All three corrected scene-level comparisons favour the in-situ offset. No participant-independent population inference is claimed.

## Inputs and reproducibility

`evals/data/06_current_driving/offset/` contains the current inputs and runs:

- `units/`: freshly extracted chessboard and driving units, outside the dataset.
- `runs/driving/` and `runs/transfer/`: existing updated canonical runs copied read-only, including both P6 recordings; original source/code hashes are retained.
- `analysis/`: the updated category comparison and statistical analysis copied with the canonical runs.
- `runs/transfer_regression/`: fresh median/linear/ridge source comparison, using the existing spec.
- `runs/linear_runtime/`, `runs/ridge_20/`, `runs/ridge_80/`: fresh runtime-model evaluations.
- Source and code hashes were checked against the current files for all runs: 255 distinct input files matched; see `data/06_current_driving/verification.json`.
- Every run retains `protocol.json`, fitted-model scores, split IDs, selections, scene errors and summaries. Detailed CSVs are gzip-compressed. Exact specs are in `evals/data/06_current_driving/specs/`.

New model runs use the existing `scripts/offset_benchmark/run_benchmark.py` with `--units-dir` and `--output-dir` pointing inside this paper repository. Source data and Horuspy are mounted read-only. To reproduce, build units with the existing `build_units.py --participants william katharina stefan --output-dir .../units`, then run each saved spec into its named run directory. Gzip `splits.csv`, `selections.csv`, and `unit_errors.csv` before figure regeneration, matching the saved artifact convention.

Regenerate the current figure, table and flat CSV exports with:

```bash
python scripts/make_section6.py
```

The generator defaults to the current run directory. Its optional arguments can select the dataset, transfer run, offset root and runtime run explicitly. It asserts identical test scene sets for chessboard/in-situ models and zero driving train/test overlap.

The flat `evals/data/06_*.csv` files are the current manuscript exports. The expanded raw scene and participant summaries are `04_scene_raw_errors.csv` and `04_driver_raw_summary.csv`. Supporting dataset totals are unchanged: 266 scenes, 18 recordings, 76,645 samples, four dates.
