# Fair recording and day transfer from the available driving measurements

Evaluated 2026-11-06. **An offset from one recording improves the other recordings for all three participants. Day transfer also helps for Katharina and William, but William's comparison includes a factory recalibration.** These measurements support reusing the correction as a useful starting point; they do not establish that the offset stays unchanged or guarantees a particular accuracy on a future day.

## Data and differences from the previous evaluation

The current measurements contain **266 eligible fixation scenes in 18 recordings**, shared by three driving participants:

| Participant | Actual days | Recordings | Fixations | Recordings eligible as calibration sources (≥5 fixations) |
|---|---|---:|---:|---:|
| William / P1 | July 15 and October 15, 2026 | 9 + 1 | 50 + 29 = 79 | 6 + 1 |
| Katharina / P2 | October 14 and 15, 2026 | 3 + 3 | 6 + 67 = 73 | 0 + 3 |
| Stefan / P6 | November 4, 2026 | 2 | 93 + 21 = 114 | 2 |

Stefan's second recording is `f39babb4-62fb-4c7c-9881-a5587627f3fa`, starting at 13:42:09, with 21 eligible fixations. It has both an existing gaze table and verified scene metadata. The previous report used only his first 93-fixation recording and manufactured six segments; **this evaluation uses his two actual recordings**. Recordings without the necessary existing measurements/verified scenes are outside this evaluation. Nothing in the dataset was generated or changed.

**Author-review discrepancy:** the fixed dataset-rules document and earlier transfer outputs describe Stefan's older, one-recording subset. His current two-recording results and expanded 20% baseline below are separate results. Historical frozen values and original transfer CSVs are retained. The manuscript, figure and main model table now also use the expanded 266-scene dataset; see [the current Section VI evaluation](06_transfer_to_driving.md). William's and Katharina's existing real-day results are reproduced here.

## Common protocol and weighting

- Fit the existing `MedianOffset`: compute a median gaze-minus-target offset within each calibration fixation, then take the componentwise median across those fixation offsets. Every calibration fixation counts once; fixation duration does not increase its influence. This retains the existing estimator. When pooling a day, recordings with more fixations contribute more calibration references; equal recording weighting applies to **evaluation**, not to this fit.
- **Recording transfer:** fit one complete recording and test all other measured recordings of that participant. Use the same direction of transfer for all three people. The primary analysis requires **at least five eligible fixations in the source recording**. This is an analyst-chosen count rule, set before viewing the transfer scores, not a proven sufficient calibration size. All recordings, including those with one or two fixations, remain eligible test targets. Sources with fewer than five fixations are excluded, rather than being declared successful calibrations.
- **Day transfer:** pool all fixations from one actual day and test the other day, then reverse the direction. A pooled day is eligible when it has at least five fixations in total. Consequently, Katharina's 4 + 1 + 1 references can calibrate jointly, although none of those three recordings calibrates alone in the primary recording test. William's day pool likewise includes the shorter recordings.
- **Evaluation weights:** each held-out recording has equal total weight; each fixation within that recording has equal weight; samples within a fixation share its weight equally. For a sample in fixation `f` of recording `r`, `w = 1 / (number of test recordings × fixations in r × samples in f)`. Thus long fixations and long recordings do not dominate. Equal fixation weight is conditional on its recording: equal global fixation weight and equal recording weight cannot both hold when recording sizes differ.
- Errors are spherical angular errors from the existing gaze/target directions. The reported median and P90 are weighted quantiles of the held-out sample-error distribution, **not** medians of fixation medians. Raw and corrected scores always use exactly the same test samples and weights.
- A table row is the **equal mean of split scores**. Each eligible source recording counts once. We do not pool participant scores or claim equal calibration budgets between people. Recording/scene/sample weights apply within each split; averaging splits is a separate step, with overlapping test recordings.
- Calibration and test fixation IDs are disjoint. For recording/day transfer, recording UUIDs are disjoint as well. No artificial days or recording segments are used.

## One recording → the other recordings

Mean held-out median angular error over eligible source recordings. William's all-recording row includes both same-day and cross-recalibration targets; the same-day restriction is given separately below.

| Participant | Source recordings / splits | Source fixations (range) | Raw median | Corrected median (split range) | Raw → corrected P90 | Improved splits |
|---|---:|---:|---:|---:|---:|---:|
| William | 7 | 5–29 | 3.96° | **0.84°** (0.74–1.12°) | 4.62° → 1.82° | 7/7 |
| Katharina | 3 | 14–28 | 1.52° | **0.89°** (0.77–0.95°) | 2.21° → 1.64° | 3/3 |
| Stefan | 2 | 21–93 | 5.98° | **1.43°** (1.43–1.44°) | 7.94° → 4.20° | 2/2 |

