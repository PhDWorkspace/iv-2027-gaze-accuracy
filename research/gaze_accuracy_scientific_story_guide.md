# Scientific Story and Editorial Guide — Gaze Accuracy for Driving

**Working title:** *Towards Reliable Gaze Supervision for Autonomous Driving: A Real-World and Controlled Evaluation*

**Updated:** 2026-11-05  
**Purpose:** This is the editorial source of truth for Codex, Claude, and anyone revising the IEEE IV 2027 paper. It captures **the argument we want readers to understand**, the role of each section, and how figures, experiments, and contributions support that argument. It is **not** a substitute for current evaluation files, LaTeX, code, or verified papers. Do not propagate numbers from this guide without checking the latest `evals/` reports.

---

## 1. The paper in one sentence

**We developed a practical, carefully verified way to measure gaze against physical targets during real driving, used the resulting context-rich benchmark to expose substantial wearer-dependent errors, investigated those errors in a complementary controlled study, and demonstrated that sparse in-situ references reduce driving error more consistently than adding complexity to laboratory-derived correction models.**

The important scientific advance is **the ability to obtain reliable reference measurements where gaze will actually be used**. A median offset is not new. Without the speech-assisted acquisition, automatic target proposals, visual tracking, independent localization, manual verification, synchronization, and scene/vehicle enrichment, however, we would not have had the real-world references needed to measure the errors, test transfer, or demonstrate the correction.

**Editorial north star:** *From gaze labels whose accuracy is assumed to gaze supervision whose accuracy can be measured, improved, and periodically checked during actual driving.*

This paper is **not** primarily a new regression, object detection, or segmentation method. It is a **real-driving measurement and validation paper**, enabled by an integrated dataset-acquisition system and supported by a systematic controlled study.

### The four ideas the reviewer should remember

1. **A distinct and informative driving dataset.** Verified physical fixation targets in natural road scenes, accompanied by synchronized gaze, LiDAR/camera depth, vehicle speed/motion, descriptions, object identities, and relative-motion scenarios. Its value is **reference quality and information density**, not a claim to be the largest gaze dataset.
2. **We can measure the actual problem.** Real driving reveals substantial person-specific systematic offsets. This is not a claim that Neon is a poor sensor; rather, it shows why unverified output is not an adequate spatial reference for all wearers and conditions.
3. **The controlled study explains what can and cannot be assumed.** Across 11 wearers, accuracy and signed bias differ substantially. Viewing distance and position influence bias; the same directional bias change can *improve* one wearer's angular error and *worsen* another's. Other influences have more limited or condition-specific evidence. Some patterns can be fitted, but doing so is not uniformly advantageous.
4. **The acquisition pipeline produces a practical payoff.** On the held-out driving scenes, a few verified in-situ references make a simple wearer-specific offset highly effective. The decisive issue is **where trustworthy calibration observations come from**, not whether a more elaborate model can fit a chessboard.

### What changed from the earlier story

- **Old:** Mostly a sensor robustness report.  
  **Now:** A **validated real-driving supervision-data foundation**, with scientific measurements and a demonstrated correction payoff.
- **Old:** A list of experiments and mostly nonsignificant factor tests.  
  **Now:** An intuitive discovery: **wearers have different offsets; conditions can shift them; identical shifts do not imply identical accuracy consequences**.
- **Old:** Chessboard corrections are ineffective.  
  **Now:** **Simple chessboard median offsets can help considerably**, but additional learned features do not consistently carry their controlled advantages into driving, and driving-derived offsets perform best on median error in the evaluated benchmark.
- **Old:** More advanced correction models are the improvement.  
  **Now:** **Representative in-situ reference acquisition is the improvement**; regression is an informative test of whether controlled error patterns transfer.
- **Old:** Quality filtering and vehicle integration are separate contributions.  
  **Now:** They are useful parts of an **integrated, quality-aware data-production workflow**, without claiming every flag predicts angular accuracy.

---

## 2. Why this matters now: modern driving supervision

Open the **Introduction** with the contemporary research need, not an inventory of sensors.

