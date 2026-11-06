# Section IV data basis: real-world driving dataset and reference acquisition

> **Current evaluation update (2026-11-06):** all driving model comparisons now include 266 scenes from 18 recordings. P6 contributes 114 scenes and 23,300 samples from two recordings on one day. Updated held-out raw / chessboard / in-situ medians for P6 are 5.97° / 1.51° / 1.43°; his median elevation bias is −6.03° and median target-relative dispersion is 1.59°. The current raw tables are `data/04_scene_raw_errors.csv` and `data/04_driver_raw_summary.csv`. The detailed narrative below is a historical 245-scene snapshot; current correction results are documented in [Section VI evaluation](06_transfer_to_driving.md).


**Extracted:** 2026-11-05 (Claude Code, for William Engel). **Purpose:** the evidence behind Section IV
([sections/04_real_world.tex](../sections/04_real_world.tex)). This file keeps three kinds of statement apart:
facts read from data, statistics derived from them, and interpretation. **Unverified** items are flagged explicitly.

## 0. How to regenerate

```bash
python3 scripts/make_section4_data.py evals/data/04_scene_inventory.csv   # standard library, data read-only
```

`evals/data/04_scene_inventory.csv` has one row per evaluated scene (245). Columns:

| Column | Meaning |
|---|---|
| participant, recording, event_id, label | scene identity (join key: recording UUID + event_id) |
| cls, subtype | target class from `scene_metadata.json` |
| validated / player_validated | Neon Player validation flag in `detections.json` / `units_driving.csv` |
| frames, active_frames, boxed_active | event frames; frames inside the fixation; of those, frames with a valid target box |
| box_h_med, box_w_med | median target box height/width (px) over boxed fixation frames |
| src_manual / src_tracking / src_model / src_unknown | frames per localisation source |
| method | tracker name and frame count |
| distance_m, distance_source | mean target distance and its source (`lidar` / `camera`) |
| ego_motion, speed_kmh, speed_source | ego motion; mean speed; `gnss` or `annotated` |
| relative_motion, target_motion, side, road, view, exposure, issues | scene tags (schema 2) |
| weather, light, observer, reviewed_by, date | session tags and metadata review provenance |

**Known gap:** for the 47 July plate scenes (older event schema), the per-frame fixation flag is absent, so their
`box_h_med` is empty. Their plate heights were measured separately over the event frames (§D).

## A. Dataset overview

| Item | Value | Source |
|---|---|---|
| Driving recordings on disk | 32 folders, 30 recording UUIDs, 3.43 h (including calibration and older HERMES material) | `driving/recordings/*/info.json` |
| Evaluated recordings | 17 (1.49 h) | `gaze_accuracy/offset/units/units_driving.csv` |
| Verified fixation scenes | 245 (all `player_validated = True` and `validated = True`) | units + `detections.json` |
| Gaze samples in scenes | 73 738 (P1 42 678, P2 10 667, P6 20 393) | `units_driving.csv` `n_samples` |
| Participants | 3: P1 passenger (79 scenes), P2 driver (73), P6 driver (93) | `scene_metadata.json` `observer_role` |
| Dates | 2026-07-15 (9 rec.), 2026-10-14 (3), 2026-10-15 (4), 2026-11-04 (1) | `recordings.csv` `date_berlin` |
| Conditions | daylight; sunny 152 scenes, cloudy 93 | `session.weather/light` |
| Locations | Frankfurt (Oct, vehicle runs `frankfurt_*`), Munich (Nov 4, `munich_*`); July drives have no vehicle run, location not documented | `driving/vehicle_runs/` |

**Classes:** licence plate 115; road sign 75; traffic light 48 (green 26, red 21); pedestrian traffic light 7.
- Sign subtypes: no stopping 25, pedestrian crossing 13, speed 8, no entry 8, cycle path 6, mandatory direction 5,
  parking 3, roundabout 2, …
- Per participant: P1 58 plates / 17 lights / 3 signs / 1 pedestrian light; P2 47 signs / 11 lights / 9 plates /
  6 pedestrian lights; P6 48 plates / 25 signs / 20 lights.

**Per recording** (scenes; distance source; localisation method):

