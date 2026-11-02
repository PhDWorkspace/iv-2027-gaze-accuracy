# Scientific Story and Editorial Guide — Gaze Accuracy Paper

**Working paper title:** *Towards Reliable Gaze Supervision for Autonomous Driving: A Real-World and Controlled Evaluation*

**Purpose of this file:** A durable editorial guide for Codex, Claude, and other writing agents revising the IEEE IV manuscript section by section. It documents the intended scientific argument, contribution positioning, reader journey, and presentation priorities—not a frozen inventory of results. Use the latest manuscript, verified evaluation artifacts, and full papers as factual sources. **This guide is about how to tell the story; it does not authorize invented or outdated numbers.**

## 1. The central message

**Calibration-free wearable eye tracking is a promising source of human-gaze supervision for autonomous driving. We do more than collect gaze recordings: we build the experimental means to measure the signal under actual driving conditions, characterize when it is reliable, correct its systematic errors with very few in-situ references, and annotate the suitability of subsequent measurements automatically.**

The paper should leave the reader with three impressions:

1. **The data are scientifically valuable.** A purposefully diverse, richly described real-driving benchmark has precisely localized, manually checked fixation-target references and synchronized vehicle context; a complementary, extensive controlled dataset is designed to isolate relevant factors.
2. **The device is good—and we have measured where and how.** Neon shows encouraging robustness to many conditions. Some specific spatial and dynamic influences matter, and wearer-dependent offsets justify measurement verification rather than blind reliance on a general specification.
3. **The experiments lead to practical improvements.** A few naturally acquired driving references remove much of the systematic error; operating-condition-matched references transfer better than laboratory-derived offsets in the evaluated data; targeted individual corrections and multimodal suitability assessment make ongoing collection more useful.

**Preferred final idea:** *Towards scalable gaze datasets in which measurement quality is evaluated rather than assumed.*

This is **a systematic measurement and validation paper**, not primarily a YOLO, speech-recognition, vehicle-integration, or new-neural-model paper. The engineering is substantial, but it serves the science.

### What we deliberately changed from the early manuscript framing

- **From “an eye-tracking experiment” to “a validated supervision-data foundation.”** The dataset itself has valuable verified references, synchronized vehicle context, and purposeful scenario coverage.
- **From “a successful engineering pipeline” to “a scientific experimental program.”** The pipeline enables the driving benchmark; its results motivate deliberately selected controlled experiments; those findings are evaluated again in driving.
- **From “many factors did not matter” to “we independently confirmed encouraging robustness.”** Null or small effects are presented as scoped evidence, without exaggerating equivalence.
- **From “chessboards failed” to “condition-matched references transfer more consistently.”** The key finding is practical in-situ calibration; the comparative transfer gap motivates investigating viewing geometry.
- **From “the best model must be more complex” to “simple corrections matched to measured errors work.”** Keep the strong median baseline central; treat targeted improvements as useful extensions.
- **From “quality filtering is a separate afterthought” to “the measurement study closes the loop with acquisition.”** The same system generates references, monitors suitability through multiple signals, and can support sparse accuracy checks.

**One-paragraph paper story:** We first make wearable gaze accuracy measurable under real driving conditions through an automated, manually verified, richly annotated benchmark. We find that Neon is a promising sensor whose dominant wearer-dependent offsets can be corrected with only a few in-situ observations, with better transfer than conventional laboratory-derived references in our evaluations. We then investigate plausible sources of residual variability in a complementary controlled dataset deliberately designed around driving-relevant conditions, confirming broad robustness while identifying specific spatial and dynamic effects. Finally, we return to driving, demonstrate further targeted improvements over a strong simple baseline, and incorporate those insights into an acquisition workflow that collects corrected, quality-annotated gaze data rather than assuming the signal is error-free.

## 2. The narrative arc: real-world → controlled → real-world

The scientific sequence is the backbone; every result should move this argument forward.

### Act 1 — Establish the real-world measurement foundation

**Question:** Can wearable gaze be measured and evaluated against deliberate, precisely localized targets under actual driving conditions?

