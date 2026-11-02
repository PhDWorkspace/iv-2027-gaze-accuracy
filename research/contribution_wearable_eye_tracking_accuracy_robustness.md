# Research Focus and Contributions: Wearable Eye-Tracking Accuracy and Robustness

**Companion file for:** `paper_summary_skill_strict_source.md`  
**Purpose:** Compare each *named* paper critically with our experimental study, especially for the **Wearable Eye-Tracking Accuracy and Robustness** subsection of an IEEE Intelligent Vehicles paper. This file describes **our** research focus and preliminary findings; it is **not evidence about any other paper** and must not be used to fill gaps in a paper's text.

## 1. Our central scientific question

**How accurate and reliable is calibration-free wearable eye tracking under real driving conditions, which factors influence its errors, and what practical improvements follow from measuring those factors?**

We investigate the **measurement quality of the actual wearable eye-tracker signal**, not merely whether a gaze-guided application succeeds or whether a model predicts where a driver might look. The distinction is crucial: a gaze dataset, attention map, or object-of-interest label is not, by itself, evidence that the underlying eye-tracker coordinates were accurate.

Our experimental logic is:

**Measure in real driving → characterize variability → investigate factors with controlled experiments → transfer the insights back to driving.**

Our goal is to provide strong independent evidence for where Pupil Labs Neon works well, identify any meaningful limitations, and improve the usefulness of gaze measurements for downstream driving supervision. We are **not** trying to demonstrate that Neon is generally defective. The fact that many suspected factors have little or no detectable effect can be a valuable robustness finding.

## 2. Our study: the actual comparison target

### C1 — Real-driving gaze accuracy benchmark (context for the robustness study)

- **Device:** Pupil Labs **Neon**, a calibration-free wearable eye tracker using infrared eye cameras and the NeonNet gaze estimator. We evaluate the measurements produced by the glasses themselves.
- **Real setting:** Naturalistic driving in an instrumented research vehicle, with physically observed targets such as signs, traffic lights, license plates, and vehicles. Do not equate this with watching driving videos, a driving simulator, a stationary vehicle, a passenger-only experiment, or laboratory walking.
- **Current evaluation:** **152 manually reviewed fixation scenes from two qualified participants**, acquired within a larger collection of **28 driving recordings (2.9 h over six days)**. Additional collection is planned. The evaluated participants have limited and potentially different roles/route distributions; do **not** claim population generalization or universal performance.
- **Ground-truth reference:** The participant deliberately announces fixation on a specific identifiable visual target; an automated system detects/associates the target and human reviewers verify its image location. The **independently localized 2D target-center coordinate** is the operational fixation-target reference, permitting measurement of **angular gaze error against a known target**. It is not an independent physiological measurement of instantaneous retinal point of regard.
- **Rich conditions:** Each scene has descriptions such as target category, distance (approximately 7–107 m in the analyzed benchmark), gaze/viewing position, ego state and speed, target motion, relative motion, road context, illumination/exposure, and dynamic gaze features. Camera–LiDAR geometry supplies distance and GNSS/INS supplies ego motion.
- **Baseline finding:** Driving-derived per-wearer median offset correction reduces median angular error from approximately **3.96° to 0.76°** and **1.48° to 0.83°** for the two analyzed participants, on scene-held-out evaluation from the recorded drives. A few randomly sampled driving references can work well. The current split is **not** leave-one-drive/day-out.

This driving benchmark is not the sole focus of the Related Work subsection here, but it matters when judging whether a purported *real-world validation* is genuinely comparable.

### C2 — Complementary controlled validation and factor investigation (**primary focus**)

