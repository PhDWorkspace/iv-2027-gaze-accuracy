# Research Focus and Contributions: Gaze Supervision and Driving Datasets

**Companion file for:** `paper_summary_skill_strict_source.md`  
**Purpose:** Critically compare **one explicitly named paper at a time** with our work, especially for the **Gaze Supervision and Driving Datasets** subsection of an IEEE Intelligent Vehicles paper. Identify what existing datasets actually record, how gaze labels are constructed, what is validated, and whether the accuracy of the underlying wearable eye-tracking signal is known.

**Evidence boundary:** This file defines **our** research focus, methods and current results for comparison. It is not evidence about any other study. Only the *named paper itself* may support statements about its authors, data, methods, findings, limitations, or novelty. Do not merge facts from other uploaded PDFs or NotebookLM sources into that paper's review.

## 1. Central scientific question

**How can human gaze become a trustworthy spatial supervision signal for autonomous driving, rather than simply a gaze point, attention map, or object label whose measurement error is unknown?**

Existing driving-gaze research can have valuable purposes: predicting driver attention, identifying salient objects, learning gaze-conditioned driving policies, or studying behavior. Our paper asks a distinct but complementary **measurement-quality** question. Before using wearable gaze as spatial supervision, can we quantify the error of its coordinates against **identified fixation targets in actual driving**, investigate variability across real scenarios, and make quality-aware data acquisition practical?

The intended research arc is:

**Real driving with localized target references → measure error and benchmark correction → use enriched scenarios to motivate controlled experiments → transfer understanding back to reliable driving-gaze data.**

**Do not presume novelty.** A previous dataset may already have precise spatial annotations, raw wearable recordings, target-referenced accuracy, online calibration, or strong validation. Read the methods and evaluate the exact overlap. Conversely, **do not say another work “already does our contribution” merely because it supplies gaze labels, heatmaps, eye-tracker videos, or traffic-object annotations**. Those are not automatically independently measured gaze-accuracy benchmarks.

## 2. Our work: the specific comparison target

### C1 — Real-driving gaze dataset, precise references and evaluation (**primary focus**)

- **Setting:** Wearable **Pupil Labs Neon** data acquired in a real instrumented research vehicle, observing physical traffic scenes rather than pre-recorded driving videos or simulation. The driving collection contains **28 recordings (2.9 h across six days)**. The current evaluated subset includes **152 manually reviewed fixation scenes from two qualified participants**. These are *fixation scenes*, not 152 independent drivers or drives. Additional data collection may follow; do not portray it as completed.
- **Deliberate target references:** During naturalistic road travel, the participant deliberately fixates a named identifiable target (e.g., traffic light, sign, license plate, vehicle) and announces it aloud. **Whisper** transcribes the utterance; **Hassil** recognizes an allowed event/object category. Gaze restricts the object detector's search, uniquely matched targets are assigned/tracked automatically, and ambiguous cases are flagged. A purpose-built player interface supports **manual verification and correction**; every target in the evaluated benchmark was reviewed.
- **Point-level spatial reference:** The validated target's center yields a **2D fixation-target reference coordinate in the eye-tracker's scene image**, used for **angular gaze–target error**, signed bias, dispersion and precision. This is a deliberately fixated *operational target reference*, not an independent physiological measurement of the instantaneous retinal point of regard. Gaze-guided candidate retrieval does not by itself guarantee independent reference selection; reviewers need to assess whether manual verification sufficiently guards against circular assignment.
- **Multi-sensor context:** Eye-tracker timestamps are aligned with a GNSS-disciplined/PTP-synchronized vehicle sensor system (with Neon clock-offset estimation). Vehicle cameras, calibrated LiDAR and GNSS/INS supply synchronized scene imagery, LiDAR-guided dense depth/target distance, vehicle speed and ego motion. The vehicle has **eight cameras and seven Ouster LiDARs**, although the paper principally uses specific front camera/roof LiDAR views; distinguish installed sensors from modalities actually used for the published labels.
- **Rich, intentionally varied scenarios:** Scene metadata include the **target class and position, viewing region, road/intersection context, ego state and speed, target state, relative motion, viewing distance, gaze dynamics and illumination/exposure**, with sample-level eye/IMU descriptors. The annotated set covers traffic signals (**35**), regulatory/guidance signs (**50**), parked/stopped vehicles (**35**) and moving road users (**32**). It spans **114 driving / 38 standstill** scenes, **120 static / 32 moving** targets, and reference distances approximately **7–107 m** (132 scenes at least 15 m; 64 over 30 m). The collection deliberately covers diverse situations but is **not a population-representative or fully balanced sample**.
- **What the data enable:** Direct measurement of wearable **gaze localization error** under actual driving conditions; correction comparison using the *same held-out target-reference scenes*; scene-specific accuracy/dispersion analysis; and, where permitted, a reproducible resource for spatial gaze supervision. Raw multimodal signals and precise reference annotations are distinct from gaze-averaged saliency maps.
- **Current availability:** A dataset release is **planned**, subject to legal/privacy approval. Do **not** imply that the full dataset has already been released, is openly downloadable, or has been adopted as a downstream benchmark. Approved pilot examples may precede full release.

