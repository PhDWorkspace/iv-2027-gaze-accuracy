# Related Work: Wearable Eye-Tracking Accuracy and Robustness (with Pupil Labs Neon in focus)

**Created:** 2026-11-02
**Purpose:** The source material for the *Wearable Eye-Tracking Accuracy and Robustness* subsection of the IEEE IV 2027 paper. Papers are ranked by how directly they bear on our contribution (see `phd-literature/skills/contribution_wearable_eye_tracking_accuracy_robustness.md`, C1–C3).
**Source pool:** 136 summaries in `phd-literature/summaries/`. Every paper listed here has a BibTeX key in `phd-literature/bib/references.bib`; all keys were checked.

## How to read this file

- **Verification status**
  - **[V-PDF]**: the numbers were checked against the full text of the PDF in `phd-literature/papers/` or `papers-inbox/`.
  - **[S]**: the numbers come from our summary only and were not re-checked in the PDF. Check the PDF before citing a number marked [S].
- **Page numbers:** `p.N` is the page index of the PDF file, which may differ from the printed journal page.
- **Absence claims:** "Not found" means we did not find the item in the PDF text we checked. It does **not** mean the authors did not do it.
- **Scope of the evidence:** every statement is about the cited paper only. Our own numbers appear only in the "Gap for us" columns and come from the contribution file.

### Summary error found during verification

- **`ehinger2019testBattery`:** the summary states 28 participants and accuracy of 0.84° (Pupil Labs) vs 0.50° (EyeLink).
- **The PDF says** N = **15** analysed (11 more excluded) and **0.82° (Pupil Labs) vs 0.57° (EyeLink)** (p.1, p.4).
- **Action:** use the PDF values and correct the summary.

---

## 1. Ranked overview