- **Current dataset:** Approximately **216 controlled recordings (2.9 h) from six participants**, with repeated observations, including participants from the driving study. Counts may increase before submission, and not every participant completed every protocol. Many repeats from one participant are **not** equivalent to the same number of independent participants.
- **Reference design:** Precisely identified targets (including **15 corners in a 5 × 3 pattern**), controlled static fixation intervals, known target configurations, automated QR-based protocol/target recognition and manual verification. Target-order reversal and repeated sessions allow examination of temporal/order effects.
- **Viewing distance:** Core analyzed comparisons at **1, 2 and 4 m**; additional sweeps also include **5, 8 and 12 m**. Do not describe the longer distances as already supporting a reported statistical effect unless the analysis establishes that.
- **Visual-field position and eccentricity:** Multiple gaze positions across the scene camera, including central/peripheral and upper/lower-field targets. Analyze eccentricity separately from image elevation or vertical row.
- **Illumination and eye appearance:** Bright/dark screen conditions with measured pupil-diameter changes; indoor/outdoor comparisons motivated partly by sunlight and infrared-based eye imaging. **Indoor vs. outdoor is not a controlled isolation of external infrared radiation**, and visible brightness is not the same variable as infrared interference.
- **Motion:** Static fixations versus **smooth pursuit**, plus head-motion and other dynamic protocols where supported by actual data. Distinguish target-relative gaze dispersion from actual eye-tracker sensor noise.
- **Temporal stability:** Repetitions, fixation order, and within-/between-session comparisons where available.
- **Metrics:** Target-referenced **angular accuracy**, signed azimuth/elevation **bias**, **dispersion** of gaze around the fixation target or moving-target residual, and sample-to-sample **precision**. These are **different quantities** and should never be conflated with each other or with target-detection accuracy.

**Current findings to compare against (study-specific, not universal claims):**

- Generally promising Neon accuracy/robustness across several tested lighting conditions, pupil-size changes, eccentricities, and repeated measurements, with **no statistically detectable degradation** for several factors in the available comparisons.
- **Distance-dependent systematic changes** in the analyzed **1/2/4 m** measurements for the two evaluated participants; dispersion did not show a corresponding increase. The mechanism has not been causally isolated.
- **Lower image-region effects:** Higher sample-to-sample jitter in all six evaluated participants and an accuracy change in a subset, rather than a universal radial eccentricity effect.
- **Smooth pursuit:** Substantially greater **target-relative dispersion** (roughly threefold) in the evaluated participant, without a similarly clear change in median accuracy; this is not proof of a universal effect across wearers.
- **Wearer/session dependence:** Uncorrected biases and responses to conditions differ by participant. Some between-session comparisons remain sensitive to preprocessing; do not use them as settled evidence for long-term drift.

### C3 — Practical correction and quality-aware acquisition (**secondary connection**)

- We compare offsets estimated from **controlled chessboard targets** with offsets from **natural driving references**, on the same held-out driving scenes. In our current evaluation driving-derived offsets transfer more consistently. We investigate **how many reference scenes are needed** and whether spatially structured point layouts beat random selection (little consistent advantage observed).
- We also investigate light-weight person-specific **spatial/causal temporal** corrections. These add modest overall improvements over an already strong median-offset baseline and can benefit certain dynamic conditions, but are exploratory and not shown to generalize across unseen drivers or independent days.
- Our acquisition pipeline adds **task-aware quality flags**, using windshield/window/mirror segmentation, image sharpness and optical flow, IMU motion, eye openness/blinks, and gaze dynamics. Their purpose is sample **suitability for downstream supervision**; they are not automatically a validated predictor of angular error.

This supporting work should be discussed **only when a paper genuinely overlaps** with correction, measurement quality or validated reliability estimation. Do not manufacture a connection to every gaze-related paper.

## 3. What NotebookLM must verify in EACH named paper

Read the **methods, experimental protocol, figures, result tables, and relevant appendix**—not merely the title, abstract, introduction or the authors' own novelty statement. Select the decisive dimensions below for the specific paper, rather than printing a large checklist of irrelevant negative answers.

### A. Device and experimental reality

- **What was actually measured?** Genuine wearable eye-tracking glasses, a remote/table-mounted tracker, recorded gaze from an existing dataset, simulated/idealized gaze, an attention map, or manual object labels?
- **Which exact device(s)?** Is **Pupil Labs Neon itself** experimentally tested, merely cited, or absent? Distinguish Neon from Pupil Core, other Pupil Labs devices, Tobii and non-wearable trackers.
- **Where did the data come from?** Physical real participants viewing real targets; a computer display; printed markers; an outdoor field setting; an actual moving car; an observer watching driving videos; or a simulator? State what the experiment *actually* validates.
- **Who participated?** Give the **number of independent human participants**, and relevant **per-condition participant coverage**. Separately report recording/session/fixation counts when meaningful. Say when results are dominated by one person or when the authors did not provide the denominator.

### B. Target reference and accuracy validity

