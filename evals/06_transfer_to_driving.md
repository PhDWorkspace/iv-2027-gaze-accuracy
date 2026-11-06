# Section VI data basis: transfer to driving

**Extracted:** 2026-11-05 (Claude Code, for William Engel). **State:** after the Nov 5 wearer relabel (see
[05_controlled.md](05_controlled.md) §2). **Purpose:** every number behind Section VI
([sections/06_transfer.tex](../sections/06_transfer.tex)), plus results not shown in the paper.

## 0. How to regenerate

```bash
# horuspy-dev image, data read-only; horuspy working tree with spec transfer_regression.json
python scripts/offset_benchmark/run_benchmark.py /home/william/data \
       scripts/offset_benchmark/specs/transfer_regression.json --output-dir <scratch>/transfer_regression
# then copy to evals/data/06_transfer_regression_run/ (large tables gzipped) and run, from the paper repo:
python scripts/make_section6.py /home/william/data evals/data/06_transfer_regression_run
```

[scripts/make_section6.py](../scripts/make_section6.py) writes:
- `figures/fig6_transfer.pdf` (Fig. 4: offset source; number of in-situ references)
- `figures/tab_transfer_models.tex` (Table IV)
- `evals/data/06_*.csv` (§7)

It asserts that chessboard- and driving-trained models were scored on identical held-out scenes, and that no
driving calibration scene is also a test scene. Both checks pass.

## A. Data and evaluation protocol

| Source | Generated | Content |
|---|---|---|
| `gaze_accuracy/offset/analysis/category_summary.csv`, `tests.csv` | 2026-11-05 16:41 (after relabel) | fold-matched raw / chessboard / driving comparison, scene-level tests |
| `gaze_accuracy/offset/runs/driving/` | 2026-11-05 12:07 | in-situ offsets from k scenes (random, single, geometric, all 20%) |
| `gaze_accuracy/offset/runs/transfer/` | 2026-11-05 16:41 | chessboard offsets (single board, full board, pooled) → driving |
| `gaze_accuracy/offset/runs/ridge_20`, `ridge_80/` | 2026-11-05 12:48 | driving-trained ridge with runtime features (velocity, 1/distance) |
| `evals/data/06_transfer_regression_run/` | **new, 2026-11-05 17:51** | horuspy spec `transfer_regression.json`: median, linear and ridge (position; position + pupil), trained on chessboard or on driving, scored on the same scenes |

- **Relabel effect:** the driving, ridge_20 and ridge_80 runs read only driving units, which the relabel did not
  change. The transfer run and the analysis were rerun after it. Only P6's chessboard-based rows changed:
  for example, the chessboard pooled offset for P6 is now 1.60°.
- **New run, written outside the dataset** (`--output-dir`) so nothing in `gaze_accuracy/` was overwritten.
  Code: the horuspy working tree as of 2026-11-05, including the **uncommitted** changes to
  `src/evaluation/offset_data.py` (pupil for driving samples) and the untracked spec. The code hashes are in
  `protocol.json`; the spec is copied as `spec_transfer_regression.json`.

### Participants and data

| Code | Name | Driving recordings | Valid scenes | Drive dates | Chessboard recordings used (complete boards) |
|---|---|---|---|---|---|
| P1 | William | 10 | 79 | 2026-07-15 (9 rec.), 2026-10-15 (1 rec., 29 scenes) | 125 |
| P2 | Katharina Winter | 6 | 73 | 2026-10-14, 2026-10-15 | 23 |
| P6 | Stefan Englmeier | 1 | 93 | 2026-11-04 | 25 |

### Protocol

**Driving folds.** Scenes are split into 5 blocks with seed 42. Each fold calibrates on one block (≈ 20%: P1
15–16, P2 14–15, P6 18–19 scenes) and tests on the other four. Each scene is therefore a test scene in four folds.
The `driving`, `ridge_20` and `transfer_regression` runs use **identical test scenes** (checked).

**Chessboard → driving.**
- Chessboard recordings are split into 5 folds; each model is fitted on 4/5 of the recordings (e.g. P2 18–19
  of 23).
