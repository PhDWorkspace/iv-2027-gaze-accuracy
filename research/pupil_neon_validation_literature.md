# Pupil Labs Neon — Validation, Accuracy, Data-Quality, and Methodology Literature

**Last updated:** 2026-11-02

## Scope

This note collects publications and technical reports that **analyse Pupil Labs Neon itself or the quality/behaviour of its signals**. It is intentionally narrower than “all papers that used Neon.” Most application papers do not evaluate the tracker and are therefore not useful for understanding its measurement limitations.

The papers are grouped into direct gaze validation, artifact/factor studies, slippage/motion, eye-event and pupillometry validation, real-world systems validation, and Neon-specific methods.

For the IV driving-accuracy paper, the most important papers to read first are:

> **Baumann & Dierkes (2023/2026), Foucher et al. (2026), Salari et al. (2026), Alecka et al. (2026), Pettenella et al. (2026), and Nolte et al. (2026).**

---

# 1. Direct gaze accuracy and precision validation

## 1.1 Baumann & Dierkes — Neon Accuracy Test Report

**Chris Baumann & Kai Dierkes. _Neon Accuracy Test Report_. Pupil Labs, 2023.**  
Updated as **v2 in February 2026**.

- **Type:** Manufacturer validation report
- **Neon-specific:** Yes
- **Main topic:** Gaze accuracy, offset correction, field position, distance, indoor/outdoor conditions, eye appearance, and frame placement/slippage robustness
- **Key headline results:**
  - Approx. **1.8° median per-subject accuracy without user-specific correction**
  - Approx. **1.3° after a simple offset correction**
  - The report shows **spatial structure over the field of view**, including somewhat poorer performance in parts of the lower visual field.
  - Indoor/outdoor median accuracy differs only by roughly **0.2–0.4°** in the reported aggregate results.
- **Important limitation:** This is a **manufacturer report**, not independent validation.
- **v2 note:** The 2026 v2 is **not a second experiment**. Its added field-of-view figure is based on the **same data as v1**; v2 also corrects the stated Neon scene-camera FOV to **103° × 77°**.
- **Relevance to IV:** Essential baseline. It motivates subject/session offset correction and provides the main manufacturer claim against which real-driving performance can be compared.

**DOI v1:** https://doi.org/10.5281/zenodo.10420388  
**DOI v2:** https://doi.org/10.5281/zenodo.18504792  
**Open report:** https://zenodo.org/records/18504792

---

## 1.2 Foucher, Krug & Sauter — Independent Comparative Evaluation of Neon

**Valentin Foucher, Alina Krug, & Marian Sauter. “Independent Comparative Evaluation of the Neon—A New Mobile Eye-tracker.” _Collabra: Psychology_, 12(1), 156503, 2026.**

- **Type:** Independent validation
- **Comparator:** EyeLink 1000 Plus
- **Main topic:** Accuracy, precision, stability, smooth pursuit, fixations, saccades, microsaccades, blinks, pupil responses, head yaw, and head roll
- **Critical finding — IR interference:**
  - Neon in the simultaneous EyeLink setup: approx. **4.27°**
  - Neon-only / EyeLink IR source occluded: approx. **1.45°**
  - Roughly a **66% reduction in angular error** after removing external IR interference.
- **Neon-only precision:**
  - RMS inter-sample distance: approx. **0.097°**
  - Fixation spread (SD): approx. **0.431°**
- **Temporal stability:** Accuracy changed only slightly over several minutes and returned near baseline after head-movement tasks; no clean monotonic drift function was established.
- **Head yaw:** Neon-only showed roughly constant **+0.6° horizontal** and **−0.5° vertical** bias across yaw target positions; error did **not** clearly increase with yaw.
- **Head roll:** Neon-only gaze estimates remained approximately within **±1.5°**.
- **Smooth pursuit:** Neon captured pursuit, although mean pursuit velocity was somewhat lower than presented target velocities; onset timing was complicated by transmission delay.
- **Fixation/saccade events:** Neon detected fewer fixations and saccades than EyeLink and reported longer durations / larger saccade amplitudes.
- **Microsaccades:** Strong limitation; Neon detected far fewer microsaccades than EyeLink.
- **Relevance to IV:** Probably the most important independent Neon benchmark. It shows that nominal laboratory accuracy can be reproduced, but also that external IR can severely degrade Neon.

