"""Write evals/04_dataset_composition.md: how the 245 evaluated driving scenes are distributed.

Usage: python3 scripts/make_dataset_composition.py [/path/to/data]
Standard library only; reads (never writes) the dataset:
  gaze_accuracy/offset/units/units_driving.csv           evaluated scenes and gaze-sample counts
  driving/recordings/<rec>/scene_metadata.json            schema-2 tags per scene and session
  driving/recordings/<rec>/annotations.csv, info.json     fixation interval, recording duration
"""
import collections
import csv
import json
import statistics as st
import sys
from pathlib import Path

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data")
OUT = Path(__file__).resolve().parents[1] / "evals/04_dataset_composition.md"
CODE = {"william": "P1", "katharina": "P2", "stefan": "P6"}
CLASS = {"license_plate": "licence plate", "road_sign": "road sign", "traffic_light": "traffic light",
         "pedestrian_traffic_light": "pedestrian traffic light"}
MOTION_GROUP = {"none": "both standing", "approaching": "ego moves, target static", "passing": "ego moves, target static",
                "receding": "target moves, ego static", "oncoming": "target moves (oncoming)",
                "being_passed": "target moves, ego static", "following": "both move, same direction",
                "closing_in": "both move, same direction", "parallel": "both move, same direction",
                "overtaking": "both move, same direction", "being_overtaken": "both move, same direction"}


def distance_bin(d):
    return "< 10 m" if d < 10 else "10–20 m" if d < 20 else "20–30 m" if d < 30 else "30–50 m" if d < 50 else "≥ 50 m"


units = [u for u in csv.DictReader(open(DATA / "gaze_accuracy/offset/units/units_driving.csv")) if u["valid"] == "True"]
by_event = {u["unit_id"].split("/")[1]: u for u in units}
scenes, recordings = [], {}
for rec in sorted({u["recording_name"] for u in units}):
    folder = DATA / "driving/recordings" / rec
    meta = json.loads((folder / "scene_metadata.json").read_text())
    info = json.loads((folder / "info.json").read_text())
    marks = {}
    for row in csv.DictReader(open(folder / "annotations.csv", encoding="utf-8-sig")):
        if row["type"] == "fixation":
            label, edge = row["name"].rsplit(".", 1)
            marks.setdefault(label, {})[edge] = int(row["timestamp [ns]"])
    for e in meta["events"]:
        u = by_event.get(e["event_id"])
        if u is None:
            continue
        span = marks.get(e["label"], {})
        speed = (e["ego"].get("speed_kmh") or {}).get("mean")
        scenes.append(dict(
            code=CODE[u["participant"]], recording=rec, date=rec.split("_")[-2][:10] if "_20" in rec else "",
            role=meta.get("observer_role"), weather=meta["session"].get("weather"), light=meta["session"].get("light"),
            cls=CLASS.get(e["target"]["class"], e["target"]["class"]), subtype=e["target"]["subtype"],
            target_motion=e["target"]["motion"], condition=e["target"].get("condition") or "–",
            side=e["target"]["side"], relative=e["relative_motion"], group=MOTION_GROUP.get(e["relative_motion"], "other"),
            ego=e["ego"]["motion"], speed_class=e["ego"].get("speed_class") or "standing", speed=speed,
            speed_source=e["ego"].get("speed_source"), distance=e["distance_m"]["mean"],
            distance_source=e["distance_source"], road=e["road"]["type"], features=e["road"].get("features") or [],
            view=e["view"], exposure=e["image"]["gaze_exposure"], issues=e["image"].get("issues") or [],
            duration=(span["end"] - span["start"]) / 1e9 if {"start", "end"} <= span.keys() else None,
            samples=int(u["n_samples"])))
    recordings[rec] = dict(code=CODE[by_event[meta["events"][0]["event_id"]]["participant"]] if meta["events"][0]["event_id"] in by_event else "",
                           duration=info["duration"] / 1e9, start=info["start_time"])
for s in scenes:
    s["date"] = next(r["date_berlin"] for r in csv.DictReader(open(DATA / "recordings.csv")) if r["recording_name"] == s["recording"])
    s["distance_bin"] = distance_bin(s["distance"])

N = len(scenes)
lines = []
w = lines.append