We set up a synchronized research-vehicle and eye-tracking acquisition system and an automated way to acquire gaze-reference events during normal drives. Spoken events identify *intent* and object class; vision identifies the candidate object; tracking maintains its location; manual validation ensures the benchmark reference is defensible. The data are not just a gaze coordinate and an RGB image: they contain target position, object category, viewing distance, ego speed and motion, relative motion, traffic context, and eye/scene quality measurements.

Then **show the discovery**, not a list of sensors: raw errors contain a substantial, wearer-dependent systematic component. A simple person-specific offset estimated from real driving observations dramatically improves median accuracy. Even a handful of naturally acquired references approaches performance using many observations. Sophisticated geometric arrangements of those few references add little in the tested configurations.

**Next question:** Would a conventional controlled chessboard supply an equally transferable offset? In the evaluated driving data, it is less consistent. The result supports condition-matched reference collection, without proving *which* difference between laboratory and driving conditions causes that transfer gap.

### Act 2 — Investigate robustness rather than assume failure

**Question:** Once systematic error is accounted for, which environmental, geometric, temporal, and dynamic factors influence gaze quality—and which do not?

Real driving annotations allow scenario comparisons, but factors co-occur and some scene categories are sparse. This motivates a **deliberately designed complementary controlled study**, not an unrelated list of indoor recordings.

The experiments were selected because they reflect real driving challenges:

| Experiment | Why it belongs in a driving paper |
|---|---|
| Viewing distance, including extended sweeps | Driving objects are often much farther away than typical laboratory targets; ask whether angular error itself changes with distance. |
| Grid position and eccentricity | Objects, road signs, and mirrors appear across the field of view; distinguish radial eccentricity from lower-field effects. |
| Bright/dark display and changing pupil size | Tunnels and changing illumination alter pupil size and eye appearance. |
| Indoor/outdoor measurements | Sunlight changes the infrared environment and viewing conditions; this is not a controlled isolation of IR interference by itself. |
| Static fixation and smooth pursuit | Following moving vehicles involves dynamic eye movements and potentially different dispersion behavior. |
| Repetitions, sessions, and reverse-order trials | Test stability and distinguish spatial effects from sequence and time effects. |

**The primary result is encouraging robustness**, not a disappointing collection of nonsignificant tests. Across several manipulated conditions there is no *detectable* accuracy degradation. At the same time, certain factors reveal interpretable structure: viewing distance and some lower-field positions affect systematic offset/precision, while pursuit can increase *target-relative dispersion* even if median accuracy stays similar. Distinguish bias, accuracy, dispersion, and sample-to-sample precision at every step.

**Next question:** Can these observations be used to improve actual driving measurements beyond a strong, simple offset baseline?

### Act 3 — Transfer findings back to driving and close the loop

**Question:** Does understanding the error structure produce practical benefits under real driving conditions?

Start by acknowledging the **strong median-offset baseline**. Small absolute improvements on a strong baseline are still scientifically useful, especially when gains concentrate in difficult, dynamic, or upper-tail observations. Select simple spatial or causal temporal correction mechanisms from calibration data only; evaluate on disjoint test scenes. Participants may benefit from different mechanisms: this is an argument for individualized verification and selection, **not** a universal learned model or a causal explanation already proven.

Now show how the experimental findings become part of a **quality-aware acquisition workflow**, not just a retrospective paper analysis:

- **Automatic reference generation:** natural spoken fixations → candidate target matching/tracking → validated 2D references; usable for benchmarking and sparse in-situ accuracy checks.
- **Semantic relevance:** a trained segmentation model distinguishes windshield, side windows, mirrors, and interior; outside-view relevance is *task-specific*, not a judgment that cockpit gaze is physiologically invalid.
- **Scene visibility and motion:** optical flow, image sharpness/Laplacian, and IMU-derived motion provide complementary indicators of whether scene images can support visual association.
- **Eye visibility and gaze events:** eyelid aperture, blink indicators, and gaze dynamics identify potentially unreliable intervals; do not globally classify saccades as bad.
- **Sample/sequence annotations:** keep original measurements and output transparent flags, enabling downstream selection instead of irreversibly discarding data.
- **Lightweight in-situ accuracy check:** a few verified natural fixations can estimate the current offset and indicate when a correction update is warranted. Do not suggest the underlying NeonNet is recalibrated or that accuracy is guaranteed continuously unless those claims are validated.