- The central 60% of each fixation is used (`keep_fraction` 0.6).
- Each model is scored on the same driving test blocks as above: 5 chessboard folds × 5 driving folds = 25 splits,
  averaged.
- `category_summary.csv` additionally matches folds before averaging.

**Selections in the driving run.**

| Code | Selection | Definition |
|---|---|---|
| E0 | raw | no correction |
| E1 | single scene | each calibration scene alone |
| E2 | random k | k ∈ {1, 2, 3, 4, 5, 8}, 20 draws per fold |
| E3 | geometric layouts | line 2/3, triangle, rectangle, rectangle + centre, rectangle + edge midpoints |
| E5 | all | all calibration scenes |

**Models.**
- `median` is the componentwise median offset.
- `linear` uses least squares; `ridge` uses α = 100.
- Features: `gaze` (position), `pupil` (mm), `velocity` (signed gaze velocity over the preceding 100 ms) and
  `inverse_distance` (annotated scene distance).

**Metrics.**
- Per test scene: the median angular error of its samples. A model's median and P90 are taken over its test
  scenes.
- Averaging: draws are averaged within a fold, then folds are averaged equally.
- Tests: paired Wilcoxon signed-rank over held-out scenes (each scene's error averaged over its test folds), with
  Holm correction per participant and RQ. CIs are 95% bootstrap (2 000 resamples, seed 42).

## B. Raw and baseline results

| Code | Raw median | Raw P90 | Scene offset az / el (median over scenes) |
|---|---|---|---|
| P1 | 3.96 | 4.63 | −0.49 / −3.77 |
| P2 | 1.48 | 2.20 | −1.09 / −0.59 |
| P6 | 6.00 | 7.80 | +0.85 / −6.09 |

**Per recording** (median over scenes of raw error, and of the error after the driving 20% median offset;
offsets in °):

| Code | Recording | Scenes | Raw | Corrected | az | el |
|---|---|---|---|---|---|---|
| P1 | free_driving_William_2026-07-15-15-45-25 | 2 | 4.09 | 0.48 | −0.28 | −4.08 |
| P1 | …-15-47-32 | 6 | 4.17 | 0.84 | −0.03 | −4.10 |
| P1 | …-15-51-34 | 11 | 4.29 | 0.99 | −0.48 | −4.28 |
| P1 | …-15-55-26 | 7 | 4.07 | 0.58 | −0.64 | −3.97 |
| P1 | …-16-04-04 | 2 | 4.12 | 0.85 | −1.26 | −3.89 |
| P1 | …-16-07-13 | 5 | 4.34 | 0.70 | −0.29 | −4.33 |
| P1 | …-16-13-59 | 5 | 3.94 | 0.50 | −0.55 | −3.91 |
| P1 | …-16-44-04 | 9 | 3.81 | 0.53 | −0.70 | −3.74 |
| P1 | …-16-50-04 | 3 | 2.65 | 1.22 | +0.06 | −2.64 |
| P1 | free-driving_William-Engel_2026-10-15-14-51-10 | 29 | 3.10 | 0.98 | −0.56 | −3.01 |
| P2 | free-driving_Katharina-Winter_2026-10-14-12-40-18 | 4 | 1.64 | 1.01 | −0.91 | −1.24 |
| P2 | …-10-14-16-08-24 | 1 | 1.23 | 0.82 | −0.79 | −0.79 |
| P2 | …-10-14-16-44-30 | 1 | 1.76 | 0.78 | −1.24 | −1.27 |
| P2 | …-10-15-10-04-48 | 28 | 1.41 | 0.75 | −1.15 | −0.69 |
| P2 | …-10-15-10-13-43 | 25 | 1.35 | 0.77 | −1.21 | −0.31 |
| P2 | …-10-15-10-29-25 | 14 | 1.20 | 0.76 | −0.80 | −0.33 |
| P6 | free_driving_Stefan-Englmeier_2026-11-04-13-01-29 | 93 | 6.21 | 1.32 | +0.85 | −6.09 |

P1's July and October drives have different vertical offsets (≈ −4.0° vs −3.0°). The pooled in-situ offset
therefore mixes two days (see F).

## C. Controlled-to-driving transfer

All values are means over 25 splits, on the same held-out scenes (`06_model_comparison_summary.csv`).

| Trained on chessboard | Features | P1 med / P90 | P2 med / P90 | P6 med / P90 |
|---|---|---|---|---|
| raw (reference) | – | 3.96 / 4.63 | 1.48 / 2.20 | 6.00 / 7.80 |
| median offset (E5 pooled) | constant | 0.88 / 1.62 | 1.40 / 2.19 | 1.60 / 3.92 |
| linear | position | 1.17 / 1.84 | 1.30 / 2.16 | 1.66 / 4.03 |
| ridge | position | 1.17 / 1.84 | 1.30 / 2.16 | 1.66 / 4.03 |
| linear | position + pupil | 1.08 / 1.75 | 1.49 / 2.38 | 1.78 / 3.98 |
| ridge | position + pupil | 1.08 / 1.75 | 1.49 / 2.38 | 1.78 / 3.98 |

Δ vs the chessboard median offset (per driving fold, averaged over chessboard folds; `06_model_vs_median_per_fold.csv`):

| Code | Model | Δ median [min, max], folds better | Δ P90 [min, max], folds better |
|---|---|---|---|
| P1 | position | +0.29 [+0.26, +0.31], 0/5 | +0.22 [+0.19, +0.25], 0/5 |
| P1 | position + pupil | +0.20 [+0.16, +0.21], 0/5 | +0.13 [+0.11, +0.14], 0/5 |
| P2 | position | −0.09 [−0.13, +0.01], 4/5 | −0.02 [−0.04, +0.01], 4/5 |
| P2 | position + pupil | +0.10 [+0.06, +0.20], 0/5 | +0.19 [+0.18, +0.24], 0/5 |
| P6 | position | +0.06 [+0.05, +0.07], 0/5 | +0.11 [+0.07, +0.14], 0/5 |
| P6 | position + pupil | +0.18 [+0.17, +0.19], 0/5 | +0.07 [+0.00, +0.11], 0/5 |

Ridge differs from linear by ≤ 0.01°, because there is a lot of chessboard data and α = 100 hardly shrinks.

**Other chessboard offsets** (`category_summary.csv`, median / P90):
- Single point (E1): P1 1.51 / 2.39, P2 1.85 / 2.73, P6 2.78 / 5.07.
- Full board, 15 points (E4): P1 1.11 / 1.96, P2 1.74 / 2.59, P6 1.97 / 4.30.

**Scene-level tests** (RQ3; Δ = a − b, mean [95% CI], Holm p):

| Code | Chessboard pooled vs raw | Driving pooled vs chessboard pooled | Driving pooled vs chessboard full board |
|---|---|---|---|
| P1 | −2.58 [−2.83, −2.30], 1.9e-13 | **−0.068 [−0.111, −0.024], .0028** | −0.29 [−0.34, −0.24], 1.7e-12 |
| P2 | +0.04 [−0.03, +0.11], .31 | **−0.58 [−0.68, −0.47], 9.9e-11** | −0.91 [−1.01, −0.81], 1.2e-12 |
| P6 | −4.61 [−4.72, −4.48], 2.2e-16 | **−0.24 [−0.32, −0.16], 9.1e-07** | −0.61 [−0.69, −0.54], 2.9e-15 |

**Compared with Section V:** on held-out chessboard recordings, the position term helped P2 (−0.17°) and P6;
P6's corrected Section V value is −0.14°. In driving it helps P2 only partly (−0.09°) and hurts P6 (+0.06°).

## D. Sparse in-situ calibration

Median / P90 (°), from `category_summary.csv`; random k is averaged over 20 draws per fold.

| Selection | P1 | P2 | P6 |
|---|---|---|---|
| single scene (each, E1) | 1.17 / 2.07 | 1.03 / 1.88 | 1.91 / 4.63 |
| random 1 | 1.06 / 1.98 | 0.98 / 1.85 | 1.76 / 4.50 |
| random 2 | 1.04 / 1.85 | 0.93 / 1.76 | 1.74 / 4.54 |
| random 3 | 0.95 / 1.83 | 0.89 / 1.73 | 1.59 / 4.41 |
| random 4 | 0.87 / 1.71 | 0.87 / 1.71 | 1.53 / 4.34 |
| random 5 | 0.86 / 1.71 | 0.87 / 1.69 | 1.54 / 4.40 |
| random 8 | 0.83 / 1.65 | 0.84 / 1.66 | 1.45 / 4.39 |
| line 2 | 1.04 / 1.87 | 0.93 / 1.76 | 1.68 / 4.44 |
| line 3 | 0.97 / 1.85 | 0.92 / 1.75 | 1.59 / 4.36 |
| triangle 3 | 0.93 / 1.81 | 0.89 / 1.75 | 1.56 / 4.38 |
| rectangle 4 | 0.86 / 1.67 | 0.86 / 1.70 | 1.48 / 4.32 |
| rectangle + centre 5 | 0.95 / 1.79 | 0.90 / 1.71 | 1.48 / 4.31 |
| rectangle + edge midpoints 8 | 0.69 / 1.63 | 0.83 / 1.72 | 1.47 / 3.94 |
| **all 20% (E5)** | **0.76 / 1.61** | **0.83 / 1.63** | **1.41 / 4.36** |
| chessboard pooled (for comparison) | 0.88 / 1.62 | 1.40 / 2.19 | 1.60 / 3.92 |

- **Fold-to-fold range of the median error** (min–max over 5 folds; `06_reference_count_per_fold.csv`):

  | Selection | P1 | P2 | P6 |
  |---|---|---|---|
  | random 1 | 1.02–1.12 | 0.93–1.03 | 1.63–2.10 |
  | random 2 | 0.92–1.09 | 0.87–0.96 | 1.55–2.33 |
  | random 4 | 0.80–0.95 | 0.81–0.96 | 1.51–1.57 |
  | random 8 | 0.74–0.95 | 0.78–0.92 | 1.43–1.48 |
  | all 20% | 0.70–0.89 | 0.78–0.94 | 1.38–1.45 |

- **Reduction from raw to 20%:** P1 81%, P2 44%, P6 77%.
- **Smallest random k that matches or beats the chessboard offset:** P2 k = 1; P1 k = 4 (0.87 vs 0.88);
  P6 k = 4 (1.53 vs 1.60; k = 3 gives 1.59).
- **Geometric vs random** (RQ2, held-out scene level): |Δ| ≤ 0.05° for all k and drivers. Several differences
  are Holm-significant, but they are tiny and point both ways.
  - Calibration-scene level (RQ1): P6 geometric is worse at k = 1, 2 and 8 (+0.45, +0.67, +0.15°; Holm < .01).
  - "Rectangle + edge midpoints" exists in only a few folds (11 score rows across all drivers, vs 300 for lines/triangles), so its 0.69° for P1 is
    not reliable.
- **P90:** in-situ offsets do not reduce P6's tail. Its 20% P90 is 4.36° vs 3.92° for the chessboard offset,
  which reflects scene-to-scene variability rather than the offset.

## E. Driving-trained models

**Same scenes, 20% calibration** (`06_model_comparison_summary.csv` and `06_driving_ridge_runtime_features.csv`;
median / P90):

| Model | Features | P1 | P2 | P6 |
|---|---|---|---|---|
| median offset | constant | **0.76** / 1.61 | **0.83** / 1.63 | 1.41 / 4.36 |
| linear | position | 0.87 / 1.77 | 0.89 / 1.78 | 1.46 / 3.54 |
| ridge | position | 0.85 / 1.73 | 0.86 / 1.73 | 1.42 / 3.49 |
| linear | position + pupil | 0.87 / 1.81 | 0.89 / 1.78 | 1.49 / 3.45 |
| ridge | position + pupil | 0.84 / 1.77 | 0.86 / 1.72 | 1.44 / 3.40 |
| ridge | position + velocity (`runtime`) | 0.83 / 1.72 | 0.84 / 1.63 | **1.36** / **2.98** |
| ridge | position + velocity + 1/distance | 0.87 / 1.83 | 0.88 / 1.67 | 1.38 / 2.92 |

Δ vs driving median offset (per fold; mean [min, max], folds better / 5):

| Code | Model | Δ median | Δ P90 |
|---|---|---|---|
| P1 | ridge position | +0.09 [−0.08, +0.43] 2/5 | +0.12 [−0.14, +0.66] 2/5 |
| P1 | ridge pos + pupil | +0.08 [−0.05, +0.40] 2/5 | +0.17 [−0.15, +0.70] 1/5 |
| P1 | ridge pos + velocity | +0.07 [−0.08, +0.29] 2/5 | +0.11 [−0.12, +0.52] 2/5 |
| P2 | ridge position | +0.03 [−0.14, +0.34] 3/5 | +0.10 [−0.10, +0.29] 2/5 |
| P2 | ridge pos + pupil | +0.03 [−0.14, +0.32] 3/5 | +0.10 [−0.10, +0.29] 1/5 |
| P2 | ridge pos + velocity | +0.01 [−0.17, +0.34] 3/5 | −0.00 [−0.20, +0.24] 3/5 |
| P6 | ridge position | +0.01 [−0.11, +0.13] 2/5 | **−0.86 [−1.15, −0.62] 5/5** |
| P6 | ridge pos + pupil | +0.04 [−0.09, +0.10] 2/5 | **−0.95 [−1.26, −0.74] 5/5** |
| P6 | ridge pos + velocity | −0.05 [−0.14, +0.05] 4/5 | **−1.38 [−1.64, −1.19] 5/5** |
| P6 | ridge pos + vel + 1/dist | −0.03 [−0.15, +0.10] 3/5 | **−1.44 [−1.77, −1.21] 5/5** |

Linear variants are listed in `06_model_vs_median_per_fold.csv`; they are slightly worse than ridge for P1 and P2.

**80% calibration** (`ridge_80`; median / P90):

| Model | P1 | P2 | P6 |
|---|---|---|---|
| median offset | 0.79 / 1.61 | 0.78 / 1.71 | 1.41 / 4.49 |
| ridge position | 0.74 / 1.61 | 0.79 / 1.67 | 1.39 / 3.35 |
| ridge pos + velocity | 0.75 / 1.63 | 0.78 / 1.54 | 1.35 / 2.85 |
| ridge pos + vel + 1/dist | 0.76 / 1.48 | 0.74 / 1.57 | 1.37 / 2.75 |

With 80% calibration, P2's tail also improves with velocity (P90 −0.16°, 5/5 folds). P1's medians improve by
−0.03 to −0.05° but only in 2–3/5 folds. The median offset itself barely improves from 20% to 80%.

## F. Interpretation and limitations

**Supported:**
1. Chessboard offsets remove most of the systematic error for P1 and P6, but not for P2.
2. Chessboard-trained position and pupil terms do not improve driving (0/5 folds for P1 and P6), even where they
   improved held-out chessboards.
3. A 20% in-situ offset is significantly better than the chessboard offset for all three drivers.
4. About 4 random scenes match the chessboard offset, and geometry adds ≤ 0.05°.
5. Driving-trained regressions give no consistent median gain. For P6 they consistently reduce P90 (velocity:
   −1.38°, 5/5 folds); for P1 and P2 they do not at 20%.

**Limitations:**
- **Uncertainty:** 5 folds; scene-level Wilcoxon tests treat scenes as independent although scenes from one drive
  are related. Differences below about 0.05° should not be interpreted.
- **Within-drive splits:** scenes are held out within the recorded drives, not new drives, days or wearers.
  P6 has a single drive. P1 pools two days with different offsets.
- **Three drivers only;** P6's driving data come from one 2026-11-04 recording, relabelled Sarah → Stefan on
  2026-11-04 (provenance `stefan_owner_confirmed_2026-11-04.json`).
- **Old Section VI content is no longer used:** the "extended correction" (temporal filters and spatial bias term
  selected per wearer, `offset/gaze_correction/`, P1/P2 only) and the quality-gating results. They were not
  regenerated after the relabel (they don't involve P6's chessboard data). Methods III-D still describes the
  extended correction, and Introduction C3 and the Conclusion (RQ3) still promise quality-aware acquisition;
  Section VI no longer covers either.
- **Section IV overlap:** Table I still reports in-situ budgets for P1 and P2 only. Section VI now repeats this
  for three drivers.
- **Uncommitted code:** the new run depends on uncommitted horuspy code (`offset_data.py` pupil change and the
  untracked spec). Commit those so the run is reproducible from horuspy alone.

## 7. Files in `evals/data/` (Section VI)

| File | Content | Key columns |
|---|---|---|
| `06_driving_offset_by_category.csv` | `category_summary.csv` for P1/P2/P6 | category, median_error_deg, p90_error_deg, matched_* improvements |
| `06_reference_count_per_fold.csv` | per fold: raw, single scene, random k (mean of 20 draws), geometric layouts, all 20% | code, selection, pattern, k, fold, median_error_deg, p90_error_deg, n_train_units |
| `06_model_comparison_summary.csv` | `transfer_regression` summary (both protocols) | code, source, model, median_error_deg, p90_error_deg, mean_error_deg, n_splits |
| `06_model_vs_median_per_fold.csv` | Δ of every model vs its median offset | code, protocol, model, metric, mean/min/max_vs_median, folds_better |
| `06_driving_ridge_runtime_features.csv` | ridge_20 and ridge_80 summaries | calibration_share, model (position / runtime / runtime_distance) |
| `06_driving_scene_tests.csv` | all analysis tests (RQ1–RQ5) for P1/P2/P6 | rq, comparison, mean_difference_deg, CI, p, p_holm |
| `06_transfer_regression_run/` | full run output: `summary.csv`, `scores.csv`, `protocol.json`, spec, gzipped `splits`, `selections`, `unit_errors` (per scene) | see horuspy `docs/offset_benchmark.md` |

RQ4/RQ5 scene-condition tests (ego motion, relative motion, target side, gaze speed/eccentricity) are in
`06_driving_scene_tests.csv`.
- **Holm < .05:** P1 relative motion (.030) and target side (.017) for raw error (RQ4b); P6 relative motion (.015)
  and gaze eccentricity (.0017) for the corrected residual (RQ5).
- These are not used in Section VI.

## Update 2026-11-06: linear models in the paper

The paper now reports **linear** models only. Ridge results remain in §E above and in
`06_driving_ridge_runtime_features.csv`.

- **Table II driving rows:**
  - "linear, position" and "linear, pos. + pupil" come from `06_transfer_regression_run`
    (`driving_to_driving`, `linear_position`, `linear_position_pupil`).
  - "linear, pos. + velocity" comes from `06_linear_runtime_run/share_20` (same spec as `ridge_20`, with linear models;
    model `runtime` = gaze position + signed gaze velocity over the preceding 100 ms).
  - The 80% share is in `06_linear_runtime_run/share_80`.
- **Same held-out scenes:** the `driving`, `ridge_20` and linear-runtime runs use identical test scenes.
- **Linear, 20% calibration** (median / P90):

  | Model | P1 | P2 | P6 |
  |---|---|---|---|
  | position | 0.87 / 1.77 | 0.89 / 1.78 | 1.46 / 3.54 |
  | pos. + pupil | 0.87 / 1.81 | 0.89 / 1.78 | 1.49 / 3.45 |
  | pos. + velocity | 0.85 / 1.76 | 0.86 / 1.66 | 1.37 / 3.02 |
  | pos. + velocity + 1/distance | 0.90 / 1.93 | 0.89 / 1.74 | 1.40 / 2.97 |

- **P6 P90 vs the median offset (4.36°):** position −0.81° and velocity −1.33°, 5/5 folds each.
- **Text:** VI-C now reads 3.54° and 3.02° (formerly the ridge values 3.49° and 2.98°).