Each source was also scored on every target recording separately: **63/63 William, 15/15 Katharina, and 2/2 Stefan source–target pairs improve their median error**. The pairs reuse sources and targets, so these are descriptive checks, not 80 independent replications.

The large pooled improvement does not mean every target reaches the pooled median. William's individual target medians reach **1.80°**, particularly the final July recording with three fixations; Katharina's reach **1.14°**. Stefan retains a substantial error tail around **4.2° P90**.

### Same-day recording transfer

Restrict test recordings to the source recording's actual day, retaining the five-fixation source rule.

| Participant | Actual day | Splits | Raw → corrected median |
|---|---|---:|---:|
| William | July 15 | 6 | 4.01° → **0.74°** |
| Katharina | October 15 | 3 | 1.34° → **0.85°** |
| Stefan | November 4 | 2 | 5.98° → **1.43°** |

William has only one measured October recording, so October cannot supply a same-day recording-transfer test. Katharina's October 14 recordings are test targets in the all-recording analysis, but none meets the source-count rule individually.

### Strictly earlier recording → next available measured recording

The main recording table uses both forward and backward transfers. To directly check reuse in the next recording, select only pairs in which the target is the participant's immediately next **measured, eligible test recording**, ordered by native `info.json.start_time`. An intervening sparse recording still counts as the next target; it is not skipped. Unprocessed recordings are not covered by this claim.

| Participant | Forward next-recording pairs | Raw → corrected median (mean over pairs) | Corrected range |
|---|---:|---:|---:|
| William | 6 | 3.81° → **0.78°** | 0.50–1.37° |
| Katharina | 2 | 1.30° → **0.86°** | 0.85–0.87° |
| Stefan | 1 | 5.96° → **1.44°** | 1.44° |

All nine forward pairs improve. William's six pairs are within July; Katharina's two are within October 15. Stefan's real forward test is **13:01 recording (93 calibration fixations) → 13:42 recording (21 test fixations): 5.96° → 1.44°, P90 8.08° → 4.23°**. His reverse test gives 6.00° → 1.43°.

## Actual day → actual day, both directions

All fixations of the source day calibrate; all fixations of the other day test. Test recordings remain equally weighted even when one has only a single fixation.

| Participant | Calibration → test day | Calibration fixations / recordings | Test fixations / recordings | Raw → corrected median | Corrected P90 |
|---|---|---:|---:|---:|---:|
| Katharina | Oct 14 → Oct 15 | 6 / 3 | 67 / 3 | 1.34° → **0.96°** | 2.10° |
| Katharina | Oct 15 → Oct 14 | 67 / 3 | 6 / 3 | 1.63° → **0.87°** | 1.51° |
| **Katharina mean** | 2 directions | | | **1.49° → 0.91°** | **1.80°** |
| William | July 15 → Oct 15 | 50 / 9 | 29 / 1 | 3.12° → **1.22°** | 2.42° |
| William | Oct 15 → July 15 | 29 / 1 | 50 / 9 | 4.02° → **1.12°** | 1.80° |
| **William mean** | 2 directions | | | **3.57° → 1.17°** | **2.11°** |

**Katharina:** this is evidence of real day transfer under the existing applied module calibration. Both directions improve, including the forward Oct 14 → Oct 15 direction. However, Oct 14 contributes only six references, and two recordings have only one fixation each. Those short recordings still receive full recording weight. The two fitted day offsets differ in elevation by **0.60°** (−1.09° vs −0.49°), so an unchanged person-specific offset is not established.

**William — factory recalibration between days:** the factory recalibration is owner-reported in the request. The current stored effective-calibration files identify July as `corrected` and October as `module_specific`, both for physical module `272097`. The analysis uses the already processed gaze directions with their existing calibration; it does not reapply a model or regenerate gaze tables. Applying the replacement scene model does not establish that the remaining gaze offset is identical across the factory recalibration. His fitted elevation offset changes by **0.96°** (−3.97° vs −3.01°). The old offset remains useful in both directions, but this comparison combines **time/day, recording conditions, and device recalibration**. Their separate effects cannot be identified from these two days.

**Stefan:** there is only one actual day. The two recordings establish recording transfer on that day; they provide no cross-day evidence.

## Existing 20% fixation pooling as context

The existing five-fold protocol is reused: seed 42, sorted fixation IDs, one shuffled block (~20%) for calibration and the other four for testing. For William and Katharina it reproduces the existing baseline. Stefan's baseline is recomputed on **both actual recordings (114 fixations)** so its coverage matches this report.