**Endpoint:** We have demonstrated a practical route toward *collecting, characterizing, correcting, and quality-annotating* gaze data at scale. The controlled and driving findings feed back into making future acquisition better.

## 3. Motivation and contribution positioning

### What motivates the work

- Human gaze can provide object-level attention/salience supervision to driving and robotic-learning systems.
- A gaze point is only as useful as its *spatial reliability* in the situation where it was recorded.
- Small angular errors correspond to substantial lateral displacement for distant targets (approximately `distance × tan(angle)` on a perpendicular target plane), which makes real driving especially consequential. **Use the geometry as an intuitive Introduction motivation**, not as an assertion that angular error must increase with distance.
- Neon is appealing precisely because **calibration-free operation makes natural driving acquisition feasible**. We evaluate its capabilities and identify limited, meaningful conditions requiring extra care. Avoid framing the paper as a sensor takedown.
- Existing driving gaze datasets and eye-tracker studies make important contributions, but collecting gaze, using it to train another model, validating the wearable on controlled targets, and **measuring angular error against verified physical targets during real driving** are not equivalent experiments. Compare precisely.

### Three headline contributions

**C1 — Multimodal real-driving benchmark and reproducible reference acquisition.** Purposefully cover different real traffic situations and targets, with voice-driven automated target association, human-verified 2D references, synchronized scene/vehicle measurements, LiDAR-guided depth, GNSS motion, and structured scenario labels. The novelty is the defensible **measurement benchmark**, not mere hardware quantity or an object detector.

**C2 — Driving-motivated controlled robustness characterization.** A substantial, complementary, systematically designed repeated-measures dataset using known targets and automated/checked protocols to distinguish factors with detectable effects from conditions where Neon remains robust. QR-coded experiment identification helps reproducibility. This is **not** a population study just because it contains many recordings.

**C3 — Evidence-informed measurement improvement and operational suitability.** Quantitatively study sparse, wearer-specific in-situ offset correction, compare it fairly with laboratory-derived offsets, and evaluate targeted extensions on held-out driving scenes. Feed the measurement insights into sample-level multimodal quality descriptors and practical offset checking. Do not treat every implemented gate as a separately validated improvement in angular accuracy.

**Avoid claiming:** “first real-world Neon study,” “first road-object gaze correction,” “all previous datasets have invalid gaze,” “all gaze samples now have ground truth,” “quality gates guarantee sub-degree accuracy,” or “we improve downstream BEV model performance” unless a careful literature audit or dedicated experiments establish each claim.

## 4. Reader journey by manuscript section

