# Section V data basis: all values, sources and findings

**Extracted:** 2026-11-05 (Claude Code, for William Engel). **State:** after the wearer relabel of 2026-11-05 (§2).
**Purpose:** every number behind Section V ([sections/05_controlled.tex](../sections/05_controlled.tex)), with
the full tables in [data/](data/), so you can re-plot, rewrite or present them differently.

## 0. How to regenerate

```bash
# from the paper repo; pandas + matplotlib, e.g. the horuspy-dev image; data mounted read-only
python scripts/make_section5.py /home/william/data evals/data/05_regression_snapshot_2026-11-05_1248
```

[scripts/make_section5.py](../scripts/make_section5.py) only reads `/home/william/data/gaze_accuracy/` and writes:

| Output | Content |
|---|---|
| `figures/fig5_controlled.pdf` | Fig. 3 of the paper: (a) error per wearer at 1 m, (b) signed offset per wearer at 1 m, (c) vertical offset vs distance |
| `figures/tab_section5_factors.tex` | Table II (factors) |
| `figures/tab_regression.tex` | Table III (correction benchmark) |
| `evals/data/*.csv` | all values below (see §7 for columns) |

`figures/tab_controlled_factors.tex` (old Table II, written by `make_tables.py`) and `fig3_controlled_factors.pdf`
are no longer used by Section V. They were left untouched.

## 1. Sources and checks

| Source (`/home/william/data/gaze_accuracy/`) | Generated | Used for |
|---|---|---|
| `factors/controlled/` (`1_distance/fixations.csv`, `*/levels.csv`, `tests.csv`, `6_pursuit/recordings.csv`) | 2026-11-05 16:06 (after relabel) | V-A, V-B |
| `offset/runs/regression_chessboard/` | 2026-11-05 12:48 (**before** relabel; copy in `data/05_regression_snapshot_2026-11-05_1248/`) | V-C |

- Definitions follow `horuspy/docs/factor_analysis.md`: `central_60` fixations, status `ok`; accuracy is the median
  angular error, offset = gaze − target (+right/+up), dispersion = PSTD (`p_std_deg`), precision = RMS-S2S. Holm
  correction is applied per participant and test. "Significant" means Holm p < .05.
- **V-A unit = recording.** For each recording, take the median over its fixations of each metric
  (`data/05_static_accuracy_per_recording.csv`). Per wearer, report the median and IQR across recordings, equal weight per recording.
  Factor-analysis levels use recording × pass instances instead, so P1 differs slightly (1 m: 3.19° here vs 3.13°
  in `levels.csv`).
- Checks done:
  - Inputs: all 278 controlled recordings have current evaluations (none stale), and the factor-protocol
    and offset-run input hashes match the files.
  - Regression benchmark: 0 of 20 splits share a recording between train and test.
  - Relabelled recordings: their regenerated `dataset.csv`/`evaluation.csv` match the old files except for
    `recording_name`.
- Git: the paper repo was up to date with origin. The data repo is not pulled; it was 1 commit ahead.

## 2. Data fix on 2026-11-05 (owner-approved wearer relabel)

USB 3_11 (2026-11-03) holds Stefan's single block (11:13–11:36), a pause, then three 1→2→4 m runs by Marilu,
Sofia and Isabel, in that order (confirmed by the owner). All of them were recorded under Stefan's Neon profile.
The import had filed Marilu's run under Stefan and split the remaining six recordings 2-2-2.

| USB folder | UUID | Distance | Was | Now |
|---|---|---|---|---|
| 11:58:08 | a0d623bd | 1 m | Stefan | Marilu |
| 11:58:47 | 4c684ccc | 2 m | Stefan | Marilu |
| 11:59:23 | 30677fcb | 4 m | Stefan | Marilu |
| 12:04:42 | 4faa75d0 | 4 m | Marilu | Sofia |
| 12:06:07 | 1b3865e8 | 1 m | Marilu | Isabel |

Changed for each of the five recordings:
- `wearer.json`
- `info.json` (`wearer_id`, `recording_name`)
- the `detections.json` path
- folder names in `controlled/recordings`, `controlled/results` and `gaze_accuracy/per_recording`
- the `recordings.csv` row (with a note)
- new `provenance/wearer_identity/nov03_block_owner_confirmed_2026-11-05.json`