**DOI:** https://doi.org/10.1525/collabra.156503  
**Open full text:** https://online.ucpress.edu/collabra/article/12/1/156503/217665/Independent-Comparative-Evaluation-of-the-Neon-A

---

## 1.3 Alecka et al. — Neon vs. Tobii Pro Fusion

**Madara Alecka, Evita Serpa, Viktorija Arhipenko, Linda Krauze, & Ilze Ceple. “Evaluation of the Wearable Eye Tracker Pupil Labs Neon for Gaze Fixation Analysis in Screen-Based Fixation Tasks: Comparison with Tobii Pro Fusion.” _Journal of Eye Movement Research_, 19(5), 98, 2026.**

- **Type:** Independent screen-based comparison
- **Comparator:** Tobii Pro Fusion
- **Participants:** 46
- **Setup:** Head stabilized, ~65 cm viewing distance, 13 target positions, white and black backgrounds, randomized target order
- **Overall Neon accuracy:** approx. **1.41° ± 0.92°**
- **White background:** approx. **1.20° ± 0.72°**
- **Black background:** approx. **1.63° ± 1.05°**
- **Background effect:** Significant for Neon (**p < 0.001**).
- **Target position / eccentricity:** No significant Neon position effect:
  - White: χ² = 4.80, p = 0.964
  - Black: χ² = 13.89, p = 0.308
- **Fixation stability:** Neon approx. **0.30 ± 0.09 deg²**, not significantly different from Tobii in their central fixation comparison.
- **Critical limitation:** Neon offset calibration was performed on a **white background for both conditions**. Thus the white/black difference cannot cleanly distinguish illumination, pupil-size change, calibration-state mismatch, or other condition effects.
- **Relevance to IV:** Important for brightness and spatial-position hypotheses. Its null target-position result contrasts with spatial structure in the manufacturer dataset.

**DOI:** https://doi.org/10.3390/jemr19050098  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC13600210/

---

## 1.4 OpenEye — Neon mounted to XR headsets

**Gangtae Park, Mingyu Han, & Ian Oakley. “OpenEye: Cross-Device Eye Tracking for Head-Mounted Displays.” _Proceedings of the ACM on Human-Computer Interaction_, 10(3), ETRA017, 2026.**

- **Type:** Cross-device Neon calibration / gaze-quality benchmark
- **Systems:** Neon mounted to Meta Quest 3, Apple Vision Pro, and XREAL Air 2 Ultra
- **Measures:** Accuracy, precision, linearity
- **Selected results:**
  - Quest 3 NeonXR baseline: approx. **2.281°**
  - Proposed calibrated mapping: approx. **1.727°**
  - Vision Pro configuration: approx. **1.324°**
  - XREAL configuration: approx. **1.835°**
- **Relevance to IV:** Useful mainly as a correction-model reference. It supports testing low-complexity 2-D spatial mappings rather than assuming only scalar radial eccentricity.
- **Limitation:** HMD mounting creates a different optical/mechanical problem than normal Neon glasses or driving.

**DOI:** https://doi.org/10.1145/3806031  
**Full article:** https://dl.acm.org/doi/10.1145/3806031

---
# 2. Pupil size, brightness, and measurement artifacts

## 2.1 Salari et al. — Pupil-size artifact in head-mounted trackers

**Mohammadhossein Salari, Diederick C. Niehorster, Marcus Nyström, & Roman Bednarik. “The effect of pupil size on data quality in head-mounted eye trackers.” _Behavior Research Methods_, 58, Article 17, 2026 (published online December 2025).**

- **Type:** Independent controlled artifact study
- **Devices:** Pupil Neon, Pupil Core, SMI ETG 2w, Tobii Pro Glasses 2, EyeLink 1000 Plus
- **Neon participants:** 24
- **Manipulation:** Screen luminance changed to induce controlled pupil-size changes while fixating a central target.
- **Approximate pupil state across the experiment:**
  - Bright: ~**2.88 mm**
  - Dark: ~**5.05 mm**
- **Critical Neon result — pupil-size artifact:**
  - Apparent gaze displacement between pupil states: approx. **0.94°**
  - Strong statistically significant apparent gaze shift.
