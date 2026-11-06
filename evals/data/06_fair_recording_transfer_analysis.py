"""Read-only measurement analysis; outputs only to the mounted paper's evals directory.
Run with horuspy/src on PYTHONPATH; DATA_ROOT defaults to /data, OUTPUT_ROOT to /paper/evals.
"""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from evaluation.offset_benchmark import score_directions, split_units, test_weights
from evaluation.offset_data import GAZE_COLUMNS, load_driving
from models.offset import MedianOffset

DATA = Path(os.environ.get('DATA_ROOT', '/data'))
OUT = Path(os.environ.get('OUTPUT_ROOT', '/paper/evals')) / 'data'
PREFIX = '06_fair_recording_transfer'
CODE = {'william': 'P1', 'katharina': 'P2', 'stefan': 'P6'}
units, samples, sources = load_driving(DATA, list(CODE))
units = units.loc[units.valid].copy()
samples = samples.loc[samples.unit_id.isin(units.unit_id)].copy()
assert units.unit_id.is_unique
inventory = units.groupby(['participant', 'recording_id', 'recording_name', 'date']).agg(fixations=('unit_id', 'size'), samples=('n_samples', 'sum')).reset_index()
records = []
for row in inventory.to_dict('records'):
    folder = DATA / 'driving/recordings' / row['recording_name']
    info = json.loads((folder / 'info.json').read_text())
    assert info['recording_id'] == row['recording_id']
    calibration_path = DATA / 'driving/results' / row['recording_name'] / 'calibration.json'
    calibration = json.loads(calibration_path.read_text())
    records.append({**row, 'start_time_ns': info['start_time'], 'calibration_status': calibration['status'], 'module_serial': calibration['module_serial'],
                    'calibration_source_at_min5': row['fixations'] >= 5})
    sources.append({'path': str(calibration_path), 'sha256': hashlib.sha256(calibration_path.read_bytes()).hexdigest()})
inventory = pd.DataFrame(records)
rows, pairs, identities = [], [], []


def evaluate(person, protocol, name, train, target, minimum=5):
    """Fit the existing scene-median model and score disjoint held-out measurements with existing weights."""
    assert len(train) and len(target)
    assert not set(train.unit_id) & set(target.unit_id)
    if protocol != 'random_20_percent':
        assert not set(train.recording_id) & set(target.recording_id)
    test = samples.loc[samples.unit_id.isin(target.unit_id)].copy()
    weights = test_weights(test)
    assert np.isclose(weights.sum(), 1)
    masses = pd.DataFrame({'recording_id': test.recording_id, 'unit_id': test.unit_id, 'w': weights})
    np.testing.assert_allclose(masses.groupby('recording_id').w.sum(), 1 / target.recording_id.nunique())
    for _, group in masses.groupby('recording_id'):
        np.testing.assert_allclose(group.groupby('unit_id').w.sum(), 1 / target.recording_id.nunique() / group.unit_id.nunique())
    model = MedianOffset(train)
    raw = score_directions(test, test[GAZE_COLUMNS].to_numpy(float), weights)
    corrected = score_directions(test, model(test), weights)
    row = dict(code=CODE[person], participant=person, protocol=protocol, min_calibration_fixations=minimum, split=name,
               calibration_fixations=len(train), calibration_recordings=train.recording_id.nunique(),
               test_fixations=len(target), test_recordings=target.recording_id.nunique(),
               calibration_days=';'.join(sorted(train.date.unique())), test_days=';'.join(sorted(target.date.unique())),
               offset_azimuth_deg=model.bias[0], offset_elevation_deg=model.bias[1])
    row.update({f'raw_{k}': v for k, v in raw.items()})
    row.update({f'corrected_{k}': v for k, v in corrected.items()})
    row['improvement_deg'] = raw['median_error_deg'] - corrected['median_error_deg']
    rows.append(row)
    identities.append({k: row[k] for k in ('participant', 'protocol', 'min_calibration_fixations', 'split')} |
                      {'calibration_unit_ids': train.unit_id.tolist(), 'test_unit_ids': target.unit_id.tolist()})
    if protocol == 'one_recording_to_others' and minimum == 5:
        for rid, block in test.groupby('recording_id'):
            w = test_weights(block)
            r = score_directions(block, block[GAZE_COLUMNS].to_numpy(float), w)
            c = score_directions(block, model(block), w)
            pairs.append(dict(code=CODE[person], source_recording_id=train.recording_id.iloc[0], target_recording_id=rid,
                              same_day=bool(train.date.iloc[0] == target.loc[target.recording_id.eq(rid), 'date'].iloc[0]),
                              source_fixations=len(train), target_fixations=block.unit_id.nunique(),
                              raw_median_deg=r['median_error_deg'], corrected_median_deg=c['median_error_deg'],
                              raw_p90_deg=r['p90_error_deg'], corrected_p90_deg=c['p90_error_deg']))


