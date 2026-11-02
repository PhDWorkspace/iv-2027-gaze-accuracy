# Related Work: In-Situ Gaze Correction and Quality Assessment

**Created:** 2026-11-03
**Purpose:** Source material for the *In-Situ Gaze Correction and Quality Assessment* part of the IEEE IV 2027 paper. Papers are ranked by how directly they bear on our contributions C1–C3 in `contribution_in_situ_gaze_correction_quality_assessment.md`:

- **C1:** sparse, condition-matched in-situ offset correction.
- **C2:** person- and condition-specific correction, plus calibration checks.
- **C3:** multimodal, task-aware suitability flags.

**Source pool:** All 136 summaries in `phd-literature/summaries/` were screened. 38 candidate PDFs were then text-extracted and checked; Barz 2016 is image-only and was read page by page. Every key below exists in `phd-literature/bib/references.bib`; all keys were checked.

## How to read this file

- **Verification status**
  - **[V-PDF]**: every number and claim in the entry was checked against the full text of the PDF in `phd-literature/papers/` or `papers-inbox/` during this review.
  - **[S]**: from our summary only; check before citing.
  - All entries in this file are [V-PDF] unless marked otherwise.
- **Page numbers:** `p.N` is the page index of the PDF file. It may differ from the printed page.
- **Absence claims:** "Not found" means we did not find it in the PDF text we checked. It does **not** mean the authors did not do it.
- **Scope of the evidence:** every statement is about the cited paper only. Our own numbers come from the contribution file and are labelled **"Ours"**.
- **Preprint warning:**
  - `park2026motionCorrected`: the local PDF is the bioRxiv preprint (posted 2025-03-27), but the bib entry points to *Nature Communications* 2026. The numbers here come from the preprint.
  - `macinnes2018wearable`: the local PDF is a bioRxiv preprint (2018).

### Summary errors and ambiguities found during verification

| Key | Summary says | PDF says | Action |
|---|---|---|---|
| `kasprowski2019implicitCalibration` | Headline "2.43 % of screen (~1.7°/1.4°) on the Pupil Labs headset, approaching explicit calibration (2.26 %)" | 2.43 % used **ground-truth (GT) targets derived from real human fixations** (Table 5, p.19). The best **fully automatic** saliency model (RARE2012) gave **3.27 %** (Table 3, p.18). | When citing "implicit calibration ≈ explicit calibration", say the targets came from human fixation data. |
| `chang2019salgaze` | Baseline "4.07 cm for the iPad Air 2" | 4.07 cm is the baseline on the **GazeCapture** test split (Table 1, p.5). On the authors' own data from **9 participants**, the baseline is **4.38 ± 1.18 cm → 3.32 ± 0.77 cm** (24.20 %) (Table 2, p.6). | Use the Table 2 numbers. |
| `macinnes2018wearable` | "Distance-matched 9-point calibration maintained accuracy at 3 m, whereas Tobii's 1-point calibration degraded" | The calibration procedure is **confounded with the device**. Each tracker used its own vendor procedure (p.10–11), and calibration distance was never varied independently. "Calibration procedures will only yield accurate data at the distance at which calibration occurs" is the authors' **interpretation** (p.25). N = 3 (p.12). | Cite as suggestive only. |

---

## 1. Ranked overview

**Overlap:**
- **Direct:** same operation and close setting.
- **Partial:** same operation, different setting, or the reverse.
- **Method:** a protocol or metric to adopt.
- **Background:** context only.