- Structured representations—scene graphs, graph-guided VLM reasoning, BEV supervision, end-to-end driving, and relational/world-model learning—have shown promising results when models identify relevant road actors and relations rather than treating all visual content equally.
- Such systems frequently use human-defined, annotated, heuristic, or model-derived notions of object importance. **Human gaze could add an observed signal of visual attention** to help select or weight scene regions, objects, and relations.
- **Attention is not ground-truth importance or causal relevance.** A fixated object is not automatically the one that matters most for safety. We motivate potential *relevance supervision*, not claim that gaze-derived relevance has already improved a downstream driver or world model.
- The actual obstacle for spatial supervision is **measurement reliability**. A modest angular error can associate the recorded gaze with the wrong road object, particularly at driving distances. Existing driving-gaze datasets frequently use estimated gaze as a label without independently measuring its angular error against the attended physical object in ordinary driving.
- This motivates the paper's empirical program: **Can we obtain verified references in real driving? What error structure do they reveal? Can controlled experiments explain or predict it? What actually improves accuracy in the intended environment?**

Use prior graph/VLM/BEV/world-model work only as *motivation*. Do not turn this paper into a review of those architectures, and do not claim downstream performance gains we have not tested. Include our earlier BEV-related paper where relevant, but distinguish that work from the new benchmark and transfer evidence.

### Short reusable motivation

> Recent structured driving models emphasize identifying which objects and interactions matter, motivating human gaze as a complementary source of attention supervision. Yet using measured gaze as a spatial label presupposes accuracy that is rarely established under the very conditions where the label will be used. We therefore develop a verified real-driving reference benchmark, characterize the errors it reveals, and evaluate what correction strategy actually transfers to the road.

---

## 3. Three research questions and what answers them

| RQ | Reader's question | Evidence and answer |
|---|---|---|
| **RQ1 — Real-world measurement** | Can we acquire trustworthy gaze references during real driving, and what is uncorrected accuracy? | Speech-assisted target declarations, independent physical-target localization, automatic consistency checks and comprehensive manual review enable a richly annotated driving benchmark. It exposes substantial person-dependent baseline errors. |
| **RQ2 — Controlled characterization and learnability** | Which driving-relevant factors influence gaze error, are their effects consistent between wearers, and can simple models learn them? | A complementary 11-participant controlled study shows broad differences in systematic bias, important distance/position dependencies, increased target-relative pursuit dispersion, and inconsistent additional gains from regression. |
| **RQ3 — Transfer and practical correction** | Do laboratory-learned corrections improve gaze in real driving, and can sparse in-situ references do better? | On the *same held-out driving scenes*, pooled chessboard offsets help, but extra regression terms do not consistently transfer; sparse driving-derived median offsets attain the lowest median error among tested approaches for all three benchmark participants. |

**Do not pre-answer RQ3 in the controlled section.** Section V creates the question, Section VI answers it. State accuracy-monitoring as a capability enabled by repeated verified references, not a fourth RQ claiming validated continuous operation.

---

## 4. The narrative arc: real world → controlled → real world

### Act I — We made accuracy measurable during driving (Section IV)

**Question:** How can we acquire reference measurements *without a laboratory target board* while driving, and what do they reveal?

Lead with a real driving example and dataset scope. Participants verbally identify an intended target; speech recognition identifies the object and event; detection/visual tracking proposes and follows the physical target; automatic checks flag competing or unstable candidates; every accepted assignment is manually reviewed, and a subset is checked by a second annotator. The target centre is localized from the physical object, **not constructed from the measured gaze coordinate**. Gaze restricts candidate search only. Do not make hypothetical circularity the main discussion.

What makes the data distinct: independently verified fixation reference coordinates, target class, object and relative-motion context, range/depth, ego speed, synchronized motion and image measurements, and scene descriptions. Include the important coverage dimensions (approach, passing, pursuit/following, stationary/oncoming, near/far targets) where supported by annotations. Acquisition under sunny/cloudy daylight is a factual scope description, not a central negative narrative.

**Then deliver an empirical result.** The verified benchmark reveals large, predominantly systematic raw error, with considerable differences across participants. This is the reason to ask which variables influence bias and whether correction can be learned. Do **not** use Section IV only to describe CoTracker/optical-flow implementation details.

**Representative snapshot to verify against the latest run:** 245 manually verified scenes, 17 evaluated road recordings, three participants, 73,738 gaze samples; raw median errors **3.96°, 1.48°, and 6.00°**. If numbers change, update manuscript, plots, and `evals/` documentation together. Keep the exact recording roles accurate in Methods without making them the principal Results story.