| Section | Question to answer | What deserves emphasis | What not to let dominate |
|---|---|---|---|
| **I. Introduction** *(write last)* | Why does reliable gaze supervision matter, especially at driving distances? | Motivation, realistic measurement gap, scientific progression, concise findings and contributions | Sensor inventories, long method explanations, every limitation |
| **II. Related Work** *(write after results)* | What has actually been established, and what is our specific experimental distinction? | Driving datasets → wearable validation → in-situ correction/quality; identify meaningful precedents and gaps | Claiming novelty from titles or paper abstracts, generic “not done” claims |
| **III-A. Wearable system** | Why this eye tracker and what sensing is available? | Calibration-free NeonNet, infrared eye cameras, scene camera, high-rate gaze, IMU | Detailed error equations and vendor offset preprocessing (put in III-D) |
| **III-B. Real-world driving dataset** | Why are the driving measurements credible and useful? | Advanced synchronized research vehicle; LiDAR/camera scene context; automated verbal target references and manual validation; scenario diversity | Full inventory of unused sensor specifications, repeat of the same dataset counts |
| **III-C. Controlled experiments** | Why were these specific tests designed? | Driving-relevant factor rationale, broad conditions, known targets, QR-driven protocol, repeated measurements; compact experimental coverage table | Long per-person recording inventories, assuming all participants completed every factor |
| **III-D. Evaluation methodology** | How do the two datasets become rigorous evidence? | Separate accuracy/bias/dispersion/precision; sparse-offset comparison; held-out tests; factor analysis; extended correction; suitability assessment | Wall of hyperparameters before the reader sees the scientific questions |
| **IV. Real-world performance** | Does gaze work in driving, and how easily can it be corrected? | Systematic offset → large gains from sparse in-situ references → number needed → laboratory-versus-driving transfer → scenario trends | Lead with chessboard failures or dozens of small p-values |
| **V. Controlled investigation** | Is Neon robust, and which factors have specific effects? | Broad robustness first; then distance/spatial bias; then pursuit dispersion; connect each result to driving | A list of unrelated null tests, claiming “no effect” as equivalence proof |
| **VI. Transfer and reliability** | Do the controlled insights deliver further practical gains? | Strong baseline; modest but meaningful personalized corrections, dynamic cases/upper tail; integrated quality monitoring and reference checks | “A negative result first,” inflated machine-learning novelty, conflating usability gates with verified gaze-accuracy improvement |
| **VII. Discussion/conclusion** | What have we demonstrated and enabled? | Neon works well after sparse correction; verified measurement foundation; systematic robustness; practical path to scalable quality-aware datasets | Repeating every statistic or ending on a laundry list of caveats |

**The reading path should feel inevitable:** Each chapter answers a question the preceding chapter created. Section III introduces *both* the driving and chessboard reference sources, so Section IV can compare them; Section V then investigates candidate reasons for differing transfer behavior.

## 5. How to make figures and tables tell the story

**Figures are claims with evidence, not illustrations added after writing.** Each should have one memorable interpretation.

- **Driving example figure:** show synchronized eye-tracker view, validated target location, vehicle-camera view with depth-colored LiDAR points, and a brief real-scene description (target, distance, speed, relative motion). This demonstrates the *kind* of data we can now produce. Describe the displayed LiDAR projection honestly; it need not display every pixel of a separate dense fused depth product.
- **Offset benchmark figure/table:** present a clean progression: **Raw gaze → laboratory references → in-situ driving references**. Then show **accuracy vs. number of driving references**, with random vs. geometry-based selection. Use labels that are understandable before the reader reads technical details; avoid squeezed axes and excessive split-level clutter.
- **Controlled-factor figure/table:** show scope and outcome together: tested factor, experimental conditions, coverage, and interpretable finding. Make **robustness visible**, not a sea of dashes; distinguish accuracy from dispersion and lower-field precision.
- **Transfer figure:** show baseline-versus-extended accuracy and P90 plus a *small* set of important driving subgroups. Make small gains legible without exaggerated axes or implying they hold for everyone.
- **Acquisition/quality workflow (if space):** a minimal diagram of two complementary paths—automated reference generation and multimodal quality monitoring—feeding corrected, quality-annotated gaze. Do not replace the real driving example with a dense software flowchart.

For a two-column IEEE manuscript, readable figures are more valuable than plotting every available metric. Use tables for exact values when plots become dense. Captions explain what is shown and the experimental comparison, not an entire second Results section.

## 6. Writing principles that protect the story