Then regenerated: their `dataset.csv` and `evaluation.csv`, and the factor analysis (16:06).
**Still running at writing time:** units, then the `chessboard`, `regression_chessboard` and `transfer` runs, then
`offset/analysis`. The data-repo changes are **not committed**.

Effect: Stefan 28 → 25 recordings (21 bright on Nov 3); Marilu, Sofia and Isabel each have a full 1/2/4 m series.
Stefan's distance effect is now significant (elevation Holm p = .015, PSTD p = .006).

## 3. Coverage (Section V)

247 recordings (2.5 h) from 11 participants: 239 static plus 8 pursuit recordings, from `factors/controlled/protocol.json`.

| Code | Name | Rec. (V total) | Static screen rec. | Distances | Dark | Days | Formal tests |
|---|---|---|---|---|---|---|---|
| P1 | William | 139 | 66 | 1/2/4/5 | 16 | 6 | all 8 factors |
| P2 | Katharina Winter | 23 | 23 | 1/2/4 | – | 2 | distance, position, session |
| P3 | Kanak Mazumder | 7 | 4 | 1 | 3 | 1 | position, illumination |
| P4 | Max Buettner | 3 | 3 | 1 | – | 1 | none (levels only) |
| P5 | Mohan Ramesh | 12 | 9 | 1/2/4 | 3 | 2 | distance, position, illumination |
| P6 | Stefan Englmeier | 25 | 21 | 1/2/4 | 4 | 2 | distance, position, illumination |
| P7 | Sarah Joy | 26 | 23 | 1/2/4 | 3 | 1 | distance, position, illumination |
| P8 | Constantin Selzer | 3 | 3 | 1/2/4 | – | 1 | none |
| P9 | Marilu Flores Turon Ramirez | 3 | 3 | 1/2/4 | – | 1 | none |
| P10 | Sofia Moreno Reynaga | 3 | 3 | 1/2/4 | – | 1 | none |
| P11 | Isabel Oliveira Trindade | 3 | 3 | 1/2/4 | – | 1 | none |

- **Groups:** seven baseline participants (P3, P4, P5, P8–P11; 3–12 recordings) and four extensive participants
  (P1, P2, P6, P7; 23–139). The driving benchmark covers P1, P2 and P6.
- **Protocols differ:** some participants have only 1 m bright recordings, some bright and dark, some a distance series.
- **Missing coverage:**
  - Illumination for P2, P4 and P8–P11.
  - Environment, pursuit, order and drift: P1 only.
  - Session: P1 and P2 only.
  - Formal tests need ≥ 3–5 units per level, so P4 and P8–P11 have descriptive levels only.
- Codes P1–P6 match Sections IV and VI; P7–P11 are new.

## 4. V-A: inter-individual variability (static bright screen)

**1 m (matched baseline, used in Fig. 3a/b):**

| Code | Rec. | Days | Error med [IQR] | Az | El | \|off\|/err | PSTD | S2S | Pupil |
|---|---|---|---|---|---|---|---|---|---|
| P2 | 9 | 2 | 1.03 [0.88, 1.13] | +0.44 | +0.09 | 0.44 | 0.38 | 0.08 | 2.96 |
| P9 | 1 | 1 | 1.08 | +0.33 | +0.12 | 0.33 | 0.39 | 0.09 | 4.87 |
| P8 | 1 | 1 | 1.13 | −0.60 | −0.66 | 0.79 | 0.45 | 0.09 | 3.70 |
| P5 | 3 | 1 | 1.28 [1.24, 1.30] | −0.50 | −0.02 | 0.40 | 0.48 | 0.09 | 3.06 |
| P4 | 3 | 1 | 1.65 [1.57, 1.77] | +0.15 | +0.48 | 0.46 | 0.43 | 0.10 | 3.58 |
| P11 | 1 | 1 | 1.70 | +0.70 | −1.40 | 0.92 | 0.24 | 0.07 | 4.11 |
| P3 | 4 | 1 | 1.93 [1.83, 2.12] | +1.05 | −1.30 | 0.82 | 0.59 | 0.09 | 3.20 |
| P7 | 7 | 1 | 2.15 [1.87, 2.28] | +0.07 | +1.87 | 0.88 | 0.52 | 0.11 | 3.14 |
| P1 | 25 | 5 | 3.19 [2.84, 3.79] | +0.10 | −3.00 | 0.94 | 0.53 | 0.12 | 3.12 |
| P6 | 9 | 2 | 5.08 [4.90, 5.40] | +0.50 | −4.59 | 0.91 | 0.50 | 0.13 | 2.92 |
| P10 | 1 | 1 | 5.37 | −0.41 | −5.11 | 0.95 | 0.47 | 0.09 | 3.86 |