**Crucial scope limits:** The current driving accuracy results cover two participants; fixation events are deliberately announced and **do not constitute unconstrained sampling of all driver attention**. Calibration/test splits currently separate **scenes**, not whole independent drives or participants. Per-target angular reference accuracy has an annotation/fixation-timing uncertainty that should not be ignored.

### C2 — Measuring and improving the actual gaze signal (**important secondary distinction**)

- We evaluate **uncorrected angular error**, person-specific systematic offsets, dispersion and sample-to-sample precision against verified target positions. Merely detecting an attended object or predicting a human attention map is **not** an equivalent metric.
- A **sparse in-situ median-offset benchmark** compares references sampled during driving against references from controlled chessboard tasks; it tests number of driving scenes, random versus structured geometric selection, and correction on scene-held-out driving observations. Current reported medians reduce from approximately **3.96° to 0.76°** and **1.48° to 0.83°** for the two participants using driving-derived offsets. Current performance does **not** demonstrate transfer to new drivers or fully held-out days.
- A complementary controlled dataset (currently **216 recordings, 2.9 h, six participants**) investigates distance, illumination, spatial gaze position, pursuit and temporal repeatability. This controlled study is **not** the primary focus of a *driving datasets* review; discuss it only if the named paper actually examines measurement factors, hardware validation, or comparable calibration protocols.

### C3 — Automated quality-aware data generation (**secondary overlap when relevant**)

- Beyond generating evaluation targets, our acquisition workflow attaches **scene-level and sample-level metadata** and implements task-aware data-suitability indicators: segmentation of windshield/windows/mirrors using **600+ annotated images**, eye openness/blinks, sharpness (Laplacian), optical flow and IMU signals, and gaze dynamics. A few in-situ reference observations can also support a current wearer-specific accuracy check.
- These are **practical collection and suitability tools**, not proof that every automatically retained sample has lower angular error. Some preliminary retention results exist, but they should not be conflated with validated error prediction or downstream driving-model improvements.
- We do **not** claim that attention supervision improves an autonomous-driving policy as part of this particular paper unless an actual downstream evaluation is supplied. The motivation is to make such supervision *measurable and better characterized*.

## 3. What to investigate in EACH prior paper

Read the **complete Methods/Experiments**, data/annotation descriptions, figures, tables and appendix where available. Start by explaining the named paper's real objective and demonstrated result, **not** by checking a list of buzzwords. Choose only the dimensions below that matter for a substantive comparison.

### A. What is the research objective and what data do they really collect?

