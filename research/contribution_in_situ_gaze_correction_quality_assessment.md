# Research Focus and Contributions: In-Situ Gaze Correction and Quality Assessment

**Companion file for:** `paper_summary_skill_strict_source.md`  
**Purpose:** Critically compare **one explicitly named paper at a time** with our proposed contributions, especially for the **In-Situ Gaze Correction and Quality Assessment** part of an IEEE Intelligent Vehicles paper. Determine precisely what the earlier work corrects, what information it requires, how performance is validated, and whether it actually evaluates measurement quality or only filters data according to heuristics.

**Evidence boundary:** This file describes **our** research methods, reported findings, and intended application. It is **not a source of facts about any other publication**. For every paper review, use the *named paper itself* as the only evidence for that paper. Do not import facts from other PDFs, prior summaries, or general background knowledge to fill gaps. Our ongoing work and future plans are not established novelty or proven capabilities.

## 1. Central scientific question and intended positioning

**How can wearable gaze measurements be made reliable enough for driving supervision using a small number of natural in-situ reference observations, while automatically identifying data that are unsuitable for the intended task?**

We do **not** claim that offset correction, implicit calibration, blink rejection, image-quality filtering, or sensor fusion are new in isolation. Our objective is to establish experimentally **what correction is necessary and sufficient in real driving**, compare laboratory and in-situ references under a shared evaluation, characterize how **wearer- and condition-specific error patterns** affect correction, and combine this with an acquisition workflow that attaches **task-aware suitability information** to the recorded gaze.

The wider paper follows a connected scientific progression:

**Collect and evaluate gaze in real driving → benchmark sparse offset correction → investigate influencing factors in controlled experiments → return to driving for targeted correction and automated quality-aware acquisition.**

The intended scientific message is constructive: **Pupil Labs Neon is a promising calibration-free device for naturalistic driving, and a few verified driving references can make the resulting supervision more measurable, correctable, and trustworthy.** A strong baseline with little remaining error is a positive finding, not an excuse to inflate the claimed novelty or magnitude of extended corrections.

## 2. Our work: the actual comparison target

### C1 — Sparse, condition-matched in-situ gaze correction (**primary focus**)

- **Platform and setting:** Pupil Labs **Neon wearable eye-tracking glasses**, gaze sampled at 200 Hz, with real-world driving recordings and deliberately announced fixations on identifiable traffic objects. Unlike purely screen-based gaze calibration, the reference observations are acquired under the operating conditions in which the corrected signal is later used.
- **Reference generation:** During a natural driving event, a participant states the fixated object category. **Whisper** transcribes speech and **Hassil** recognizes supported fixation intents. Object detection searches in a region around gaze, automatically assigns an unambiguous target, and flags ambiguous cases. A dedicated player interface enables manual checking and correction; the evaluated reference targets have been **manually reviewed**. The reference is the 2D center of the verified physical object in the eye-tracker scene image. This is an operational fixation-target reference, not a direct physiological measurement of the exact instantaneous point of regard.
- **Benchmark quantity:** Compare measured gaze and target direction in angular coordinates. Distinguish **raw gaze**, systematic signed azimuth/elevation **bias**, total angular **accuracy error**, **dispersion**, and temporal **precision**. We remove wearer-specific offsets previously stored in the vendor app before comparing raw and corrected estimates, so the preprocessing matters to interpretation.
- **Correction method:** Use the **componentwise median gaze-minus-target offset** from a small number of reference scenes, applied per wearer. This is **post-estimation offset correction**, not retraining NeonNet or calibrating the eye cameras.
- **Direct baseline comparison:** Estimate offsets using either **controlled chessboard fixations** (one board or pooled controlled recordings) or **natural driving fixation scenes**. Compare these sources on the **same held-out driving target-reference scenes**. Also vary the **number of in-situ reference scenes**, random selection versus spatial/geometric layouts, and the amount of calibration data.
- **Reported finding:** In the current two-participant driving evaluation, driving-derived median-offset correction reduces median angular errors from approximately **3.96° and 1.48° to 0.76° and 0.83°**, respectively, outperforming pooled laboratory-derived offsets (**approximately 0.89° and 1.40°**) on the same driving benchmark. Even one driving scene can substantially improve the estimates; a few randomly chosen scenes approach pooled performance. Geometrically optimized layouts show little consistent advantage over random reference selection in the evaluated setting.
- **Interpretation, not proven mechanism:** The advantage of reference observations taken under **similar operating conditions** is supported by the comparison. The available data do not isolate exactly whether target distance, wearer fit, visual-field position, environment, motion, or another difference causes the transfer gap.
- **Scale and evaluation limits:** The broader driving collection currently includes **28 recordings (2.9 h across six days)**; the evaluated target-reference benchmark has approximately **152 fixation scenes** across **two participants**. Test scenes are held out from calibration **at scene level**; scenes from the same driving recording may occur in both sets. This is **not yet** leave-one-drive/day/wearer-out validation. Neither the number of recorded gaze samples nor the number of overlapping folds equals the number of independent people or sessions.