| Recording | Scenes | Distance | Localisation |
|---|---|---|---|
| P2 free-driving_Katharina-Winter_2026-10-14-12-40-18 | 4 | camera | manual boxes |
| P2 …-10-14-16-08-24 / …-16-44-30 | 1 / 1 | LiDAR | manual |
| P2 …-10-15-10-04-48 / …-10-13-43 / …-10-29-25 | 28 / 25 / 14 | LiDAR | manual |
| P1 free-driving_William-Engel_2026-10-15-14-51-10 | 29 | LiDAR 23, camera 6 | bidirectional flow + template |
| P6 free_driving_Stefan-Englmeier_2026-11-04-13-01-29 | 93 | LiDAR 91, camera 2 | CoTracker3 (92), DIS flow (1) |
| P1 free_driving_William_2026-07-15 (9 recordings) | 2–11 each, 50 total | camera | Player plugin (YOLO vehicle + plate detector, IoU tracking); 3 with manual frames |

## B. Scene and target metadata (schema 2, `docs/scene_metadata.md`)

| Field | Coverage | Distribution |
|---|---|---|
| Target distance | 245/245 | mean per scene 4.7–119.6 m, median 27.3 m; `lidar` 183, `camera` (Depth Anything fused with box size) 62 |
| Ego speed | GNSS 191, annotated class 54 (July, no vehicle data) | GNSS mean speed median 26.6 km/h, max 46.2 |
| Ego motion | 245 | moving 181, stationary 55, braking to stop 6, starting 3 |
| Target motion | 245 | stationary 189, moving 56 |
| Relative motion | 245 | approaching 129, none 45, oncoming 22, following 16, passing 16, receding 8, parallel 3, closing in 3, being passed 2, overtaking 1 |
| Target side | 245 | ahead-right 95, ahead-left 87, ahead 38, overhead 17, left 4, right 4 |
| Road type | 245 | urban 160, suburban 81, highway 4 |
| View | 245 | windshield 243, right side window 2 |
| Eye-image exposure around gaze | 245 | normal 137, partly overexposed 63, largely overexposed 45 |
| Image issues | 6 scenes | occluded/detection problem 5, blink 1 |
| Scene description sentence | 245 | fixed structure (who/motion · target/distance/relative motion · image issues) |

**Synchronised data:**
- Frankfurt and Munich runs have vehicle runs with LiDAR, GNSS/INS and the front-left camera. The clock offset
  comes from Time Echo plus manual frame pairs (`docs/synchronization.md`).
- Per-fixation LiDAR/GNSS exports: `driving/vehicle_runs/<run>/event_exports/` (`docs/event_exports.md`).
- July drives have no vehicle data: camera-based distance, annotated speed class.

**Metadata review provenance:**
- The 152 Frankfurt/July scene descriptions and tags were owner-reviewed (scene review 2026-10-31, comment review
  2026-11-01).
- P6's 93 descriptions were generated from measurements, with every event's frame inspected (contact sheets), but
  **not yet owner-reviewed** (`provenance.reviewed_by` = null).
- This concerns the descriptive tags, not target identity: all 93 P6 targets are Player-validated.

## C. Reference-generation workflow

| Step | What is verified here | Status |
|---|---|---|
| Spoken announcement → event | Fixation intervals exist as `annotations.csv` events (`<class>.<nn>.start/end`, type `fixation`); no transcripts are stored in the dataset | Whisper + Hassil are named in Methods III-B and `research/contribution_in_situ_…md`. **Speech code and transcripts are not on this machine; not verified.** The 2026-10-27 audit explicitly did not test the voice pipeline. |
| Candidate detection | July plates: YOLO11m vehicles (conf ≥ 0.25, classes car/motorcycle/bus/truck/bicycle), then a licence-plate detector inside the vehicle box (input 96 px, conf ≥ 0.5) | Neon Player plugin `target_annotation/detection.py` (prototype for plates). Traffic-object YOLO training sets exist (`datasets/traffic_objects`, 1 989 + 2 885 images). |
| Gaze-restricted search region | Methods III-B says the search starts in an extended region around the measured gaze | **Region size not verified** (not in local code). The local plugin seeds by an annotator click; all saved frames have `search_mode = full_frame`. |
| Ambiguity rule | Plugin: IoU ≥ 0.5 to continue a track; stops as ambiguous if the two best candidates differ by < 0.15 IoU; a seed conflicting with the existing track is reported | `detection.py` |
| Reference point | `target_definition = bounding_box_center` (annotation metadata) | `detections.json` |