- Is the paper about **driver gaze measurement**, **attention prediction**, **saliency**, **driving policy learning**, **behavioral analysis**, **object-of-interest classification**, **gaze mapping**, or **sensor validation**? These questions are related but not interchangeable.
- Did the gaze data come from **a real driver physically driving**, a **passenger in a moving vehicle**, a **stationary car**, **people watching road videos**, **a simulator/VR environment**, **existing datasets**, or a **synthetic predictor**? Specify each setting accurately and avoid the blanket term “real-world driving” when the measurement setup differs.
- What device provides the gaze? Actual **wearable eye-tracking glasses**, remote dashboard-mounted gaze estimation, video-based gaze annotation, predicted saliency, or simulated human attention? Was **Neon** used specifically, or another device? Which device properties were actually evaluated?
- How many **participants, drivers/passengers/observers**, recordings, drives/hours, frames and gaze annotations? Keep units distinct. Are the participants trained/selected? Is the source diverse across wearers, road types, lighting and scenarios, or mostly repeated measurements of a few individuals?

### B. What exactly is the gaze label and how was it obtained?

- Does the dataset contain **raw gaze coordinates and timestamps** in a wearable camera or angular frame, **per-fixation points**, **per-frame point-of-regard**, **object identities**, **semantic scene labels**, **aggregated gaze heatmaps**, **Gaussian attention maps**, **normalized screen coordinates**, or **predicted model attention**? Is the original raw signal retained or recoverable?
- What is the reference? A **known physical fixation target with independently determined position**, a manually marked object center, an eye-tracker-produced gaze point reused as its own label, an annotator's behavioral judgment, or an inferred saliency map? Do the authors distinguish the intended target from actual eye fixation?
- Was reference localization **automatic, manually verified, independently annotated, or inferred through gaze proximity**? If gaze is used for both association and validation, check for possible circularity and whether the authors have safeguards. Do not treat human review alone as proof of perfect labels.
- Are the per-sample/per-fixation gaze errors **actually measured in degrees/pixels relative to a reference**? If not, do **not** equate gaze prediction, object overlap, attention-map correlation, detection AP or downstream task performance with eye-tracker angular accuracy.

### C. What information supports real-world usefulness and reproducibility?

- Do data include **aligned eye/scene video, vehicle cameras, LiDAR/depth, GNSS/IMU/vehicle speed, target range, object trajectories, road conditions and scenario-level descriptions**? Which are *actually provided* in the dataset, rather than only recorded in the vehicle or mentioned in the setup?
- How are the sensor clocks aligned? Is timing error measured? Are moving objects handled at matched timestamps? Are spatial transforms and depth measurements calibrated, validated, or only assumed?
- How many **physical traffic target classes**, ego states, relative motions, target distances, road settings and difficult illumination conditions are present and quantified? Are they examples or systematically characterized? Does coverage enable factor-specific analysis, or are subsets tiny?
- Is the data **publicly released**, only available on request, accompanied by source code, or planned for release? Verify actual download availability if the named paper states it; never infer release just from a website or statement of intention.
- Were gaze annotations measured/validated at collection time, verified offline, corrected using known target references, or only used as given?

### D. What evaluations substantiate the dataset's claims?

- What is the **measured outcome**: quantitative sensor accuracy, fixation-reference reliability, agreement among annotators, label validity, gaze-to-object association, attention prediction, policy benefit, or broad behavior coverage?
- What **baselines** and fair comparisons exist? Are there independent spatial references, experimental error estimates, calibration comparisons, external ground truth, repeated measures, and out-of-sample splits?
- Does the evaluation use **held-out frames, fixation scenes, drives, days, subjects, environments or vehicles**? Distinguish these; random frame or scene splits can share motion, wearer offsets, and recording conditions.
- What are the important numeric results, uncertainties and failure cases? Cite concrete tables or figures. If angular error is absent, say it was **not reported**, not that the dataset is necessarily inaccurate.
- For gaze-supervised model papers, distinguish **demonstrated downstream model benefit** from **demonstrated underlying gaze-label correctness**. Both can be worthwhile contributions, but they answer different questions.

## 4. Critical novelty comparison: be rigorous in BOTH directions

A paper deserves to be called **directly overlapping** only if the scientific objective and demonstrated evidence actually coincide. Decide whether it is:

1. **Direct experimental overlap:** Provides real on-road wearable-gaze observations with a comparable **independent or clearly justified physical target reference and evaluated gaze-coordinate accuracy**, or directly comparable automatic target-reference annotation/correction protocols. State exactly what was demonstrated and by how many participants/scenes.
2. **Partial or methodological precedent:** Has some of the same dataset components (real drivers, raw gaze, motion/speed, depth, object labels, annotations, calibration, or signal quality), but a materially different reference/evaluation or research objective. Give credit for the overlapping part and describe only the meaningful difference.
3. **Background/application relevance:** Uses gaze to improve prediction, attention maps or policies, without directly evaluating the wearable measurement quality relevant to our benchmark. Useful motivation is not the same as duplication.
4. **Cannot determine from the named paper:** The needed methods or availability details are not reported or inaccessible. Do not turn absent reporting into a categorical negative claim.

**Specifically avoid these false equivalences:**

- “Has real driving gaze data” ≠ “evaluates wearable angular gaze accuracy in real driving.”
- “Has a fixation point/heatmap” ≠ “has an independently verified 2D gaze-reference coordinate.”
- “Detects the object of attention” ≠ “quantifies sub-degree spatial accuracy against target ground truth.”
- “Uses LiDAR/depth” ≠ “provides target-level metric range aligned to wearable gaze references.”
- “Collected many hours/frames” ≠ “has many independently evaluated participants or fixation references.”
- “A model learns from gaze” ≠ “the gaze-label errors were characterized.”
- “Performs calibration with traffic signs” ≠ “evaluates our exact reference sampling/transfer protocol.”
- “Raw data are not described” ≠ “raw data are definitely unavailable.”

**Also challenge our own framing.** If the reviewed work already has independently referenced real-driving gaze, rich synchronized sensor metadata, a similar automated annotation protocol, or a rigorous gaze-accuracy benchmark, acknowledge it directly. The user cannot claim novelty simply because their system is newer, uses more sensors, includes a different model, or has more total hours. Real driving with announced target fixations is not identical to spontaneous attention; manual verification and target-center assumptions introduce uncertainty; a legal review means our full dataset is not yet public.

## 5. Desired output for a named paper

Follow `paper_summary_skill_strict_source.md` exactly for the **main review format** (plain-language explanation, main contributions, methods/evaluation, key results, critical assessment, and only materially relevant comparison). Do **not** produce a section for every question in this file.

In the **Critical assessment** and, where justified, **Relevance to my proposed work**, explain:

1. What did the authors actually collect or predict, with how many people, in what setting, and in which coordinate/annotation format?
2. How were labels generated, synchronized, checked and evaluated? What do their ground-truth and accuracy terms *actually mean*?
3. Which precise part of our **real-driving spatial-reference benchmark** or **automated quality-aware acquisition** overlaps experimentally, if any?
4. What does the paper's evidence establish that we must acknowledge, and what would our own results still need to show to claim a defensible distinction?
5. What should this paper support in Related Work: **motivation for supervision**, **dataset precedent**, **ground-truth/annotation precedent**, **accuracy evaluation**, **calibration precedent**, or **contradictory evidence**?

**Sourcing:** Every factual statement about the named paper must be grounded exclusively in that paper, preferably with a page/section/figure reference. Our counts and methods in this file are **context**, not facts about the reviewed publication. If its evidence is incomplete, say **“Not reported in the named paper”**. Do not use abstracts alone to classify a paper as close prior work. Review exactly **one named paper at a time**; cross-paper synthesis must be a separately requested task with individually sourced comparisons.

## Suggested NotebookLM prompt

> Summarize **"[EXACT PAPER TITLE]"** using `paper_summary_skill_strict_source.md`. Use `contribution_gaze_supervision_driving_datasets.md` only as my research focus and comparison target. Read the paper's full methods and experiments and critically establish what its driving-gaze labels represent, how they were obtained and validated, what participants and sensors were actually used, and whether the authors independently measured gaze-coordinate accuracy. Compare only genuine methodological or experimental overlap with our real-driving dataset and quality-aware acquisition approach. Cite the paper's exact pages or sections. Do not infer novelty from the title, device brand, or the mere existence of gaze annotations.