- **Absolute Neon accuracy did not significantly change at group level:**
  - Bright: **1.36° ± 0.59°**
  - Dark: **1.41° ± 0.82°**
  - t(23) = 0.34; adjusted p = 1.0
- **Interpretation:** Signed gaze bias can change substantially even when scalar absolute error does not systematically worsen across participants.
- **Precision:** No consistent significant bright/dark effect for Neon in STD precision or RMS-S2S.
- **Data loss:** Neon median data loss was essentially 0% in both conditions.
- **Relevance to IV:** One of the strongest papers for a correction model. It motivates modelling signed error as a function of pupil change relative to a reference state rather than simply “dark vs. bright.”
- **Important limitation:** It does **not** establish a universal degrees-per-mm correction coefficient or the shape of the relationship.

**DOI:** https://doi.org/10.3758/s13428-025-02880-3  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12675653/  
**Open data / code:** https://github.com/mh-salari/psa_data_quality

---

## 2.2 Maquiling, Abdrabou & Kasneci — Pupil–vergence coupling

**Virmarie Maquiling, Yasmeen Abdrabou, & Enkelejda Kasneci. “As Far as Eye See: Vergence-Pupil Coupling in Near-Far Depth Switching.” _ETRA 2026_, Article 112.**

- **Type:** Neon-based measurement-artifact study
- **Main topic:** Whether pupil-size fluctuations contaminate vergence estimates during real near/far fixation
- **Setup:** Physical near/far targets using a beamsplitter; static, luminance-modulated, and blockwise fixation conditions
- **Main finding:** Near/far vergence remained separable, but **pupil–vergence coupling varied substantially between participants and conditions**.
- **Conclusion:** Controlling illumination reduced variability but did **not eliminate pupil-linked vergence effects**.
- **Relevance to IV:** Supports the broader conclusion that pupil state can contaminate derived eye-geometry signals; more relevant if vergence/depth is used than for ordinary 2-D angular accuracy.

**DOI:** https://doi.org/10.1145/3797246.3806212  
**Open preprint:** https://arxiv.org/abs/2604.01917

---

## 2.3 Pfeffer & Dierkes — Neon Pupillometry Test Report

**Thomas Pfeffer & Kai Dierkes. _Neon Pupillometry Test Report: An Evaluation of Neon’s Pupillometry Feature_. Pupil Labs, 2024.**

- **Type:** Manufacturer pupillometry validation report
- **Main topic:** Pupil diameter in millimetres, gaze-angle dependence, slippage robustness, spontaneous pupil dynamics, light reflex, cognitive-load effects
- **Main claim:** Neon pupil-size estimates are designed to remain relatively stable across gaze angle and realistic frame-placement variation.
- **Important distinction:** This validates **pupil diameter**, not gaze accuracy.
- **Relevance to IV:** Useful if pupil diameter is used as a correction/model feature.

**DOI:** https://doi.org/10.5281/zenodo.10057185  
**Open report:** https://zenodo.org/records/10057185

---

## 2.4 Karaer et al. — Neon as a pupillometry comparator

**Irem Karaer, Callum Hunt, Ha-Jun Yoon, Runfeng Ma, Reenette Savant, Vanessa Rodwell, Riddhi Shenoy, Zhanhan Tu, Qadeer Arshad, Elizabeta B. Mukaetova-Ladinska, & Mervyn G. Thomas. “Technical validation of a virtual reality-based eye tracker for neuro-ophthalmic assessment: a reliability and reproducibility study.” _Scientific Reports_, 16, 1134, 2026.**

- **Type:** Clinical technical comparison with Neon as wearable comparator
- **Participants:** 39
- **Main Neon-relevant measurements:** Pupillary light reflex / pupil metrics
- **Agreement examples:**
  - Baseline pupil diameter bias: about **−0.48 mm**
  - Peak constriction bias: about **−0.56 mm**
  - Constriction velocity bias: about **0.22 mm/s**
  - Duration bias: about **−0.052 s**
- **Relevance to IV:** Secondary independent support that Neon pupil metrics capture physiologically meaningful changes; not a gaze-accuracy benchmark.

**DOI:** https://doi.org/10.1038/s41598-025-30773-0  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12789551/

---

# 3. Slippage and physical robustness

## 3.1 Pettenella et al. — Direct slippage-to-gaze-error study