## D. Annotation verification

**Validation:** all 245 scenes have the Player validation flag (`validated`/`event_validated` True).
**Localisation sources** (frames inside fixations): manual 3 023, tracking 6 026, unknown (July plugin) 12 + the
July event frames.

| Tracker (`method`) | Scenes | Checks recorded per frame |
|---|---|---|
| `cotracker3` (P6) | 93 (some scenes also use DIS flow) | tracking status/quality |
| `bidirectional_flow_template` (P1 Oct) | 29 | forward/backward NCC (e.g. 0.95 / 0.89), direction gap (px), quality, `accepted` reason |
| `dis_optical_flow` | 2 (mixed with other methods) | – |
| manual boxes (all 73 P2 scenes; 3 P1 July scenes partly) | 73 + 3 | `manual_box`, `manual_anchor`; 18 frames `manual_null_target_not_visible` |
| July plugin (YOLO + plate, IoU tracking) | 47 | vehicle/plate confidences |

**Second reviewer:** **no documentation found** in the data repo, `provenance/`, the horuspy review folders or the
`remote-dev` review tools. The manuscript does not claim one. If a second-reviewer subset exists, record who
reviewed which scenes before citing it.

**Agreement metrics:** none available; none reported.

**Corrections and rejections:**
- The schema-2 build corrected 4 scenario/ego contradictions and moving-target distances for 6 Frankfurt events
  (`horuspy/results/driving_scene_metadata_review/README.md`, `driving_scene_metadata_stefan/README.md`).
- Rejected target proposals are not stored as a list. Excluded events simply do not appear among the validated
  units.

**Target size** (derived; box height in scene pixels, median over frames):

| Class | Scenes measured | Median | IQR | Range |
|---|---|---|---|---|
| Licence plate (all 115; July measured over event frames) | 115 | 6.3 | 4.8–8.7 | 2.7–19.8 |
| Road sign | 75 | 14.8 | 12.7–19.2 | 5.6–46.4 |
| Traffic light | 48 | 8.5 | 6.5–10.8 | 4.4–23.1 |

- **Angular scale:** the scene camera focal length is ≈ 888 px (module 272097 calibration), so 1 px ≈ 0.065° at
  the image centre and a 6 px plate is ≈ 0.4° tall.
- **Interpretation, not a measurement:** localising the box centre is uncertain by a fraction of the box. That is
  small compared with the 1–6° systematic offsets, but no annotation-error measurement exists.

**Example scene of Fig. 2:**
- Recording: P2, `89171fda`, event `license_plate.02`, parked car passed on the right.
- Measured values: GNSS speed 26.0 km/h (25.6–26.3); LiDAR distance 18.7 → 13.7 m (mean 16.2); the frame shown is
  the closest, 13.7 m.
- This resolves the `\todo` in Fig. 2's caption: the scene does exist; 13.7 m is the minimum, not the mean.
- Source: `illustration/paper_visuals/01_system_overview/driving_example/` in the data repo.

## E. Task-aware quality checks

