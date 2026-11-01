## Automatic Driving Gaze Dataset Generation Pipeline

I want to emphasize the innovative and practical aspects of our driving gaze dataset generation pipeline. This is an important contribution of our paper, so the explanation should be positive, engaging, and scientifically convincing.

**The central idea:** We developed a semi-automated pipeline that allows us to collect and evaluate gaze accuracy during natural driving, without requiring dedicated calibration targets or manually annotating every frame from scratch.

### How it works

1. **Natural driving and voice annotations:** We drive around wearing Pupil Neon eye-tracking glasses. Whenever I intentionally fixate an object, I give a voice command such as "Fixating stop sign." Our voice detection system identifies this event, providing a timestamp and the object category being fixated.

2. **Gaze-guided object detection:** We already have the gaze coordinates. Because we know the approximate expected gaze error, we define a search region around the gaze position instead of searching the entire image. We then detect objects of the requested category, such as stop signs, within that region.

3. **Automatic target assignment:** The pipeline identifies the most plausible matching object, typically based on proximity to the gaze position and other available criteria. When the assignment is sufficiently unambiguous, the target can be assigned automatically.

4. **Ambiguity detection:** In complex scenes, multiple objects may be plausible candidates, such as several vehicles or license plates. Instead of blindly assigning a target, the pipeline flags ambiguous cases for manual review.

5. **Integrated visual validation:** We developed a dedicated **Pupil Neon Player plugin** that allows us to inspect recordings, gaze coordinates, object detections, tracking results, and target assignments. Within this interface, we can:
   - Inspect and validate automatically assigned targets.
   - Correct incorrect assignments.
   - Manually annotate targets when object detection fails.
   - Correct missing or inaccurate detections and tracking results.

6. **Manually validated dataset:** Importantly, **every target assignment in our current dataset has been manually validated**. Automation accelerates the initial annotation process, while human review ensures that the final dataset is not dependent on unverified automatic detections.

### Why this is an important contribution

Traditional controlled gaze accuracy experiments rely on predefined targets, such as chessboards, and carefully structured fixation sequences. These are useful for measuring accuracy under controlled conditions, but they cannot easily reproduce the complexity of natural driving.

Our pipeline bridges this gap:

- **Naturalistic data collection:** We measure gaze behavior in actual driving situations, including different object types, distances, relative motions, and environmental conditions.
- **Efficient annotation:** Voice triggers, gaze-guided detection, and automatic association dramatically reduce the amount of manual annotation required.
- **Human-in-the-loop reliability:** Ambiguous detections can be reviewed and corrected, while all final assignments are manually validated.
- **Reproducibility and traceability:** Recordings, voice events, gaze measurements, detections, and validated target assignments remain associated, allowing subsequent evaluation and verification.
- **Scalability:** Instead of manually identifying every target throughout long recordings, we can automatically generate candidate annotations and focus manual effort on validation and difficult cases.

### How to present this in our paper

The key message is that **we turn natural driving recordings into systematically annotated gaze evaluation data through an efficient, gaze-guided, human-in-the-loop pipeline.**

This is more than simply running object detection on driving videos. We combine intentional voice annotations, eye-tracking measurements, targeted visual detection, automatic object association, ambiguity handling, and an integrated manual validation interface.

The result is a practical dataset generation methodology that makes real-world gaze accuracy evaluation more feasible and supports systematic investigations of gaze uncertainty under diverse driving conditions.

Present the pipeline as a methodological contribution in its own right, alongside our gaze accuracy characterization and offset correction experiments.

Keep the explanation positive and focused on what we developed and demonstrated. At the same time, distinguish automatic candidate generation from the manual validation step; we should not claim the dataset is generated entirely without human intervention.