**Alberto Pettenella, Marcus Nyström, Marco Carminati, & Diederick C. Niehorster. “Uncovering the effect of slippage on wearable eye trackers: a motion capture study.” _ETRA 2026_.**

- **Type:** Independent motion-capture + gaze-error study
- **Devices:** Pupil Labs Neon, Tobii Pro Glasses 3, ViewPointSystems Lite
- **Participants:** 12
- **Tasks:** Facial expressions, induced glasses motion, locomotion
- **Key contribution:** Explicitly relates **physical displacement/slippage to gaze error**.
- **Reported high-level Neon result:** Neon was relatively robust against catastrophic slippage errors, staying below roughly **3.5° average gaze error** in the reported conditions.
- **Relevance to IV:** Very high. Driving contains head motion, facial movement, vibration, and frame movement.
- **Caution:** “Robust” does not mean zero slippage-related error; several-degree errors can still matter for your use case.

**DOI:** https://doi.org/10.1145/3797246.3803029  
**Publication record:** https://portal.research.lu.se/en/publications/uncovering-the-effect-of-slippage-on-wearable-eye-trackers-a-moti/

---

## 3.2 Niehorster et al. — Physical slippage during real behaviour

**Diederick C. Niehorster, Alberto Pettenella, Giulio Marano, Marco Carminati, Luca Merigo, & Marcus Nyström. “Slippage of head-worn glasses during real-world behavior: an examination, dataset and testing protocol.” _Proceedings of the ACM on Computer Graphics and Interactive Techniques_, 9(2), Article 20, 2026.**

- **Type:** Physical slippage characterization
- **Participants:** 35
- **Devices:** Two eye trackers and two smart glasses
- **Tasks:** 10 naturalistic tasks
- **Reported physical slippage:**
  - Approx. **0.26–4.05 mm**
  - Approx. **0.10–1.81°**
- **Finding:** Slippage differed substantially by **task**, but not strongly by headset.
- **Critical distinction:** Primarily quantifies **frame motion**, not Neon gaze error.
- **Relevance to IV:** Pair with Pettenella et al. to distinguish “how much the glasses move” from “how much gaze error that movement creates.”

**DOI:** https://doi.org/10.1145/3803534  
**Open PDF:** https://re.public.polimi.it/retrieve/cc2b5f74-9e05-42ec-b631-47f5a7508b2e/Slippage%20of%20head-worn%20glasses%20during%20real-world%20behavior%20an.pdf

---
# 4. Eye-event and gaze-signal behaviour

## 4.1 Turuwhenua et al. — Limits of the Neon gaze signal for OKN

**Jason Turuwhenua, Mohammad Norouzifard, Zaw LinTun, Misty Edmonds, Rebecca Findlay, Joanna Black, & Benjamin Thompson. “A Comparison of Centroid Tracking and Image Phase for Improved Optokinetic Nystagmus Detection.” _Journal of Eye Movement Research_, 19(1), 12, 2026.**

- **Type:** Neon gaze-signal / eye-event validation
- **Participants:** 22
- **Question:** Can standard Neon gaze output reliably detect low-amplitude / short-duration optokinetic nystagmus (OKN)?
- **Baseline Neon gaze method:**
  - Detection accuracy: approx. **0.88**
  - Sensitivity: approx. **0.85**
- **Eye-image alternatives:** Improved overall classification accuracy to roughly **0.91–0.93** and sensitivity.
- **Main conclusion:** Small or brief eye movements can be missed in standard Neon gaze output; direct eye-image methods can recover information.
- **Relevance to IV:** Important distinction between **point-of-gaze accuracy** and **event-detection fidelity**.

**DOI:** https://doi.org/10.3390/jemr19010012  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12922098/

---

## 4.2 Cui et al. — Neon vs. EyeLink DUO for listening-effort markers

**M. Eric Cui, Emilie Verno-Lavigne, Shreshth Saxena, Lauren K. Fink, & Björn Herrmann. “Mobile eye-tracking glasses capture ocular and head markers of listening effort.” _JASA Express Letters_, 5(12), 125202, 2025.**