| Component | Implementation | Evidence | Status |
|---|---|---|---|
| Region segmentation | `pupil-neon-ros2/scripts/gaze_metrics.py`: YOLO segmentation every n-th frame; the gaze sample's region; classes windscreen, rear mirror, left/right side-view mirror, front-left/right window | Training run `datasets/windshield_segmentation/training_runs/curious_capybara`: yolo26m-seg, 640 px, 44 epochs; final mask P 0.97, R 0.92, mAP50 0.96, mAP50-95 0.76 (best 0.80). Local COCO archive: 15 images (DR(eye)VE), classes windscreen/rear-mirror/road objects | Implemented. **The training set used ("Pupil_Windshield-7") is not stored here; "three vehicles" and the annotation count are unverified.** The gates use more classes than curious_capybara, so they likely use a later model. |
| Blink / eye state | `gaze_gates.py`: `eyes_open` = no native blink and mean eyelid aperture ≥ 2.0 mm; `no_saccade` = outside native saccade events | Neon native `blinks`, `eye_state`, `fixations` streams | Implemented |
| Sharpness | Laplacian variance at half resolution; `sharp` if ≥ 0.5 × recording median | `gaze_metrics.py`, `gaze_gates.py` | Implemented; threshold is a default, not validated |
| Head rotation vs blur | `print_imu_blur`: Spearman(gyro °/s, sharpness) and sharpness per gyro band (0–10–30–60–120 °/s) | Diagnostic printout only; no saved results found | Implemented as diagnostic |
| Gate output | `valid_scenes/gates.csv`, `scenes.csv` (runs ≥ 0.5 s), Player events per failing gate | No `valid_scenes/` folders found in the data repo | Not run on the benchmark (results not stored) |
| Earlier gate test | "4 recordings, 1 participant, 28 min: region + sharpness + eye-openness gates retained 82% in intervals ≥ 0.5 s" | Old Section VI and `research/contribution_in_situ_…md` | **Source outputs not found; not re-verified; not used in Section IV** |
| Exposure × rotation × optical flow × marker detection (motion blur) | – | **No documentation or results found.** Related but different: the exposure command-rate test (`camera_settings_sweep/exposure_rate_tests/`, commands visible ≤ 25 Hz, ≈ 65–80 ms latency), the Munich camera-settings sweep (`camera_settings_sweep/evaluations/munich_20261104_snake_sweep/`, RoMa matching vs settings) and the controller's IMU-rotation pause (`eye-vehicle-fusion/README.md`) | **Not cited in Section IV.** Point me to the experiment if it exists elsewhere. |
| Repeated accuracy checks | Capability: references can be acquired in any drive and offsets re-estimated (Section VI) | – | Online monitoring not validated (stated in text) |

## F. Provenance and outstanding issues

**Sources:**
- `gaze_accuracy/offset/units/units_driving.csv` (2026-11-05 ~16:10, rebuilt after the relabel; driving units
  unchanged by it).
- `driving/recordings/*/{detections.json,scene_metadata.json,annotations.csv,info.json}`.
- `docs/scene_metadata.md`, `docs/synchronization.md`, `datasets/README.md`.
- Neon Player plugin `~/Pupil Labs/Neon Player/plugins/target_annotation/`.
- `~/workspace/pupil-neon-ros2/scripts/{gaze_metrics,gaze_gates}.py`.

**Outstanding issues:**
1. **Methods III-B overlap.** III-B still describes the pipeline with old counts (152 scenes, 2 participants,
   16 drives, distances 7–107 m, 53 345 samples; class counts). Section IV now gives the current ones (245 scenes,
   3 participants, 17 recordings). Suggest trimming III-B to vehicle/synchronisation and moving Fig. 2 into
   Section IV; Section IV already references it.
2. **Speech pipeline and gaze-restricted search region** are not verifiable from local code. The text keeps them
   generic.
3. **No second-reviewer record**, so none is claimed.
4. **Motion-blur/marker experiment not found**, so it is not cited.
5. **Segmentation training data** (count, vehicles) not verifiable locally, so the text says "separately developed
   model" without numbers.
6. **P6's scene descriptions are not owner-reviewed** (target identities are validated).
7. **Table I (`figures/tab_driving_offsets.tex`) is no longer used.** Its results are in Section VI and
   `06_transfer_to_driving.md`.


## G. Refinement of 2026-11-05 (evening): real-world accuracy, figure, owner statements

**Reproduce:**

```bash
python scripts/make_section4.py /home/william/data --figure \
  2bc261876dff5c83baca7b2368ba8bb5 059abc99f815526aa887e650b736d6f5 b329c0dcb73c57c7b37f2f7cfbc35f4d
```

The full event IDs are in `data/04_fig_dataset_scenes.csv`. The script needs pandas and OpenCV (horuspy-dev image),
reads the data read-only, and writes:
- `data/04_scene_raw_errors.csv`: one row per scene, metric-valid samples inside the validated event (median and P90
  angular error, signed offset az/el, target-relative dispersion √(var az + var el), median target distance).