def table(title, key, order=None, note=""):
    """One categorical split: counts, share of scenes, and per participant."""
    counts = collections.Counter(key(s) for s in scenes)
    per = {c: collections.Counter(key(s) for s in scenes if s["code"] == c) for c in ("P1", "P2", "P6")}
    keys = order or [k for k, _ in counts.most_common()]
    w(f"\n### {title}\n")
    if note:
        w(note + "\n")
    w("| Value | Scenes | Share | P1 | P2 | P6 |")
    w("|---|---|---|---|---|---|")
    for k in keys:
        if counts[k]:
            w(f"| {k} | {counts[k]} | {counts[k] / N:.0%} | {per['P1'][k]} | {per['P2'][k]} | {per['P6'][k]} |")


def crosstab(title, row, col, rows, cols):
    c = collections.Counter((row(s), col(s)) for s in scenes)
    w(f"\n### {title}\n")
    w("| | " + " | ".join(cols) + " | Total |")
    w("|---|" + "---|" * (len(cols) + 1))
    for r in rows:
        total = sum(c[(r, k)] for k in cols)
        if total:
            w(f"| {r} | " + " | ".join(str(c[(r, k)] or "·") for k in cols) + f" | {total} |")


days = collections.Counter(s["date"] for s in scenes)
dur = [s["duration"] for s in scenes if s["duration"]]
d_all = [s["distance"] for s in scenes]
sp = [s["speed"] for s in scenes if s["speed"] is not None and s["speed_source"] == "gnss"]
w("# Section IV: driving dataset composition\n")
w("**Generated by** `scripts/make_dataset_composition.py` from the dataset (read-only); unit = verified fixation "
  "scene (245). Tags follow `docs/scene_metadata.md` (schema 2). Shares are of all 245 scenes. Use this to show "
  "coverage and balance; it contains no accuracy results.\n")
w("## 1. Overview\n")
w("| Item | Value |\n|---|---|")
w(f"| Verified fixation scenes | {N} |")
w(f"| Gaze samples in scenes | {sum(s['samples'] for s in scenes):,} |")
w(f"| Fixation duration per scene | median {st.median(dur):.2f} s (IQR {st.quantiles(dur, n=4)[0]:.2f}–{st.quantiles(dur, n=4)[2]:.2f} s); total {sum(dur) / 60:.1f} min |")
w(f"| Evaluated recordings | {len(recordings)} ({sum(r['duration'] for r in recordings.values()) / 3600:.2f} h) |")
w(f"| Recording days | {len(days)}: " + ", ".join(f"{d} ({n} scenes)" for d, n in sorted(days.items())) + " |")
w("| Participants | 3: P1 front passenger, P2 driver, P6 driver |")
w(f"| Locations | Frankfurt (Oct 14/15), Munich (Nov 4); July 15 location not documented |")
w(f"| Light / weather | " + ", ".join(f"{k} {v}" for k, v in collections.Counter(f"{s['light']}, {s['weather']}" for s in scenes).items()) + " |")
w(f"| Target distance | {min(d_all):.1f}–{max(d_all):.1f} m, median {st.median(d_all):.1f} m |")
w(f"| Ego speed (GNSS, {len(sp)} scenes) | {max(0, min(sp)):.0f}–{max(sp):.0f} km/h, median {st.median(sp):.1f} km/h |")

w("\n### Per participant and day\n")
w("| Participant | Role | Day | Recordings | Scenes | Gaze samples |\n|---|---|---|---|---|---|")
for (c, d), group in sorted(collections.defaultdict(list, {k: [s for s in scenes if (s["code"], s["date"]) == k]
                                                       for k in {(s["code"], s["date"]) for s in scenes}}).items()):
    w(f"| {c} | {group[0]['role']} | {d} | {len({s['recording'] for s in group})} | {len(group)} | {sum(s['samples'] for s in group):,} |")

w("\n## 2. Targets\n")
table("Target class", lambda s: s["cls"])
table("Target subtype", lambda s: s["subtype"].replace("_", " "))
table("Target motion", lambda s: s["target_motion"])
table("Target condition", lambda s: s["condition"], note="Parked / waiting apply to vehicles (licence plates).")

w("\n## 3. Distance\n")
bins = ["< 10 m", "10–20 m", "20–30 m", "30–50 m", "≥ 50 m"]
table("Mean target distance during the fixation", lambda s: s["distance_bin"], bins)
table("Distance source", lambda s: s["distance_source"], note="`lidar`: LiDAR points on the target; `camera`: Depth Anything fused with box size.")
crosstab("Target class × distance", lambda s: s["cls"], lambda s: s["distance_bin"],
         list(CLASS.values()), bins)