| Rank | BibTeX key | Contribution | What it actually does | Setting / device | Independent people | Overlap |
|---:|---|---|---|---|---|---|
| 1 | `jia2018gaze` | C1 | Online offset correction using detected **stop signs** as calibration targets | Screen video (EyeLink 1000) + **front-passenger** in a moving car (SMI glasses) | 8 + 3 | **Direct** (closest precedent) |
| 2 | `baumann2026neonAccuracy` | C1, C2 | **Neon** uncalibrated vs mean-offset-corrected accuracy; offset fitted on held-out clips | Lab screen at 0.4 m and 1.3 m; in-the-wild up to 4.0 m, indoor/outdoor (vendor report) | 206 + 402 | **Direct** (same device, same correction) |
| 3 | `kasprowski2019implicitCalibration` | C1 | Implicit calibration from probable fixation targets; error vs number of fixations | Screen viewing; Pupil Labs headset + remote tracker | 12 / 29 / 20 | **Partial** (implicit references, screen only) |
| 4 | `barz2016prediction` | C1, C2 | Measures the effect of calibration-to-use **distance mismatch**; SVR predicts error from geometry | Chin rest, PUPIL monocular, display at 0.5–3 m | 12 recruited (10–11 analysed) | **Partial** (supports condition-matching) |
| 5 | `kar2020mlgaze` | C2 | Regression of gaze error on gaze angles under head/platform conditions; simple vs complex models | Remote trackers, chin rest, desktop/tablet | 20 | **Partial** (simple model ≈ best) |
| 6 | `jamalifard2026fiud` | C3 | Image-quality factors (blur, light, eye openness …) → predicted error; validated against true angular error | Appearance-based gaze datasets (ETH-XGaze, Gaze360, MPIIFaceGaze) | dataset-level | **Partial** (quality-vs-error validation we lack) |
| 7 | `niehorster2026fundamentals7` | C3, C1 | Defines data-quality measures; quality is "good enough" only relative to the research question | Methods tutorial | — | **Method** |
| 8 | `kotseruba2024dataLimitations` | C3 | Audits driver-attention datasets: blinks/saccades share, in-cabin fixations, projection outliers | DR(eye)VE, BDD-A, LBW, MAAD | — | **Partial** (task-suitability argument) |
| 9 | `santini2019grip` | C2 | Slippage-robust gaze estimator; calibrate at start, evaluate ~19 min later | Museum visit, Pupil headset | 78 analysed (109 recruited) | **Partial** (temporal hold-out design) |
| 10 | `foucher2026neon` | C2 | **Neon** one-point offset correction; accuracy decay over time; head-yaw/roll effects | Lab screen | 20 Neon-only (21 recruited); 28 dual-tracker (32 recruited) | **Partial** (Neon calibration health) |
| 11 | `nagpure2025learningToAdapt` | C1, C2 | Few-shot in-vehicle personalisation (one sample per gaze zone) + self-supervised adaptation | Remote driver-facing camera, IVGaze | 125 subjects (3-fold) | **Partial** (in-vehicle few-shot, other sensor) |
| 12 | `macinnes2018wearable` | C1 | Accuracy of 3 wearables at 1–3 m with vendor calibration procedures | Indoor wall targets | **3** | **Partial** (suggestive only) |
| 13 | `chang2019salgaze` | C1 | Saliency-based implicit personalisation; gain vs amount of data | iPad front camera | 9 | **Partial** |
| 14 | `stapel2022driverPerception` | C2, C3 | On-road gaze–object analysis; recalibration rule; horizontal-only gaze to avoid pitch artefacts | Real driving, remote Smart Eye | 13 | **Partial** |
| 15 | `kasahara2022lookBothWays` | C3 (C4) | On-road wearable gaze used as ground truth; scene–gaze self-supervision | Real driving, Tobii Pro Glasses | 28 | **Partial** |
| 16 | `gopinath2021maad` | C1, C2 | Corrects **simulated** noise and miscalibration using scene saliency | Lab, chin rest, driving videos | 23 | **Partial** |
| 17 | `fuhl2024pistol` | C3 | Offline eye-feature tool: eyelids, eye opening, validity-based rejection | Pupil Invisible / Look! in the wild | 4 | **Partial** (eye-state signals) |
| 18 | `choe2016pupilSize` | C2 | Regresses out pupil-size-induced gaze error | Desktop EyeLink, chin rest | 23 | Background (condition-specific correction) |
| 19 | `park2026motionCorrected` | C2 | Corrects gaze drift using auxiliary head-motion signals | fMRI, camera eye tracker | 20 included | Background (auxiliary-signal correction) |
| 20 | `pettenella2026slippage` | C2 | **Neon** gaze offset under measured frame slippage | Standing, poster at 1 m | 12 | Background (why offsets change) |
| 21 | `salari2026pupilSize` | C2 | **Neon** apparent gaze shift from pupil size after app offset correction | Lab screen, chin rest | 24 | Background |
| 22 | `alecka2026neon` | C2 | **Neon** offset set on a white background, accuracy tested on white and black | Lab screen, chin rest | 46 | Background (condition mismatch) |
| 23 | `nolte2026bestPractices` | C1 | **Neon** used uncalibrated after a pilot; start/end validation outdoors | Outdoor walking | **1** | Background |
| 24 | `zhang2026pupeyes` | C3 | Deblinking removes eyelid opening/closing samples (pupil data) | Desktop EyeLink/Tobii | — | Background |
| 25 | `zhang2026gazeifyVoiceify` | C1 (reference generation) | Gaze + voice object referencing; voice corrects selection errors | Quest Pro passthrough, tabletop | 23 | Background (gaze+speech grounding) |
| 26 | `lai2026glanceSay` | C1 (reference generation) | Gaze grounds objects, speech specifies actions | Meta ARIA, tabletop | 16 | Background |
| 27 | `niehorster2024glassesvalidator` | C1 | Printable poster + software for wearable accuracy/precision | Poster at known distance | 61 (one tracker) | **Method** (lab reference) |
| 28 | `hu2022data` | C1 | "Calibration-free" learned gaze–scene mapping | VR simulator (HTC Vive Pro Eye) | see entry | Background (term clash) |
| 29 | `saxena2025socialEyes`, `park2026openEye`, `xu2026signalConstruct`, `contreras2026laia`, `lee2026edith` | C1/C3 | Practical Neon offset steps, exclusion rules, availability-type quality, Whisper use | Various | — | Background mentions only |

