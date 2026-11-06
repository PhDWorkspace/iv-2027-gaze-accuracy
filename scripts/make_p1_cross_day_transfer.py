"""P1 genuine cross-day transfer: July 15 (9 drives) <-> October 15 (1 drive). evals only; dataset read-only.

Usage (horuspy-dev image, horuspy/src on PYTHONPATH): python scripts/make_p1_cross_day_transfer.py /path/to/data
Same method as scripts/make_day_recording_transfer.py (MedianOffset of calibration scenes; score_directions with
test_weights; uncorrected and corrected on the same held-out samples). Caveat: the two days use different applied
scene calibrations (July 'corrected', October native 'module_specific', both module 272097), so this split also
contains a device-calibration change. Writes evals/data/06_p1_cross_day_transfer.csv.
"""
import sys
from pathlib import Path

import pandas as pd
from evaluation.offset_benchmark import score_directions, test_weights
from evaluation.offset_data import GAZE_COLUMNS, load_driving
from models.offset import MedianOffset

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data")
units, samples = load_driving(DATA, ["william"])[:2]
units = units[units.valid] if "valid" in units else units
days = {"2026-07-15": units[units.recording_name.str.contains("2026-07-15")],
        "2026-10-15": units[units.recording_name.str.contains("2026-10-15")]}
rows = []
for a, b in (("2026-07-15", "2026-10-15"), ("2026-10-15", "2026-07-15")):
    train, test_units = days[a], days[b]
    test = samples[samples.unit_id.isin(test_units.unit_id)]
    w = test_weights(test)
    model = MedianOffset(train)
    raw, cor = score_directions(test, test[GAZE_COLUMNS].to_numpy(float), w), score_directions(test, model(test), w)
    rows.append(dict(code="P1", split=f"{a} -> {b}", calibration_scenes=len(train), calibration_recordings=train.recording_id.nunique(),
                     test_scenes=len(test_units), test_recordings=test_units.recording_id.nunique(),
                     offset_azimuth_deg=model.bias[0], offset_elevation_deg=model.bias[1],
                     raw_median_deg=raw["median_error_deg"], corrected_median_deg=cor["median_error_deg"],
                     raw_p90_deg=raw["p90_error_deg"], corrected_p90_deg=cor["p90_error_deg"]))
out = pd.DataFrame(rows)
out.to_csv(Path(__file__).resolve().parents[1] / "evals/data/06_p1_cross_day_transfer.csv", index=False, float_format="%.4f")
print(out.round(2).to_string())
print("mean corrected", round(out.corrected_median_deg.mean(), 2), "mean raw", round(out.raw_median_deg.mean(), 2))