- **Spread between wearers** (n = 11, one value per wearer): median 1.70°, range 1.03–5.37°, IQR 1.21–2.67°.
  Pooled over recordings instead, the median is 2.69° (64 recordings), dominated by P1.
- **Within a wearer** (IQR width, wearers with ≥ 3 recordings at 1 m): P5 0.05, P4 0.20, P2 0.25, P3 0.30,
  P7 0.41, P6 0.51, P1 0.96. P1's spread mixes two board configurations and five days.
- **Offsets:** elevation −5.11…+1.87° (7 of 11 below the target), azimuth −0.60…+1.05°.
- **Offset share:** for the six least accurate wearers (P11, P3, P7, P1, P6, P10), |median offset| / median error
  = 0.86–0.95. For the five most accurate it is 0.33–0.79.
- PSTD 0.24–0.59°; S2S 0.07–0.13°.

**All distances (sensitivity check):** range 1.08–5.81°, median across wearers 1.65°. The ordering of the least
accurate wearers (P6, P10, P1) is unchanged. Per-wearer values are in `data/05_static_accuracy_per_participant.csv` (scope = all distances).

## 5. V-B: driving-relevant factors

### Distance (level medians; `data/05_distance_levels.csv`)

| Code | Rec. 1/2/4 m | Error 1 → 2 → 4 m | Elevation 1 → 2 → 4 m | PSTD 1 → 4 m | Holm (err / el / PSTD) |
|---|---|---|---|---|---|
| P1 | 25/20/18 (+3 at 5 m) | 3.13 → 3.34 → 3.49 | −2.98 → −3.31 → −3.42 | 0.53 → 0.38 | .40 / .10 / .06; S2S .017* |
| P2 | 9/6/8 | 1.03 → 1.23 → 2.27 | +0.09 → −0.84 → −2.15 | 0.38 → 0.23 | .0009* / .0004* / .020* |
| P5 | 3/3/3 | 1.28 → 1.20 → 1.68 | −0.02 → +0.54 → +1.08 | 0.48 → 0.21 | .18 / .16 / .16 |
| P6 | 9/6/6 | 5.08 → 6.25 → 6.23 | −4.59 → −6.13 → −6.05 | 0.50 → 0.26 | .078 / .015* / .006*; S2S .012* |
| P7 | 7/6/10 | 2.15 → 1.61 → 1.21 | +1.87 → +1.47 → +1.08 | 0.52 → 0.37 | .004* / .013* / .70 |
| P8 | 1/1/1 | 1.13 → 1.32 → 1.97 | −0.66 → −1.07 → −0.95 | 0.45 → 0.18 | n = 1 |
| P9 | 1/1/1 | 1.08 → 0.95 → 1.60 | +0.12 → −0.40 → −1.15 | 0.39 → 0.46 | n = 1 |
| P10 | 1/1/1 | 5.37 → 5.78 → 6.78 | −5.11 → −5.71 → −6.69 | 0.47 → 1.29 | n = 1 |
| P11 | 1/1/1 | 1.70 → 2.53 → 2.87 | −1.40 → −2.42 → −2.86 | 0.24 → 0.21 | n = 1 |

- **P1 paired series (Aug 25–28, 18 repetitions):**
  - 4 − 1 m: error +0.58° [0.42, 0.75], elevation −0.66° [−0.87, −0.49] (Holm < .001).
  - 2 − 1 m: error +0.33° [0.20, 0.46], elevation −0.41° [−0.58, −0.24] (Holm .002).