**End-of-act question:** Why are these wearer-dependent offsets so different, and do known viewing factors explain them?

### Act II — We investigated the errors rather than guessing (Section V)

**Question:** Which observed dependencies are reproducible, wearer-specific, and useful for predicting error?

Begin with the **scope**, simply: 11 participants in the controlled study; seven contributed shorter static-target series with selected distance and illumination conditions; four received more extensive repeated characterization, including three participants from the driving benchmark. More intensive measurements across sessions/days add within-wearer depth. **Do not pretend all 11 completed the same protocol.** Pursuit, outdoor, and other specialized tests must be attributed to their *evaluated* coverage accurately; do not assert an all-four pursuit result unless those files have been scored.

Then tell three connected findings:

1. **Different starting biases.** Under a comparable 1 m bright static condition, wearer-level median angular error spans approximately **1.03–5.37°** and vertical offset approximately **−5.11° to +1.87°**. Large error is often systematic, while gaze dispersion is comparatively less variable. Show all participants in one readable figure, with limited baseline repetitions visibly distinguished.
2. **Conditions can change the offset without having one universal consequence for accuracy.** Viewing distance often causes a downward vertical change, but this **reduces error for a wearer with an initially upward offset and increases error for a wearer already biased downward**. The updated exploratory summary reports downward shifts for eight of nine wearers with measurements at multiple distances, but some measurements have only one recording or are day-confounded. Make the repeated-measures evidence prominent. Field position is also relevant; do not confuse vertical row effects with general radial eccentricity.
3. **Other factors and learning.** Bright/dark testing changes pupil size without a consistently detectable accuracy or signed-offset shift under our evaluated conditions. Pursuit increases *target-relative dispersion*, which contains genuine eye-following dynamics as well as measurement variability. Indoor/outdoor and repetition findings have narrower coverage. Simple linear/Ridge models sometimes improve held-out chessboard accuracy markedly for a wearer, but a constant median remains competitive and is better for others.

**Representative controlled examples:** one participant's position+distance model improves from **1.41° to 0.87°** indoors; for another, adding learned features does not beat the median. These are examples, **not** evidence that all learnt corrections are ineffective. State the regression split and ensure test recordings are disjoint from calibration recordings.

**End-of-act question:** Even when a model explains chessboard error, does that improvement actually survive driving?

### Act III — We tested transfer and found a usable solution (Section VI)

**Question:** Which corrections help when their actual evaluation target is real driving?

Use the **same held-out on-road scenes** and compare corrections by source and model. Explain the baseline concept before showing participant-specific values:

1. **Transfer from controlled measurements.** Pooled chessboard median offsets reduce driving error appreciably. Additional chessboard-trained position/pupil regressions do **not consistently improve** that transfer. Do not claim chessboard calibration fails, or that every learned model is worse.
2. **Sparse in-situ calibration.** A few verified driving references provide strong improvements, and results improve/stabilize with more reference scenes. Random reference selection is competitive with the tested geometric strategies. The 20% calibration subset and the 80% held-out evaluation subset must remain disjoint.
3. **Model complexity versus reference quality.** Driving-trained linear/Ridge corrections do not beat the simple driving-derived median in **median angular error** across the three benchmark participants, though certain models may improve tail (P90) error for an individual. Keep that nuance in a sentence or small table, not a full model-ranking narrative.

**Representative snapshot to verify against the current final evaluations:**

| Correction source | Participant 1 | Participant 2 | Participant 3 |
|---|---:|---:|---:|
| No person-specific correction | 3.96° | 1.48° | 6.00° |
| Pooled chessboard median offset | 0.89° | 1.40° | 1.71° |
| Median offset from the driving calibration partition (20%) | **0.76°** | **0.83°** | **1.41°** |

**Crucial interpretation:** The greatest payoff came from the **verified in-situ reference source**, not from inventing a new estimator. Do not assert an independently tested causal explanation for the transfer gap. Do not say all three errors are below one degree: two are; the third is near 1.4°.

The correction benchmark is held out **by scenes**, principally within already recorded drives. Describe that exactly, without implying generalization to new drives, new sessions, or new wearers. Mention this briefly where interpretation requires it; avoid letting it overshadow what the experiment legitimately establishes.

**End-of-act implication:** The same architecture can generate further verified references, estimate an offset when needed, and support task-aware data quality assessment for subsequent collection.