- **Type:** Construct / signal validation
- **Comparator:** EyeLink DUO
- **Participants:** 26
- **Signals:** Gaze dispersion, pupil size, head movement during speech-in-noise
- **Main finding:** Neon and EyeLink showed similar task-related changes in gaze dispersion and pupil size; Neon additionally captured head movement.
- **Important limitation:** **Not a spatial gaze-accuracy study.**
- **Relevance to IV:** Supporting evidence that Neon captures meaningful dynamic eye/pupil signals, not evidence for point-level angular ground truth.

**DOI:** https://doi.org/10.1121/10.0041807

---

# 5. Real-world / ecological and systems validation

## 5.1 Nolte et al. — Mobile eye tracking in the real world: Best practices

**Debora Nolte, Jasmin L. Walter, Lane von Bassewitz, Jonas Scherer, Martin M. Müller, & Peter König. “Mobile eye tracking in the real world: Best practices.” _Journal of Vision_, 26(2):6, 2026.**

- **Type:** Real-world methodology and validation
- **Device:** Pupil Labs Neon
- **Context:** Large-scale outdoor / urban mobile eye tracking
- **Important contribution:** Measurement quality is explicitly validated **in the environment in which data are collected**, rather than simply assuming laboratory specifications transfer.
- **Gaze validation:** Includes an explicit **10-point Neon gaze validation at approximately 3 m**.
- **Head-tracker validation:** Neon heading compared with physical compass:
  - median heading error approx. **0.55°**
  - no significant start-vs-end deterioration in the reported comparison
- **Relevance to IV:** Extremely high conceptually. Strong precedent for **in-situ quality validation / monitoring**.

**DOI:** https://doi.org/10.1167/jov.26.2.6  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12908716/

---

## 5.2 SocialEyes — Multi-person Neon streaming and synchronization

**Shreshth Saxena, A. Visram, N. Lobo, Z. Mirza, M. Khan, B. Pirabaharan, A. Nguyen, & Lauren K. Fink. “SocialEyes: Scaling Mobile Eye-tracking to Multi-person Social Settings.” _Proceedings of CHI 2025_, 2025.**

- **Type:** Systems / ecological validation
- **Scale:** 60 participants across two events; 30 simultaneous Neon devices per event
- **Contexts:** Live concert and film screening
- **Main contribution:** Streaming, recording, time synchronization, remote monitoring, and projection of egocentric gaze into a shared coordinate system.
- **Limitation:** Not an intrinsic angular-accuracy benchmark.
- **Relevance to IV:** Relevant to ROS/streaming/synchronization and to treating system infrastructure as a methodological contribution separate from gaze accuracy.

**DOI:** https://doi.org/10.1145/3706598.3713910  
**Publication record:** https://experts.mcmaster.ca/scholarly-works/3581896

---

## 5.3 Xu et al. — Neon in real general-aviation flight

**Rongbing Xu, Shi Cao, Michael Barnett-Cowan, Gulnaz Bulbul, Suzanne Kearns, & Ewa Niechwiej-Szwedo. “From signal to construct evidence: multimodal consumer-wearable sensing in real general-aviation flight.” _Frontiers in Neuroergonomics_, 7:1911259, 2026.**

- **Type:** Real operational / ecological signal-quality study
- **Participants:** 40 pilots
- **Context:** Real Cessna 172 flight
- **Signals:** Eye tracking plus EEG, cardiac, EDA, temperature, flight dynamics, self-report, instructor ratings
- **Neon relevance:** Demonstrates strong data availability and usable eye-tracking signal in a genuine operational environment.
- **Important limitation:** Does **not** provide target-level angular ground truth throughout flight.
- **Relevance to IV:** One of the closest ecological analogues to real driving; useful for arguing that operational measurement quality deserves explicit analysis.

**DOI:** https://doi.org/10.3389/fnrgo.2026.1911259  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC13574616/

---

# 6. Neon-specific analysis software / methodology

## 6.1 Chu et al. — PyNeon

**Qian Chu, Jan-Gabriel Hartel, Alex Lepauvre, & Lucia Melloni. “PyNeon: A Python package for the analysis of Neon multimodal mobile eye-tracking data.” _Behavior Research Methods_, 58(8), 2026.**

- **Type:** Neon-specific analysis / methods paper
- **Main contribution:** Open-source Python framework for reading Neon recordings, preprocessing, synchronization, epoching, visualization, mapping gaze to scene video, and standardized export (including BIDS).
- **Literature relevance:** Summarizes Neon hardware and cites both the manufacturer accuracy report and independent Foucher validation.
- **Limitation:** Does not independently validate gaze accuracy.
- **Relevance to IV:** Useful citation for Neon processing, multimodal synchronization, and reproducible analysis tooling.

