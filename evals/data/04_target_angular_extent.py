"""Annotated target footprint, not measured fixation-reference error. Dataset is read-only.
Run with horuspy/src on PYTHONPATH; DATA_ROOT defaults to /data.
"""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from dataset.angular_error import angular_errors_from_directions, pixel_directions

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get('DATA_ROOT', '/data'))
units = pd.read_csv(ROOT / 'evals/data/06_current_driving/offset/units/units_driving.csv')
units = units.loc[units.valid]
rows, sources = [], []
for name, group in units.groupby('recording_name'):
    folder = DATA / 'driving/recordings' / name
    paths = [folder / 'detections.json', DATA / 'driving/results' / name / 'calibration.json']
    detections, calibration = [json.loads(p.read_text()) for p in paths]
    K, D = np.array(calibration['camera_matrix']), np.array(calibration['dist_coefs'])
    sample_path = DATA / 'driving/results' / name / 'dataset.csv'
    sample_frames = pd.read_csv(sample_path, usecols=['frame_index', 'event_id', 'metric_valid'], dtype={'event_id': 'string', 'metric_valid': 'boolean'}, low_memory=False)
    sample_frames = sample_frames.loc[sample_frames.metric_valid.eq(True) & sample_frames.event_id.isin(group.event_id)]
    scored_frames = sample_frames.groupby('event_id').frame_index.apply(set).to_dict()
    frames = {}
    if 'events' in detections:
        for event in detections['events']:
            frames[event['event_id']] = [(f, event.get('target_type')) for f in event['frames']]
    else:
        for frame in detections['frames']:
            eid = ((frame.get('annotation') or {}).get('metadata') or {}).get('event_id')
            if eid:
                frames.setdefault(eid, []).append((frame, None))
    for unit in group.itertuples():
        extents = []
        for frame, fallback in frames.get(unit.event_id, []):
            annotation = frame.get('annotation') or {}
            if frame['frame_index'] not in scored_frames.get(unit.event_id, set()):
                continue
            obj = (frame.get('objects') or {}).get(annotation.get('object_id') or fallback)
            if not obj or not obj.get('valid', True) or not obj.get('box'):
                continue
            x0, y0, x1, y1 = obj['box']
            if x1 <= x0 or y1 <= y0:
                continue
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            points = [[x0, cy], [x1, cy], [cx, y0], [cx, y1], [x0, y0], [x1, y1], [x0, y1], [x1, y0]]
            directions = pixel_directions(points, K, D)
            errors = angular_errors_from_directions(directions[[0, 2, 4, 6]], directions[[1, 3, 5, 7]])
            extents.append([errors[0], errors[1], max(errors[2:])])
        values = np.median(extents, axis=0) if extents else [np.nan] * 3
        rows.append(dict(unit_id=unit.unit_id, participant=unit.participant,
                         annotated_frames=len(extents), width_deg=values[0], height_deg=values[1], diagonal_deg=values[2]))
    sources.extend({'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in [*paths, sample_path])
frame = pd.DataFrame(rows)
frame['target_class'] = frame.unit_id.map(units.set_index('unit_id')['target.class'])
frame.to_csv(ROOT / 'evals/data/04_target_angular_extent.csv', index=False, float_format='%.8f')
valid = frame.loc[frame.annotated_frames.gt(0)]
summary = {'eligible_scenes': len(frame), 'scenes_with_boxes': len(valid), 'aggregation': 'median extent over target boxes in frames used by metric-valid gaze samples per scene; equal scene weights',
           'interpretation': 'descriptive angular footprint of annotated boxes; not a validated uncertainty bound or measurement of exact human fixation position',
           'all': {c: {'median': float(valid[c].median()), 'p90': float(valid[c].quantile(.9))} for c in ['width_deg', 'height_deg', 'diagonal_deg']},
           'sources': sources, 'code_sha256': {'analysis': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'angular_geometry': hashlib.sha256(Path(pixel_directions.__code__.co_filename).read_bytes()).hexdigest()},
           'units_sha256': hashlib.sha256((ROOT / 'evals/data/06_current_driving/offset/units/units_driving.csv').read_bytes()).hexdigest()}
(ROOT / 'evals/data/04_target_angular_extent_summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'sources'}, indent=2))