---

## 5. Main contributions: three coherent achievements

**C1 — A verified, enriched on-road gaze benchmark and reference-acquisition methodology.**  
Speech-assisted fixation events, object proposals, independent localization, tracking/consistency checks, manual validation of every accepted assignment, and synchronized reference/vehicle/depth/scene metadata. This is the enabling innovation: a practical way to create the reference evidence needed for independent accuracy evaluation and sparse in-situ calibration. It is not a claim of fully automatic ground truth or a newly invented tracker.

**C2 — A complementary, driving-motivated controlled investigation of wearable gaze-error behavior.**  
Measurements across 11 people with different coverage depths characterize individual baseline differences, distance/field-position dependencies, illumination and pursuit behavior, and temporal effects. Testing simple regressions asks whether observed dependencies are predictive—not whether an increasingly sophisticated estimator can win a leaderboard.

**C3 — A fair, real-driving calibration-source and model-transfer evaluation.**  
We compare uncorrected gaze, chessboard-derived median and regressions, and sparse driving-derived median and regressions on the same held-out scenes. We quantify few-reference behavior and show the practical value of calibration observations acquired under the intended conditions.

**Supporting integrated capability—not a fourth independent algorithmic claim:** Task-aware data suitability annotations (exterior viewing region/windshield segmentation trained on images from three vehicles, blink/eye-state signals, and empirically informed exposure/motion-blur checks) and the ability to repeat in-situ reference checks. Clearly separate **operational flags** from **verified angular accuracy**.

The strong final idea is **measurement → understanding → effective correction → better future data collection**.

---

## 6. Reader journey by manuscript section — current structure

| Section | Question it answers | Lead with | Avoid |
|---|---|---|---|
| **I. Introduction** | Why should gaze supervision be measured in the context of modern driving models? | Graph/BEV/VLM/world-model motivation → gaze as possible attention signal → missing spatial reliability evidence → RQs, contributions | Promising downstream gains we did not test, long hardware catalogues |
| **II. Related Work** | What is known, what varies across studies, and what precise gap remains? | Driving gaze labels; wearable Neon factor studies with differing findings; correction and transfer precedents | Claiming everyone else is wrong or has never used in-situ correction |
| **III. Experimental Setup and Evaluation** | How are synchronized references and valid comparisons defined? | Neon/vehicle system, controlled design, angular metrics, reference provenance and grouped partitions | Repeating all of Section IV's pipeline story or Results numbers |
| **IV. Real-World Driving Dataset and Reference Acquisition** | What verified dataset did we build, and what accuracy problem does it expose? | Dataset coverage/richness, intuitive acquisition and verification, brief suitability layer, **initial uncorrected road error** | A second implementation-methods section, long lists of tracking algorithms, participant/session nitpicking |
| **V. Controlled Investigation of Gaze Error** | Why do errors differ, do conditions affect them, and can they be learned? | Baseline heterogeneity → geometry and different accuracy consequences → other factors → simple regression | P-ID-heavy narration, a catalogue of null p-values, claiming all factors act oppositely |
| **VI. Calibration Transfer to Real Driving** | What calibration works on the road? | Controlled median vs models → few driving references → driving model vs median; **source matters** | Chessboard ‘failure’ claim, model zoo, hiding upper-tail exceptions |
| **VII. Discussion and Conclusion** | What did we achieve, and what does it enable? | RQ1–3 answered; pipeline enabled measurement and substantial correction; future scalable reference acquisition and gaze-informed learning | Ending as a list of caveats or claiming validated downstream model benefits |

**Critical fix relative to the old guide:** Section **IV is now the real-driving dataset, reference-acquisition workflow, and first raw-accuracy result**. Detailed calibration comparisons are in **VI**. The controlled study is **V**. Do not revert to an older scheme that puts both dataset descriptions only in Section III or treats VI primarily as advanced temporal corrections.

---

## 7. Figures and tables must communicate the discoveries

**Do not make a figure unless its main takeaway is obvious before the caption is read.** The user prefers compact, polished, readable IEEE two-column figures with minimal annotation and actual measurements.