- **Direction:** the offset moves downward in 8 of 9 wearers with ≥ 2 distances. The exception is P5 (upward,
  +1.10°), whose 1 m data come from Oct 12 and 2/4 m from Nov 3, so distance is confounded with day.
- **Accuracy effect has opposite signs:** a downward shift moves P7's positive offset toward 0 (error improves
  2.15 → 1.21°*), but pushes negative offsets further away (P2 1.03 → 2.27°*, P10 5.37 → 6.78°).
- **Dispersion:** falls with distance for most wearers (significant for P2 and P6). P9 (2 m) and P10 (4 m) are
  single-recording outliers.
- **Distance correlates with target angle:** farther boards span smaller angles. The factor run also has
  distance × eccentricity-bin levels (`1_distance/levels.csv`, view `experiment_distance_m+eccentricity_bin`).

### Field position (1 m; Lower − Upper row; `data/05_factor_tests_holm.csv`, rq = 2_position)

| Code | Δ elevation row / same ecc. bin | Δ error row / same ecc. bin | Other |
|---|---|---|---|
| P1 | −1.92* / −1.65* | +1.97* / +1.75* | Right−Left: az −1.63*, err +0.66*; ecc. 10–30° error *lower* than 0–10° (−0.94*, −1.08*) |
| P2 | −0.31 / −0.41 | +0.06 / +0.14 | – |
| P3 | −0.37 / −0.32 | +0.88 / +1.01* | – |
| P5 | −1.71 / −1.87 (Holm .07) | −0.03 / −0.37 | – |
| P6 | +0.06 / +0.64 | +0.51 / −0.04 | az −2.08* / −1.73*; PSTD +0.83* / +0.74*; S2S +0.32* / +0.31* |
| P7 | −0.76 / −0.70* | −0.61 / −0.21 | – |

- Gaze in the lower row lies lower for 5 of 6 tested wearers (0.31–1.92°). The error goes up or down depending on
  the sign of the offset (P7 improves).
- P4 and P8–P11 have levels only (`2_position/levels.csv`). Isabel (P11) is now included.
- The old claim "precision consistently poorer in the lower row" no longer holds: only P6 shows it. P1 has
  ΔS2S +0.01, and its Holm-significant p reflects the median, not the mean difference.
- Eccentricity is confounded with row in the 5 × 3 layout. Do not report it as "stable" or as "worse in the periphery".

### Secondary factors (`data/05_illumination_environment_session_levels.csv`)

| Factor | Coverage | Values | Tests |
|---|---|---|---|
| Bright/dark (1 m) | P1 16+16, P3 4+3, P5 3+3, P6 9+4, P7 7+3 rec. | pupil +1.20/+1.00/+0.96/+0.49/+0.72 mm; Δel +0.34/−0.12/−0.03/+0.78/+0.26°; Δerr −0.30/−0.14/−0.14/−0.07/+0.28° | pupil sig. P1, P6; error/offset/PSTD none significant |
| Indoor/outdoor | P1, 20+20 rec. (Oct 30 same day 6+12) | error 3.89 → 3.99, el −3.82 → −3.87, pupil 4.11 → 2.37 mm, PSTD 0.23 → 0.27 | pupil*, PSTD* (all days); same day only pupil* |
| Pursuit | P1, 8 pursuit vs 50 static | error 4.06 vs 3.90, el −3.88 vs −3.81, target-relative PSTD 0.93 vs 0.27 | PSTD* (Holm < .001; same day .011) |
| Within-day drift | P1 Aug 25/26, 7–8 reps per distance | Spearman \|ρ\| ≤ .86, all Holm ≥ .24; pass 2 − 1: err +0.12 [−0.10, 0.39] | none |
| Between days | P1: Aug 25/26/28, Sep 28, Oct 1; P2: Oct 21/30 | P1 el −2.83/−2.95/−2.56 vs −4.58/−4.26; P2 error 1.03 vs 0.96 | P1 err/az/el/PSTD/S2S *; P2 none |

- **Illumination vs. the literature:** Salari et al. report a ≈ 0.94° Neon gaze shift between pupil states. Our
  vertical shifts (up to 0.78°) are of similar size, but none is significant here.
- **P1's between-day effect is confounded:** August used board configs `e6fcb80e4512`/`0b8b1b7d4d95`
  (legacy `static`), September/October used `d30a47c70c2f`.
