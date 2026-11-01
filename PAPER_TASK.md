# Task: Structure and Write the IEEE IV Gaze Accuracy Paper

## 1. Objective

Set up our IEEE IV scientific paper using the experimental results, existing datasets, documentation, and evaluation code in this repository.

**Working title:**

*Towards Reliable Gaze Supervision for Autonomous Driving: A Real-World and Controlled Evaluation*

The paper must communicate a coherent, positive, evidence-based scientific story. It should highlight the significance of the research without exaggerating results or hiding material limitations.

**Most importantly: This is a systematic experimental study, not primarily a paper about engineering a dataset pipeline or developing an offset-correction algorithm.**

We followed a scientific progression:

**Real-world measurements → Performance characterization → Controlled experimental investigation → Transfer of findings back to driving.**

Our strength lies in combining two complementary experimental datasets, comprehensive evaluations, practical correction methods, and reproducible data generation.

## 2. Scientific Motivation

Human gaze provides valuable information about visual attention and decision-making. It offers promising supervision signals for autonomous driving systems, including end-to-end driving models, BEV-based perception, and vision-language models.

Beyond driving, similar requirements arise in robotics, human–robot collaboration, and learning from human demonstrations.

However, such applications require reliable gaze measurements.

Pupil Labs Neon offers convenient calibration-free operation, making it attractive for naturalistic data collection. Yet its actual accuracy and robustness must be evaluated in relevant operating conditions, especially when the measurements are used as spatial supervision.

Our goal is not to demonstrate that Neon is unreliable.

**We want to establish how well it performs, identify conditions affecting measurement quality, and determine how practical methods can further improve gaze reliability.**

## 3. Main Scientific Story

### Stage 1 — Real-world dataset and benchmark

We first investigate Neon under naturalistic driving conditions.

To accomplish this, we developed an automated data acquisition and evaluation pipeline:

- Voice-triggered reference-target annotation.
- Automated object detection and target association.
- Precise 2D fixation-target reference coordinates.
- Manual review and correction where necessary.
- Windshield and vehicle-window segmentation for determining relevant gaze regions.
- Object distance information through camera–LiDAR fusion.
- Vehicle speed from GNSS measurements.
- Rich metadata describing relative motion, ego motion, target motion, object type, road type, and driving conditions.

Our current driving benchmark contains **153 richly annotated scenes from two qualified expert drivers**.

We may include additional drivers later, but the current paper must be written using the available two-driver evaluation. Do not invent future participants or results.

Driving our research vehicle requires specific qualifications and authorization. Accordingly, we emphasize a thorough, task-specific measurement study rather than population-level generalization.

The dataset and automatic evaluation methodology are important scientific assets. The pipeline enables collecting large numbers of reference observations under real driving conditions with manageable annotation effort.

**Main discovery:** Neon demonstrates promising measurement performance. Sparse driving-derived reference observations enable substantial reductions in systematic gaze error.

We also show that driving-derived offset correction transfers more successfully to driving than conventional chessboard-derived correction in our evaluated participants.

Spatially optimized reference-point configurations offer little additional benefit over random selection.

This is particularly valuable because our automated pipeline makes acquiring reference observations in the actual operating environment practical.

### Stage 2 — Understanding measurement variability

During real-driving evaluation, we observe that accuracy and dispersion vary across scenes and conditions.

Because our driving scenes are richly annotated, we can analyze these differences systematically instead of treating them as unexplained noise.

This motivates a second scientific question:

**Which environmental, geometric, and dynamic factors actually influence measurement quality?**

We therefore designed an extensive complementary controlled study.

The existing controlled dataset comprises approximately **200 indoor recordings from eight participants**.

Investigated factors include:

- Viewing distance.
- Gaze eccentricity and spatial image position.
- Brightness and illumination.
- Indoor versus outdoor conditions.
- Static fixation versus smooth pursuit.
- Temporal stability and session effects.
- Accuracy, systematic offset, dispersion, and precision.

The central result should be presented positively:

**Neon demonstrates substantial robustness across many investigated conditions, while specific factors exhibit measurable effects.**

Important findings include:

- No general accuracy degradation with eccentricity across the evaluated participants.
- No significant illumination-dependent accuracy degradation in the tested brightness comparisons.
- No matched indoor–outdoor accuracy loss after corrected preprocessing.
- No detectable systematic within-day offset drift.
- Viewing distance influences accuracy in the evaluated participants.
- Lower image regions show reduced precision, with participant-dependent accuracy effects.
- Smooth pursuit substantially increases dispersion despite relatively stable accuracy.