---

## 2. Direct and strongest partial precedents (ranks 1–11)

### 1. `jia2018gaze`: Gaze Tracking Accuracy Maintenance Using Traffic Sign Detection (AutomotiveUI 2018 WiP) [V-PDF]

**What it does:**
- A traffic-sign detector (ICF) runs on a scene camera.
- When the gaze lies within **100 px (~2.5°)** of a detected target, the method **assumes** the person is fixating or pursuing it (p.2–3).
- Gaze clusters use a 50 px dispersion threshold and at least 20 samples.
- A distance-weighted offset is averaged over a **3-frame sliding window** and subtracted from the gaze (p.3, Eqs. 1–2).

**How it was tested (p.3–4):**
- Stimuli were **stop signs that participants were instructed to pursue**.
- **Exp. 1:** 8 participants, a driving video on a 17″ monitor, EyeLink 1000, 9-point calibration. Offsets from trial 1 were applied to trial 2. Error fell **77 %, from 80.0 to 18.3 px**.
- **Exp. 2:** **3 participants in the front passenger seat** of a car at ~30 mph, SMI glasses at 120 Hz, 3-point calibration. Error fell **63.3 %, from 26.0 to 9.6 px**.
- Invalid gaze points were disregarded (Fig. 7 caption, p.4).

**Limitations (do not overstate):**
- No natural target inference: participants were told to pursue the stimuli.
- Exp. 2 used passengers, not drivers. The people were 3.
- Errors are in **pixels**, not angles, for the in-car experiment.
- For Exp. 2, the paper does not say whether the correction data and test data were separated.
- Target association was not independently verified.
- The "near-constant drift" conclusion rests on short trials (p.4).

**Overlap with us:** This is the precedent for "road objects as in-situ references for offset correction". We must not claim that idea.

**Our difference** (Ours, from the contribution file):
- Fixations are **announced by the driver** and targets are **manually reviewed**.
- Error is measured in **angular units** on **held-out driving scenes**.
- We explicitly **compare lab and in-situ reference sources** and vary the **number and layout of references**.
- Our evaluation still uses only two participants and a scene-level split.

---

### 2. `baumann2026neonAccuracy`: Neon Accuracy Test Report (Pupil Labs, vendor-authored) [V-PDF]

**What it does:** Measures Neon accuracy without calibration and after the Companion-app **additive offset**. The report says this offset can account for, e.g., angle kappa (p.3).

**Offset protocol** (relevant to our median-offset baseline):
- **Lab:** the offset is the **mean error vector over the first 16 valid targets** of a trial, applied to the remaining estimates (p.5).
- **In-the-wild:** the offset is fitted on **one quarter of each subject's clips**, using samples within the central 30°, and evaluated on the other three quarters. Calibration and validation clips came from different slippage states, and the same offset was used indoors and outdoors (p.10).

**Quality gates in the evaluation (p.4–5):** A target was discarded if:
- the gaze SD exceeded 1° (not fixating), or
- the target location SD in the scene camera exceeded 0.25° (head motion), or
- a blink was detected in the window.

4.8 % of targets were removed for incorrect fixation and 5.6 % for head motion (p.5).