- **P6's dark recordings (Oct 12):** PSTD 1.10° and S2S 0.37°, about 2–3× his bright values. Not significant,
  but worth a quality check.

## 6. V-C: correction benchmark (pre-relabel snapshot, 12:48)

- **Protocol:** `recording_blocks`, 5 folds; each fold trains on one block (≈ 20% of a participant's recordings)
  and tests on the rest. Seed 42; ridge α = 100.
- **Train/test recordings per fold:** P1 25/106, P2 4–5/18–19, P6 5–6/22–23, P7 5/21.
- **Features:** gaze position and pupil are available at run time. Inverse distance (stated board distance)
  must be known or estimated.
- **P6 values use the pre-relabel data**, which still include Marilu's three recordings, as you asked.
  P1, P2 and P7 are unaffected (their data did not change). The rerun is in progress.

Median error (°), mean of 5 folds (`data/05_regression_benchmark_summary.csv`):

| Code | Raw | Median | Pos. | Pos.+pupil | Pos.+dist. | Pos.+dist.+pupil | Ridge pos.+dist. |
|---|---|---|---|---|---|---|---|
| P1 | 3.71 | **1.01** | 1.06 | 1.09 | 1.03 | 1.06 | 1.03 |
| P2 | 1.45 | 1.41 | 1.24 | 1.26 | **0.87** | 0.87 | 0.87 |
| P6 | 5.45 | 2.00 | 1.82 | **1.74** | 2.03 | 1.94 | 2.01 |
| P7 | 1.64 | 1.02 | 1.06 | 1.11 | **0.95** | 1.01 | 0.94 |

Δ vs median offset (mean [min, max] over folds; folds better / 5):

- **P1:** position +0.05 [+0.01, +0.10] 0/5; pos+dist +0.02 [−0.05, +0.12] 2/5. Nothing beats the median.
- **P2:** position −0.17 5/5; pos+dist −0.54 [−0.59, −0.48] 5/5. P2's median offset barely helps (raw 1.45).
- **P6:** position −0.18 5/5; pos+pupil −0.27 [−0.54, −0.11] 5/5; pos+dist +0.03 [−0.28, +0.69] 3/5 (unstable).
- **P7:** pos+dist −0.08 [−0.18, −0.02] 5/5; pos+pupil +0.09 1/5.
- Ridge vs linear: ≤ 0.03° everywhere. Pupil terms help only P6.
- Five folds are too few for useful confidence intervals. Report fold ranges or n/5 consistency instead.

## 7. Files in `evals/data/`

| File | Rows | Columns |
|---|---|---|
| `05_static_accuracy_per_recording.csv` | 161 static screen recordings | code, participant, recording_name, date, distance_m, board_config, error, azimuth, elevation, pstd, s2s, pupil, fixations, offset_norm |
| `05_static_accuracy_per_participant.csv` | 11 × {1 m, all distances} | recordings, days, distances, `<metric>_median/_q25/_q75`, offset_share |
| `05_fig_accuracy_offset_per_wearer.csv` | 11 | plotted values of Fig. 3a/b (1 m): n, med, lo, hi, q25, q75, az, el, IQRs |
| `05_distance_levels.csv` | 30 participant × distance | factor-analysis level medians/IQRs |
| `05_factor_tests_holm.csv` | 332 | every factor test with p, p_holm, mean difference, CI, rho, `significant` |
| `05_illumination_environment_session_levels.csv` | 24 | illumination, environment, session levels |
| `05_regression_benchmark_summary.csv` | 40 participant × model | summary error, P90, fold min/max, Δ vs median, folds better |
| `05_regression_split_recordings.csv` | 4 | train/test recordings per fold |
| `05_regression_snapshot_2026-11-05_1248/` | – | `summary.csv`, `scores.csv`, `splits.csv`, `protocol.json` of the run used for V-C |

## 8. Open issues and inconsistencies (not changed: outside Section V)

1. **Abstract, Introduction (lines 85, 121) and Methods III-C** still say "216 recordings from six participants"
   (2.9 h). Section V now uses 247 recordings from 11 participants (2.5 h).
2. **Abstract and Conclusion still give the old narrative:**
   - "accuracy robust to ... eccentricity"
   - "lower-field precision consistently poorer"
   - "distance shifts gaze downward (both participants tested)"

   The new data support a downward shift for 8 of 9 wearers, but a lower-row precision loss only for P6.
3. Section IV has a pre-existing `\todo` (source of ρ = 0.37/0.63). Bibliography: `\k` encoding error (OT1), also
   pre-existing.
4. The offset reruns (chessboard, regression, transfer, analysis) were still running at writing time. When they finish,
   Stefan's V-C row and Section VI numbers that use P6 or the chessboard run may change.
5. P5's distance shift is confounded with day; P1's session effect is confounded with board configuration.
6. P9's 2 m and P10's 4 m recordings have unusually high PSTD (0.96°, 1.29°), so single-recording levels are fragile.
7. Compile check (TeX Live 2026, scratch copy): the paper is 7 pages, as before. Section V runs from page 4 to page 6,
   with no overfull boxes from Section V.

## 9. Older pursuit recordings added (2026-11-05, evening)

**Data change (owner-approved).** The three older screen pursuit recordings of 2026-07-16 (P1; screen target without QR code,
so no stimulus timeline; per owner, the pattern config's "printed ArUco board moved by hand" description is wrong; slow / medium / fast, median target speed 7.8 / 17.1 / 22.6 °/s) now have per-stroke
fixation intervals:
- **Source:** `controlled/patterns/pursuit_<speed>/observed_motion.csv`, reconstructed from the target's scene-camera
  motion.
- **Labels:** `crosshair_<direction>.NN` in `annotations.csv`.
- **Applied with horuspy** (no code change): `read_annotations` → `apply_annotations` → `save_json(detections.json)`
  → `create_dataset` (module 272097 calibration) → `create_evaluation`.
- **Unchanged:** gaze, target and calibration values are identical to before; only the fixation intervals changed.
- **Result:** 22 / 17 / 16 strokes become fixations; evaluation rows 88 / 68 / 64. The fast recording has 7
  `empty_selection` rows because the target was detected in only 59% of its frames.
- **Environment note:** the horuspy-dev image ships OpenCV 5.0, but horuspy requires `opencv<5`
  (`cv2.undistortPointsIter`), so OpenCV 4.14 was supplied for this run.

**Counts:**
- 118 pursuit sequences in total: 55 old strokes + 63 screen segments (`data/05_pursuit_counts.csv`).
- The official factor analysis (`6_pursuit`) still covers only the 8 screen recordings, because its loader needs
  the screen timelines.

**Comparison** (`scripts/make_pursuit_comparison.py`, same definitions as factor test 6; outputs in
`data/05_pursuit_old_vs_screen_{recordings,phases,directions}.csv`):

| Group | Windows | Error | Az / El offset | Target-relative dispersion |
|---|---|---|---|---|
| Static 1 m, P1 (50 rec.) | – | 3.90 | −0.18 / −3.81 | 0.27 |
| Screen pursuit (8 rec.) | – | 4.06 | −0.10 / −3.88 | 0.93 |
| Old (no QR) slow | 41 | 3.79 | +0.14 / −3.75 | 0.47 |
| Old (no QR) medium | 32 | 3.33 | −0.57 / −3.21 | 0.63 |
| Old (no QR) fast | 16 | 3.22 | −0.76 / −2.74 | 2.29 |

**Near turn − straight** (median per recording):
- Old: error −0.29°, dispersion −0.70°.
- Screen: +0.30° and +0.86°.
- The opposite sign is plausibly due to pauses at the turns of these older patterns (`turns.csv` pause columns).

**Direction (straight samples):**
- Down: largest error and most negative elevation offset in both sets (old 4.46° / −4.42°; screen 4.48° / −4.14°).
- Up: smaller error (old 3.38°; screen 2.89°).
- Old Right and Up dispersion (5.35° / 3.82°) are inflated by fast-recording gaps.

**Interpretation:**
- The P1 systematic offset is reproduced in the July recordings.
- Target-relative dispersion grows with target speed (0.47 → 0.63 → 2.29°). The fast value is partly
  detection-limited.
- Directions and turns are head-relative and reconstructed, not scheduled.