Do not imply that every investigated factor has an influence.

Negative and null findings are scientifically valuable because they characterize the operating conditions under which Neon remains reliable.

Clearly distinguish systematic accuracy, spatial bias, dispersion, and precision.

### Stage 3 — Transfer to real-world driving

We now return to the driving dataset.

Having characterized systematic errors and relevant influencing factors, we investigate how these findings can improve the practical usability of gaze measurements.

The first baseline is conventional per-person median-offset correction.

Our evaluation demonstrates that a relatively small amount of driving reference data substantially improves accuracy.

Then we investigate extended person-specific correction approaches involving position-dependent corrections and causal temporal processing.

The current results show:

- Consistent overall improvements over the driving median baseline across the evaluated split configurations.
- Modest overall gains, with larger improvements in some challenging dynamic conditions.
- Improvements in upper-tail errors for the participant benefiting from temporal filtering.
- Different participants benefit from different correction mechanisms.

The extended method is not necessarily a sophisticated neural model, and that is not a weakness.

**The scientific contribution is demonstrating that experimentally informed, practical correction strategies can improve real-world gaze measurements beyond a strong baseline.**

Complementary quality assessment uses image exposure, IMU information, and windshield segmentation to identify observations that may be unsuitable for supervision.

This provides a practical path from measured gaze to better-characterized, quality-controlled gaze data.

Only claim validated improvements in quality filtering or uncertainty prediction when supported by corresponding evaluations.

## 4. Research Questions

Use three coherent research questions.

**RQ1 — Real-world performance**

How accurately and reliably does calibration-free wearable eye tracking perform under naturalistic driving conditions, and how effectively can sparse in-situ references correct systematic errors?

**RQ2 — Controlled characterization**

Which environmental, geometric, and dynamic factors influence gaze accuracy, precision, and dispersion?

**RQ3 — Knowledge-informed improvement**

How can insights from real-world and controlled evaluations be used to improve gaze measurements and assess their suitability for downstream supervision?

The questions must follow naturally from the motivation. Each should be answered explicitly in the results and conclusion.

## 5. Scientific Contributions

Present three main contributions in the Introduction.

**C1 — Real-world dataset and benchmark**

An automated acquisition and evaluation methodology producing richly annotated driving scenes with precise 2D fixation-target references, camera–LiDAR-based spatial information, GNSS vehicle motion, and detailed driving-scenario descriptions.

**C2 — Comprehensive controlled validation**

A complementary experimental dataset and systematic characterization of wearable gaze accuracy, precision, dispersion, and robustness across relevant environmental, spatial, and dynamic conditions.

**C3 — Practical measurement improvement**

A systematic evaluation of sparse in-situ offset correction and extended person-specific methods, demonstrating improvements over conventional correction baselines and characterizing benefits in challenging driving conditions.

The dataset is planned for publication. We will establish a dataset landing page with approved pilot examples while legal and release requirements are resolved. Do not claim that the complete dataset is already public.

## 6. Quantitative Results to Incorporate

Read the existing November 1 results summary and verify all values against current evaluation artifacts before writing final claims.

Key reported results:

**Driving median angular error:**

| Method | William | Katharina |
|---|---:|---:|
| Raw | 3.96° | 1.48° |
| Pooled chessboard correction | 0.89° | 1.40° |
| Driving-derived correction | 0.76° | 0.83° |

These results support the importance of collecting reference observations under representative operating conditions.

**Controlled experiments:**

- Distance-related accuracy effects in both evaluated participants.
- No general eccentricity effect across six participants.
- Lower-row precision degradation across six participants.
- Approximately threefold higher residual dispersion during smooth pursuit.
- Broadly robust behavior across several tested illumination and temporal conditions.

**Extended correction, 20% calibration scenes:**

- Katharina: 0.822° → 0.762°, approximately 7.3% improvement.
- William: 0.804° → 0.784°, approximately 2.5% improvement.

The extended correction shows larger relative improvements in several dynamic scenario subsets for Katharina, including fast gaze, approaching targets, and a moving ego vehicle.

Do not merge numbers from different evaluation configurations, and do not imply that all subgroup improvements generalize across participants.

Also examine large-error percentiles, sensitivity to the calibration share, and performance across scene categories.

## 7. Recommended Manuscript Structure

Target a concise IEEE conference paper, using the existing manuscript template and respecting the applicable conference page limit.

**I. Introduction**

Establish the importance of reliable gaze supervision, the application gap, our scientific objective, research questions, and three contributions.

**II. Related Work**