**Results:**
- **Lab (N = 206):** median 2.1° (0.4 m) and 1.8° (1.3 m) uncalibrated → **1.4° and 1.3° with offset** (p.5).
- **In-the-wild (N = 402):**
  - Offset correction improves indoor and outdoor accuracy by 0.6° (p.10).
  - The lowest-accuracy 5 % of subjects have 4–6° indoors and 5–7° outdoors uncalibrated, improving to 2.5–4° and 3.5–5° (p.10).
- **Activity "effective accuracy"** (2.1–2.4° → 1.6–1.7°, Table 1, p.13) is a **weighted computation, not a measurement during those activities** (p.13).

**Limitations:**
- Vendor-authored.
- No driving.
- Target distances up to 4.0 m only (p.8).
- The offset is a **mean** fitted from dedicated target fixations, not from naturally occurring references.

**Overlap with us:** Establishes that a simple per-wearer offset helps Neon and that a disjoint-clip hold-out is feasible.

**Our difference:**
- We use **median** offsets from **few in-situ driving references**.
- We compare these against **lab chessboard offsets** on the **same held-out driving targets**.

Our Neon "raw" baseline also removes the app offset first (contribution file), so our numbers are not directly comparable to Baumann's "uncalibrated".

---

### 3. `kasprowski2019implicitCalibration`: Implicit Calibration Using Probable Fixation Targets (Sensors 2019) [V-PDF]

**What it does:**
- Extracts discrete probable fixation targets (PFTs) from saliency maps, human fixation maps (GT) or expert labels.
- Searches for the gaze-to-PFT mapping (genetic or incremental search with mapping-comparison functions).
- Fits a polynomial mapping from **raw eye-camera features** to screen coordinates.

This **calibrates the estimator**. It is not a post-estimation offset.

**How it was tested:** 12 participants with a Pupil Labs headset viewing images on a 21″ screen, heads free (p.14). There were also 29 and 20 participants with a remote Eye Tribe tracker. The ground truth was user-clicked 9-point reference screens (p.14–15).

**Results:**
- Headset, classic explicit calibration: **2.26 %** of scene size (Table 2, p.17).
- PFT with GT targets: 2.59 %; best fusion with GT targets: **2.43 %** (Tables 3 and 5, p.18–19).
- Best fully automatic saliency target set (RARE2012): **3.27 %** (Table 3, p.18).
- Conversion to degrees uses ×0.7 (horizontal) and ×0.53 (vertical) (p.15).
- With the incremental algorithm, error **stabilises after ~50 fixations (20–30 s)** (p.22, Figs. 9–10).

**Limitations stated by the authors (p.23–24):**
- Accuracy drops toward screen edges because targets cluster centrally.
- Implicit errors remain "significantly higher" than classic calibration.
- Screen-only; no driving, outdoor or wearable-motion conditions tested.

**Overlap with us:** The reference-count question (how many natural references are enough).

**Our difference:**
- Physical road targets, assigned by announcement and human review.
- Angular evaluation on held-out driving scenes.
- Our "one scene already helps" finding is about **offset**, not a full mapping.

---

### 4. `barz2016prediction`: Prediction of Gaze Estimation Error for Error-Aware Gaze-Based Interfaces (ETRA 2016) [V-PDF, read as images]

**What it does:** Measures how calibration coverage and **calibration-vs-recording distance** affect a monocular PUPIL head-mounted tracker. It also models display-mapping error and trains RBF-SVR models to predict x/y error.

**Evidence:**
- 12 participants recruited, with chin rest; 10 analysed for extrapolation and 11 for parallax (p.2).
- **Parallax:** mean error **1.68° at 0 cm** calibration–recording distance difference, **1.9° at ±50 cm**, **2.13° at ±100 cm** and **2.44° at ±150 cm** (Table 1, p.2). The ANOVA is significant (p.3).
- Combined model RMSE: **0.86° (x)** and **0.52° (y)**. Baselines: a constant 0.6° and the measured mean 1.26°. Validation used 50 repeated random 70/30 splits (p.3).

**Limitations:**
- Chin rest, display targets, random splits within the same datasets.
- No adaptive interface was tested.
- The authors list slippage, motion blur and a joint x/y model as future work (p.4).

**Overlap with us:** Direct support for the claim that **calibration under different operating conditions (distance) transfers imperfectly**. This motivates condition-matched references.