- Was the target's **2D or 3D position independently defined**? By what method: known screen point, physical marker, chessboard, optical tracking, scene-object detection, manual ground truth, gaze-based association, or another approach?
- Did the study actually calculate **angular or pixel error between wearable gaze and a known target**? Or did it report only object agreement, fixation detection, saliency similarity, classification, visual inspection, or downstream task performance?
- Was it measuring **absolute accuracy**, **systematic offset**, **precision**, **dispersion**, **tracking availability**, or **reliability/uncertainty**? Extract the exact definitions and avoid treating them as synonyms.
- How were user calibration, post-hoc offset corrections, vendor profiles, gaze mapping, and outlier exclusions handled? Distinguish **raw/uncorrected** performance from **corrected** performance.
- Was evaluation independent of the gaze signal used to locate/choose the ground truth? Were calibration and test observations independent, and at what level (sample, fixation, recording, session, participant)?

### C. Factors and quantitative findings

Verify which factors were **experimentally varied and analyzed**, with exact conditions and relevant counts:

- Viewing distance and target geometry, including the **actual distance range**.
- Eccentricity, gaze direction, and upper-versus-lower image region.
- Illumination, bright/dark viewing, pupil diameter, sunlight, **direct infrared interference** (if truly controlled), indoor/outdoor environment.
- Static fixation versus pursuit, rapid eye movements, head motion, vibration, walking or vehicle motion.
- Re-wearing/glasses displacement, repeated sessions and temporal drift.

For directly overlapping experiments, report **actual numerical outcomes** (error in degrees, effect sizes, uncertainty, significance, baseline and comparison) and whether a factor affected **accuracy, bias, precision, dispersion, or tracking availability**. Report **null effects** too; they are important to evaluating robustness. Identify when the evidence concerns only one or a few participants.

## 4. How to judge overlap with OUR contributions

**Do not use “they also tested Neon” as a conclusion of substantive overlap.** Sharing the tracker only establishes common hardware. Similarly, “tested outside” does not mean “validated while driving,” and “measured fixation accuracy” does not necessarily mean “benchmarked long-distance gaze in a moving vehicle.”

Give a defensible assessment using these categories in prose:

- **Direct experimental overlap:** Same scientific question and directly comparable measurement/reference protocol with relevant real participants and outcomes. Name exactly which part of C2 (or relevant C1/C3) overlaps and what the prior study has already demonstrated.
- **Partial or methodological precedent:** Shares some metrics, factors, or techniques, but differs in scientifically meaningful ways (for example, targets only at 1 m, screen-only evaluation, no real driving, no held-out transfer, or dispersion without independent target accuracy).
- **Background relevance only:** Useful motivation or general eye-tracking context, but not experimental evidence that our contribution is already performed.
- **Cannot determine:** Key details are unavailable in the named paper; say **“Not reported in the named paper”**, not “the authors did not do it.”

**Be equally critical in both directions.** If a paper already performs a comparable controlled validation, acknowledge that plainly; our novelty cannot be “we measured brightness” or “we tested Neon.” Equally, do not erase our real-driving target-referenced measurements, cross-setting experimental design, far-field geometry, wearer-specific analysis, and practical transfer simply because a paper evaluates Neon in one of several laboratory conditions. A new setting or extra sample count alone is also **not** proof of novelty: require a substantive new measurement, evaluation, condition, insight or use case.

## 5. Desired output when comparing one paper

Follow `paper_summary_skill_strict_source.md` for its standard concise per-paper structure. In its **Critical assessment** and **Relevance to my proposed work** sections, make sure the reader can answer:

1. **What did this paper actually test and find, with how many people and under what conditions?**
2. **Does it experimentally validate wearable gaze accuracy and robustness, specifically Neon, or does it study something adjacent?**
3. **Which exact experiment or claim genuinely overlaps our controlled study?**
4. **What important distinctions remain untested or unreported in the named paper, and how might our study address them?**
5. **What should we cite this paper for?** For example, supporting evidence of robustness, contrary findings, a directly comparable factor/baseline, a ground-truth protocol, or a method we should not claim as new.

**Evidence rule:** Every factual statement about the reviewed paper must be grounded in that paper alone, ideally with page, section, figure or table pointers. The counts/results in this contributions file are contextual claims about **our study only**. Never transfer them to another paper. Review **one explicitly named paper at a time**; do not merge conclusions from different uploaded papers unless explicitly asked for a separate, clearly sourced synthesis.
