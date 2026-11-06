"""Does a driving median offset transfer across recordings and days? (evals only; the dataset is read-only)

Usage (horuspy-dev image, horuspy/src on PYTHONPATH):
  python scripts/make_day_recording_transfer.py /path/to/data
Reuses the offset benchmark unchanged: units/samples from evaluation.offset_data.load_driving, the correction
models.offset.MedianOffset (median of the calibration scenes' offsets) and held-out scoring
evaluation.offset_benchmark.score_directions with test_weights (recordings, then scenes, then samples equal).
Calibration and test scenes never overlap; uncorrected and corrected errors are scored on the same test samples.

Splits:
  P1 (William): the 9 July 15 recordings only (same applied 'corrected' scene calibration; the Oct 15 drive uses the
      native module calibration and is excluded). one recording -> all other July recordings (9 splits);
      pseudo-days: recordings 1-5 vs 6-9 by start time (15:45-16:07 vs 16:13-16:50), both directions (2 splits).
  P2 (Katharina): real days 2026-10-14 (3 rec.) and 2026-10-15 (3 rec.). leave-one-recording-out: all other
      recordings -> the held-out one (6 splits); cross-day: one day -> the other day (2 splits).
  P6 (Stefan): one drive, scenes ordered by start time and split into six consecutive segments of 15-16 scenes;
      segment -> all other segments (6 splits); pseudo-days: segments 1-3 vs 4-6, both directions (2 splits).
Writes evals/data/06_day_recording_transfer_splits.csv and evals/data/06_day_recording_transfer_summary.csv.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from evaluation.offset_benchmark import score_directions, test_weights
from evaluation.offset_data import load_driving
from models.offset import MedianOffset

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data")
OUT = Path(__file__).resolve().parents[1] / "evals/data"
CODE = {"william": "P1", "katharina": "P2", "stefan": "P6"}

loaded = load_driving(DATA, list(CODE))
units, samples = loaded[0], loaded[1]
units = units[units.valid] if "valid" in units else units
samples = samples[samples.unit_id.isin(units.unit_id)]
start = samples.groupby("unit_id").gaze_timestamp_ns.min().rename("start_ns")
units = units.merge(start, left_on="unit_id", right_index=True)
raw_columns = [c for c in samples.columns if c.startswith("gaze_") and c.endswith("_deg")]


def evaluate(code, kind, name, train_ids, test_ids):
    train, test_units = units[units.unit_id.isin(train_ids)], units[units.unit_id.isin(test_ids)]
    assert not set(train.unit_id) & set(test_units.unit_id)
    test = samples[samples.unit_id.isin(test_units.unit_id)]
    weights = test_weights(test)
    model = MedianOffset(train)
    from models.offset import GAZE_COLUMNS
    raw = score_directions(test, test[GAZE_COLUMNS].to_numpy(float), weights)
    corrected = score_directions(test, model(test), weights)
    return dict(code=code, kind=kind, split=name, calibration_scenes=len(train), calibration_recordings=train.recording_id.nunique(),
                test_scenes=len(test_units), test_recordings=test_units.recording_id.nunique(),
                offset_azimuth_deg=model.bias[0], offset_elevation_deg=model.bias[1],
                raw_median_deg=raw["median_error_deg"], corrected_median_deg=corrected["median_error_deg"],
                raw_p90_deg=raw["p90_error_deg"], corrected_p90_deg=corrected["p90_error_deg"])


rows = []
# P1: July recordings only
p1 = units[(units.participant == "william") & units.recording_name.str.contains("2026-07-15")]
recs = p1.groupby("recording_name").start_ns.min().sort_values().index.tolist()
for r in recs:
    rows.append(evaluate("P1", "recording -> other recordings (same day)", r[-8:],
                         p1[p1.recording_name == r].unit_id, p1[p1.recording_name != r].unit_id))
groups = {"A (15:45-16:07)": recs[:5], "B (16:13-16:50)": recs[5:]}
for a, b in (("A (15:45-16:07)", "B (16:13-16:50)"), ("B (16:13-16:50)", "A (15:45-16:07)")):
    rows.append(evaluate("P1", "pseudo-day: recording group -> group", f"{a[0]} -> {b[0]}",
                         p1[p1.recording_name.isin(groups[a])].unit_id, p1[p1.recording_name.isin(groups[b])].unit_id))

# P2: two real days
p2 = units[units.participant == "katharina"].copy()
p2["day"] = p2.recording_name.str.extract(r"(2026-\d\d-\d\d)")[0]
for r in sorted(p2.recording_name.unique()):
    rows.append(evaluate("P2", "leave-one-recording-out (other recordings -> held-out)", r[-8:],
                         p2[p2.recording_name != r].unit_id, p2[p2.recording_name == r].unit_id))
for a, b in (("2026-10-14", "2026-10-15"), ("2026-10-15", "2026-10-14")):
    rows.append(evaluate("P2", "cross-day (real days)", f"{a} -> {b}", p2[p2.day == a].unit_id, p2[p2.day == b].unit_id))

# P6: one drive, six chronological segments
p6 = units[units.participant == "stefan"].sort_values("start_ns").copy()
p6["segment"] = np.array_split(np.arange(len(p6)), 6) and np.concatenate([[i + 1] * len(c) for i, c in enumerate(np.array_split(np.arange(len(p6)), 6))])
for s in range(1, 7):
    rows.append(evaluate("P6", "segment -> other segments (same drive)", f"segment {s}",
                         p6[p6.segment == s].unit_id, p6[p6.segment != s].unit_id))
for a, b in (((1, 2, 3), (4, 5, 6)), ((4, 5, 6), (1, 2, 3))):
    rows.append(evaluate("P6", "pseudo-day: segment group -> group", f"{a[0]}-{a[-1]} -> {b[0]}-{b[-1]}",
                         p6[p6.segment.isin(a)].unit_id, p6[p6.segment.isin(b)].unit_id))

splits = pd.DataFrame(rows)
splits["improvement_deg"] = splits.raw_median_deg - splits.corrected_median_deg
summary = splits.groupby(["code", "kind"], sort=False).agg(
    splits=("split", "size"), calibration_scenes_mean=("calibration_scenes", "mean"),
    calibration_scenes_min=("calibration_scenes", "min"), calibration_scenes_max=("calibration_scenes", "max"),
    raw_median_deg=("raw_median_deg", "mean"), corrected_median_deg=("corrected_median_deg", "mean"),
    corrected_min=("corrected_median_deg", "min"), corrected_max=("corrected_median_deg", "max"),
    raw_p90_deg=("raw_p90_deg", "mean"), corrected_p90_deg=("corrected_p90_deg", "mean"),
    splits_improved=("improvement_deg", lambda v: int((v > 0).sum()))).reset_index()
OUT.mkdir(parents=True, exist_ok=True)
splits.to_csv(OUT / "06_day_recording_transfer_splits.csv", index=False, float_format="%.4f")
summary.to_csv(OUT / "06_day_recording_transfer_summary.csv", index=False, float_format="%.4f")
pd.set_option("display.width", 220)
print(summary.round(2).to_string())
print(splits[["code", "kind", "split", "calibration_scenes", "test_scenes", "offset_elevation_deg", "raw_median_deg", "corrected_median_deg"]].round(2).to_string())