**Our difference:** We test transfer from near-field lab boards to **far road targets in real driving**, not 0.5–3 m display distances.

---

### 5. `kar2020mlgaze`: MLGaze (Vision 2020) [V-PDF]

**What it does:**
- 20 participants with Tobii EyeX 4C and Eye Tribe remote trackers, chin rest and 9-point calibration (p.4).
- Distance, head pose and tablet pose were varied one factor at a time.
- Gaze error was regressed on gaze angle, yaw and pitch.

**Results (Table 8, p.22):**
- ElasticNet had the lowest RMSE.
- **Plain linear/ridge models were nearly identical** (e.g., desktop neutral 2.24 vs 2.25).
- Polynomial and neural-network models were often **worse** (e.g., polynomial 7.48 and NN 4.01 vs linear 2.24 for desktop neutral).

**Limitations:**
- Remote trackers, chin rest, single-factor conditions.
- Predicts error magnitude, not signed bias.
- Augmentation was used for classification. The independence of train and test is not something we could fully audit from the text.

**Overlap with us:** Supports our **negative finding** that a more complex per-sample ridge model did not beat the median offset. Simple models are a strong baseline.

---

### 6. `jamalifard2026fiud`: Factor-Informed Uncertainty Distillation (ETRA 2026) [V-PDF]

**What it does:**
- A gradient-boosting "teacher" predicts angular error from **image-quality factors**: illumination, **sharpness/blur**, geometry, head pose, **eye aspect ratio / pupil visibility** (p.2).
- A ResNet-18 student distils this into a single-pass uncertainty head.

**Evidence:**
- **Spearman ρ between predicted uncertainty and true error:**
  - Gaze360: **0.498** (vs 0.324 NLL)
  - ETH-XGaze: **0.132** (vs 0.119)
  - MPIIFaceGaze: 0.168 (Table 3, p.5)
- AUSE: 7.39° vs 9.09° on Gaze360 (Table 4, p.5).

**Limitations (p.5):**
- Evaluated only on samples where landmark detection succeeded (93.3–97.5 %), which may bias toward "detectable" cases.
- Subject-specific error is weakly captured.
- Training needs ground-truth error.
- Appearance-based webcam/face images, not a wearable eye tracker.
- Even the best rank correlations are moderate.

**Overlap with us:** The closest example of **validating quality signals against measured angular error**, which our C3 explicitly has **not** done. Cite it to frame that gap honestly. Do not claim our gates predict error.

---

### 7. `niehorster2026fundamentals7`: The fundamentals of eye tracking, Part 7: Determining data quality (BRM 2026) [V-PDF]

**Use for:**
- The definitions of inaccuracy, imprecision and data loss.
- Data loss: up to ~10 % can be expected from blinks alone (p.11).
- The key framing for C3: whether data quality is "good enough" "depends on the study's context, including the question being asked …", quoting McConkie (1981) that it is "not appropriate to adopt standards concerning what is acceptable data" (p.4).
- An example of a task decision driven by wearable inaccuracy of **1.73–3.37°**, cited from Hessels et al. (p.2).

**Overlap with us:** Supports **task-relative suitability** rather than universal valid/invalid labels.

---

### 8. `kotseruba2024dataLimitations`: Data Limitations for Modeling Top-Down Effects on Drivers' Attention (IV 2024) [V-PDF]

**Evidence (p.4–5):**
- **Blinks and saccades** make up **27 %** of DR(eye)VE and **18 %** of MAAD data. The authors argue they add noise if not removed.
- **In-cabin fixations** are **3 %** in DR(eye)VE (0–10 % per video) and count as noise for scene saliency. The authors also note that in-vehicle gaze "may also contain useful information" for other tasks (p.4–5).
- Homography projection from head-mounted scene video to the car camera:
  - Median error mostly within 20 px.
  - **>13 % of frames are outliers**, half of them >200 px.
  - Errors are worse at night and in rain, and at high horizontal eccentricity (p.4).

**Limitations:** A dataset audit. The projection errors concern **cross-camera mapping**, not eye-tracker angular error.

**Overlap with us:** Strong support for C3's framing:
- cockpit gaze is **unsuitable for scene supervision but not invalid**;
- saccade and blink handling is a task decision.

---

### 9. `santini2019grip`: Get a Grip (ETRA 2019) [V-PDF]

**What it does:** A slippage-robust, glint-free gaze **estimator** (it changes the estimation model, not a post-hoc offset).