1. **Lead with what was learned; follow with supporting evidence.** Suggested order per results paragraph: *question → main finding → decisive data/figure → interpretation → next question*.
2. **Quantify, then interpret.** Readers should not have to decode 15 values to discover one claim. Use a few decisive values in prose and put additional uncertainty/statistics in a compact figure, table, or supplement.
3. **Present strong evidence positively without making it universal.** “Robust under the evaluated conditions” is better than “unaffected by everything.” “No detectable degradation” is not proof of equivalence.
4. **Treat wearer variation as a reason for verification and personalization**, not as failure of the calibration-free sensor. Do not attribute all variation specifically to physical fit unless tested.
5. **Keep simple successful methods central.** Median offset using sparse in-situ references is a meaningful practical result. An extended correction need not be a neural network; complexity is not itself a contribution.
6. **Distinguish bias from noise.** Distance-related direction shifts are not the same as increasing lateral displacement from a fixed angular error. Pursuit-related target-relative dispersion is not automatically sensor noise: it also includes tracking dynamics.
7. **Celebrate dataset quality, not just dataset size.** Purposeful coverage (moving and static targets, intersections, approaches, passes, different distances, viewing regions) and verified reference coordinates matter more than inflating the recording count. Report acquisition scale and evaluated scene/sample scale separately.
8. **Technical precision where it matters.** Sensor synchronization, physical target references, scene-camera intrinsics, offset removal, train/test separation, and depth provenance matter because they establish credibility. List unused vehicle hardware only briefly.
9. **Do not conceal material caveats.** Participant coverage, overlapping drive environments, uneven factor coverage, and exploratory model selection may constrain claims. Explain them briefly at the point where they affect interpretation; do not turn Results into a recital of weaknesses.
10. **Never treat absence of a test as evidence of failure.** Especially in Related Work, distinguish simulation, video observation, real participants, physical fixation targets, wearable devices, on-road studies, and independent angular-error evaluation.
11. **Manual review is a strength, not a contradiction.** Describe **automated generation with manual quality assurance**. Avoid “fully automatic ground truth” if human checks are essential for benchmark validity.
12. **Keep application claims honest.** “Suitable foundation for downstream driving supervision” is supported by measurement evidence; “improves an end-to-end driving model” requires a downstream model experiment.

## 7. Quality monitoring: desired role and evidence boundaries

The quality layer is part of the **same acquisition pipeline**, not a detached fourth paper. It takes the synchronized gaze/scene streams and emits transparent usability annotations in parallel with reference collection. The intent is to *streamline quality-aware data acquisition*, not to assert that a heuristic automatically measures instantaneous gaze accuracy.

Keep the distinct concepts separate:

- **Accuracy**: angular error versus an independently checked fixation target; quantitatively evaluated in the benchmark.
- **Suitability**: whether a sample/interval belongs to an exterior viewing region, the eyes are sufficiently open, and the relevant scene imagery meets selected visibility criteria. Defined operationally for a downstream task.
- **Quality flags**: computed by combining segmentation, optical flow, Laplacian sharpness, IMU, eyelid/blink, and gaze-event information. The current validated evidence for each component may differ.
- **In-situ reference check**: sparse verified fixation events estimate systematic offset and can support deciding when an offset update would be helpful. This is not proof of continuously guaranteed error bounds.

A preliminary high retained-time fraction demonstrates **coverage under the chosen gates**, not improved angular accuracy of retained samples. Don't make a promised accuracy-validation experiment the center of the Discussion if the study is not designed to perform it. Explain what the pipeline actually does and frame retained coverage accurately.

## 8. Related Work: critical differentiation, not performative novelty

Use three story-aligned subsections, then a short synthesis:

**A. Gaze supervision and driving datasets.** Establish the value of previous datasets. Ask whether the data come from actual driving, passengers, video viewers, simulation, or VR; distinguish raw wearable gaze, mapped heatmaps, gaze-on-object labels, and **verified physical target references for accuracy benchmarking**. A large dataset is not automatically an accuracy-validation dataset.

**B. Wearable eye-tracking accuracy and robustness.** Respect thorough vendor and independent Neon studies; check actual participants, distances, brightness/IR, eccentricity, pursuit, repetition, reference apparatus, statistics, and data splits. Our distinction is the **driving-specific, distance-rich benchmark linked to a systematic controlled study**, not merely that we tested Neon. If a prior paper really did a comparable experiment, say so.

**C. In-situ correction and quality assessment.** Explicitly discuss prior traffic-sign and implicit calibration methods, manufacturer offset options, and relevant error/quality modeling. Our distinction is a **fair, systematic transfer comparison with few-reference requirements and verified real-driving targets**, plus a quality-aware acquisition workflow. Road-object-based correction itself is not new.

