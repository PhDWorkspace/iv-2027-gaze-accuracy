# Evidence and contribution audit: wearable gaze accuracy in driving

**27 October 2026 · target: IEEE IV 2027 · task: research planning and novelty/experiment audit**

The recommended paper is a focused validation study of when wearable gaze supports object-level analysis in actual driving, with correction and reliability evaluated on held-out data. Three contribution designs are feasible from the existing recordings: a task-specific suitability assessment, transferable correction, and reliability-aware annotation. They remain proposed contributions: neither successful model performance nor reliable road ground truth has been established by this audit.

Read [contribution_proposal.md](contribution_proposal.md) for the shorter decision document. Existing bibliography entries, summaries, code, recordings and the Downloads contribution file were not edited.

## 1. Evidence and scope

**Source-verified local facts:** inspected the current Downloads contribution plan, the three older Google Drive notes, HorusPy README/local workflow skill and relevant source, the remote dataset README/catalog, and recording metadata and saved-artifact schemas through the working SSH tunnel to `william-ivl`. HorusPy source snapshot: `7a7a8decdcdcd00a341d7cac95889e802844ff6f`.

**Literature:** all 125 local summaries were screened for relevance; the closest works were checked against their PDFs, including methods and evaluation details that change the comparison. The accompanying [screening CSV](summary_screening.csv) records a decision for every summary; [primary_sources.csv](primary_sources.csv) records the principal primary checks. Selected sections were inspected rather than every page of every primary paper. A targeted external search checked recent Neon validation, in-car correction, uncertainty and analysis tools. This is not an exhaustive systematic review and cannot establish a universal absence of prior work.

**User assumption:** voice-event detection works. This audit does not test its implementation or accuracy. It also does not equate a detected utterance with ground-truth eye direction.

**Not established:** new model results; a published-quality accuracy estimate from the current tables; complete participant identity; independent donning-session IDs; reference-label accuracy; road coverage for each desired condition. No new models or full recording reprocessing were run.

