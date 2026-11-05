"""Older hand-moved pursuit recordings (2026-07-16) vs the 8 scored screen pursuits, with the factor-analysis metrics.

Usage: python scripts/make_pursuit_comparison.py /path/to/data
Reads only: controlled/results/<rec>/dataset.csv (per-stroke fixations crosshair_<direction>.NN, added 2026-11-05),
controlled/patterns/pursuit_<speed>/turns.csv, and factors/controlled/6_pursuit/{recordings,phases,directions}.csv.
Same definitions as horuspy scripts/factor_analysis/analyze_factors.py (test 6): metric-valid samples; error = gaze -
target (az wrapped, +right/+up); 1 s windows with >= 20 samples spanning >= 0.5 s, recording = median of windows;
residual_p_std = sqrt(var az error + var el error); near turn = within 0.25 s of a turn; directions from straight samples.
Writes evals/data/05_pursuit_old_vs_screen_{recordings,phases,directions}.csv.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data")
OUT = Path(__file__).resolve().parents[1] / "evals/data"
OLD = {"smooth_pursuit_William_2026-07-16-17-19-27_947b51e5": "slow",
       "smooth_pursuit_William_2026-07-16-17-27-07_98d3d73b": "medium",
       "smooth_pursuit_William_2026-07-16-17-28-33_e223599c": "fast"}
NAMES = {"up_right": "Up-right", "up_left": "Up-left", "down_right": "Down-right", "down_left": "Down-left",
         "up": "Up", "down": "Down", "left": "Left", "right": "Right"}
METRICS = ["angular_error_median_deg", "bias_azimuth_deg", "bias_elevation_deg", "residual_p_std_deg"]


def summarize(g):
    out = g.agg(angular_error_median_deg=("angular_error_deg", "median"), bias_azimuth_deg=("error_azimuth", "median"),
                bias_elevation_deg=("error_elevation", "median"), samples=("angular_error_deg", "size"))
    out["residual_p_std_deg"] = np.sqrt(g[["error_azimuth", "error_elevation"]].var(ddof=1).sum(axis=1, min_count=2))
    return out


rec_rows, phase_rows, dir_rows = [], [], []
for rec, speed in OLD.items():
    cols = ["gaze_timestamp_ns", "metric_valid", "angular_error_deg", "feature_gaze_azimuth_deg", "feature_gaze_elevation_deg",
            "target_azimuth_deg", "target_elevation_deg", "fixation_id"]
    d = pd.read_csv(DATA / "controlled/results" / rec / "dataset.csv", usecols=cols, low_memory=False)
    ann = pd.read_csv(DATA / "controlled/recordings" / rec / "annotations.csv")
    starts = ann[ann.name.str.startswith("crosshair_") & ann.name.str.endswith(".start")].sort_values("timestamp [ns]")
    labels = starts.name.str.removeprefix("crosshair_").str.rsplit(".", n=2).str[0].map(NAMES).to_numpy()
    d = d[d.metric_valid.fillna(False).astype(bool) & d.fixation_id.notna()].copy()
    d["direction"] = labels[d.fixation_id.astype(int).to_numpy()]
    d["error_azimuth"] = (d.feature_gaze_azimuth_deg - d.target_azimuth_deg + 180) % 360 - 180
    d["error_elevation"] = d.feature_gaze_elevation_deg - d.target_elevation_deg
    turns = pd.read_csv(DATA / f"controlled/patterns/pursuit_{speed}/turns.csv").turn_ns.to_numpy()
    d["near_turn"] = np.min(np.abs(d.gaze_timestamp_ns.to_numpy()[:, None] - turns[None, :]), axis=1) <= 0.25e9
    d["window"] = ((d.gaze_timestamp_ns - d.gaze_timestamp_ns.min()) // 1e9).astype(int)
    w = summarize(d.groupby("window"))
    span = d.groupby("window").gaze_timestamp_ns.agg(lambda t: (t.max() - t.min()) / 1e9)
    w = w[(w.samples >= 20) & (span >= 0.5)]
    rec_rows.append(dict(recording_name=rec, group=f"old hand-moved ({speed})", speed=speed, windows=len(w),
                         samples=int(len(d)), **w[METRICS].median().to_dict()))
    d["phase"] = np.where(d.near_turn, "Near turn", "Straight")
    phase_rows.append(summarize(d.groupby("phase")).reset_index().assign(recording_name=rec, group="old", speed=speed))
    dir_rows.append(summarize(d[~d.near_turn].groupby("direction")).reset_index().assign(recording_name=rec, group="old",
                                                                                       speed=speed))

F = DATA / "gaze_accuracy/factors/controlled/6_pursuit"
new = pd.read_csv(F / "recordings.csv")
recordings = pd.concat([pd.DataFrame(rec_rows),
                        new.assign(group=lambda t: np.where(t.task == "Pursuit", "screen pursuit (8)", "static 1 m (P1)"))],
                       ignore_index=True)
phases = pd.concat(phase_rows + [pd.read_csv(F / "phases.csv").assign(group="screen")], ignore_index=True)
directions = pd.concat(dir_rows + [pd.read_csv(F / "directions.csv").assign(group="screen")], ignore_index=True)
recordings.to_csv(OUT / "05_pursuit_old_vs_screen_recordings.csv", index=False, float_format="%.4f")
phases.to_csv(OUT / "05_pursuit_old_vs_screen_phases.csv", index=False, float_format="%.4f")
directions.to_csv(OUT / "05_pursuit_old_vs_screen_directions.csv", index=False, float_format="%.4f")

pd.set_option("display.width", 200)
print(recordings.groupby("group")[METRICS].median().round(2).to_string())
print(recordings[recordings.group.str.startswith("old")][["speed", "windows", "samples"] + METRICS].round(2).to_string())
p = phases.pivot_table(index=["group", "recording_name"], columns="phase", values=["angular_error_median_deg", "residual_p_std_deg"])
print((p.xs("Near turn", axis=1, level=1) - p.xs("Straight", axis=1, level=1)).groupby("group").agg(["median", "min", "max"]).round(2).to_string())
print(directions.groupby(["group", "direction"])[["angular_error_median_deg", "bias_elevation_deg", "residual_p_std_deg"]].median().round(2).unstack(0).to_string())