**Mandatory literature rule:** Do not decide closeness from title or abstract. Examine methods and results; record actual device, experimental setup, participants, target references, evaluation metrics, train/test separation, and what the cited paper *demonstrates*. Say *not reported* when unknown; do not assume not done. Compare only overlapping contributions and acknowledge close precedents.

## 9. Evidence and scope rules for agents

Before changing a claim or number, inspect the current source of truth: the latest experiment summary, results tables, scripts or generated evaluation artifacts, and LaTeX figure. **The current PDF contains provisional numbers and potentially inconsistent updates. Do not silently reconcile them or choose the most favorable result.** Flag discrepancies with a short TODO for verification.

In particular:

- Keep the **number of driving recordings, evaluated scenes, fixation samples, controlled recordings, and participants** distinct. Additional planned participants and recordings are not yet measured results.
- Different controlled protocols have different participant counts and repetitions. Do not imply every participant experienced every condition.
- Report the **evaluated distance range** for each result separately from the full **recorded distance coverage**.
- A person-specific correction evaluated on **held-out scenes from the same recordings** does not establish held-out-day, held-out-drive, new-wearer, or population transfer.
- State whether raw vendor wearer profile offsets were removed, so the meaning of “uncorrected” is clear.
- Depth may be **LiDAR-guided dense metric prediction** from calibrated, deskewed LiDAR plus Depth Anything; keep the actual fusion method/provenance truthful and do not imply every predicted pixel is directly observed by LiDAR.
- A gaze-guided search for candidate objects can introduce selection limitations; a manually verified 2D target reference is independently *localized* relative to the gaze error calculation but does not make the full acquisition process immune to gaze-dependent selection bias.
- Report quality gating and segmentation as **implemented capabilities**; report measured error reductions only where independently supported.
- Be exact about dataset-release status; pilot samples or a landing page do not imply a legally approved full release.
- Do not interpret literature comparisons or observed effects as causal explanations without an experiment isolating the proposed mechanism.

## 10. Reusable instruction to other writing agents

> **Use this guide to revise the current IEEE IV manuscript incrementally.** Preserve the paper's scientific arc: real-driving benchmark → driving-informed controlled validation → transfer back to driving → quality-aware acquisition implications. The reader should see an encouraging, empirically supported validation of Neon and a practical path to creating trustworthy gaze-supervision datasets, not a software-engineering inventory or a catalogue of weaknesses. Lead with contributions and discoveries, use selective quantitative evidence, explain why each experiment follows from the last, and make the benchmark's rich references and scenario coverage tangible. Compare prior studies critically from their actual experimental methods, acknowledging real overlap without treating superficial similarity as duplication. Do not invent or silently change results; mark unresolved details for verification. Keep the current section's role in the larger narrative visible and do not rewrite unrelated sections unless needed for consistency.

## 11. Revision acceptance checklist

Before marking a section ready, ask:

- Can a reader unfamiliar with our research explain **why this section exists** after its opening paragraph?
- Does it foreground **one or two meaningful discoveries** instead of leading with a number dump?
- Does the evidence support the language used—neither too timid nor too certain?
- Do the figure and its caption visually reinforce the main claim at IEEE two-column size?
- Does the section connect to the next experiment naturally?
- Are method details sufficient for reproducibility while avoiding irrelevant technical inventory?
- Are participant coverage, evaluation splits, and prototype-vs-validated capability accurately scoped?
- Does the passage contribute to the final promise: **measured, corrected, and quality-aware gaze supervision**?

---

**Editorial north star:** *The paper validates a promising calibration-free eye tracker for real driving, demonstrates that sparse condition-matched references provide practical correction, explains residual influences through a carefully designed controlled study, and embeds those insights into a scalable multimodal data-acquisition workflow. The novelty is the rigor and experimental connection—not the mere existence of a dataset, a chessboard, or an offset equation.*
