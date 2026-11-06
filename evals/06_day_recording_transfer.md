# Driving median offset: transfer across recordings and days

**Generated:** 2026-11-06 with `scripts/make_day_recording_transfer.py` (horuspy-dev image, horuspy `src` read-only).
The dataset is read-only; the outputs are only `evals/data/06_day_recording_transfer_{splits,summary}.csv`.

**Method (unchanged from the offset benchmark):**
- Scenes and samples come from `evaluation.offset_data.load_driving`.
- Correction: `models.offset.MedianOffset`, i.e. the median of the calibration scenes' offsets.
- Scoring: `score_directions` with `test_weights` (recordings, then scenes, then samples weighted equally).
- Uncorrected and corrected errors are scored on the same held-out samples.
- Calibration and test scenes never overlap (asserted).

## Compact comparison

Mean over splits; median angular error (°) on held-out scenes. "Improved" counts splits where the corrected error is
below the uncorrected one.

| Participant | Split type | Kind | Splits | Calibration scenes (mean, range) | Uncorrected | Corrected (range) | Improved |
|---|---|---|---|---|---|---|---|
| P1 | one recording → other July recordings | same day, recording | 9 | 5.6 (2–11) | 4.02 | **0.87** (0.67–1.59) | 9/9 |
| P1 | recording group → group (15:45–16:07 ↔ 16:13–16:50) | **pseudo-day** | 2 | 25 (22–28) | 3.98 | **0.68** (0.66–0.69) | 2/2 |
| P2 | other recordings → held-out recording | leave-one-recording-out (both days) | 6 | 60.8 (45–72) | 1.45 | **0.83** (0.72–0.97) | 6/6 |
| P2 | Oct 14 ↔ Oct 15 | **real cross-day** | 2 | 36.5 (6–67) | 1.49 | **0.91** (0.87–0.96) | 2/2 |
| P6 | one segment → other five | same drive, segment | 6 | 15.5 (15–16) | 6.00 | **1.44** (1.35–1.51) | 6/6 |
| P6 | segments 1–3 ↔ 4–6 | **pseudo-day** | 2 | 46.5 (45–48) | 6.00 | **1.40** (1.39–1.40) | 2/2 |

For reference, the random-scene benchmark of Section VI (20% of scenes, five folds) gives 0.76 / 0.83 / 1.41°. Its
test sets differ, so these numbers are comparable in size but are not paired with the splits above.

## Findings

- **The offset transfers in every split** (27/27 improve), across recordings, recording groups, segments and real
  days. The errors fall from 4.0 → 0.7–0.9° (P1), 1.5 → 0.8–0.9° (P2) and 6.0 → 1.4° (P6).
- **Genuine cross-day transfer (P2 only).** An offset from one day reduces the other day's error from 1.49° to
  0.87–0.96°. This is about 0.05–0.1° worse than calibrating within the same recordings (LORO 0.83°;
  random-scene 0.83°). The Oct 14 → Oct 15 direction rests on only 6 calibration scenes from 3 short drives, and
  the two days' offsets differ by about 0.6° in elevation (−1.09° vs −0.49°).
- **Pseudo-days (P1, P6)** test temporal and recording-group robustness within one session or drive, not day-to-day
  stability. Both are as good as or better than the random-scene benchmark (P1 0.68°, P6 1.40°), which shows no
  drift of the offset within a session.
- **Single recordings as calibration (P1)** usually work (0.67–0.79° for most), with two weaker cases:
  - `3f9e4e5b`, 3 scenes, elevation offset −2.6° vs about −4.0° for the others: corrected error 1.59°.
  - `04f6eeff`, 2 scenes: corrected error 1.07°.

  A recording with few or atypical scenes gives a less reliable offset, consistent with the reference-count curve
  in Section VI.
- **Per-split offsets are stable within each person:**
  - P1 elevation −3.7° to −4.3° (except the 3-scene recording above).
  - P6 −5.7° to −6.7° across the six segments.
  - P2 −0.4° to −0.7° (LORO).

## Caveats

- **P1:** only the 9 July 15 recordings were used, all with the same applied scene calibration (`corrected`,
  module 272097). The Oct 15 drive uses the native module calibration and was excluded so as not to mix device
  calibrations. A P1 cross-day test (July vs October) would mix calibrations and was not run.
- **P2:**
  - Oct 14 contributes only 6 scenes (4 + 1 + 1).
  - In LORO, two held-out recordings consist of a single scene, so those splits are single-scene tests.
- **P6:** the six segments are consecutive blocks of 15–16 scenes ordered by start time, all from one drive. No
  real day change.
- **Uncertainty:** with 2–9 splits per row, means and ranges are reported; no significance tests.

## Files

- `data/06_day_recording_transfer_splits.csv`: one row per split. Columns: calibration/test scene and recording
  counts, fitted offset (az/el), uncorrected/corrected median and P90, improvement.
- `data/06_day_recording_transfer_summary.csv`: the table above, plus P90 means.

## Addendum (2026-11-06): P1 genuine cross-day transfer

`scripts/make_p1_cross_day_transfer.py` → `data/06_p1_cross_day_transfer.csv`. Same method as above; a separate
output, so the fixed results above are unchanged.

| Split | Calibration | Test | Offset az / el | Uncorrected | Corrected |
|---|---|---|---|---|---|
| 2026-07-15 → 2026-10-15 | 50 scenes, 9 drives | 29 scenes, 1 drive | −0.46 / −3.97 | 3.12 | **1.22** |
| 2026-10-15 → 2026-07-15 | 29 scenes, 1 drive | 50 scenes, 9 drives | −0.56 / −3.01 | 4.02 | **1.12** |
| **Mean (2 splits)** | | | | 3.57 | **1.17** |

- **Both directions improve strongly** (2/2): about 1.9–2.9° less error.
- **Weaker than within July 15:** 1.17° vs 0.87° (one recording → others) and 0.68° (groups). The two days' vertical
  offsets differ by about 1° (−3.97° vs −3.01°).
- **Caveat:** July uses the applied `corrected` scene calibration, October the native module calibration (both module
  272097). This split therefore contains a day change *and* a device-calibration change, which is why it was
  excluded from the main transfer analysis.