- `data/04_driver_raw_summary.csv`
- `figures/fig4_dataset.pdf` and `data/04_fig_dataset_scenes.csv`

**Raw (uncorrected) accuracy per participant** (scene level; median over scenes, with IQR):

| Code | Scenes | Samples | Median error [IQR] | P90 (median over scenes) | Offset az / el | \|offset\| | \|offset\| / error | Dispersion |
|---|---|---|---|---|---|---|---|---|
| P1 | 79 | 42678 | 3.86 [3.10, 4.12] | 4.28 | -0.49 / -3.77 | 3.80 | 0.99 | 0.48 |
| P2 | 73 | 10667 | 1.37 [1.10, 1.64] | 1.97 | -1.09 / -0.59 | 1.24 | 0.91 | 0.80 |
| P6 | 93 | 20393 | 6.21 [5.51, 7.00] | 6.99 | +0.85 / -6.09 | 6.15 | 0.99 | 1.69 |

**Values used in the text:**
- **Held-out benchmark (Section VI):** raw median error 3.96 / 1.48 / 6.00°, P90 4.63 / 2.20 / 7.80°, from
  `06_driving_offset_by_category.csv`, "Raw driving". This is the mean over 5 folds of the median over held-out
  scenes, so it differs slightly from the scene-level medians above (3.86 / 1.37 / 6.21°).
- **"Offset makes up 91–99%"** is the `offset_share` column. **"Dispersion 0.5–1.7°"** is the `dispersion_median`
  column.
- **Foreshadowed corrections:** 3.96 → 0.76° (P1) and 6.00 → 1.41° (P6) are the 20% driving offsets of Section VI.

**Figure (Fig. 3, `fig4_dataset.pdf`):** the middle frame of each fixation, cropped around the target and gaze.
The green cross is the median verified target centre in that frame; the red circle is the median gaze. Distance and
speed come from `scene_metadata.json` (LiDAR / GNSS).
1. P2 pedestrian-crossing sign, approaching, 22 m, 24 km/h, error 1.2°.
2. P1 red traffic light, both standing, 17 m, error 3.9°.
3. P6 licence plate of a followed car, 28 m, 41 km/h, error 6.1°.

Fig. 2 (III-B, the P2 parked-car example) is unchanged.

**Owner statements used in the text without a local file record:**
1. A subset of references was reviewed by a second annotator (coverage and agreement not documented).
2. The segmentation model was trained on images from three vehicles.
3. Motion-blur checks were informed by experiments on exposure time, rotation and marker detection.

Section E above still lists what *is* verifiable locally. Add the source records for these three statements to
complete the provenance.

**Wording corrections against the task:**
- "Three drivers" is written as "three participants (two drivers, one front passenger)", because P1 was the
  passenger.
- The relative motions named in the text are those present in the data: approaching 129, none 45, oncoming 22,
  following 16, passing 16.
- **Word count:** 501 → 550 (`wc -w`, including the new figure caption, +9.8%).

## H. Owner decisions of 2026-11-06 (override the metadata-derived counts above)

The owner confirmed the following as fixed facts (see `tasks/gaze_accuracy_dataset_rules.md`). The scene metadata
and the derived tables in this file and in `04_dataset_composition.md` do not yet reflect them:

1. **Distance:** every verified scene has a camera–LiDAR-fused target distance. `scene_metadata.json` still marks
   62 scenes as `distance_source = camera` (all 50 July scenes, 4 Oct 14, 6 Oct 15, 2 Nov 4), and the July drives
   have no vehicle run in `driving/associations.csv`.
2. **GNSS/INS:** synchronised GNSS/INS data are associated with every verified scene. The metadata still has
   `speed_source = annotated` for 54 scenes (all 50 July scenes and 4 from the first Oct 14 drive).
3. **Task-suitability flags:** these were applied to the benchmark and validated manually. Their outputs are not
   stored in the data repository.

**To do:** add the underlying LiDAR and GNSS associations and the suitability outputs for these scenes to the data
repository, so that the metadata and these records agree with the paper.