w("\n## 4. Ego motion and speed\n")
table("Ego motion", lambda s: s["ego"])
table("Speed class", lambda s: s["speed_class"], ["standing", "creeping", "slow", "moderate", "fast"],
      note="creeping < 10, slow 10–30, moderate 30–50, fast > 50 km/h; GNSS for Frankfurt/Munich, annotated class for July.")
table("Speed source", lambda s: s["speed_source"])

w("\n## 5. Relative motion\n")
table("Relative motion (grouped)", lambda s: s["group"])
table("Relative motion (tag)", lambda s: s["relative"].replace("_", " "))
crosstab("Target class × relative motion (grouped)", lambda s: s["cls"], lambda s: s["group"], list(CLASS.values()),
         ["ego moves, target static", "both standing", "target moves (oncoming)", "both move, same direction",
          "target moves, ego static"])

w("\n## 6. Position in the field of view and context\n")
table("Target side (relative to the car)", lambda s: s["side"].replace("_", " "),
      ["ahead", "ahead left", "ahead right", "left", "right", "overhead"])
table("View region of the gaze", lambda s: s["view"].replace("_", " "))
table("Road type", lambda s: s["road"])
table("Road features (a scene can have several)", lambda s: ", ".join(s["features"]) or "none")
table("Eye-image exposure around gaze", lambda s: s["exposure"].replace("_", " "),
      ["normal", "partly overexposed", "largely overexposed"])
table("Image issues", lambda s: ", ".join(s["issues"]) or "none")

w("\n## 7. Suggested groupings for the paper\n")
w("Coarse groups with enough scenes in each cell, for a balance figure or table:\n")
groups = {
    "Target": lambda s: "licence plate" if s["cls"] == "licence plate" else "road sign" if s["cls"] == "road sign" else "traffic light (incl. pedestrian)",
    "Distance": lambda s: "near (< 20 m)" if s["distance"] < 20 else "medium (20–40 m)" if s["distance"] < 40 else "far (≥ 40 m)",
    "Ego": lambda s: "standing" if s["ego"] == "stationary" else "moving (incl. braking/starting)",
    "Speed (moving scenes)": lambda s: None if s["ego"] == "stationary" else "≤ 30 km/h" if s["speed_class"] in ("creeping", "slow") else "> 30 km/h",
    "Relative motion": lambda s: "target static, ego approaching/passing" if s["group"] == "ego moves, target static" else "both standing" if s["group"] == "both standing" else "target moving",
    "Side": lambda s: "ahead / overhead" if s["side"] in ("ahead", "overhead") else "left side" if "left" in s["side"] else "right side",
    "Road": lambda s: "urban" if s["road"] == "urban" else "suburban / highway",
    "Exposure": lambda s: "normal" if s["exposure"] == "normal" else "over-exposed (partly/largely)",
}
w("| Dimension | Groups (scenes) |\n|---|---|")
for name, f in groups.items():
    c = collections.Counter(f(s) for s in scenes if f(s) is not None)
    w(f"| {name} | " + "; ".join(f"{k} {v} ({v / sum(c.values()):.0%})" for k, v in c.most_common()) + " |")
w("\n**Balance notes (facts from the tables above):**")
w("- Every coarse group has at least ~18% of scenes except where noted; the sparse cells are pedestrian traffic "
  "lights (7), highway (4), side-window gaze (2) and the rarer relative motions (parallel, overtaking, being passed).")
w("- Target class and participant are linked: licence plates come mainly from P1 and P6, road signs mainly from P2 "
  "and P6. Compare classes within participants or state this when pooling.")
ann = collections.Counter(s["date"] for s in scenes if s["speed_source"] != "gnss")
cam = collections.Counter(s["date"] for s in scenes if s["distance_source"] == "camera")
w(f"- Speed: GNSS speed for {N - sum(ann.values())} scenes; annotated speed class only for {sum(ann.values())} (" + ", ".join(f"{d}: {n}" for d, n in sorted(ann.items())) + "), drives without vehicle data.")
w(f"- Distance: camera-based for {sum(cam.values())} scenes (" + ", ".join(f"{d}: {n}" for d, n in sorted(cam.items())) + "); LiDAR otherwise.")

OUT.write_text("\n".join(lines) + "\n")
print(f"wrote {OUT} ({N} scenes)")