| Figure / table | What a reviewer should see immediately | Design guidance |
|---|---|---|
| **Real driving examples (IV)** | These are *verified physical targets in real scenes* with distances, speeds, and meaningful relative-motion context. | Use actual synchronized frames; distinct gaze point and verified target centre; optional LiDAR/depth and succinct target description. Real examples beat dense software flowcharts. |
| **Controlled baseline and geometry (V)** | Wearers differ markedly; offset is often vertical; a similar distance-related bias shift can help one wearer and hurt another. | Matched 1 m baseline for 11 participants, visibly mark n=1; one clear distance-response panel for well-sampled participants. Put secondary factors in a short table. |
| **Calibration result (VI-a)** | Raw error → chessboard correction → in-situ correction. | One visually economical comparison for the three benchmark participants, with clear angular-error units. |
| **Reference efficiency (VI-b)** | More verified driving references tend to improve/stabilize error; compare against chessboard baseline. | **Solid lines = driving-derived offset from k reference scenes. Dashed horizontal lines = pooled chessboard-offset performance on the same test scenes. Rightmost 20% marker = using all scenes in the 20% calibration partition**, not ground truth and not a value that must match the dashed line. Label this distinction directly. Bands are fold ranges, not confidence intervals, unless statistically calculated as such. |
| **Regression comparisons (V/VI)** | Extra features sometimes help in controlled data, but the driving-derived median is consistently strong. | Small numeric table with raw, median and a few meaningful model variants; retain P90 where it changes the interpretation. Do not read all cells aloud in prose. |

Figures should use the **same participants, same held-out scenes, and consistent correction definitions** wherever they purport to compare methods. Captions explain methods enough to interpret the plot but do not reproduce a second Results section. Never use generic web images in the submitted paper when actual dataset frames are available.

---

## 8. Reference reliability and the true role of pipeline engineering

**This is a strength to explain once, confidently and accurately—not a standing invitation to speculative criticism.**

- Participants explicitly announce the intended physical target, often a well-defined feature such as the centre of a license plate. Spoken information identifies the object and event independently of the numerical gaze offset.
- Gaze is used to define a **generous candidate-search region**; it is *not* used as the target's reference coordinate. Detection and tracking localize the actual object; template/flow/point-tracking and temporal checks support consistency where implemented.
- Multiple competing candidates and implausible associations are flagged; **all accepted labels are manually reviewed**, with a subset independently checked by a second reviewer. The current accepted benchmark contains no unresolved target-identity ambiguity.
- Small objects such as licence plates may occupy only a few image pixels vertically, making **geometric centre localization** substantially finer than several-degree raw gaze offsets in typical scenes. Do not conflate geometric localization with a guarantee that a human precisely foveated a mathematical centre; do not claim zero uncertainty.
- Large, repeatable signed offsets across targets are consistent with a systematic gaze effect and are not explained merely by random bounding-box jitter. Low measured gaze dispersion alone is **not** proof of annotation-centre accuracy.
- Do not present the method as circular just because gaze assists candidate retrieval. Equally, do not claim perfect independence of *scene selection* from estimated gaze: target localization and target selection are different issues. Explain whichever matters for interpretation in a proportionate sentence, rather than burying the core result in hypothetical failure stories.

Avoid listing CoTracker versions, optical-flow formulas, IoU gates, template-matching thresholds, and model filenames in the main paper unless one technical detail is necessary to make the evaluation reproducible. Preserve these in `evals/04_driving_dataset.md` and method documentation.

**Practical distinction:** The main difficulty in in-situ correction is acquiring sufficiently trustworthy references with small human-review effort. The median calculation itself is trivial. This is why the pipeline and empirical calibration result form **one connected contribution**.

---

## 9. Quality-aware acquisition: useful but properly scoped

The pipeline's segmentation, eye-state, and image/motion signals demonstrate that we considered how to create usable data efficiently. They are **supporting infrastructure**, not separately proven gaze-accuracy improvements.

- **Region suitability:** Windshield/window/mirror/interior segmentation trained with annotations from three vehicle types supports determining whether a gaze sample applies to exterior-road supervision. Cockpit gaze can be valid for other tasks.
- **Eye state:** Blink, eyelid aperture, gaze-event and validity signals indicate intervals requiring exclusion or a downstream-specific flag. Do not assert all saccades are invalid for all learning tasks.
- **Image suitability:** Exposure-time and motion tests using marker detectability, alongside available gyroscope/optical-flow/sharpness indicators, inform practical blur checks. Verify exact implemented checks and thresholds; do not claim guaranteed sharpness or direct angular-error prediction.
- **Repeated reference checks:** New verified fixation events can support a fresh estimate of systematic offset and decisions about when recalibration might help. This is **potential monitoring and updating**, not a demonstrated always-on accuracy guarantee.
- **Provenance:** Preserve raw gaze, reference details, quality/suitability flags and scene metadata so later downstream applications can set their own selection criteria.