| Rank | BibTeX key | Device(s) | Participants analysed | Setting | What is measured | Overlap with our work |
|---:|---|---|---|---|---|---|
| 1 | `foucher2026neon` | **Neon** vs EyeLink 1000 Plus | 28 (dual-tracker) + 20 (separate Neon-only group) | Lab screen, 60 cm | Accuracy, precision, drift over time, head yaw/roll, pursuit, microsaccades, blinks, pupil; **IR interference** | **Direct** (independent controlled Neon validation) |
| 2 | `baumann2026neonAccuracy` | **Neon** (vendor report) | 206 (lab) + 402 (in-the-wild) + 4 (activities) | Lab screen at 0.4 m & 1.3 m; in-the-wild at 0.3–4.0 m, indoor/outdoor | Uncalibrated vs offset-corrected accuracy over the field of view, demographics, indoor/outdoor, slippage | **Direct** (baseline we must compare against; vendor-authored) |
| 3 | `alecka2026neon` | **Neon** vs Tobii Pro Fusion | 46 (accuracy), 32 (stability) | Lab screen, 65 cm, chinrest | Accuracy at 13 positions, white vs black background, BCEA | **Direct** (eccentricity and brightness factors) |
| 4 | `salari2026pupilSize` | **Neon**, Pupil Core, SMI ETG 2w, Tobii G2, EyeLink 1000 Plus | 24 (Tobii G2: 6) | Lab screen, 930 mm, chinrest | Pupil-size artefact: bright vs dark screen → apparent gaze shift, accuracy, precision, data loss | **Direct** (pupil-size factor) |
| 5 | `pettenella2026slippage` | **Neon**, Tobii G3, VPS Lite | 12 | Standing, poster target at 1 m, motion capture | Gaze error vs measured 6DOF frame slippage (facial, induced, locomotion) | **Direct** (slippage/motion factor) |
| 6 | `nolte2026bestPractices` | **Neon** | **1** (case study) | Outdoor urban walking, handheld target at 3 m | Start/end 10-point validation per 10-min segment | **Partial** (outdoor, temporal stability, n = 1) |
| 7 | `maquiling2026vergencePupil` | **Neon** | 8 | Chinrest, physical targets at 0.25 m and 0.9 m | Vergence vs pupil-size coupling | **Partial** (depth and pupil confound; not angular accuracy) |
| 8 | `niehorster2026slippage` | **Neon**, Tobii G3, Ray-Ban Meta, Nuance Audio | 35 | Motion capture, 10 tasks | Physical 6DOF frame slippage only (**no gaze data**) | **Partial** (quantifies slippage; no accuracy) |
| 9 | `park2026openEye` | **Neon module** inside HMDs | 18 | VR/AR headsets | Gaze error after custom calibration; ~90 Hz IR flicker from HMDs | **Partial** (IR interference; HMD, not glasses) |
| 10 | `hooge2023robust` | Pupil Core, **Pupil Invisible**, SMI ETG2, SeeTrue, Tobii G2, Tobii G3 (no Neon) | 4 | Physical target at 1.65 m; stand/walk/skip/jump; head straps | Accuracy and precision under body motion | **Partial** (motion precedent, not Neon) |
| 11 | `onkhar2024evaluating` | Tobii G2, Tobii G3 | 36 (Tobii G3: 33–34) | Wall dots at 15° eccentricity with/without chinrest; walking along a 21.7 m corridor | Accuracy, precision, bias; workload and participant factors | **Partial** (static vs dynamic precedent) |
| 12 | `macinnes2018wearable` | Pupil Labs 120 Hz, SMI ETG 2.6, Tobii G2 | **3** | Indoor targets at 1, 2, 3 m × −10/0/+10° | Accuracy and precision by distance and gaze angle | **Partial** (only distance-sweep precedent; N = 3) |
| 13 | `niehorster2024glassesvalidator` | 6 wearable trackers (software test) | 61 (one tracker) | Printed poster validation | Accuracy/precision tool; head-still instruction; assumed vs estimated distance | **Method** (validation protocol) |
| 14 | `ehinger2019testBattery` | Pupil Labs (pre-Neon) vs EyeLink 1000 | 15 | Lab screen, 60 cm | Comprehensive test battery | **Method** (battery reused by `foucher2026neon`) |
| 15 | `niehorster2026fundamentals7` | — (methods paper) | — | — | Definitions of inaccuracy, imprecision, data loss | **Method** (terminology) |
| 16 | `cui2025listeningEffort` | **Neon** + EyeLink DUO | 26 | Chin/forehead rest, speech-in-noise task | Gaze dispersion, pupil, head movement as effort markers | Background (Neon, effect-level only) |
| 17 | `karaer2026vrEyeTracker` | BulbiCAM VR; **Neon** for pupillometry | 39 (Neon paired: 23) | Clinical | Pupillometry agreement | Background (pupil, not gaze) |
| 18 | `pfeffer2024neonPupillometry` | **Neon** (vendor report) | 7 | Lab, motor rail | Pupil-diameter robustness to gaze angle and slippage | Background (pupil, not gaze) |
| 19 | `turuwhenua2026okn` | **Neon** | 22 | OKN stimulus | False-negative OKN detection from Neon gaze | Background (Neon signal limits) |
| 20 | `xu2026signalConstruct` | **Neon** + other wearables | 40 | **Real flight** (Cessna 172) | Signal availability, construct validity | Background (real vehicle, no accuracy) |
| 21 | `velisar2024noise` | Pupil Core | see note | Walk/run/jump; calibration patterns | Eye-camera motion; 3D gaze depth | Background (slippage/noise) |
| 22 | `buter2024eyeTracking` | Pupil Core vs Tobii G3 | 10 | Surgical console | Gaze error in cm; temporal stability | Background |
| 23 | `choe2016pupilSize` | EyeLink (desktop) | 23 | Lab | Pupil-size-induced gaze error and its correction | Background (pupil factor, correction) |
| 24 | `holmqvist2022headMovements` | 5 P-CR trackers (non-wearable) | — | Artificial and human eyes | Head motion increases and colours noise | Background (precision/noise) |
| 25 | `blignaut2014dataQuality` | Tobii TX300 (remote) | 71 | Lab | Ethnicity, distance and lighting effects on data quality | Background (participant factors) |
| 26 | `santini2019grip` | Head-mounted (Grip method) | 109 (museum dataset) | Field dataset | Slippage-robust gaze-estimation method | Background (correction, C3) |
| 27 | `kar2020mlgaze` | Desktop/tablet tracker | 20 | Lab | ML modelling of gaze-error sources (distance, head pose) | Background (error modelling, C3) |
| 28 | `kasprowski2019implicitCalibration` | — | [S] | — | Implicit calibration from probable fixation targets | Background (natural-target correction, C3) [S] |
| 29 | `calvi2023comparing` | Tobii glasses | 14 field / 18 simulator | **Real urban driving** vs simulator | Eye-tracking parameters field vs simulator (no accuracy) | Background (driving context) |