| Participant | Calibration fixations per fold | Raw → corrected median | Corrected P90 |
|---|---:|---:|---:|
| William | 15–16 | 3.96° → **0.76°** | 1.61° |
| Katharina | 14–15 | 1.48° → **0.83°** | 1.63° |
| Stefan, both recordings | 22–23 | 5.97° → **1.43°** | 4.29° |

Random fixation pooling can see calibration references from the same recording as its test fixations. It answers a different question from applying an offset to an unseen recording/day. Its test sets and calibration budgets differ from the transfer tests; differences between these table means are **descriptive, not paired estimates of a transfer penalty**. Stefan's older **1.41°** baseline refers to his first recording only and remains unchanged in the earlier files.

## Sensitivity to the calibration-source minimum

The main all-recording transfer analysis repeated with the same count threshold for everyone:

| Minimum source fixations | William: splits / corrected median | Katharina: splits / corrected median | Stefan: splits / corrected median |
|---|---:|---:|---:|
| 3 | 8 / 0.93° | 4 / 0.87° | 2 / 1.43° |
| **5 (primary)** | **7 / 0.84°** | **3 / 0.89°** | **2 / 1.43°** |
| 8 | 3 / 0.89° | 3 / 0.89° | 2 / 1.43° |

Every source split improves at all three thresholds. William's three-fixation source produces **1.55°** corrected median when included, illustrating the risk of a small or atypical source. This does not prove a sharp cutoff at five, or that more fixations always improve transfer: their target coverage matters and these thresholds select different recordings/test sets.

## What the evidence supports

- **Reuse across recordings: supported for these three participants.** The correction helps on all primary held-out recording pairs, including every available forward next-recording pair with an eligible source. Typical residual median error is about 0.8–0.9° for William/Katharina and 1.4° for Stefan. It is a useful default, with measurable remaining error and variation between targets.
- **Reuse across days: preliminary support for Katharina.** Both directions help, including calibration from only six pooled day-one references. This is one person over one day transition, not evidence that a personal correction is stable indefinitely.
- **William across days/recalibration: useful, with a changed residual offset.** Both directions help substantially, at roughly 1.1–1.2° residual median. A claim of pure day stability or invariance to factory recalibration would overstate the evidence.
- **Stefan across days: untested.** His second recording strengthens the same-day recording evidence only.

For deployment, carrying the offset into a subsequent recording is reasonable on these measurements. If the application needs sub-degree error in each recording, the results do **not** establish that requirement: individual recordings exceed 1°, Stefan's median is about 1.4°, and his tail remains around 4.2°. Checking a few new references on a new day or after recalibration remains useful. There are only three people, two observed day transitions (one confounded), and overlapping evaluation splits; no general population guarantee or significance claim follows.

## Reproducibility and checks

The analysis reads the canonical gaze tables and verified scenes through `evaluation.offset_data.load_driving`, then reuses `MedianOffset`, `test_weights`, `score_directions`, and the existing five-fold splitter. Dataset and Horuspy source mounts are read-only. Only files in this paper's `evals` directory are written.

```bash
docker run --rm \
  -v /home/william/data:/data:ro \
  -v /home/william/workspace/horuspy/src:/src:ro \
  -v /home/william/PhDWorkspace/iv-2027-gaze-accuracy:/paper \
  -e PYTHONPATH=/src -e PYTHONDONTWRITEBYTECODE=1 \
  horuspy-dev:latest python /paper/evals/data/06_fair_recording_transfer_analysis.py
```

The script asserts recording UUID identity, train/test disjointness, normalized weights, equal recording mass, and equal fixation mass within each recording. It also inherits the loader's checks of verified events, finite valid samples, unique IDs, and stored versus recomputed spherical errors. Source hashes, code hashes, and exact calibration/test fixation IDs are saved in the provenance file. Current results reproduce William/Katharina's frozen random-pooling and real-day scores to their reported precision.

Artifacts (all under `evals/data/`):

- `06_fair_recording_transfer_analysis.py`: rerunnable analysis.
- `06_fair_recording_transfer_inventory.csv`: recording UUIDs, actual days, fixation/sample counts, effective calibration and source eligibility.
- `06_fair_recording_transfer_splits.csv`: fitted offsets and matched raw/corrected scores for every split and threshold.
- `06_fair_recording_transfer_summary.csv`: aggregate results.
- `06_fair_recording_transfer_pairs.csv`: primary source–target recording scores, including temporal direction and next-recording flags.
- `06_fair_recording_transfer_next_recording_summary.csv`: the forward next-recording comparison.
- `06_fair_recording_transfer_provenance.json`: source/code hashes and exact split identities.