**DOI:** https://doi.org/10.3758/s13428-026-03089-8  
**Open full text:** https://pmc.ncbi.nlm.nih.gov/articles/PMC13314724/  
**Code:** https://github.com/ncc-brain/PyNeon

---

# 7. Summary matrix

| Study | Independent? | Accuracy | Precision | Pupil | Illumination | Spatial / eccentricity | Head / motion | Slippage | Real-world |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Baumann & Dierkes | No | **Yes** | Some | — | **Yes** | **Yes** | Some | Some | **Yes** |
| Foucher et al. | **Yes** | **Yes** | **Yes** | Yes | **IR effect** | Grid | **Yaw/Roll** | — | No |
| Alecka et al. | **Yes** | **Yes** | Fixation stability | — | **White/black** | **13 positions** | Head fixed | — | No |
| Salari et al. | **Yes** | **Yes** | **Yes** | **Yes** | **Bright/dark** | Central target | Head fixed | — | No |
| Pettenella et al. | **Yes** | **Yes** | — | — | — | — | **Yes** | **Yes** | Semi-natural |
| Niehorster et al. | **Yes** | No | No | — | — | — | **Yes** | **Physical slippage** | **Yes** |
| OpenEye | **Yes** | **Yes** | **Yes** | — | HMD-specific | **Spatial mapping** | HMD | Mounting | No |
| Turuwhenua et al. | **Yes** | Event classification | — | — | Some discussion | — | Eye motion | — | Clinical-ish |
| Cui et al. | **Yes** | No point GT | Gaze dispersion | **Yes** | Controlled | — | **Head motion** | — | Lab |
| Pfeffer & Dierkes | No | No | — | **Yes** | **Light reflex** | Gaze-angle effect on pupil | Some | Pupil robustness | Some |
| Nolte et al. | **Yes** | **In-situ validation** | — | — | Outdoor | Validation targets | **Head heading** | — | **Yes** |
| SocialEyes | **Yes** | Projection validation | — | — | Dynamic | Cross-view mapping | **Yes** | — | **Yes** |
| Xu et al. | **Yes** | No point GT | Signal quality | Yes | Operational | — | **Yes** | — | **Yes: flight** |
| Karaer et al. | **Yes** | Not main target | — | **Yes** | Light reflex | — | — | — | Clinical |
| Maquiling et al. | **Yes** | Vergence | — | **Yes** | **Manipulated** | Depth | — | — | No |
| Chu et al. / PyNeon | **Yes** | No | No | Processing | — | Mapping tools | IMU support | — | Methods |

---
# 8. What is actually established about Neon?

## A. Subject/session spatial offset matters

Multiple studies place Neon accuracy roughly in the 1–2° range after an appropriate offset correction. The manufacturer report shows a clear improvement from approximately **1.8° to 1.3°**.

A robust per-person/session median offset is therefore a legitimate and difficult baseline to beat.

## B. External IR can severely degrade Neon

Foucher et al. observed approximately:

- **4.27°** with EyeLink IR active
- **1.45°** with the interfering source removed

This is the clearest large environmental/hardware effect reported for Neon.

Do **not** translate this into “sunlight causes the same error.” The paper demonstrates external IR interference, not sunlight itself.

## C. Pupil-size change can shift estimated gaze

Salari et al. found an approximately **0.94° apparent gaze shift** induced by the bright/dark pupil manipulation.

However:

- absolute accuracy did **not** significantly worsen at group level,
- Neon precision did **not** show a significant bright/dark effect,
- the direction of the shift differs between people.

Thus pupil state is a plausible **bias-prediction feature**, not a universal fixed correction coefficient.

## D. Visual/background condition can change measured Neon accuracy

Alecka et al. found:

- white: ~**1.20°**
- black: ~**1.63°**

But calibration was always performed on white, so this cannot isolate brightness from calibration-state mismatch and pupil-state change.

## E. A universal radial eccentricity effect is not established

Evidence is mixed:

- Pupil Labs' large dataset shows **spatial structure** and somewhat poorer regions in the lower visual field.
- Alecka et al. found **no significant target-position effect** across 13 positions.