In the narrative, mention these capabilities **briefly in Section IV** and return to their future value in the Conclusion. Do not let them displace the tested acquisition accuracy and correction results.

---

## 10. Related Work — the precise unanswered question

Arrange the literature around the argument, not a chronological catalogue.

1. **Driving attention and structured supervision:** Existing gaze/attention datasets and new structured graph/VLM/BEV/world-model approaches motivate object-level attention signals. Differentiate target-referenced *measurement accuracy* from datasets that contain gaze estimates or attention maps. Gaze-derived importance remains a hypothesis for future downstream evaluation.
2. **Wearable accuracy and influencing factors:** Respect prior controlled Neon studies; highlight that brightness/pupil and field-position studies report differing findings with distinct setups. The scientific question is **which effects reproduce, how they vary by wearer, and whether their predictive value transfers**—not whether another paper is “wrong.”
3. **Correction, in-situ references, and error modelling:** Prior work has used simple offsets, road objects/traffic signs, implicit calibration, and regression/ML. A neural network may underperform linear regression in one prior task, but **predicting error magnitude is not the same as correcting signed 2D gaze bias**; comparisons must reflect what was actually evaluated. Our distinct test is the chessboard-versus-driving **source comparison on the same verified held-out driving targets**, plus few-reference efficiency.

**Literature evidence standard:** For every claimed gap or close precedent, examine the actual method and experiment: wearable versus remote, physical versus screen/video targets, real driving versus simulation/passenger view, amount of manual reference work, angular metric, and held-out protocol. Do not infer absence or novelty from a title/abstract.

---

## 11. Evidence discipline and instructions for future writing agents

Before changing a result, consult the **current actual source of truth** (data and versioned evaluation in `evals/`, source scripts, split manifests, current LaTeX figures). Some earlier model runs were generated before participant-recording identities were corrected. **Do not copy an older best score or invent a reconciliation.**

### Mandatory checks

- Keep totals distinct: entire acquisition set vs accepted benchmark, recordings vs scenes vs gaze samples, all 11 controlled wearers vs the subset evaluated for each factor or model. Do not claim all wearers received identical tests.
- Keep **angular error**, **signed azimuth/elevation bias**, **target-relative dispersion (PSTD)**, and **sample-to-sample precision (RMS-S2S)** separate.
- Explain that uncorrected means **without the fitted person-specific correction**, and consistently document whether a vendor wearer offset was removed from the data.
- Do not imply all ranges or dense depth pixels are direct LiDAR measurements. Verify LiDAR-derived vs LiDAR-guided/predicted depth provenance and the fraction of scenes with measured distance.
- Distinguish **training-calibration reference scenes** from held-out test scenes. For transfer/model comparison, keep the split identical across methods.
- Do not extrapolate **scene-held-out within recordings** to unseen drivers, independent days or entire sessions. State this precisely, once where material.
- Use participant-level or recording-level aggregation appropriate to the statistical question. Do not make hundreds of samples from one person into hundreds of independent wearers.
- A lack of significance is not proof of no effect; overlapping conditions and board geometry can confound apparent distance/position or between-day dependencies.
- Never say all correction models fail: the controlled data show genuine gains for some wearers, and a driving model may improve P90 while not improving the median.
- Treat flags as **suitability/quality indicators** unless separately validated against actual angular error.
- Avoid unsupported claims like “first ever,” “richest,” “fully automatic ground truth,” “sub-degree for everyone,” or “downstream world-model improvement.” Frame distinct dataset attributes and verifiable results instead.
- Keep publication/release commitments accurate; availability of pilot samples is not proof that all legal permissions for full public release are complete.

### Companion evidence files

- `evals/04_driving_dataset.md`: dataset, acquisition, annotation verification, scene coverage, depth/motion and task-suitability evidence.
- `evals/05_controlled.md`: all controlled baseline/factor findings, participant/recording coverage, tests, regression scores and limitations.
- `evals/06_transfer_to_driving.md`: all transfer sources, model specifications, split/fold scores, reference-count curves, median/P90, and comparisons.