**Important comparison question:** Does a prior paper truly compare *multiple calibration-source conditions* and *reference counts* on **independently evaluated real-driving angular errors**, or does it merely propose calibration with known targets, apply a correction during a demonstration, or report gaze-on-object agreement?

### C2 — Error-informed, person-specific correction and calibration checks (**primary focus when relevant**)

- **Motivation from the controlled study:** Complementary structured experiments examine gaze distance, target position/eccentricity, bright/dark and indoor/outdoor conditions, smooth pursuit, and repetitions. In the analyzed groups, Neon generally performs robustly across several tested conditions, but **distance and lower visual-field position can affect systematic bias**, and **pursuit can increase target-relative dispersion**. Responses differ by wearer; not every factor was tested equally across people.
- **What we actually evaluate:** A small set of **causal temporal filtering and position-dependent correction candidates**, chosen per participant using **calibration scenes only** and assessed on held-out driving scenes. This is different from a trained end-to-end gaze-estimation system or a general uncertainty-regression model.
- **Reported result:** At around 20% calibration scenes, the extended correction improves an already strong median-offset baseline by roughly **2.5% for one participant and 7.3% for the other**; greater calibration shares yield additional modest gains. The favored mechanisms differ: position-dependent bias correction versus short causal temporal smoothing. One participant shows especially useful **upper-tail and dynamic-scene gains**. These are **study-specific findings**, not demonstrated universal behavior.
- **Negative finding to preserve where comparison matters:** A more general per-sample ridge model using gaze position, gaze velocity and annotated distance did **not** outperform the simple median-offset baseline under the available calibration data. More model complexity is not inherently an improvement.
- **Practical follow-on:** Because a few in-situ references estimate the current wearer-specific offset, we can incorporate a **lightweight accuracy or calibration-health check** into the acquisition workflow and update correction when warranted. Explain whether this capability is merely technically enabled, implemented, or independently evaluated; **do not claim proven continuous online drift detection, guaranteed per-sample accuracy, or generalization across days** without the relevant evidence.
- **Scientific distinction:** It is useful to separate **wearer–glasses configuration**, **session/fit effects**, **environmental condition**, and **gaze dynamics**, rather than asserting one universal explanation for observed offsets. Calibration-free operation and the practical value of sparse post-hoc correction are compatible.

**Important comparison question:** Does the prior paper estimate a simple offset, calibrate the gaze estimator, learn a spatial mapping, filter temporal noise, monitor drift, or predict uncertainty? These are different operations, even when all are called “calibration” or “correction.”

### C3 — Multimodal, task-aware gaze quality / suitability assessment (**primary focus when relevant**)

The aim is **not** to label every physical gaze movement as valid or invalid. The aim is to determine whether an observation is **suitable for a particular driving-supervision task**, and to preserve complementary signals for later filtering and analysis.