---

## 2. Core comparison table: target-referenced Neon gaze-accuracy studies

This table answers: what was tested, with how many people, under which conditions and targets, and what was found.

| Key | Participants | Neon configuration | Targets / test | Viewing distance | Factors varied | Main accuracy result (Neon) | Factor findings (Neon) |
|---|---|---|---|---|---|---|---|
| `foucher2026neon` [V-PDF] | Dual-tracker: 32 recruited, 4 excluded → 28. Neon-only: 21 recruited, 1 excluded → 20. **Different people in the two setups** (p.3) | Personal offset from a single central target, dragged manually in Pupil Cloud (p.4) | 7×7 grid (49 targets, ±18.2° H, ±7.7° V) plus 13-point small grids; head yaw/roll; pursuit at 16–24°/s; free viewing; microsaccades; blinks; pupil (p.5) | 60 cm, 27″ screen (44.8° × 29.2°) (p.3) | IR from a concurrent EyeLink; time since offset correction; head yaw/roll | Neon-only large grid **1.45°** (IQR 1.12–1.75; H 0.89°, V 0.93°); RMS-S2S 0.097°; SD 0.431°. **With EyeLink IR present: 4.27°** (p.10) | **Time:** 1.51° at ~249 s (LMM: significant decrease) and 1.46° at ~319 s (n.s.) (p.10–12). **Head yaw:** systematic +0.6° H and −0.5° V offsets (p.13, p.15). **Head roll:** within ±1.5°, linear in roll angle (p.15). **Pursuit:** velocity 13.1°/s for 16–24°/s targets (p.12). **Microsaccades:** 0.35/s vs 2.01/s on EyeLink (p.12) |
| `baumann2026neonAccuracy` [V-PDF] (vendor) | Lab: **206** (18–85 y). Wild: **402** from 53 countries. Activities: 4 (p.5, p.8, p.12) | Uncalibrated, and additive offset fitted on the first 16 valid targets (lab) or on ¼ of clips within the central 30° (wild) (p.5, p.10) | Lab: random targets from a 4×4 grid over ~60° × 35°, button-press gamified, chinrest. Wild: predefined targets, deliberate re-seating of glasses between clips, 3 frames (p.3–4, p.8) | Lab: **0.4 m and 1.3 m**. Wild: **0.3–4.0 m** (p.3, p.8) | Distance (2 levels), demographics, field-of-view position, indoor/outdoor incl. direct sun, slippage states | Lab median per-subject: **2.1° (0.4 m) / 1.8° (1.3 m) uncalibrated; 1.4° / 1.3° with offset**; 94% of subjects < 2° at 1.3 m with offset (p.5–6) | **Demographics:** subgroup medians within tenths of a degree (p.6–7). **Field of view:** ~1° variation; best in upper centre (1.6° indoor / 1.9° outdoor uncalibrated); **lower field worse** (attributed to lids/lashes) (p.10). **Outdoor:** uniformly 0.4° worse; offset improves both by 0.6° (p.10). **Worst 5% of subjects:** 4–6° indoor / 5–7° outdoor uncalibrated (p.10). **Activity-weighted:** 2.1–2.4° uncalibrated, 1.6–1.7° with offset (p.13) |
| `alecka2026neon` [V-PDF] | **46** accuracy (22 ± 2 y); 32 stability (p.3) | IPD set plus one-point offset in the app, done on a **white** background (p.5) | 13 positions (19.7° H / 10.1° V spacing), 5 s each, white vs black background; gaze mapped with Reference Image Mapper (p.4–6) | **65 cm**, chin+forehead rest (p.5) | Eccentricity/position; background luminance | Overall **1.41° ± 0.92°** (Tobii Fusion 1.23° ± 0.79°; p < 0.001) (p.7) | **Position:** no effect (Friedman white χ² = 4.80, p = 0.964; black χ² = 13.89, p = 0.308) (p.9). **Background:** white 1.20° ± 0.72° vs black **1.63° ± 1.05°**, significant (Z = −4.092, p < 0.001) (p.7, p.10). **Stability:** BCEA 0.30 vs 0.28 deg², n.s. (p.10). Data loss observed but not quantified (p.12) |
| `salari2026pupilSize` [V-PDF] | **24** (17 m / 7 f, 27.3 y) (p.3) | Offset correction in the Neon Companion app (v2.8.37) (p.5) | Central target; 10 s bright / 10 s dark screen; 4 corner references (p.4–5) | **930 mm**, chinrest (p.3) | Pupil size via screen luminance (2.88 → 5.05 mm) (p.7) | Bright **1.36° ± 0.59°**, dark **1.41° ± 0.82°** (p.9, Table 2) | **Apparent gaze shift** between dark and bright: **0.94°** (d = 2.20), the smallest of all head-mounted trackers (Pupil Core 3.46°) (p.7). **Accuracy change:** n.s. for Neon (adj. p = 1.0, d = 0.07); all others except Tobii G2 changed significantly (p.7, p.9). **Precision** (STD, RMS-S2S): no consistent pattern for Neon. **Data loss:** median 0% in both conditions (p.10) |
| `pettenella2026slippage` [V-PDF] | **12** (33.3 y; 2 authors) (p.1) | IPD measured and entered; **no offset correction reported**; **no head strap** (p.3) | Single central target on a GlassesValidator poster; 10-s tasks: speak, raise eyebrows, scrunch nose, manual ~1 cm shifts (H/V/back-and-forth), walk/run/jump in place (p.2) | **1 m**, standing (p.2) | Measured 6DOF frame displacement (200 Hz motion capture) | 9-point validation **2.11° ± 0.39°**; baseline **2.15° ± 0.72°** (p.3, Table 2) | **Mean gaze offset by task:** speak 2.4°, eyebrows 2.8°, scrunch 3.0°, move H 3.5°, move V 2.9°, back-and-forth 2.6°, walk 2.2°, run 2.4°, jump 2.3° (p.3, Table 3). **Mean data loss:** 1.7–4.9% (p.3). **Displacement effect:** horizontal-shift task ε² = 0.50, KS D = 0.37; vertical offset vs vertical motion during nose scrunch \|r\| = 0.51 (p.4–6). Authors: Neon "< 3.5° in all tasks" (p.6). Tobii G3 < 2.5° throughout; VPS Lite up to 29.3° |
| `nolte2026bestPractices` [V-PDF] | **1** (p.2) | **Uncalibrated**; a pilot found "no significant difference" with vs without calibration (no statistics given) (p.7) | 10-point handheld target (12 cm), manually annotated; start and end of each 10-min segment; 650 validation points over 13 recordings (p.9, p.12) | **3 m**, outdoors (Limassol, summer) (p.9) | Time within segment; sun hat against glare (p.7) | Median **2.80°** (IQR 1.94–3.22) at start; **2.65°** (IQR 2.02–3.28) at end (p.12) | **Start vs end:** n.s. (Wilcoxon W = 30.0, p = 0.31) (p.12). **Heat:** devices overheated; one phone replaced (p.7) |