Critically examine eye-tracking validation, calibration and offset correction, gaze datasets, and real-driving accuracy assessment.

Distinguish laboratory evaluation, simulation, existing-dataset analysis, and real-world measurement. Verify important claims against the methods and experiments of the original papers rather than titles or abstracts.

**III. Experimental Methodology and Datasets**

Present the two complementary experimental settings: the real-world driving benchmark and the controlled experimental dataset.

Explain automated annotation, reference localization, spatial metadata, gaze error metrics, and evaluation protocols. Keep software implementation details concise.

**IV. Real-World Performance and Offset Benchmark**

Show real-driving accuracy, systematic offsets, driving-derived correction, chessboard transfer, and reference-point sampling.

Establish both the promising performance and the remaining variability.

**V. Controlled Investigation of Influencing Factors**

Present the controlled analysis as a direct response to the phenomena observed in real-world driving.

Distinguish meaningful influences from factors showing no detectable effects.

**VI. Transfer and Reliability Improvement**

Evaluate extended correction against the driving median baseline, including overall performance, difficult conditions, and practical quality assessment.

**VII. Discussion and Conclusion**

Synthesize the scientific findings, implications for gaze supervision, and material limitations. Summarize the evidence supporting reliable gaze collection and the practical value of condition-matched correction.

Adapt section merging as necessary to fit the page budget without losing the scientific progression.

## 8. Figure Strategy

Plan approximately four primary figures, combining panels where appropriate.

**Figure 1 — Experimental framework and complementary datasets**

Real-world driving, precise target references, automated annotations, spatial information, and controlled experiments.

**Figure 2 — Real-world accuracy and correction**

Raw gaze versus chessboard and driving-derived correction. Include calibration-reference requirements and sampling strategy.

**Figure 3 — Controlled robustness characterization**

Show the major influencing-factor results, highlighting both robust performance and measurable effects. Distinguish accuracy from dispersion.

**Figure 4 — Transfer to real driving**

Overall extended correction, upper-tail performance, and results in challenging dynamic driving conditions.

Every figure should communicate one important scientific finding, not merely display data.

## 9. Writing and Scientific Storytelling Rules

Follow these principles throughout:

1. **Lead with contributions and evidence.** Do not frame the paper primarily as a list of limitations.
2. **Show robustness as a finding.** The absence of substantial degradation under tested conditions is valuable when supported by the data.
3. **Make the experimental methodology visible.** Explain why the real-world observations motivated controlled experiments and how their findings were transferred back.
4. **Be comprehensive internally, selective in the manuscript.** Investigate all important validity threats, but dedicate main-text space to those affecting interpretation.
5. **Do not invent novelty.** Verify competing research carefully and distinguish the precise experimental differences.
6. **Keep the claims appropriately scoped.** Two expert drivers are sufficient for a focused exploratory driving measurement study, but do not support population-level generalization.
7. **Avoid unnecessary engineering emphasis.** The automated pipeline enables the science; it is not the entire scientific story.
8. **Present simple successful methods positively.** A well-validated practical method is valuable even if it is mathematically simple.
9. **Preserve honest negative results.** Include material contradictory findings and do not claim universal improvements.
10. **Do not fabricate results, references, availability claims, or sensor provenance.** If data availability or modality coverage differs among recordings, maintain accurate technical documentation. Keep such details proportional to their relevance in the manuscript.

For evaluation, distinguish person-specific calibration from participant generalization. Preserve scene-level holdouts and explicitly identify any untested cross-drive or cross-day transfer.

## 10. Implementation Instructions

Before writing, inspect the existing paper files, dataset documentation, analysis summaries, figures, and evaluation scripts.

Reuse existing manuscript files, definitions, references, and figures wherever appropriate. Do not overwrite completed sections without justification.

First produce:

- A concise one-page scientific storyboard.
- A section-by-section manuscript outline with paragraph objectives.
- A research-question-to-evidence-to-contribution mapping.
- A figure plan with exact supporting evaluation artifacts.
- A list of missing experiments or numerical values necessary for final claims.

Then set up or revise the LaTeX manuscript and begin drafting the Introduction, Methods, Results, and Discussion from the available verified evidence.

Use the repository's existing coding and scientific-writing skills where applicable.

**The intended impression on the reviewer is:**

This is a comprehensive, reproducible experimental investigation of wearable eye-tracking reliability under realistic driving conditions. It combines a valuable real-world dataset, controlled scientific validation, and practical measurement improvements, while demonstrating that calibration-free wearable eye tracking is a promising foundation for reliable human-gaze supervision.