- **Semantic viewing region:** A segmentation model trained on **over 600 labeled examples** recognizes the windshield, side windows and mirrors. A gaze coordinate projected onto those regions is relevant to **outside-the-vehicle** supervision. Looking at the dashboard/cockpit is not inherently faulty gaze, but may be unsuitable for that application. Distinguish semantic **task relevance** from sensor accuracy.
- **Scene visibility and motion:** Use **Laplacian image sharpness**, **optical flow**, and **IMU** gyroscope/acceleration information as complementary indicators of camera motion and potentially degraded scene imagery. They help characterize whether scene content is suitable for target detection, association, or cross-camera use. Blurry scene video does **not necessarily** mean the physiological eye-tracker gaze is inaccurate.
- **Eye visibility and dynamics:** Use eye openness/eyelid aperture, Neon blink events, and gaze dynamics to flag unreliable periods or define fixation-compatible intervals. Partial eyelid closure and recovery around blinks motivate more nuanced filtering than a simple blink-event flag. **Saccades are legitimate eye movements**, not globally defective measurements: exclude them only if the downstream task explicitly needs stable fixations.
- **Outputs:** Time-aligned **sample-level quality/suitability flags**, component-level rejection reasons, and contiguous intervals suitable for the selected supervision task. These operate **alongside** the automated reference-generation pipeline; they need not change the raw gaze stream.
- **Preliminary evidence boundary:** In an early analysis of **four recordings from one participant (28 minutes)**, region + scene-sharpness + eye-openness gates retained about **82%** of the time in intervals of at least 0.5 seconds. This establishes **retention under these operational criteria**, not confirmed angular-error reduction or proof that optical-flow/IMU fusion increases accuracy. Adding a blanket saccade-exclusion criterion reduced retained time substantially and was not adopted as a universal quality requirement.
- **Assessment status:** Region segmentation, eye state, visual/IMU descriptors, and time-interval gates are implemented components of a **multimodal quality-aware acquisition workflow**; some validation and thresholding is based on controlled observations and manual review. Do not claim that every gate, combination, or retained sample has independently validated angular ground truth or an empirically calibrated error probability. Do not relabel this as fully validated prediction of gaze dispersion/uncertainty without such an evaluation.

**Important comparison question:** Does another work actually fuse **independent scene semantics, eye-state evidence and visual/motion signals** to produce *task-specific usable intervals*, or does it provide only a tracking-confidence score, remove blinks, segment the windshield, or detect blur as a separate step? Conversely, if a paper has already evaluated an equivalent integrated framework, acknowledge the overlap.

### Related C4 — Driving benchmark and reference data (**necessary context, not the primary review topic**)

Our driving dataset connects these methods to *measured* performance: synchronized eye-tracker, front vehicle camera, LiDAR-guided depth, GNSS/INS motion, and structured scene annotations (relative motion, target position, distance, gaze dynamics, road context and illumination). Controlled experiments complement driving observations by examining possible factors individually. **Do not turn this correction/quality review into a general discussion of all driving-gaze datasets or hardware validation** unless the reviewed study specifically addresses correction, calibration validity, confidence estimation, or filtering against reference targets.

## 3. What NotebookLM must verify in EACH named prior paper

Read the named paper's **Methods, Experiments, tables, figures and relevant supplementary material**. Do not classify overlap from the title, abstract, or whether it uses Neon. Select only the dimensions that bear on that paper's actual contribution.

### A. Exactly what is corrected, predicted, or filtered?

- **Objective and output:** Does the method produce corrected 2D/3D gaze coordinates, a constant offset, a nonlinear gaze mapping, a temporal signal, a validity indicator, a sample-quality score, a confidence interval, a calibrated error distribution, a gaze-on-object decision, or merely cleaned event labels?
- **Input/evidence:** Explicit calibration targets, screen/printed markers, natural scene features, detected traffic signs, user-announced fixations, automatically inferred fixations, IMU, scene frames, optical flow, eye images, blinks, eyelid openness, or a previously collected gaze dataset?
- **Device and applicability:** Exact eye-tracker model(s), whether wearable or remote, whether Pupil Labs **Neon itself** is experimentally tested, and whether the approach depends on device-specific internals, manual user interaction, 3D calibration, or known camera geometry.
- **Implementation status:** Is it proposed, implemented in offline processing, performed online, deployed during real recording, or validated in real-time use? Does the method work at the gaze-sample level, fixation level, session level, or recording level?

### B. How strong is the evaluation, and under what conditions?