### Important reading notes for the table

1. **Baumann's distance claim is not data beyond 4 m.** `baumann2026neonAccuracy` states that results at 1.3 m are "indicative of gaze-estimation accuracy at all larger depths" because vergence changes little beyond that point (p.3, p.6). This is an argument, not a measurement. Their lab test used only 0.4 m and 1.3 m, and the in-the-wild set went up to 4.0 m (p.8). Our C2 sweep (1/2/4 m plus 5/8/12 m) and C1 far-field driving targets test exactly this extrapolation.
2. **Brightness and Neon accuracy: two papers disagree.**
   - `alecka2026neon` found Neon significantly worse on black backgrounds (1.20° vs 1.63°).
   - `salari2026pupilSize` found no accuracy change between bright and dark screens (1.36° vs 1.41°), but did find a 0.94° apparent gaze shift.
   - The setups differ: offset done on a white background at 65 cm with 13 positions (Alecka) vs a central target only at 930 mm with offset correction (Salari).
   - Our bright/dark experiment with measured pupil-size change speaks directly to this disagreement.
3. **Infrared (IR) interference.**
   - `foucher2026neon` attributes the 4.27° vs 1.45° gap to EyeLink IR, but the two numbers come from **different participant groups** (p.3, p.10).
   - The authors discuss sunlight and other IR sources as possible risks, but did **not test** them (p.16–18).
   - `park2026openEye` found ~90 Hz IR flicker from HMDs in the Neon signal and filtered it (p.5).
   - Our indoor/outdoor comparison is **not** an isolated IR test either; the contribution file says so explicitly.