**Evaluation design:**
- Calibration from a marker collection at the start of a museum visit.
- Evaluation on a second collection **after ~18.8 min (SD 8.83)** of free roaming (p.4–5).
- 78 analysed of 109 recruited (31 excluded) (p.5).
- Median per-participant offset **5.66° (polynomial fit) → 3.18° (Grip)**, a 43.8 % reduction (p.6).
- For about half the participants, little difference, likely because they had little slippage (p.6).
- The authors report Pupil's confidence threshold (0.6) as a sample-quality heuristic (p.5).

**Overlap with us:** A precedent for **temporal/session hold-out** evaluation that our scene-level split lacks. It also shows that wearer–frame configuration changes drive error (C2).

---

### 10. `foucher2026neon`: Independent Comparative Evaluation of the Neon (Collabra 2026) [V-PDF]

**Offset method (p.4):**
- One-point **manual** offset in Pupil Cloud: the gaze circle is dragged onto a central target.
- The fixation used was the last central fixation of the validation procedure.
- So the offset and the validation are not fully independent.

**Results:**
- Groups: dual-tracker 32 recruited, 4 excluded; Neon-only 21 recruited, 1 excluded (p.3).
- **Neon-only accuracy** 1.45°, versus 4.27° in the dual-tracker setup that the authors attribute to EyeLink IR interference. These come from different participant groups (p.1, p.10).
- Accuracy over time: **1.45° → 1.51° (+4 %)** after continued use (p.11).
- During head yaw (Neon-only): a consistent horizontal offset of about +0.6° and a vertical offset of about −0.5° (p.13).
- Head roll (Neon-only): within ±1.5° (p.15).

**Overlap with us:** Independent evidence that a per-wearer Neon offset is small but useful, and that drift over minutes was small in the lab. Our in-car calibration-health check is **not** evaluated anywhere in this literature.

---

### 11. `nagpure2025learningToAdapt`: Test-Time Personalized Gaze Estimation for In-Vehicle Scenarios (IV 2025) [V-PDF]

**What it does:**
- Adapts an appearance-based driver gaze model (remote face camera).
- Self-supervised test-time adaptation, then fine-tuning on **one sample per gaze zone** (p.5).

**Evidence (IVGaze, 44,705 images from 125 subjects, 3-fold subject split, p.4):**

| Configuration | Mean angular error |
|---|---|
| Unadapted baseline | 6.78° |
| Zone fine-tuning only | 6.13° |
| Self-supervised adaptation only | 6.72° |
| Combined | **6.00°** |

Source: Table, p.5.

**Limitations:**
- Errors are ~6°, an order of magnitude above wearable-tracker accuracy.
- The setup phase needs deliberate zone looks.
- No variance across folds reported (not found).

**Overlap with us:** An IV-venue precedent that a **handful of in-vehicle reference looks** personalises gaze. Different sensor and correction type.

---

## 3. Supporting precedents (ranks 12–29)

**`macinnes2018wearable`** [V-PDF, preprint] (C1):
- **N = 3** (p.12); Pupil Labs, SMI and Tobii G2 at 1/2/3 m with vendor calibrations (p.10–11).
- The authors interpret their results as calibration being accurate only at the calibrated distance (p.25).
- Device and calibration procedure are confounded, so cite this only as suggestive support for condition-matched calibration.

**`chang2019salgaze`** [V-PDF] (C1):
- 9 participants × 10 sessions on an iPad (p.5).
- Saliency-based fine-tuning: 4.38 → 3.32 cm (24.2 %).
- Gains grow with data: 1 session 14.8 %, 8 sessions 22.8 % (Tables 2–3, p.6).
- Testing used the point phase of all 10 sessions, which includes sessions whose video phase was used for fine-tuning (p.6). This is not a fully unseen-session test.

**`stapel2022driverPerception`** [V-PDF] (C2/C3):
- Real urban driving, 13 drivers (p.6).
- Remote Smart Eye calibration "typically resulted in 1.2° accuracy and was repeated when accuracy exceeded 2°" (p.6). This is a simple calibration-health rule.
- Gaze analysis was limited to the **horizontal component** to reduce artefacts from vehicle pitch (p.4). This is a task-motivated data restriction.