for person in CODE:
    pool = units.loc[units.participant.eq(person)]
    counts = pool.groupby('recording_id').size()
    for minimum in (3, 5, 8):
        for rid in counts[counts.ge(minimum)].index:
            train, target = pool.loc[pool.recording_id.eq(rid)], pool.loc[pool.recording_id.ne(rid)]
            evaluate(person, 'one_recording_to_others', rid, train, target, minimum)
    # Additional same-day restriction separates William's device-calibration change.
    for day, day_pool in pool.groupby('date'):
        for rid, train in day_pool.groupby('recording_id'):
            target = day_pool.loc[day_pool.recording_id.ne(rid)]
            if len(train) >= 5 and len(target):
                evaluate(person, 'one_recording_to_others_same_day', rid, train, target)
    if pool.date.nunique() == 2:
        for day, train in pool.groupby('date'):
            evaluate(person, 'real_cross_day', day, train, pool.loc[pool.date.ne(day)])
    for split in split_units(pool, {'split': 'blocks', 'folds': 5, 'train_blocks': 1}, 42):
        evaluate(person, 'random_20_percent', str(split['fold']), pool.loc[pool.unit_id.isin(split['train_ids'])],
                 pool.loc[pool.unit_id.isin(split['test_ids'])], minimum=0)

splits = pd.DataFrame(rows)
summary = splits.groupby(['code', 'participant', 'protocol', 'min_calibration_fixations'], sort=False).agg(
    splits=('split', 'size'), calibration_fixations_min=('calibration_fixations', 'min'), calibration_fixations_max=('calibration_fixations', 'max'),
    raw_median_deg=('raw_median_error_deg', 'mean'), corrected_median_deg=('corrected_median_error_deg', 'mean'),
    corrected_min_deg=('corrected_median_error_deg', 'min'), corrected_max_deg=('corrected_median_error_deg', 'max'),
    raw_p90_deg=('raw_p90_error_deg', 'mean'), corrected_p90_deg=('corrected_p90_error_deg', 'mean'),
    splits_improved=('improvement_deg', lambda x: int(x.gt(0).sum()))).reset_index()
pair_table = pd.DataFrame(pairs)
starts = inventory.set_index('recording_id').start_time_ns
next_recording = {}
for _, group in inventory.groupby('participant'):
    ids = group.sort_values('start_time_ns').recording_id.tolist()
    next_recording.update(dict(zip(ids[:-1], ids[1:])))
pair_table['forward_in_time'] = pair_table.source_recording_id.map(starts) < pair_table.target_recording_id.map(starts)
pair_table['next_available_recording'] = pair_table.source_recording_id.map(next_recording).eq(pair_table.target_recording_id)
next_summary = pair_table.loc[pair_table.next_available_recording].groupby('code').agg(
    pairs=('source_recording_id', 'size'), raw_median_deg=('raw_median_deg', 'mean'), corrected_median_deg=('corrected_median_deg', 'mean'),
    corrected_min_deg=('corrected_median_deg', 'min'), corrected_max_deg=('corrected_median_deg', 'max'),
    corrected_p90_deg=('corrected_p90_deg', 'mean')).reset_index()
OUT.mkdir(parents=True, exist_ok=True)
for suffix, frame in [('inventory', inventory), ('splits', splits), ('summary', summary), ('pairs', pair_table), ('next_recording_summary', next_summary)]:
    frame.to_csv(OUT / f'{PREFIX}_{suffix}.csv', index=False, float_format='%.8f')
code_files = ['/src/evaluation/offset_data.py', '/src/evaluation/offset_benchmark.py', '/src/models/offset.py', __file__]
provenance = dict(analysis_date='2026-11-06', primary_min_calibration_fixations=5, sensitivity_thresholds=[3, 5, 8],
                  scoring='equal recordings, equal fixations within recording, equal samples within fixation; weighted empirical median/P90',
                  fitting='MedianOffset: equal fixation offsets; componentwise median, unchanged', random_baseline_seed=42,
                  source_hashes=sources, code_sha256={p: hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in code_files}, splits=identities)
(OUT / f'{PREFIX}_provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
print(inventory.to_string(index=False))
print(summary.round(4).to_string(index=False))
print('CROSS DAY')
print(splits.loc[splits.protocol.eq('real_cross_day')].round(4).to_string(index=False))
print('NEXT RECORDING')
print(next_summary.round(4).to_string(index=False))