4. **Head straps, offsets and comparability.**
   - `pettenella2026slippage` used no head strap and reports no Neon offset correction. Its 2.1–3.5° values are therefore closer to an "uncalibrated" baseline than Baumann's offset-corrected 1.3°.
   - `hooge2023robust` used head straps.
5. **The vendor report is not independent.** `baumann2026neonAccuracy` and `pfeffer2024neonPupillometry` are by Pupil Labs. Note that `alecka2026neon` and `foucher2026neon` both cite the Baumann report with year 2023, while our PDF is dated 13 Feb 2026 (Zenodo DOI 10.5281/zenodo.18504792). Check which version the bib entry should point to.

---

## 3. Other Neon studies (adjacent: not target-referenced angular accuracy)

| Key | Participants | Setting / test | What they found | What to cite it for |
|---|---|---|---|---|
| `maquiling2026vergencePupil` [V-PDF] | 8 (p.3) | Chinrest; physical near (≈0.25 m) and far (≈0.9 m) targets via beamsplitter; static vs luminance-modulated (p.3) | Near and far reliably separable by vergence. Pupil–vergence (PSA) slopes from ≈ −4 to +6 deg/mm under static light, varying in sign across participants and depths (p.4). The authors state this is **not** a validation of absolute vergence accuracy (p.5) | Pupil size is a wearer- and state-dependent confound in Neon. Supports our finding that wearer and condition responses differ |
| `niehorster2026slippage` [V-PDF] | 35 (p.7) | Motion capture of 4 glasses during 10 tasks; **"The eye tracking data are not included in this paper"** (p.6) | Natural-task slippage 1.25–1.42 mm / 0.57–0.62° on average across glasses (p.11). Neon: 1.42 mm (95th percentile 3.32 mm), 0.62° (95th percentile 1.43°) (p.13). Bayesian evidence against a difference between glasses (BF₀₁ = 18.3 position, 67.2 orientation) (p.12). Their 3-task battery overlaps natural slippage (> 0.931 position, > 0.894 orientation) (p.13) | Realistic slippage magnitudes. Paired with `pettenella2026slippage`, it links mm of slippage to degrees of error |
| `park2026openEye` [V-PDF] | 18 (p.7) | Neon module in Apple Vision Pro, XREAL Air 2 Ultra, Quest 3; custom 25-point polynomial calibration | ~90 Hz IR flicker from the headsets (p.5). Error 1.324° (AVP), 1.835° (XREAL) (p.11). Quest 3: 1.727° vs 2.281° for the NeonXR baseline (p.12) | Second evidence that external IR affects the Neon signal |
| `cui2025listeningEffort` [V-PDF partial] | 26 (p.2) | Neon + EyeLink DUO recorded at the same time; chin/forehead rest (p.3) | Both devices show reduced gaze dispersion and pupil dilation under difficult listening (p.2) | Neon dispersion is a usable relative measure in the lab. Target-referenced accuracy not found in our check |
| `karaer2026vrEyeTracker` [V-PDF partial] | 39; Neon paired n = 23 (p.1, p.4) | Pupillometry comparison | Bias −0.48 mm baseline, −0.56 mm peak constriction vs BulbiCAM (p.1) | Pupil only; not gaze accuracy |
| `pfeffer2024neonPupillometry` [V-PDF partial] (vendor) | 7, incl. 2 authors (p.4) | Head rotation tasks; motor rail displacing the module | Gaze-angle dependence of pupil size < 5% over the field of view (p.7); rail displacement 5 mm at 0.5 Hz (p.8) | Pupil-size robustness; motor-rail slippage method |
| `turuwhenua2026okn` [V-PDF partial] | 22 | OKN stimuli | Neon gaze output can produce false-negative OKN detections; video-based methods reduce them | Neon gaze signal limits for small, fast movements (consistent with Foucher's microsaccade result) |
| `xu2026signalConstruct` [V-PDF partial] | 40 pilots | **Real flight**, Cessna 172, five maneuvers | Neon at 200 Hz (p.4); eye tracking had a 99.9% worn-rate at 195 Hz effective sampling (p.10). Angular accuracy against targets not found in our check | Neon deployed in a real vehicle; availability only, not accuracy |

---

## 4. Other wearable accuracy and robustness studies (non-Neon precedents)

| Key | Participants | Devices | Targets / conditions | Distance | Main findings |
|---|---|---|---|---|---|
| `hooge2023robust` [V-PDF] | 4 (p.1) | Pupil Core, Pupil Invisible, SMI ETG2, SeeTrue, Tobii G2, Tobii G3 | Static target; stand → walk → skip → jump → stand; **head straps** (p.3–4) | 1.65 m (p.3) | All trackers recorded gaze during skipping and jumping. Accuracy worsened with more vigorous movement; largest error 5.8°, most errors < 3° (p.1) |
| `onkhar2024evaluating` [V-PDF] | 36 (Tobii G3: 33–34) (p.1, p.10) | Tobii G2, Tobii G3 | 9 printed dots at 15° eccentricity, with/without chinrest; walking along 21.7 m toward a bullseye (p.3–4) | Seated ≈ 1 m (1 m table against the wall, p.3); walking 21.7 m → 0 | **Tobii G3 mean (all dots):** chinrest 1.78°, no chinrest 1.60°, walking 1.74°. **Tobii G2:** 2.77°, 1.99°, 3.53° (p.10, Table 3). The chinrest hurt accuracy because it forces larger eye eccentricity. Accuracy was associated with self-reported workload, not with gender, contact lenses, eye colour or pupil size (p.11) |
| `macinnes2018wearable` [V-PDF] | **3** (p.12) | Pupil Labs 120 Hz, SMI ETG 2.6, Tobii G2 | Target grids at −10°, 0°, +10° | **1, 2, 3 m** (p.12) | Overall accuracy: Pupil Labs 0.84° (0.42), SMI 1.21°, Tobii 1.42°. Precision: 0.16° / 0.19° / 0.34° (p.18). Tracker × distance interaction F(4,54) = 5.07; differences largest at 3 m (p.19–20) |
| `niehorster2024glassesvalidator` [V-PDF partial] | 61 with one tracker; software tested on 6 trackers (p.1) | Wearable trackers | Printed poster with ArUco markers and fixation targets | Estimated by the software | Validation takes about 1 minute (p.1). The [S] summary adds: a "keep head still" instruction did not change accuracy or precision, and assuming a fixed distance adds small errors |
| `ehinger2019testBattery` [V-PDF] | **15** (11 excluded) (p.4) | Pupil Labs (pre-Neon) vs EyeLink 1000 | Comprehensive battery (grid, pursuit, blinks, etc.) | 60 cm (p.4) | Accuracy 0.82° (Pupil Labs) vs 0.57° (EyeLink) (p.1). **The summary file misstates these numbers** (see top) |
| `velisar2024noise` [V-PDF partial] | see summary | Pupil Core | Walk/run/jump with artificial eyes; calibration patterns for 3D gaze | — | In jumping, eye-camera motion can account for up to ~20% of detected eye motion (p.21). The [S] summary also reports gaze depth underestimation |
| `buter2024eyeTracking` [V-PDF partial] | 10 (p.1) | Pupil Core vs Tobii G3 | AprilTag grid at a surgical console | Unknown; angular accuracy "couldn't be assessed" (p.2) | Both around 4 cm error after calibration; Tobii more stable over time (p.1) |

---

## 5. Methods and factor background (cite selectively)

| Key | Status | What it is | Why it is relevant |
|---|---|---|---|
| `niehorster2026fundamentals7` | [V-PDF partial] | Definitions of inaccuracy, imprecision and data loss; notes Neon needs no calibration but can still be validated (p.5) | Terminology for keeping accuracy, bias, precision and dispersion separate (required by our contribution file) |
| `choe2016pupilSize` | [V-PDF] | 23 observers, desktop EyeLink. Pupil-size dynamics bias gaze; regressing out pupil size cut the SD of gaze positions by 31.6 ± 24.1% (p.7) | Classic pupil-size artefact; precedent for correcting it |
| `holmqvist2022headMovements` | [V-PDF partial] | Five P-CR (non-wearable) trackers; small head movements raise noise level and colour (p.1) | Separating sensor noise from movement-induced noise (precision vs dispersion) |
| `blignaut2014dataQuality` | [V-PDF partial] | 71 participants, Tobii TX300 remote. Operating distance had the largest effect; Asian participants had worse accuracy and precision (p.1) | Participant- and distance-dependent data quality (remote tracker) |
| `santini2019grip` | [V-PDF partial] | Slippage-robust, glint-free gaze estimation; 109-subject museum dataset; error reduced by > 43% vs polynomial regression (p.1, p.4) | Correction precedent (C3) |
| `kar2020mlgaze` | [V-PDF partial] | 20 participants, desktop and tablet; ML models of error sources (distance, head pose, platform pose) (p.2) | Error-factor modelling precedent (C3) |
| `kasprowski2019implicitCalibration` | [S] | Implicit calibration from probable fixation targets (saliency/expert-defined) | Precedent for correcting from natural targets (C3: driving-derived offsets) |
| `calvi2023comparing` | [V-PDF partial] | Tobii glasses in real urban driving (14) vs simulator (18), Rome (p.1, p.2) | Wearable eye tracking in real driving; compares behavioural parameters, not accuracy |

---

## 6. Factor-by-factor synthesis (for writing the subsection)

| Factor | What prior work established (with key) | What remains open, relevant to us (C1/C2/C3) |
|---|---|---|
| **Baseline Neon accuracy, lab** | 1.3° (offset) / 1.8° (uncalibrated) at 1.3 m, N = 206 (`baumann2026neonAccuracy`). 1.45° with offset, N = 20 (`foucher2026neon`). 1.41°, N = 46 (`alecka2026neon`). ~2.1° with IPD only, N = 12 (`pettenella2026slippage`) | All are screen or poster targets at ≤ 1.3 m in the lab |
| **Viewing distance** | Neon: only 0.4 vs 1.3 m (2.1° vs 1.8° uncalibrated) (`baumann2026neonAccuracy`), plus 0.3–4.0 m pooled in-the-wild without a per-distance breakdown (p.8–9). Non-Neon: 1–3 m, N = 3 (`macinnes2018wearable`) | A systematic distance sweep beyond 4 m on Neon was not found. Our 1/2/4 m (+5/8/12 m) sweep and 7–107 m driving targets |
| **Eccentricity / field position** | No position effect over 13 screen positions (`alecka2026neon`). ~1° variation over the field of view with the lower field worse (`baumann2026neonAccuracy`) | Our lower-image-region jitter and accuracy findings agree with Baumann's lower-field observation. Analyse elevation separately from eccentricity |
| **Brightness / pupil size** | No accuracy change but a 0.94° apparent shift (`salari2026pupilSize`). Worse on black background (`alecka2026neon`). Wearer-specific PSA slopes (`maquiling2026vergencePupil`) | Conflicting prior results. Our measured pupil change with bright/dark screens adds evidence |
| **Indoor / outdoor, sunlight** | Outdoor uniformly 0.4° worse (vendor, `baumann2026neonAccuracy`). Outdoor 2.65–2.80° median, n = 1, 3 m (`nolte2026bestPractices`) | No independent multi-participant indoor/outdoor Neon comparison was found |
| **External IR** | Concurrent EyeLink IR degraded Neon to 4.27° (between-group comparison) (`foucher2026neon`). HMD IR flicker (`park2026openEye`) | Sunlight-IR effect untested in these papers. Our outdoor test is not an IR isolation |
| **Slippage / body motion** | Neon < 3.5° mean across facial, induced and locomotion tasks without straps (`pettenella2026slippage`). Slippage magnitudes (`niehorster2026slippage`). In-the-wild re-seating included (`baumann2026neonAccuracy`). Head yaw offsets of +0.6°/−0.5° (`foucher2026neon`). Non-Neon motion: `hooge2023robust`, `onkhar2024evaluating` | No study measured Neon accuracy in a **moving vehicle** against real targets |
| **Smooth pursuit** | Pursuit velocity underestimated (13.1°/s vs 16–24°/s) and larger catch-up saccades on Neon (`foucher2026neon`) | Target-relative pursuit dispersion vs accuracy not reported in these papers. Our ~3× dispersion result (one participant) |
| **Temporal stability / repeats** | Small change over ~5 min (`foucher2026neon`). No start–end difference over 10 min outdoors, n = 1 (`nolte2026bestPractices`) | Between-session and re-wearing stability on Neon was not found |
| **Wearer dependence** | Demographic subgroups within tenths of a degree (`baumann2026neonAccuracy`). Worst 5% of subjects at 4–7° (`baumann2026neonAccuracy`). Participant-specific PSA (`maquiling2026vergencePupil`) | Per-wearer offsets and their transfer (our C1/C3) |
| **Offset correction** | Single offset improves ~0.5–0.6° (`baumann2026neonAccuracy`). Used by `foucher2026neon`, `alecka2026neon`, `salari2026pupilSize` | Offsets estimated from **natural driving references**, and how many references are needed, was not found (C3) |
| **Real vehicles** | Neon used in real flight, availability only (`xu2026signalConstruct`). Tobii glasses in real driving, no accuracy (`calvi2023comparing`) | No paper here benchmarks wearable gaze accuracy against known targets while driving (C1) |

---

## 7. Excluded or tool-only papers (reasons)

| Key | Reason |
|---|---|
| `chu2026pyneon`, `saxena2025socialEyes`, `niehorster2025gazeMapper`, `zhang2026pupeyes`, `fuhl2024pistol`, `niehorster2025fundamentals` | Software tools or methods. They do not test accuracy (cite only if we use the tool; `gazeMapper` is used by `pettenella2026slippage`) |
| `nagy2024takeover` | Neon used in a driving simulator for behaviour; the summary says no accuracy values are reported [S] |
| `holmqvist2017common` | The full text is not available (the summary itself says it is an unpublished preprint); do not cite numbers |
| `park2026motionCorrected` | fMRI eye tracking; not wearable |
| Driving-attention, saliency and gaze-guided learning papers (e.g. `palazzi2019dreyeve`, `xia2018bdda`) | Not about measurement quality of the wearable gaze signal |

---

## 8. Verification log

- **Full text read (accuracy sections):** `baumann2026neonAccuracy`, `alecka2026neon`, `foucher2026neon` (methods, results, discussion), `pettenella2026slippage`, `salari2026pupilSize` (methods, results).
- **Targeted extraction of the cited numbers:** `nolte2026bestPractices`, `maquiling2026vergencePupil`, `niehorster2026slippage`, `park2026openEye`, `hooge2023robust`, `onkhar2024evaluating`, `macinnes2018wearable`, `ehinger2019testBattery`, `choe2016pupilSize`, `santini2019grip`, `velisar2024noise`, `xu2026signalConstruct`, `calvi2023comparing`, `cui2025listeningEffort`, `karaer2026vrEyeTracker`, `pfeffer2024neonPupillometry`, `buter2024eyeTracking`, `blignaut2014dataQuality`, `holmqvist2022headMovements`, `kar2020mlgaze`, `niehorster2026fundamentals7`, `niehorster2024glassesvalidator`.
- **Summary only:** `kasprowski2019implicitCalibration`, `nagy2024takeover`, and the [S]-marked parts of the tables above.
- **Text extraction method:** pypdf. Page indices refer to the PDF files in `phd-literature/papers*/`.
