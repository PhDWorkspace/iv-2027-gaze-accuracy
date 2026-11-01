# Research question and three proposed contributions

**IEEE IV 2027 planning note · 27 October 2026 · proposals, not results**

The strongest direction is **validating when Neon is suitable for object-level gaze analysis in real driving**, then testing correction and identifying which measurements are reliable enough to use. HorusPy and your recordings support a focused study; broad population claims would exceed the data.

**Working title:** *Validating Wearable Gaze for Object-Level Analysis in Real Driving*.

## Research question

**Under which measured conditions can Neon support reliable object-level gaze analysis in real driving, and can correction plus reliability estimates improve its usefulness on held-out recordings?**

In plain language: Can we distinguish the road object a driver is looking at, when should we trust that measurement, and does a correction learned earlier still help later?

## 1. Establish when Neon is suitable for the driving task

Combine controlled point-target recordings with audited reference events from actual driving. Measure angular error, bias, precision and missing data where point references are defensible. Where speech identifies only an object, measure agreement with its region and ambiguity between competing objects. Relate performance to object size/separation and supported conditions such as gaze direction, image brightness and head motion.

**Contribution:** a task-specific validation with clear operating limits, beyond a single average accuracy number. Success means establishing which measured conditions meet a requirement chosen for the intended annotation task; it does not require every condition to pass.

**Available data:** 169 controlled recordings and 23 free-driving recordings, about 2.03 driving hours. Controlled data cover six named people, but 143 recordings and every condition sweep belong to William. Separate intensive within-person evidence from limited replication.

## 2. Establish whether correction transfers to new recordings

Learn signed angular corrections from trustworthy point-reference data, using available gaze, pupil/eye, image-quality and IMU signals. Compare raw gaze, a fixed personal median offset, regularized linear correction and a small boosting model. Hold out complete recordings and, where supported, complete days. Test controlled-to-driving transfer through field-reference agreement.

**Contribution:** evidence about whether condition-dependent correction remains useful outside its training recording and improves over a fixed offset. Error prediction and road-object correction already exist; the transfer experiment is essential.

HorusPy implements the scoring and baseline models. Training remains to be done. Evaluate deployment without test calibration separately from a brief initial labeled calibration block, giving competing methods the same calibration budget. William supplies most of the repeated-condition evidence; equivalent personalized models for everyone are not supported by the inventory.

## 3. Establish which corrected measurements are reliable enough to use

Estimate residual reliability and test whether it identifies ambiguous measurements. Start with a constant residual region and a simple predicted-error score; add condition-dependent predictive regions if supported. Compare assigning an object to every eligible measurement against retaining measurements that meet a reliability criterion.

**Contribution:** a demonstrated improvement in the quality–coverage tradeoff of driving gaze annotations: better agreement at matched retained coverage, or more retained measurements at matched agreement. For probabilistic regions, also test empirical coverage and region size against a constant-region baseline.

Controlled targets can support training/calibration; audited road events support a transfer test. A dispersion ellipse or a correlation with error alone is insufficient. Keep reference ambiguity separate from tracker uncertainty.

## Closest related work

| Existing citation key | Verified overlap and useful distinction |
|---|---|
| `baumann2026neonAccuracy` | Neon already has lab and in-the-wild validation, including 402 people, lighting/slippage variations and offset correction. Your distinction must be driving-task evidence and transfer. |
| `jia2018gaze` | Traffic-sign-based offset correction already works in a moving-car experiment; its three participants were front-seat passengers using SMI glasses. Actual-driver Neon measurements provide a different test. |
| `barz2016prediction`, `kar2020mlgaze` | Condition-dependent error prediction is established in controlled head-mounted and remote-tracker settings. |
| `jamalifard2026fiud` | Factor-informed uncertainty and selective prediction already exist for appearance-based gaze benchmarks. Demonstrate wearable annotation utility beyond error ranking. |
| `niehorster2024glassesvalidator`, `niehorster2025gazeMapper` | Open validation/world-based analysis tools exist, including Neon support. HorusPy enables the experiments; software alone is a weaker novelty claim. |
| `stapel2022driverPerception` | Actual driving, road-object perception and awareness labels already exist, using vehicle-mounted Smart Eye tracking. Your outcome is measurement quality rather than awareness. |
| `salari2026pupilSize`, `pettenella2026slippage`, `foucher2026neon` | Modern Neon pupil-size, slippage and independent-performance evidence provides controls and context. |

An additional paper outside your bibliography uses **Neon with ten actual urban drivers**, studying fixation-duration profiles and attention anomalies. “First Neon driving study” would therefore be unjustified. [Publisher paper](https://www.mdpi.com/2624-8921/7/4/145). No citation key was invented or added.

## Three issues to resolve first

1. **References:** working voice detection identifies a reported target, not an exact fixation point. A car center is not gaze ground truth. Audit instructions, target identity, timing and geometry independently of measured gaze; otherwise report object-target consistency rather than precise road angular accuracy.
2. **Provenance and splits:** audit historical camera calibration and rebuild valid groups. HorusPy currently derives `session_id` from repetition numbers; recording breaks also do not prove glasses were removed and re-worn.
3. **Scope:** keep conclusions within the recorded wearers and usable conditions. Do not promise broad driver generalization, night/tunnel performance or slippage characterization without matching evidence.

These are three feasible contribution designs using existing recordings plus analysis/reannotation. Their strength depends on the results. If the road-reference audit fails, the current data cannot establish precise real-driving gaze accuracy, regardless of model sophistication.

[Detailed evidence and experiment report](evidence_report.md) · [All 125 summary screening decisions](summary_screening.csv) · [Primary-source checks](primary_sources.csv)