- **Participants and independence:** How many **independent people**, sessions, days, recordings, fixation targets and usable test points? Is the study mainly one participant with many samples? Is an experiment screen-based, indoor/outdoor, real on-road driving, a vehicle passenger demo, simulated driving, or pre-recorded video viewing?
- **References:** What physical/known target provides ground truth? Is the reference independently determined from the gaze prediction being evaluated, or inferred using gaze itself? Does any human verification resolve target ambiguity?
- **Train/test separation:** Does performance use independent targets, independent fixations, scenes, recordings, sessions, drives, wearers, or a genuinely external dataset? A held-out sample or scene is not automatically an unseen-session evaluation.
- **Baselines:** Does the method compare to **uncorrected gaze**, median/mean bias subtraction, user/vendor calibration, a full chessboard, **one versus multiple** natural reference points, spatially selected versus random targets, temporal smoothing, or existing quality scores? Does it report calibration effort and runtime burden?
- **Measurements:** Extract angular accuracy and signed bias **separately from** dispersion, sample-to-sample precision, detection/association accuracy, valid-data rate, temporal delay, and retained-time coverage. Report the actual improvements and uncertainty (with units, denominators and metrics) rather than saying only “better.”
- **Claims of robustness:** Which participants and conditions support reported robustness—distance, eccentricity, bright/dark, outdoor IR, moving targets, head motion, slippage, time since calibration, or changing wearer/session? Which were **actually manipulated and tested**, not merely mentioned as plausible use cases?

### C. What is the true quality-assessment capability?

- **What is called “quality”?** Correct angular gaze position, eye-detection confidence, tracking availability, task-relevant gaze region, image detectability, fixation stability, scene-video sharpness, temporal consistency, or downstream label utility? These are not interchangeable.
- **Quality signal:** Eye openness/blinks, eye confidence, pupil size, model uncertainty, optical flow, Laplacian/focus, exposure, external lighting, motion/IMU, semantic segmentation, gaze velocity, fixation/saccade classification, or multimodal combinations?
- **Fusion mechanism:** Are independent signals integrated into a joint classifier, score, weighted decision, rule-based gates, thresholding system or simply listed as metadata? Is each contribution evaluated or at least clearly characterized?
- **Quality validation:** Does the paper compare flags against **manual ground truth**, known fixation targets, actual angular errors, failure annotations, downstream supervision quality, or only the amount of retained data? Report sensitivity/specificity, false rejection, error-versus-coverage curves, calibration of estimated uncertainty, or actual accuracy improvement **only if performed**.
- **Target semantics:** Does “valid” mean physically meaningful eye movement, likely accurately estimated gaze, external scene relevance, or task suitability? A saccade is not automatically a bad observation; a gaze on the cockpit is not invalid for every application.

### D. How transferable and practically useful is the method?

- **Calibration effort:** Does it require explicit multi-point user calibration or a dedicated calibration board, or can it use incidental/natural fixations collected during ongoing activity?
- **Operating-condition match:** Is the correction learned and tested in comparable conditions? What evidence supports transfer from controlled lab targets to distant real traffic objects, or vice versa?
- **Adaptation:** Is the method per-sample, per-session, per-wearer or cross-wearer? Are recalibration frequency, drift checks, false alarms, and computational costs measured?
- **Integration:** Can the approach support continuous or batch **collection, verification, correction and quality flagging** of recorded gaze? Do not infer it can from a standalone calibration or filtering component.
- **Reusability:** What practical baseline, ground-truth protocol, threshold validation method, software or experimental comparison could we adopt? Cite it even if it challenges our novelty.

## 4. Critical novelty comparison: challenge BOTH studies

**Never infer that a prior paper “already did our contribution” because it uses gaze calibration, traffic signs, Neon, a confidence score, or an IMU.** Compare the **scientific claim and supporting evaluation**, including the reference source, operating conditions, error metric, number of independent participants, tested holdout level, calibration effort and task suitability.

Equally, **do not treat a new combination of familiar components as automatically novel**. If prior work already verifies gaze corrections in natural driving with independently checked references, evaluates few-shot calibration and transfer, or jointly assesses task-oriented quality using video/eye/motion signals, explain exactly what it already demonstrates and whether our proposed extension would be substantively different.

Distinguish at least these categories when material:

