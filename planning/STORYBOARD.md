# IV 2027 gaze-accuracy paper: storyboard and evidence map

State: 2026-11-01. Every number below was re-read from the saved evaluation outputs in
`~/data/{driving,controlled}/evaluations/` (runs of 2026-11-01, after the Companion-offset rebuild).
Nothing was taken from `artifacts/` folders. Older `horuspy/results/driving_*` folders (2026-10-30, pre-rebuild)
are **not** cited.

Venue facts (ieee-iv.org/2027 information for authors, read 2026-11-01): 6 pages expected, 8 max with page
charges; **double-blind**; IEEE conference template; remove the copyright notice; US Letter PDF; deadline
**2026-11-15 23:59 AWST**. Participants are pseudonymised: P1 = William (driving: passenger seat),
P2 = Katharina (driving: driver), P3 Kanak, P4 Max, P5 Mohan, P6 Stefan. The mapping lives only in
`scripts/make_figures.py` and `main.tex` macros.

## 1. One-page storyboard

**Problem.** Human gaze is a promising supervision signal for driving models (end-to-end, BEV, VLM) and for
robot learning, but only if the measured gaze location is spatially reliable. Calibration-free wearables
(Neon) make naturalistic collection practical; how reliable they are in the actual operating condition, and
what limits them, is not established for driving.

**Stage 1 — Real-world benchmark (RQ1, C1).** 152 validated driving scenes, two qualified participants,
precise 2D target references, LiDAR/GNSS/scene tags. Raw median error 3.96° (P1) / 1.48° (P2).
Sparse driving references remove most systematic error (pooled 20 % scenes: 0.76° / 0.83°); they beat
chessboard-derived correction (0.88° / 1.40°), which for P2 does not transfer at all. Spatially optimised
reference layouts give no advantage over random scenes. Residual variability between scenes remains.

**Stage 2 — Controlled characterisation (RQ2, C2).** Remaining variability motivates a controlled study:
216 recordings, six participants. Neon is robust to eccentricity, illumination, indoor/outdoor and
within-day time; viewing distance shifts gaze downward (both participants tested); the lower image region
loses precision (6/6) and, for some participants, accuracy; smooth pursuit triples residual dispersion
without changing accuracy. The distance effect explains *why* near-field chessboards fail for far road
targets: calibration must be condition-matched.

**Stage 3 — Transfer back to driving (RQ3, C3).** Using the insight that residual error is
person-specific (constant offset + position term for P1, sample noise for P2) we select a causal per-person
correction on calibration scenes only. It beats the strong median baseline in every split configuration
(20 %: −7.3 % P2, −2.5 % P1), removes 14–19 % of P2's P90 tail, and helps most in dynamic scenes (fast gaze,
approaching targets, moving ego vehicle). Per-sample quality descriptors (eye-image exposure, IMU, view
region) are attached to every sample; no validated filtering gain is claimed.

**Take-away.** Calibration-free wearable gaze is a promising supervision source *if* a small number of
in-situ references is collected; our pipeline makes that cheap, and the controlled study tells where the
remaining errors come from.

## 2. Section outline (paragraph objectives)

| Section | Paragraphs (objective) | ≈ length |
|---|---|---|
| I Introduction | (1) gaze as supervision for AD/robotics; (2) needs spatial reliability, Neon attractive; (3) gap: no driving-condition validation with references + correction; (4) RQ1–3 and the three-stage design; (5) contributions C1–C3 + release statement | 0.8 p |
| II Related work | (A) wearable validation (lab, poster, Neon reports); (B) influence factors; (C) offset/implicit correction incl. Jia; (D) driving gaze datasets: simulator vs real, attention maps vs sensor error | 0.5 p |
| III Methodology | (A) device + two settings overview (Fig. 1); (B) driving benchmark acquisition + references + metadata; (C) controlled protocols; (D) metrics; (E) correction protocols, splits, statistics | 1.1 p |
| IV Real-world | (1) raw accuracy; (2) chessboard vs driving correction (Fig. 2a); (3) budget + geometry (Fig. 2b); (4) residual variability → motivates V | 0.7 p |
| V Controlled | (1) Table I overview; (2) robust factors; (3) distance; (4) lower region precision; (5) pursuit; (6) link back to Stage 1 | 0.8 p |
| VI Transfer | (1) failed per-sample ridge (negative result); (2) selected correction overall + shares; (3) tails; (4) dynamic subsets; (5) quality descriptors | 0.7 p |
| VII Discussion + conclusion | answers to RQ1–3; implications for supervision; limitations (2 participants, same-drive splits, P1 session, no cross-day test); release | 0.5 p |

## 3. RQ → evidence → contribution

| RQ | Evidence (artifact) | Contribution |
|---|---|---|
| RQ1 real-world accuracy + sparse correction | `driving/evaluations/driving_offset_benchmark/category_summary.csv`, `boxplot_data.csv`; scene-level tests `driving/evaluations/offset_analysis/tests.csv` (RQ2, RQ3 rows) | C1 |
| RQ2 influencing factors | `controlled/evaluations/factor_analysis/tests.csv`, `*/levels.csv`, `6_pursuit/recordings.csv`; chessboard benchmark `controlled/evaluations/median_offset_benchmark/summary.csv` | C2 |
| RQ3 knowledge-informed improvement | `driving/evaluations/ridge_offset/gaze_correction_{20,40,60,80}/per_seed.csv`, `fold_scores.csv`, `scene_errors.csv`, `situations.csv`; `ridge_offset/tags.csv`; `ridge_20/summary.csv` (failed ridge) | C3 |