**`kasahara2022lookBothWays`** [V-PDF] (C3/C4):
- 28 drivers, 6.8 h of public-road driving.
- Tobii Pro Glasses gaze is registered to the car camera by feature homography and used as **ground truth** (p.6–7).
- Filtering removes missed gaze registrations, missed face detections and dropped frames (p.7).
- No glasses-accuracy check was found.
- The self-supervised scene–gaze consistency gives only small gains: e.g., 6.8° → 6.5° at the 20/60/20 split (Table 2, p.12).

**`gopinath2021maad`** [V-PDF] (C1/C2):
- 23 subjects, chin rest, 9-point calibration, watching driving videos in the lab (p.6).
- Scene saliency is used to recover gaze from **synthetically** added noise and **synthetic** affine miscalibration (p.8–9).
- It does not evaluate real calibration error.

**`fuhl2024pistol`** [V-PDF] (C3):
- An offline tool for Pupil Invisible and Look! (p.1).
- Provides eyelids, **eye opening** and eye-movement classes including blink; frames where features are invalid while the eye is open are marked as errors (p.4).
- Evaluated with **4 subjects** on feature-detection and movement-classification accuracy (p.2, p.9–10).
- Angular gaze accuracy against targets was not found.

**`choe2016pupilSize`** [V-PDF] (C2):
- 23 observers, EyeLink, chin rest (p.1–2).
- Regressing out pupil size substantially improved accuracy and reliability (abstract, p.1).
- A precedent for **condition-specific post-hoc correction**; lab only.

**`park2026motionCorrected`** [V-PDF, preprint] (C2):
- fMRI: calibration error 0.435° vs validation error **7.093°** caused by head drift (p.6).
- Regression on head-motion parameters reduces error to **0.41°** (p.11); 20 participants included (p.20).
- Analogue for correcting with **auxiliary motion signals** (cf. our IMU use). Completely different setting.

**Neon offsets change with conditions** (C2 context; numbers in our wearable-accuracy related-work file):
- `pettenella2026slippage` [V-PDF]: offsets under slippage tasks stay "< 3.5°" for Neon (p.1, p.6).
- `salari2026pupilSize` [V-PDF]: after app offset correction (p.5), a dark vs bright screen produces a **0.94°** apparent gaze shift (p.1).
- `alecka2026neon` [V-PDF]: offset set on a **white** background (p.5); Neon accuracy 1.20° on white vs 1.63° on black (p.7).

Together these show that an offset estimated under one condition need not hold under another.

**`nolte2026bestPractices`** [V-PDF] (C1):
- **1 participant**, outdoors.
- Neon was used **uncalibrated** after a pilot found "no significant difference" with vs without calibration; no statistics given (p.7).
- Start/end validation: 2.80° vs 2.65°, n.s. (p.12).

**`zhang2026pupeyes`** [V-PDF] (C3): Deblinking removes samples during blinks **and during eyelid opening and closing** (p.7). This supports our more nuanced eyelid handling, but concerns **pupil-size** preprocessing in desktop data.

**`zhang2026gazeifyVoiceify`** [V-PDF] and **`lai2026glanceSay`** [V-PDF] (C1 reference generation):
- Gazeify: Quest Pro, 23 participants; initial gaze selection was correct in **53 %** of trials; voice corrected **58.4 %** (239) of the errors (p.1, p.8, p.10).
- Glance-Say: gaze grounds objects and speech specifies actions, with Meta ARIA (p.1–2).
- Both are tabletop interaction studies. Cite them only as neighbours for **gaze + speech object grounding**. They do not evaluate eye-tracker accuracy.

**`niehorster2024glassesvalidator`** [V-PDF] (C1): A printable poster plus software to measure wearable accuracy and precision; tested with 61 participants on one tracker (p.1). Use it as the methodological analogue of our chessboard lab reference.

**`hu2022data`** [V-PDF] (C1): "Calibration-free" here means learning the gaze-to-scene mapping without manual cross-camera calibration, in a **VR simulator** with HTC Vive Pro Eye (p.1–2). Do not cite it as evidence about eye-tracker calibration.

**Brief mentions only:**
- `saxena2025socialEyes` [V-PDF]: single-target Neon offset before sessions (p.7).
- `park2026openEye` [V-PDF]: sessions with mean error >5° and blink-overlapping fixations excluded (p.8).
- `xu2026signalConstruct` [V-PDF]: Neon quality reported as 99.9 % worn-rate at 195 Hz in real flight (p.10). This is an availability-type quality measure.
- `contreras2026laia` [V-PDF]: simulator; IMU head-tilt correction before homography; Tobii I-VT filter with a 100°/s threshold (p.6–7).
- `lee2026edith` [V-PDF]: uses Whisper for speech timestamps (p.3).