The paper gives the **selected evidence**, not all numerical tables. The `evals/` files preserve the complete analysis so every published value can be traced and rechecked.

---

## 12. Writing and review rules

1. **A first-time reader must understand the dataset before encountering many P-labels or experiment-specific counts.** Introduce the scientific question and coverage, then the pattern, then the decisive numbers.
2. **Paragraphs should have a discovery, not a number dump.** Prefer *question → result → a few decisive values → interpretation → next question*.
3. **Reserve space.** Section V should stay around a compact one-page treatment with one explanatory figure and small factor/model tables; other sections should keep their established length unless a verified result justifies more.
4. **The figures are claims.** Use actual reference frames and measured plots, selected to highlight differences or the calibration source comparison. Avoid crowded legends, unreadable rows, decorative dashboards and duplicate tables.
5. **Positive without advocacy.** Show the real technical achievement, but don't rely on exaggerated novelty or gloss over a limitation that changes interpretation.
6. **Don't let individual edge cases lead the story.** One-off dispersion changes, one participant's recording count, or speculative failure modes go in the evidence notes unless they alter the main conclusion.
7. **Use exact participant role only where methodologically material.** The evaluated benchmark contains three participants who qualify as drivers, although recording roles can differ. Don't claim everyone physically drove in every scene; don't let role differentiation dominate the result.
8. **Don't overemphasize engineering minutiae.** Explain the sequence *spoken fixation → target proposal → independent physical localization and checks → manual validation → depth/vehicle enrichment*. A full package/class name is not itself a contribution.
9. **Connection across sections must feel inevitable.** IV reveals the problem; V investigates it; VI tests the payoff. The conclusion closes the loop with future quality-aware acquisition and attention supervision.
10. **Keep the conclusion a positive end.** Recap the verified driving benchmark, controlled investigation, and in-situ accuracy gains; future gaze-guided graph/VLM/BEV/world-model research is an application enabled by this evidence, not an evaluated outcome.

### Section readiness checklist

- [ ] Does the opening tell a new reader why the section exists?
- [ ] Is the dataset or experimental coverage comprehensible before any participant-by-participant exceptions?
- [ ] Are the main claims and key numbers supported by the current validated data?
- [ ] Does the figure show the *finding* rather than merely list variables?
- [ ] Are reference localization and manual checking described clearly, without overclaiming perfection or turning verification into a defensive digression?
- [ ] Are corrected and uncorrected values compared on matching evaluation scenes?
- [ ] Is model complexity appropriately secondary to reference provenance?
- [ ] Is quality/suitability distinguished from independently measured angular accuracy?
- [ ] Does this section naturally create the next question?
- [ ] Would a reviewer remember the central enabling achievement: **we can now obtain and verify the references needed to improve gaze where it is used**?

---

## 13. Reusable master instruction for Codex / Claude

> Use this guide as the editorial contract for the IEEE IV 2027 gaze-accuracy paper. Preserve the three-stage argument: **(IV) verified, context-rich real-driving reference acquisition reveals a substantial accuracy problem; (V) the controlled study characterizes wearer-specific bias and investigates whether its dependencies can be learned; (VI) a direct real-driving transfer benchmark shows that sparse in-situ references and a simple median offset outperform the evaluated more elaborate alternatives on median error.** Keep the dataset-acquisition and manual-verification capability prominent as the enabling contribution, not just a list of software components. Use a handful of meaningful numbers and memorable figures, not participant-by-participant narration. Show that chessboard median correction can help but added learned terms do not consistently transfer; acknowledge that some models improve selected controlled or upper-tail metrics. Describe quality flags and monitoring as capabilities with explicit evidence boundaries. Ground every specific result in the latest evaluation data, preserve complete numbers in `evals/`, and keep conclusions positive, proportional and reproducible. Modern graph/VLM/BEV/world-model motivation belongs in the Introduction and outlook, not as an untested downstream performance claim.

**Final take-home message:** *A carefully verified in-situ data-acquisition pipeline enables us to measure real-driving gaze error, understand the important wearer-dependent influences, and reduce substantial systematic errors through sparse, representative references—creating a practical foundation for future quality-aware human-attention supervision.*
