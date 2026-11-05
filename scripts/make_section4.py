"""Section IV: raw driving accuracy per scene and the dataset figure.

Usage: python scripts/make_section4.py /path/to/data [--figure EVENT_ID EVENT_ID EVENT_ID]

Reads only (nothing in the dataset is written):
  <data>/gaze_accuracy/offset/units/units_driving.csv     evaluated scenes (unit_id = recording UUID/event UUID)
  <data>/driving/results/<rec>/dataset.csv                 canonical gaze samples with target references
  <data>/driving/recordings/<rec>/scene_metadata.json      scene tags; Neon scene video for the figure
Writes evals/data/04_scene_raw_errors.csv, evals/data/04_driver_raw_summary.csv and (with --figure)
figures/fig4_dataset.pdf plus evals/data/04_fig_dataset_scenes.csv.

Per scene, metric-valid samples inside the validated event: median and P90 angular error; signed offset =
componentwise median of gaze - target (azimuth wrapped, +right/+up); target-relative dispersion =
sqrt(var(az error) + var(el error)), the definition used for pursuit in Section V.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DRIVERS = {"william": "P1", "katharina": "P2", "stefan": "P6"}
COLUMNS = ["gaze_x_px", "gaze_y_px", "frame_index", "event_id", "metric_valid", "angular_error_deg",
           "feature_gaze_azimuth_deg", "feature_gaze_elevation_deg", "target_azimuth_deg", "target_elevation_deg",
           "target_x_px", "target_y_px", "target_distance_m"]


def scene_errors(data):
    units = pd.read_csv(data / "gaze_accuracy/offset/units/units_driving.csv")
    units = units[units.valid].copy()
    units["event_id"] = units.unit_id.str.split("/").str[1]
    rows = []
    for rec, u in units.groupby("recording_name"):
        d = pd.read_csv(data / "driving/results" / rec / "dataset.csv", usecols=COLUMNS,
                        dtype={"event_id": "string", "metric_valid": "boolean"}, low_memory=False)
        d = d[d.metric_valid.fillna(False) & d.event_id.isin(u.event_id)]
        az = (d.feature_gaze_azimuth_deg - d.target_azimuth_deg + 180) % 360 - 180
        el = d.feature_gaze_elevation_deg - d.target_elevation_deg
        d = d.assign(err_az=az, err_el=el)
        for eid, g in d.groupby("event_id"):
            unit = u[u.event_id == eid].iloc[0]
            rows.append(dict(participant=unit.participant, code=DRIVERS[unit.participant], recording=rec, event_id=eid,
                             label=unit.label, samples=len(g), median_error_deg=g.angular_error_deg.median(),
                             p90_error_deg=g.angular_error_deg.quantile(0.9), bias_azimuth_deg=g.err_az.median(),
                             bias_elevation_deg=g.err_el.median(),
                             dispersion_deg=float(np.sqrt(g.err_az.var() + g.err_el.var())),
                             target_distance_median_m=g.target_distance_m.median()))
    scenes = pd.DataFrame(rows)
    summary = scenes.groupby("code").agg(
        scenes=("event_id", "size"), samples=("samples", "sum"),
        scene_median_error=("median_error_deg", "median"), scene_error_q25=("median_error_deg", lambda v: v.quantile(.25)),
        scene_error_q75=("median_error_deg", lambda v: v.quantile(.75)), scene_p90_median=("p90_error_deg", "median"),
        bias_azimuth=("bias_azimuth_deg", "median"), bias_elevation=("bias_elevation_deg", "median"),
        dispersion_median=("dispersion_deg", "median"))
    summary["offset_norm"] = np.hypot(summary.bias_azimuth, summary.bias_elevation)
    summary["offset_share"] = summary.offset_norm / summary.scene_median_error
    return scenes, summary


def figure(data, scenes, events):
    import cv2
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    for f in Path("/usr/share/fonts").rglob("NimbusRoman-*.otf"):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({"font.family": "serif", "font.serif": ["Nimbus Roman", "DejaVu Serif"], "font.size": 6.5,
                         "pdf.fonttype": 42})
    fig, axes = plt.subplots(1, len(events), figsize=(3.5, 1.32), layout="constrained")
    info = []
    for ax, eid in zip(axes, events):
        s = scenes[scenes.event_id == eid].iloc[0]
        rec = s.recording
        meta = json.loads((data / "driving/recordings" / rec / "scene_metadata.json").read_text())
        ev = next(e for e in meta["events"] if e["event_id"] == eid)
        d = pd.read_csv(data / "driving/results" / rec / "dataset.csv", usecols=COLUMNS,
                        dtype={"event_id": "string", "metric_valid": "boolean"}, low_memory=False)
        d = d[(d.event_id == eid) & d.metric_valid.fillna(False)]
        frame = int(d.frame_index.iloc[len(d) // 2])          # middle of the fixation
        f = d[d.frame_index == frame]
        cap = cv2.VideoCapture(str(data / "driving/recordings" / rec / "Neon Scene Camera v1 ps1.mp4"))
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ok, bgr = cap.read()
        assert ok, (rec, frame)
        tx, ty = f.target_x_px.median(), f.target_y_px.median()
        gx, gy = f.gaze_x_px.median(), f.gaze_y_px.median()
        half = max(70, int(1.4 * max(abs(gx - tx), abs(gy - ty))) + 25)  # square crop around target and gaze
        cx, cy = (tx + gx) / 2, (ty + gy) / 2
        x0, y0 = int(np.clip(cx - half, 0, 1600 - 2 * half)), int(np.clip(cy - half, 0, 1200 - 2 * half))
        crop = cv2.cvtColor(bgr[y0:y0 + 2 * half, x0:x0 + 2 * half], cv2.COLOR_BGR2RGB)
        ax.imshow(crop, extent=(x0, x0 + 2 * half, y0 + 2 * half, y0))
        ax.scatter([tx], [ty], marker="+", s=60, color="#1baf7a", linewidths=1.4, zorder=3)
        ax.scatter([gx], [gy], marker="o", s=26, facecolor="none", edgecolor="#eb3434", linewidths=1.2, zorder=3)
        ax.set_xticks([]); ax.set_yticks([])
        dist = ev["distance_m"]["mean"]
        speed = (ev["ego"].get("speed_kmh") or {}).get("mean")
        cls = ev["target"]["class"].replace("_", " ").replace("license", "licence")
        motion = {"none": "both standing"}.get(ev["relative_motion"], ev["relative_motion"].replace("_", " "))
        ax.set_title(f"{cls}, {motion}", fontsize=6.3, pad=2)
        ax.set_xlabel(f"{dist:.0f} m, " + (f"{speed:.0f} km/h" if speed and speed >= 1 else "standing") + f"; error {s.median_error_deg:.1f}°",
                      fontsize=6.3, labelpad=2)
        info.append(dict(event_id=eid, recording=rec, frame=frame, label=ev["label"], target_class=ev["target"]["class"],
                         relative_motion=ev["relative_motion"], distance_m=dist, distance_source=ev["distance_source"],
                         speed_kmh=speed, speed_source=ev["ego"].get("speed_source"), median_error_deg=s.median_error_deg,
                         description=ev["description"], crop=f"{x0},{y0},{2 * half}"))
    fig.savefig(ROOT / "figures/fig4_dataset.pdf")
    pd.DataFrame(info).to_csv(ROOT / "evals/data/04_fig_dataset_scenes.csv", index=False, float_format="%.3f")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("data", type=Path)
    parser.add_argument("--figure", nargs="*", default=[])
    args = parser.parse_args()
    scenes, summary = scene_errors(args.data)
    scenes.to_csv(ROOT / "evals/data/04_scene_raw_errors.csv", index=False, float_format="%.4f")
    summary.to_csv(ROOT / "evals/data/04_driver_raw_summary.csv", float_format="%.4f")
    print(summary.round(2).to_string())
    if args.figure:
        figure(args.data, scenes, args.figure)