Therefore do not assume:

```math
error = f(eccentricity)
```

as a universal Neon law.

A better empirical model is:

```math
e_x = f(h, v)
```

```math
e_y = g(h, v)
```

and then test whether vertical / lower-field structure survives held-out validation.

## F. Head yaw is not clearly a major independent term

In Foucher's Neon-only yaw task, the device showed roughly constant:

- **+0.6° horizontal bias**
- **−0.5° vertical bias**

These biases did not strongly scale with yaw position. This supports a global 2-D offset interpretation more than a continuous yaw-dependent correction.

## G. Physical slippage exists, but Neon appears relatively robust

Natural tasks can move glasses by several millimetres / over a degree. Pettenella et al. show that Neon is comparatively robust, but this does not mean slippage is irrelevant for high-accuracy applications.

## H. Neon gaze output does not perfectly preserve every eye event

Foucher et al. and Turuwhenua et al. identify limitations for:

- microsaccades,
- very small / brief OKN,
- some fixation/saccade metrics.

This matters when distinguishing **point-of-gaze accuracy** from **event-detection accuracy**.

---

# 9. Gap most relevant to the IV driving paper

Across this literature, there is still no obvious prior study combining all of the following:

1. **Pupil Labs Neon**
2. **actual on-road driving**
3. **explicit target-referenced gaze accuracy measurements during driving**
4. **repeated in-situ validation events**
5. **driving/environmental metadata**
6. **analysis of systematic factors / bias**
7. **correction benchmark evaluated on held-out real-driving observations**
8. **synchronized vehicle / ROS infrastructure**
9. **a dataset where gaze measurement quality is itself documented**

Existing papers cover pieces:

- laboratory accuracy → Baumann, Foucher, Alecka
- pupil-size artifact → Salari
- slippage → Pettenella / Niehorster
- outdoor in-situ validation → Nolte
- operational data quality → Xu
- scalable multimodal systems → SocialEyes
- Neon processing → PyNeon

A strong driving-paper framing is therefore:

> **We make the accuracy of wearable gaze measurable and monitorable in real driving.**

Even if a median offset remains the best correction method, a rigorous pipeline showing:

```text
controlled reference measurements
        ↓
known session/person bias
        ↓
periodic in-situ driving validation
        ↓
quantified residual error / uncertainty
```

is still a meaningful measurement contribution.

---

# 10. References

1. **Baumann, C., & Dierkes, K. (2023).** *Neon Accuracy Test Report*. Pupil Labs. https://doi.org/10.5281/zenodo.10420388  
   Updated v2 (2026): https://doi.org/10.5281/zenodo.18504792

2. **Foucher, V., Krug, A., & Sauter, M. (2026).** Independent Comparative Evaluation of the Neon—A New Mobile Eye-tracker. *Collabra: Psychology, 12*(1), 156503. https://doi.org/10.1525/collabra.156503

3. **Alecka, M., Serpa, E., Arhipenko, V., Krauze, L., & Ceple, I. (2026).** Evaluation of the Wearable Eye Tracker Pupil Labs Neon for Gaze Fixation Analysis in Screen-Based Fixation Tasks: Comparison with Tobii Pro Fusion. *Journal of Eye Movement Research, 19*(5), 98. https://doi.org/10.3390/jemr19050098

4. **Salari, M., Niehorster, D. C., Nyström, M., & Bednarik, R. (2026).** The effect of pupil size on data quality in head-mounted eye trackers. *Behavior Research Methods, 58*, Article 17. https://doi.org/10.3758/s13428-025-02880-3

5. **Pfeffer, T., & Dierkes, K. (2024).** *Neon Pupillometry Test Report*. Pupil Labs. https://doi.org/10.5281/zenodo.10057185

6. **Pettenella, A., Nyström, M., Carminati, M., & Niehorster, D. C. (2026).** Uncovering the effect of slippage on wearable eye trackers: a motion capture study. *Proceedings of ETRA 2026.* https://doi.org/10.1145/3797246.3803029

7. **Niehorster, D. C., Pettenella, A., Marano, G., Carminati, M., Merigo, L., & Nyström, M. (2026).** Slippage of head-worn glasses during real-world behavior: an examination, dataset and testing protocol. *Proceedings of the ACM on Computer Graphics and Interactive Techniques, 9*(2), Article 20. https://doi.org/10.1145/3803534