## 4. Figure plan

| Fig. | Message | Source | Status |
|---|---|---|---|
| 1 | Three-stage design and the two complementary datasets | TikZ in `main.tex` | drafted; add an example scene frame (anonymised) if space allows |
| 2 | In-situ references beat chessboards; few random scenes suffice | `driving_offset_benchmark/boxplot_data.csv`, `category_summary.csv` | `figures/fig2_driving_correction.pdf` |
| 3 | Robust to most factors; distance, lower-row precision and pursuit dispersion matter | `factor_analysis/*` | `figures/fig3_controlled_factors.pdf` (+ `fig3b_data.csv`) |
| 4 | Extended correction beats the median baseline, cuts tails, helps in dynamic scenes | `ridge_offset/gaze_correction_*`, `ridge_offset/tags.csv` | `figures/fig4_transfer.pdf` (+ `fig4ab_data.csv`) |

Regenerate: `python scripts/make_figures.py /home/william/data` (needs pandas, matplotlib).

## 5. Open items before submission (must be resolved or kept out of the paper)

Discrepancies between PAPER_TASK.md and the data:

1. **Scene count:** the benchmark has **152** eligible scenes (P1 79, P2 73), not 153. Draft uses 152.
2. **Controlled participants:** the catalog has **6** participants (216 recordings, 2.9 h), not 8 / ~200.
   Draft uses 6. If two more participants exist, they are not in `recordings.csv`.
3. **"Two expert drivers":** `observer_role` is `driver` for P2 and `passenger` for P1 in all 16 driving
   recordings. Draft says both are qualified research-vehicle drivers, P2 drove and P1 rode in the front
   passenger seat. Confirm, and whether P1 is authorised to drive the vehicle.
4. **Pipeline (updated from COLLECTION_PIPIELINE.md):** paper now describes voice event → gaze-guided
   detection in a search region → automatic assignment + tracking → ambiguity flagging → validation in the
   Neon Player plugin; every target manually validated. Still needed for the paper:
   (a) speech detector name; (b) search-region radius; (c) object detector (model, classes);
   (d) **efficiency numbers**: share of targets accepted unchanged / corrected / flagged / annotated manually,
   ideally review time per scene. Without (d) the paper must not claim a quantified annotation saving.
   Note: saved provenance in the 152 scenes shows only `manual`, `tracking` and `unknown` sources, so (d)
   cannot be derived from `detections.json` as it stands.
   (e) Independence: automatic assignment only with a single candidate; multiple candidates → manual
   review. Paper states this; no further check needed.
5. **Indoor/outdoor numbers:** the Nov 1 summary says same-day accuracy 4.08° vs 4.08°, but
   `5_environment/levels.csv` gives indoor 4.08° vs outdoor 3.85° (Oct 30; Holm p = 1.0) and P_STD
   0.22° → 0.30°. Draft uses levels.csv.
6. **P1 large-error claim:** "worst 10 % of scenes 1.58° → 1.49°" could not be reproduced from
   `scene_errors.csv` (worst-decile scenes 2.31° → 2.33° at 60 %). Not used. P1's P90 is unchanged.
7. **P2 P90:** −14.5 % at 20 % share (not 15 %); −18 to −19 % at 40–80 %.
8. **Eccentricity:** formal tests exist for 5 participants (P4 has 3 recordings, descriptive only).

Validity items:

9. Driving splits are scene-level within the same drives; **no cross-drive / cross-day transfer** is tested.
   P1's driving spans two days (Jul 15, Oct 15), P2's two consecutive days. A leave-one-day-out run would
   strengthen RQ1/RQ3 (P1 is feasible).
10. P1's controlled offset differs between August and Sep/Oct (elevation bias ≈ −2.8° vs −4.4°); P2 is
    stable. The summary flags this as coinciding with the Companion-offset removal: verify before claiming
    either session stability or a session effect.
11. Recording `413b4ada` (P1, 29 scenes): earlier audit noted a wearer UUID shared with P2's profile and
    sparse clock evidence (PTP failure). Confirm identity and that the 29 scenes are unaffected.
12. The extended correction (§3b of the summary) was designed after the plain ridge failed: report it as
    exploratory (done in the draft).
13. Quality descriptors (exposure, IMU, windshield/side-window view) exist per sample/scene, but no
    filtering or uncertainty evaluation on the rebuilt data exists. The Oct 30 dispersion-prediction results
    (`horuspy/results/driving_dispersion_baseline`) pre-date the rebuild; rerun before citing.
14. Neon hardware specs in §III (200 Hz gaze; scene camera 1600×1200 px, 30 Hz, 103°×77°) — 200 Hz verified
    from timestamps; confirm the camera numbers.
15. Missing references (identified in the Oct 27 audit, not in `references.bib`): ADAS gaze profiling with
    Neon on real roads (MDPI Vehicles 7(4):145), PyNeon (BRM 2026, doi 10.3758/s13428-026-03089-8). Add via
    the literature workflow; the draft does not cite them yet.
16. Dataset release: draft says "landing page with pilot examples; full release after legal review" — no
    URL (double-blind).