**Policy:** the exact IV 2027 author page and main site could not be retrieved on the access date: [author information](https://ieee-iv.org/2027/contributions/information-for-authors/), [conference site](https://ieee-iv.org/2027/). This is an evidence/planning report, not final manuscript prose or a claim of venue compliance. Dates and policies in the older notes were not adopted.

## 2. What is actually in the recordings

The remote catalog has 277 logical IDs: 203 Neon recording IDs and 74 external DR(eye)VE sequences. Some native/cloud packages duplicate recording IDs; folder count is not study sample size. Counts below use logical recordings.

| Collection | Verified inventory | Interpretation |
|---|---|---|
| Controlled | 169 recordings, about 2.46 h: 136 static accuracy, 18 brightness sweeps, 6 distance sweeps, 8 smooth pursuit, 1 head motion | Strongest source of geometrically defined targets. One head-motion recording does not establish a robust motion study. |
| Participants in controlled data | Six names across seven wearer UUIDs; William 143 recordings, other five people 26 combined | Intensive within-person evidence with small replication. Wearer UUIDs are not independent people. |
| Main free driving | 23 recordings, about 2.03 h, dated 15 July and 14–15 October 2026 | Actual field material, not all densely annotated. Hours are catalog durations, not usable fixation-reference hours. |
| Driving identity labels | 13 Katharina Winter, 9 William, 1 William Engel; the last shares Katharina's wearer UUID | Resolve the conflicting label before joining person-specific data. Do not count it as a verified third driver. |
| Other Neon driving/calibration material | 4 older driving recordings and 1 eye–vehicle ArUco calibration recording | Together with free driving, 28 IDs and about 2.94 h; this larger total includes calibration and heterogeneous older data. |
| Camera-setting sweep | 6 recordings, about 7.16 min, William | Mainly cross-camera acquisition/mapping work; not additional independent driving accuracy ground truth. |
| External DR(eye)VE | 74 sequences | Background/downstream mapping material, not another Neon validation cohort. |

All brightness, distance, pursuit and head-motion protocols are William's. The other participants' controlled recordings are static accuracy. A pooled plot would otherwise make a single person's condition effects look like general device behavior.

William's repeated controlled data span several dates. Katharina's controlled data are dated 21 October, after her 14–15 October driving. William's nine July road recordings are from one day. Therefore:

- Controlled leave-day-out evaluation is plausible for William.
- Multiple road recordings do not establish multiple re-wearing sessions.
- A controlled-to-road test using later laboratory data is retrospective domain transfer, not prospective deployment.
- Road leave-day-out evaluation is constrained by the small and unequal date/driver coverage.
- The old assumption of “three intensively measured expert drivers” is not established by this catalog.

### Annotation and processing readiness

All 169 controlled recordings have saved detections and dataset CSVs. There are 119 controlled per-recording evaluation files. Twenty-two controlled recordings contain protocol-fixation files; 137 aligned stimulus-timeline files exist in controlled results. Their alignment provenance must be checked. Protocol-guided timing can be inferred from gaze movement and an assumed cadence; verified QR alignment uses stimulus timing. The inferred timing must not silently serve as independent proof of gaze accuracy.

Sixteen native driving recordings have saved detection/dataset results. Nine July pilot recordings contain 50 license-plate event objects, 45 flagged `validated`. Seven October recordings contain frame-based detections with sparse saved frame lists relative to video length. A `validated` flag records processing state; it is not evidence of an independent scientific ground-truth audit. Other driving recordings remain unprocessed in these canonical locations.

There are 185 existing dataset CSVs, roughly 4.96 GB. None includes the modern `calibration_status` column inspected in current HorusPy, and companion calibration sidecars were absent in the inspected result locations. This does not prove their numeric results are wrong. It means the current provenance contract cannot be assumed for historical outputs. Some recordings have alternate/original scene-video variants; rebuild or audit with explicit identity, camera calibration, resolution, frame/timestamp correspondence and transformation history before comparing accuracy. Establish whether vendor/user gaze offsets were already applied; camera reprojection and personal offset correction are different operations.

Vehicle MCAP/LiDAR and camera exports exist, but some associations are timing candidates and some exports lack acquisition timestamps. They need not be a dependency of this paper: native scene-camera evaluation avoids conflating tracker error with cross-camera registration error. Reserve the full mapping problem for the separate mapping project.

## 3. What HorusPy provides, and what remains research work

| Capability checked in local source | Current status and implication |
|---|---|
| Native Neon streams and experiment metadata | Gaze, scene/eye clocks, pupil/eye state, IMU, events and raw eye-image access support the proposed features. |
| Controlled target geometry and timing | QR/config-driven boards and pursuit targets; protocol-guided fallback has weaker timing independence. |
| Dataset construction | Separates synchronization, target and metric validity and preserves rows. This supports an auditable denominator. |
| Angular metrics | Gaze–target angular distance, signed azimuth/elevation, bias, dispersion, sample-to-sample measures and coverage are available. |
| Scene calibration/reprojection | Current code checks module identity and records calibration/reprojection provenance. Reprojection is distinct from a learned personal gaze correction. |
| Median and boosting correction | Existing code supplies baseline implementations; it does not establish fitted results for this paper. |
| Reliability model | No validated predictive uncertainty model was established. A sample-spread ellipse is not a calibrated future-error region. |
| Road object processing | Detector components and historical detections exist; README states YOLO components are not yet connected to the recording pipeline. The assumed voice pipeline does not automatically complete geometric reference validation. |

Specific analysis repairs are necessary before paper experiments:

1. `src/models/median_offset.py:44` sets `session_id` from `experiment_repetition`. Repetition integers can recur across people and dates; they are not unique wearing-session identities. Build a manifest with recording UUID, verified wearer, date and independently known donning/block identity. Split according to the claim.
2. `boosting.py` includes an `all_runtime_plus_distance` option using `experiment_distance_m`. Known controlled-target distance is not automatically available in driving. Exclude it from deployable models unless independently measured. Ground-truth target/error columns must never enter deployed features.
3. `fixation_filter.py` offers target-distance sigma clipping. Selecting samples because they are close to a reference can make accuracy appear better. Use a predeclared temporal selection and independent reference-quality rules as primary; any residual-based filtering needs a sensitivity analysis and an explicit retained fraction.
4. Nearest eye-image joins can select a later image. This is acceptable for a declared offline analysis, but does not establish causal online processing or latency. No real-time claim is needed here.
5. Consecutive recordings, simultaneous data streams and many gaze samples are not independent replications. Report counts and aggregate at event, recording/day and wearer levels.
6. `dataset/angular_error.py` undistorts scene pixels and measures separation between scene-camera rays. This is appropriate for scene-image annotation agreement, but is not automatically the angle at the anatomical eye. State the origin/metric explicitly, especially for near targets, and do not compare degrees across protocols without matching their geometry.

## 4. Closest work: what the primary papers actually did

The following distinctions come from the primary PDFs, not from the summaries' relevance claims. Citation keys are existing keys in `phd-literature/bib/references.bib`.

| Key | Verified primary evidence | Overlap and defensible distinction |
|---|---|---|
| `baumann2026neonAccuracy` | Manufacturer report, §§3–5: laboratory targets and an in-the-wild study with 402 people from 53 countries; predefined targets at 0.3–4 m, indoors/outdoors, direct sun, induced headset displacement and offset correction. Also relates gaze-direction distributions to activities. | Strong precedent for modern Neon real-world validation and task-dependent interpretation. Your small sample cannot supersede its population coverage. Driving-specific reference validity and held-out correction/reliability are the proposed additional evidence. |
| `jia2018gaze` | AutomotiveUI 2018 adjunct, PDF pp.3–4: eight laboratory participants; three moving-car participants seated in the **front passenger seat**, using SMI mobile glasses at 120 Hz. Traffic signs supply targets for offset maintenance. A lab trial-to-trial transfer test is reported. | Closest direct precedent for road-object-based correction. Do not describe it as simulator-only, or claim any transfer test is new. Actual-driver Neon measurements, condition-dependent correction and rigorously grouped deployment tests may add evidence. |
| `barz2016prediction` | PDF pp.1–4, OCR checked: monocular head-mounted PUPIL, controlled display/marker geometry; separate error sources and support-vector regression using viewing/calibration geometry. Random partitions of the controlled measurements. | Error-aware wearable interfaces and condition-based error prediction already exist. New claims must concern the modern measurement system, field reference task and independent recording/day transfer. |
| `kar2020mlgaze` | Methods and ML sections, PDF pp.4,16,23: Tobii EyeX 4C and Eye Tribe remote trackers, controlled desktop/tablet conditions, 20 participants; classification and regression, shuffled sample splits. | Condition-linked gaze error and simple regression are established. This is not wearable actual-driver validation. Avoid equating gaze-map saliency metrics with sensor precision. |
| `jamalifard2026fiud` | PDF pp.1–4: image-quality/geometry factors, gradient-boosting teacher and distilled uncertainty for appearance-based gaze estimation on ETH-XGaze, Gaze360 and MPIIFaceGaze; error ranking and selective prediction. | Factor-based uncertainty and rejection are established. Do not call all its data static/laboratory. Your proposed output concerns residual Neon measurement quality and annotation utility across recorded sessions, not a new appearance-based gaze network. |
| `niehorster2024glassesvalidator` | PDF pp.1–4: printable target poster and Python validation, 61 participants for procedure testing, multiple wearable systems for software testing; angular accuracy/precision. | An open, convenient validation pipeline is not new. Your candidate protocol addresses reference targets in moving road scenes and must validate its extra uncertainty. |
| `niehorster2025gazeMapper` | PDF pp.1,4 and workflow: open GUI/Python analysis, world-plane mapping, synchronization and validation; supports Neon among 11 tracker formats. | Do not present wearable analysis, synchronization, target geometry or Neon software support alone as novel. Plane-based validation is a useful controlled comparator, not a complete solution to ambiguous road fixation references. |
| `stapel2022driverPerception` | PDF pp.1,3–5: 13 actual drivers, 91 urban left turns, road-scene perception and a recognition-based awareness task. Uses four-camera vehicle-mounted Smart Eye Pro dx 5.0 tracking. | Actual driving and gaze–object association are established. This paper measures awareness/recognition rather than independent wearable sensor residuals. Its results also argue against treating a fixation as proof of awareness. |
| `salari2026pupilSize` | Abstract and method: controlled brightness while fixating a central target; includes Neon alongside Core, SMI and Tobii. Neon showed an apparent pupil-size-related shift, but unlike the other trackers did not show a significant accuracy change in that experiment. | Pupil/brightness effects in Neon have already been measured. Do not assume that pupil size necessarily explains your driving error, or generalize a screen-brightness intervention to all sunlight conditions. |
| `pettenella2026slippage` | PDF pp.1–3: 12 participants, MoCap, Neon/Tobii Glasses 3/Viewpointsystem Lite, facial expressions, induced displacement and locomotion. | Modern Neon movement/slippage evidence exists. Your IMU measures motion, not displacement of the glasses relative to the face; it cannot identify slippage without additional reference evidence. |
| `foucher2026neon` | Abstract and experimental sections: independent Neon–EyeLink comparison including dedicated Neon-only testing. Concurrent IR illumination substantially affected the comparison; Neon-only accuracy differed. | Independent modern validation already exists. Check interference/control conditions rather than citing the concurrent poor result as normal Neon performance. No equivalent reference eye tracker is present in the inventoried driving data. |
| `alecka2026neon` | Screen fixation tasks, Neon versus Tobii Pro Fusion, 46 participants, chinrest and background variations, with Neon offset handling. | Modern device comparison under controlled fixation is established; it does not itself establish object-specific performance in road scenes. Your sample is much smaller. |
| `macinnes2018wearable` | Methods: Pupil binocular/SMI/Tobii Glasses 2, image-based dynamic mapping and targets at several distances/angles. | Dynamic wearable mapping and multi-distance testing are prior art. Useful historical protocol comparison, with a different hardware generation. Do not call its complete method static-only. |
| `hooge2023robust`, `onkhar2024evaluating` | Primary methods examine wearable movement robustness and static/dynamic Tobii Glasses 2/3 performance. | Movement effects and dynamic validation are not untouched subjects; your one head-motion recording cannot match broad movement-factor coverage. |
| `kasprowski2019implicitCalibration` | Primary method: calibration using probable fixation targets during viewing, rather than only explicit calibration points. | Implicit target association/correction predates this project. In your evaluation, target selection must remain independent of the gaze being scored. |
| `nagpure2025learningToAdapt` | IV 2025, method: face-image gaze model, self-supervised adaptation and weak gaze-zone labels on IVGaze. | Personalized in-vehicle estimation is prior art. It changes an appearance-based estimator; you propose correction/validation of wearable measurements. Do not infer simulator-only data without source support. |
| `hu2022data` | PDF pp.2,4: HTC VIVE PRO EYE virtual-reality platform and more than 550,000 relabeled samples for calibration-free attention estimation. | The simulator/relabeling distinction is supported here. Its learned attention/mapping output is different from independent Neon hardware-error validation. |
| `kasahara2022lookBothWays` | PDF pp.1,3–6: actual on-road collection, Tobii glasses, driver/road cameras and 28 subjects with five held out. | Real-road driver gaze datasets and held-out-person evaluation already exist. Your distinction must concern measurement validation, not simply “real driving.” |
| `kotseruba2024dataLimitations`, `kotseruba2024taskContext` | Primary papers analyze driving datasets, synchronization/mapping/label limitations and task effects; the latter corrects DR(eye)VE gaze-map processing. | Useful precedent for auditing supervision quality. Reduced saliency-map noise is different from identifying signed sensor bias, but your pipeline must also separate sensor, timing and mapping error. |
| `contreras2026laia` | PDF pp.1,4: CARLA simulator, 44 participants and Tobii Glasses 3. | Simulator distinction is supported for LAIA. Do not extrapolate that limitation to all public driving gaze datasets. |

Additional methods/context papers are retained in the screening file: Ehinger's test battery, Blignaut's data-quality study, Choe's pupil dynamics, noise/measurement fundamentals, slippage-robust estimation and Pupil Invisible tooling. They inform metrics or controls but do not independently establish your proposed contribution.

### Relevant work missing from the present bibliography

- **Enhancement of ADAS with Driver-Specific Gaze Profiling Algorithm—Pilot Case Study.** The publisher's methods describe ten licensed young drivers on an actual urban route using Neon. The target is fixation-duration profiling/attention anomalies, with manually coded categories, rather than independently referenced angular sensor accuracy. This rules out a “first Neon actual-driving study” claim. [Publisher](https://www.mdpi.com/2624-8921/7/4/145).
- **PyNeon: A Python package for the analysis of Neon multimodal mobile eye-tracking data.** Official project documentation and publication metadata establish a 2026 Behavior Research Methods paper, DOI 10.3758/s13428-026-03089-8, with Neon data import, preprocessing and scene-video/AprilTag mapping. Generic integrated Neon analysis is already covered. [Official project](https://ncc-brain.github.io/PyNeon/), [publisher](https://doi.org/10.3758/s13428-026-03089-8).

No keys were invented and no bibliography was changed for these two external sources. Add them through the normal verification workflow before a manuscript cites them with keys. Other search hits were not used to establish detailed novelty claims when their primary text could not be retrieved.

### Why the summaries cannot be the final authority

At least one summary (`ehinger2019testBattery`) attributes its opening description to Niehorster et al. while naming Ehinger's paper; several summaries contain inferred metadata or sweeping relevance claims. The current report uses actual PDFs for distinctions that affect novelty. The screening CSV takes titles from BibTeX when available but is not a full bibliographic correctness audit.

## 5. Recommended scientific design

The three contributions are one connected argument: **measure suitability → test correction → decide what can be used**. The framework and a small auditable example subset support all three. Do not split the same dataset/tooling achievement into several purported scientific discoveries.

### C1 — Task-specific suitability under recorded conditions

Define the intended task before viewing final test results: identifying the referenced road object among visible alternatives, not estimating microsaccades, proving awareness, or certifying safety. Define the required accuracy/agreement and retained coverage from that task rather than inventing a universal angular threshold.

Create three reference tiers:

- **Point reference:** independently localized, precisely instructed fixation point and defensible timing. Score gaze–target angular error and signed residuals. The instruction/compliance assumption remains explicit.
- **Object reference:** the utterance/protocol identifies an object but not a point within it. Annotate its region and possible competing objects independently of gaze. Score target consistency, ambiguity and angular distance to the region, not center-distance as true gaze error.
- **Unreferenced free gaze:** use for operating-condition and tracking-availability distributions, not accuracy ground truth.

For road polygons, a zero distance to the intended-object region means consistency with the reference, not proof of exact fixation accuracy. Detector boxes may include background, so audit tight regions on the evaluation subset. For narrow, explicitly instructed license-plate points, quantify localization/timing and finite target extent; do not assume the instruction existed just because the detector produces a center.

Report task-scale performance, error quantiles and coverage per wearer, recording and supported condition. The existing `image_left/right_brightness` features describe eye images, not scene illumination. Scene-brightness features would need extraction from the existing scene videos. Check finite feature coverage before choosing model inputs; neither image measure is calibrated ambient illuminance. Brightness sweeps may identify within-protocol effects for William; observational road condition differences are associations, not causal effects. Pursuit tracking and head motion need separate metrics/interpretation from static fixation precision.

### C2 — Correction with explicit deployment conditions

For point-reference samples use signed residuals `e = (az_gaze − az_target, el_gaze − el_target)`. Predict a correction from training data; score corrected gaze with the spherical angular metric already implemented. The azimuth/elevation representation needs wrap and high-eccentricity checks.

Start with four comparisons: raw; fixed personal median offset; regularized linear correction; small boosting model. A complex neural estimator is not necessary for a strong answer. Compare models at the same eligible samples and coverage.

Use two distinct deployments:

1. **Zero labeled calibration in the test block:** training-only personal correction, no test residuals or unknown test-session effects.
2. **Brief calibration:** a predeclared initial labeled block estimates a small offset; freeze it and score only subsequent, disjoint events. The baseline receives the same calibration budget.

Outer splits keep whole recordings/days together; any known common donning block stays together. Inner tuning, feature selection, normalization and reliability calibration use training data only. Check repeated stimulus/config correlations and domain overlap. A model trained on controlled point targets can be transferred to field object consistency without pretending the field supplies exact signed residuals.

Avoid unsupported target distance and session IDs as inputs. Distinguish all-runtime models from offline oracle ablations. Show simple feature-group ablations and whether the result survives removal of questionable reference events. Report held-out failures as well as improvements.

### C3 — Reliability and annotation usefulness

Start with a training/calibration-only constant two-dimensional residual region and an empirical error threshold. Compare a simple scalar error/reliability predictor; condition-dependent variance is a later candidate. If enough independent calibration events exist, evaluate 50/80/95% predictive regions with empirical coverage and size. Nominal 95% coverage cannot be interpreted strongly with very few held-out events.

Ranking quality, probability calibration and annotation utility are different outcomes. Evaluate reliability using retained-coverage versus error/agreement curves, and compare retained object-reference agreement at matched coverage. A method that discards almost everything must not appear superior merely because the remaining few targets are easy.

For the field subset, ambiguity about which object was intended, where within it the eye was directed, and speech delay must remain visible. A larger error region can improve object inclusion without improving discrimination; report ambiguity and assignment to competing objects. A calibrated region on controlled targets does not automatically stay calibrated on the road.

Do not advertise the already implemented dispersion ellipse as predictive uncertainty. If condition-dependent uncertainty fails to beat a constant region, keep the constant region and report that limitation; the stronger model contribution is then unsupported.

## 6. Minimum experiment package and decision gates

| Priority | Work using existing material | Evidence produced / decision |
|---|---|---|
| P0 | Freeze a logical-ID inventory; resolve wearer conflict and known donning blocks; document missing identities. | Valid denominators and defensible splits. |
| P0 | Audit one representative recording from each format/video variant, then rebuild/audit all analyzed data with explicit calibration and clock provenance. | Separates geometric processing effects from personal correction. |
| P0 | Blind reference audit of existing road events: voice identity/timing, target geometry, instruction meaning and ambiguity. Include difficult/rejected cases. | Decide whether field claims concern point accuracy, object consistency, or only availability. |
| P1 | Independent manual subset: two annotators where practical; compare timing, object identity, geometry and disagreements, including failures. | Quantifies reference/automation error; agreement does not prove actual eye fixation. |
| P1 | C1 metrics by wearer and supported conditions, with task requirements chosen before final testing. | Measured suitability envelope and limits. |
| P1 | C2 raw/offset/linear/boosting tests with grouped outer splits and matched calibration budgets. | Evidence for correction transfer, or a justified simpler model. |
| P1 | C3 constant versus predicted reliability, matched-coverage object consistency and reference sensitivity. | Evidence for usable reliability, or limits to that claim. |
| P2 | Minimal runnable HorusPy example and small audited subset, within existing release permissions. | Reproducibility support; full raw-data release is not required. |

Primary metrics: per-event angular-error summaries and tails where point references exist; signed bias; fixation dispersion; eligible duration and tracking/reference availability; object agreement/ambiguity; risk versus retained coverage. Keep tracking loss, missing reference, synchronization failure and deliberate rejection as separate quantities. Use native timestamps for sampling gaps; do not define data loss only as the fraction of surviving CSV rows marked invalid.

First aggregate within events, then show recordings/days and wearers so long fixations and William's many samples do not dominate every result. Resample blocks/events at a defensible level for descriptive uncertainty; with very few days or wearers, show the individual results rather than presenting a narrow population confidence interval. Do not infer population driver variance from the current small cohort.

A workable figure set is: data/reference flow and coverage; controlled-versus-road task-scale performance; grouped held-out correction comparisons; reliability/coverage curves with ambiguity. An annotation-time/quality comparison can substantiate the enabling protocol, but needs actual measurement rather than a claimed efficiency gain.

## 7. Critical verdict and changes to the earlier plan

**Keep:** known wearer–device characterization, signed bias versus residual spread, independent-session tests, separate zero-shot/brief calibration, uncertainty quality rather than merely a large ellipse, and reproducible reference processing.

**Narrow:** population claims; “three expert drivers”; comprehensive motion effects; cross-session road claims where only one road day is verified; physically measured illumination/slippage; public full-dataset promises; mandatory full covariance modeling.

**Move to supporting infrastructure:** “YOLO + angular error + open source.” Prior tools and road-object correction already establish major components. The methodological value is a validated reference process with measured uncertainty and reproducible experiments.

**Reserve for the mapping paper:** cross-camera fusion, LiDAR/depth recovery, exposure optimization and downstream BEV supervision. They introduce additional error sources and could obscure the accuracy question.

The strongest reviewer objection is that apparent road error is actually target/timing ambiguity and that the correction learns it. The decisive repair is independent reference construction and a point-versus-object distinction. The next objection is leakage or pseudoreplication: address it with verified grouping and per-wearer/day results. A third objection is incremental novelty: answer it with the actual driving task, independently quantified reference quality and transfer/annotation-usefulness evidence, not simply the newer tracker name.

**Decision:** proceed with the three contribution designs in the short report, without promising positive results. Existing recordings plausibly support them after provenance checks and reannotation. If the road-reference audit fails, a precise real-driving accuracy claim cannot be rescued by a more sophisticated model; narrow the paper to controlled validation plus exploratory field consistency, or obtain additional defensible references. This is the main feasibility uncertainty left by the audit.