8. **Park, G., Han, M., & Oakley, I. (2026).** OpenEye: Cross-Device Eye Tracking for Head-Mounted Displays. *Proceedings of the ACM on Human-Computer Interaction, 10*(3), ETRA017. https://doi.org/10.1145/3806031

9. **Turuwhenua, J., Norouzifard, M., LinTun, Z., Edmonds, M., Findlay, R., Black, J., & Thompson, B. (2026).** A Comparison of Centroid Tracking and Image Phase for Improved Optokinetic Nystagmus Detection. *Journal of Eye Movement Research, 19*(1), 12. https://doi.org/10.3390/jemr19010012

10. **Cui, M. E., Verno-Lavigne, E., Saxena, S., Fink, L. K., & Herrmann, B. (2025).** Mobile eye-tracking glasses capture ocular and head markers of listening effort. *JASA Express Letters, 5*(12), 125202. https://doi.org/10.1121/10.0041807

11. **Nolte, D., Walter, J. L., von Bassewitz, L., Scherer, J., Müller, M. M., & König, P. (2026).** Mobile eye tracking in the real world: Best practices. *Journal of Vision, 26*(2), 6. https://doi.org/10.1167/jov.26.2.6

12. **Saxena, S., Visram, A., Lobo, N., Mirza, Z., Khan, M., Pirabaharan, B., Nguyen, A., & Fink, L. K. (2025).** SocialEyes: Scaling Mobile Eye-tracking to Multi-person Social Settings. *Proceedings of CHI 2025.* https://doi.org/10.1145/3706598.3713910

13. **Xu, R., Cao, S., Barnett-Cowan, M., Bulbul, G., Kearns, S., & Niechwiej-Szwedo, E. (2026).** From signal to construct evidence: multimodal consumer-wearable sensing in real general-aviation flight. *Frontiers in Neuroergonomics, 7*, 1911259. https://doi.org/10.3389/fnrgo.2026.1911259

14. **Maquiling, V., Abdrabou, Y., & Kasneci, E. (2026).** As Far as Eye See: Vergence-Pupil Coupling in Near-Far Depth Switching. *Proceedings of ETRA 2026*, Article 112. https://doi.org/10.1145/3797246.3806212

15. **Karaer, I., Hunt, C., Yoon, H.-J., Ma, R., Savant, R., Rodwell, V., Shenoy, R., Tu, Z., Arshad, Q., Mukaetova-Ladinska, E. B., & Thomas, M. G. (2026).** Technical validation of a virtual reality-based eye tracker for neuro-ophthalmic assessment: a reliability and reproducibility study. *Scientific Reports, 16*, 1134. https://doi.org/10.1038/s41598-025-30773-0

16. **Chu, Q., Hartel, J.-G., Lepauvre, A., & Melloni, L. (2026).** PyNeon: A Python package for the analysis of Neon multimodal mobile eye-tracking data. *Behavior Research Methods, 58*(8). https://doi.org/10.3758/s13428-026-03089-8

---

# 11. Recommended reading order for the IV paper

1. **Foucher et al. 2026** — broad independent Neon evaluation
2. **Baumann & Dierkes 2023/2026** — manufacturer baseline + large FOV / in-the-wild dataset
3. **Salari et al. 2026** — strongest pupil-state artifact evidence
4. **Alecka et al. 2026** — accuracy, background condition, target-position null result
5. **Pettenella et al. 2026** — slippage → gaze error
6. **Nolte et al. 2026** — in-situ real-world validation philosophy
7. **Niehorster et al. 2026** — natural-task physical slippage
8. **Xu et al. 2026** — operational ecological measurement-quality precedent
9. **OpenEye 2026** — spatial correction / calibration architecture
10. **PyNeon 2026** — Neon processing / reproducibility
11. **Turuwhenua et al. 2026** — limits for short/small eye-event detection
12. **Pfeffer & Dierkes 2024** — pupillometry validation
13. **Cui et al. 2025** — physiological / construct validation
14. **Maquiling et al. 2026** — pupil effects on vergence
15. **SocialEyes 2025** — systems/synchronization at scale
16. **Karaer et al. 2026** — clinical pupillometry comparison