---

## 4. What the literature establishes vs. what remains open (for positioning)

### C1: Sparse, condition-matched in-situ correction

**Established; we must not claim these:**
- Detected road objects as references for online offset correction (`jia2018gaze`).
- Implicit calibration from probable fixation targets, and that ~50 fixations stabilise it on screens (`kasprowski2019implicitCalibration`).
- A per-wearer additive offset improves Neon, including a disjoint-clip hold-out (`baumann2026neonAccuracy`, `foucher2026neon`).
- A distance mismatch between calibration and use increases error (`barz2016prediction`; suggestive: `macinnes2018wearable`).
- Few-shot in-vehicle personalisation for remote cameras (`nagpure2025learningToAdapt`).

**Not found in the checked papers** (candidate gap, still to be confirmed by a broader search):
- A head-to-head comparison of **lab-board vs in-situ driving reference sources** on the **same held-out real-driving targets** in angular units.
- A sweep over the **number and spatial layout** of in-situ references for a wearable tracker.
- References that are **driver-announced and human-verified** rather than assumed from proximity (`jia2018gaze` assumes proximity; Kasprowski searches mappings).

**Our weakness to state:** two participants and a scene-level split. `santini2019grip` and `baumann2026neonAccuracy` used stronger hold-outs (temporal; disjoint slippage clips).

### C2: Person- and condition-specific correction

**Established:**
- Error depends on distance, eccentricity, pupil size, background, slippage and head motion (`barz2016prediction`, `kar2020mlgaze`, `choe2016pupilSize`, `salari2026pupilSize`, `alecka2026neon`, `pettenella2026slippage`, `foucher2026neon`).
- Simple regressions are hard to beat (`kar2020mlgaze`, Table 8).
- Auxiliary motion signals can correct drift in other settings (`park2026motionCorrected`).

**Open:** whether condition-dependent correction improves a **strong median-offset baseline** in real driving at an equal calibration budget. Our answer is a modest gain (2.5 % / 7.3 %), so present it as modest.

**Calibration-health checks:** only simple threshold rules were found (`stapel2022driverPerception`: recalibrate if >2°; `santini2019grip`: recollect if subpar). None of these is an evaluated drift detector. Ours is not evaluated either.

### C3: Multimodal, task-aware suitability

**Established:**
- Individual signals: blink/eyelid handling (`fuhl2024pistol`, `zhang2026pupeyes`), evaluation-time gates for fixation stability, head motion and blinks (`baumann2026neonAccuracy`), exclusion thresholds (`park2026openEye`).
- Quality is task-relative (`niehorster2026fundamentals7`).
- In-cabin gaze and blinks/saccades are noise for scene-saliency tasks but not universally invalid (`kotseruba2024dataLimitations`).
- Image-quality factors can rank angular error, moderately (`jamalifard2026fiud`).

**Not found in the checked papers:**
- **Fusion** of scene semantics (windshield/mirror segmentation), eye state, scene sharpness/optical flow and IMU into **task-specific usable intervals** for driving supervision.

**Our weakness to state:**
- Our gates are characterised only by **retention** (~82 % of 28 min, one participant; Ours).
- They are not validated against angular error, unlike `jamalifard2026fiud`'s error-ranking evaluation.

---

## 5. Considered and excluded

The following candidates were screened and found to contribute nothing to correction or quality assessment beyond the context already covered. They belong in other related-work files:
- **Wearable accuracy factors:** `hooge2023robust`, `onkhar2024evaluating`, `velisar2024noise`, `niehorster2026slippage`, `blignaut2014dataQuality`, `holmqvist2017common` (no local PDF), `holmqvist2022headMovements`, `ehinger2019testBattery`, `buter2024eyeTracking`.
- **Driving gaze datasets and attention models:** `palazzi2019dreyeve`, `govil2026drivergaze360`, `calvi2023comparing`, `kim2020toward`, `nagy2024takeover`.
- **Tooling:** `chu2026pyneon`, `niehorster2025gazeMapper`.
- **Reviews:** `khan2019gaze`, `lin2025recentProgress` (generic calibration discussion, no evaluation).