| Potentially related work | What it may already establish | What must be checked before calling it equivalent to ours |
| --- | --- | --- |
| Vendor or laboratory calibration | Accuracy gains from known targets; basic offset removal | Whether it compares lab **versus natural driving** corrections on common held-out road references, with a sparse-calibration budget |
| Implicit/natural-target calibration | Offset or gaze mapping from probable fixations or detected objects | Whether target choice is independently verified, used in **actual driving**, and evaluated in angular units on separate observations |
| Traffic-sign / in-vehicle recalibration | Calibration maintenance using detected traffic objects | Exact participants/roles, physical driving setting, target assignment ground truth, number of references, accuracy evaluation and error robustness |
| Learned gaze-error mapping | Position-, motion-, or context-conditioned correction | Whether it improves a strong **median offset** baseline on genuinely held-out driving scenes, at the same calibration budget |
| Blink/eye-tracking quality filters | Removes closures, tracking loss, implausible gaze | Whether retained labels are actually shown to be more accurate; whether other **task-specific** limitations are addressed |
| Image blur or motion filtering | Uses sharpness, flow, IMU to flag degraded images | Whether it distinguishes *scene detectability* from *eye tracking angular error* and whether signals are fused and validated |
| Semantic viewing-region segmentation | Identifies relevant viewing area or attended objects | Whether it assesses **task suitability** rather than falsely labeling all outside-mask gazes as eye-tracker failures |
| Multimodal reliability / uncertainty | Combines signals and reports reliability or predictive confidence | Whether the score is **quantitatively calibrated** against measured errors; an arbitrary quality score is not an uncertainty distribution |

**The specific distinction worth investigating:** Our contribution is not a novel mathematical median, a YOLO segmentation architecture, or universal uncertainty prediction. It is the **systematic, reference-grounded investigation of how few realistic calibration observations are needed, how well laboratory corrections transfer, what residual error structure remains, and how an automated driving acquisition pipeline can provide corresponding correction and task-aware suitability data**. This distinction must survive close comparison against the full methods of prior work.

**Potential weaknesses in our own evidence:** Current driving correction results cover **two people**; scene-level splits may include correlated scenes from the same drive; exact target centers and intended gaze targets have annotation uncertainty; the extended method is exploratory and not shown to generalize to new wearers/days; the full multi-signal quality monitor has **not** demonstrated a calibrated per-sample angular error prediction or end-to-end benefit to a trained driving model. The user may later add participants and stronger tests—do not attribute such work to the existing paper prematurely.

## 5. Desired output for one paper

Use the ordinary, concise structure prescribed by `paper_summary_skill_strict_source.md`:

1. **In simple terms:** Explain what the named paper actually does and what it achieves, without comparing it to ours yet.
2. **Main contributions, how it works and how they tested it, main findings:** State real participant counts, hardware, experiment, reference data, concrete results, and evidence boundaries where they matter.
3. **Critical assessment:** Separate supported claims from limitations or untested transfer. Do not equate a proposed pipeline with a validated measurement system.
4. **Relevance to my proposed work:** Include **only genuine connections**. Explain (a) actual overlap, (b) the material differences, (c) what remains unproven on both sides, and (d) what to cite or reuse. A paper may overlap with only sparse correction, only uncertainty, or only quality assessment.

**Do not turn the paper summary into a filled questionnaire or output a large table of every absent feature.** For a weakly relevant paper, omit an extended contribution comparison. For direct predecessors, give enough method and quantitative detail to assess the overlap, including where in the paper the evidence appears.

**Strict-source rule:** Every factual claim about the reviewed paper must come from **that named paper** with page/section/figure/table references where available. Say **“Not reported in the named paper”** when a relevant detail is missing; do not change that into “not done.” Never borrow findings from another uploaded study to make a paper look more similar or more different than it is. The contribution numbers above describe **our project only**.

## Suggested NotebookLM prompt

> Summarize **“[EXACT PAPER TITLE]”** using `paper_summary_skill_strict_source.md` and `contribution_in_situ_gaze_correction_quality_assessment.md`. Use only that explicitly named paper for facts about the authors, participants, methods and findings. Examine its full methods, experiments and supplementary evidence. Identify exactly whether it performs (1) sparse in-situ correction and how the references are obtained and validated, (2) person-/condition-specific correction evaluated against a strong baseline, or (3) multimodal quality/suitability assessment, and which of those have actually been quantitatively tested. Explain the paper first, then compare only true overlaps with our work. Be critical of novelty claims on both sides, distinguish measured angular accuracy from retained-data coverage and heuristic confidence, and cite exact evidence locations. Do not invent missing details or merge sources.
