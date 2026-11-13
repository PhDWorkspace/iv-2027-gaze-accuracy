"""Audit the saved four-driver median-offset benchmark against Horuspy; dataset is read-only.

Run with Horuspy src and scripts/offset_benchmark on PYTHONPATH, DATA_ROOT=/home/william/data.
Reproduces driving units, all pooled/raw scores, sparse selections and category summaries.
Writes only the paper's evals/data/06_four_drivers/verification.json.
"""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

from analyze_runs import driving_categories
from evaluation.offset_benchmark import ACCURACY_COLUMNS, make_splits, score_directions, test_weights
from evaluation.offset_data import BIAS_COLUMNS, GAZE_COLUMNS, load_driving
from models.offset import MedianOffset

ROOT = Path(__file__).resolve().parents[2]
DATA = Path(os.environ.get('DATA_ROOT', '/home/william/data'))
OFFSET = ROOT / 'evals/data/06_four_drivers/offset'
PEOPLE = ['william', 'katharina', 'stefan', 'constantin']
units, samples, sources = load_driving(DATA, PEOPLE)
units = units.loc[units.valid]
saved = pd.read_csv(OFFSET / 'units/units_driving.csv').query('valid').set_index('unit_id')
assert set(saved.index) == set(units.unit_id)
np.testing.assert_allclose(units.set_index('unit_id').loc[saved.index, BIAS_COLUMNS + ['n_samples']], saved[BIAS_COLUMNS + ['n_samples']], atol=1e-12)
chessboard = pd.read_csv(OFFSET / 'units/units_chessboard.csv')
indexed = pd.concat([units, chessboard], ignore_index=True).set_index('unit_id')
hashes, scores, checks = {}, {}, {}
for name in ['driving', 'transfer', 'driving_recordings']:
    run = OFFSET / 'runs' / name
    protocol = json.loads((run / 'protocol.json').read_text())
    for source in protocol['sources']:
        path = Path(source['path'])
        if str(path) not in hashes:
            hashes[str(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
        assert hashes[str(path)] == source['sha256'], path
    horuspy = Path(__import__('models.offset', fromlist=['']).__file__).resolve().parents[2]
    for path, expected in protocol['code_sha256'].items():
        assert hashlib.sha256((horuspy / path).read_bytes()).hexdigest() == expected, path
    splits = pd.read_csv(run / 'splits.csv.gz')
    scores[name] = pd.read_csv(run / 'scores.csv.gz', low_memory=False)
    selected = scores[name].loc[scores[name].selection.isin(['none', 'all'])]
    replayed = 0
    for (person, split_id), group in selected.groupby(['participant', 'split_id']):
        split = splits.loc[splits.participant.eq(person) & splits.split_id.eq(split_id)]
        train_ids = split.loc[split.role.eq('train'), 'unit_id']
        test_ids = split.loc[split.role.eq('test'), 'unit_id']
        assert not set(train_ids) & set(test_ids)
        train, test_units = indexed.loc[train_ids], indexed.loc[test_ids]
        if len(train) and train.domain.eq('chessboard').all():
            assert train.complete.all()
        if name == 'driving_recordings':
            assert not set(train.recording_id) & set(test_units.recording_id)
            if group.protocol.iloc[0] == 'one_day':
                assert not set(train.date) & set(test_units.date)
        test = samples.loc[samples.unit_id.isin(test_ids)]
        weights = test_weights(test)
        np.testing.assert_allclose(weights.sum(), 1)
        mass = test.assign(weight=weights).groupby('recording_id').weight.sum()
        np.testing.assert_allclose(mass, 1 / len(mass))
        for row in group.itertuples():
            directions = test[GAZE_COLUMNS].to_numpy(float) if row.model == 'raw' else MedianOffset(train)(test)
            result = score_directions(test, directions, weights)
            np.testing.assert_allclose([result[c] for c in ACCURACY_COLUMNS], [getattr(row, c) for c in ACCURACY_COLUMNS], atol=1e-10)
            replayed += 1
    # Verify the saved split identities against the unchanged split generator.
    for person in protocol['spec']['participants']:
        pool = pd.concat([units.loc[units.participant.eq(person)], chessboard.loc[chessboard.participant.eq(person)]], ignore_index=True)
        for spec in protocol['spec']['protocols']:
            generated = make_splits(pool, spec, protocol['spec']['seed'])
            for number, split in enumerate(generated, 1):
                actual = splits.loc[splits.participant.eq(person) & splits.split_id.eq(f"{spec['name']}/{number:04d}")]
                for role in ['train', 'test']:
                    assert set(actual.loc[actual.role.eq(role), 'unit_id']) == set(split[f'{role}_ids'])
    checks[name] = {'replayed_raw_and_pooled_scores': replayed, 'split_identities_match': True}

# Compare the two calibration sources on exactly the same held-out scenes in every fold.
drv = pd.read_csv(OFFSET / 'runs/driving/splits.csv.gz')
tr = pd.read_csv(OFFSET / 'runs/transfer/splits.csv.gz')
for person in PEOPLE:
    for fold in range(1, 6):
        a = drv.loc[drv.participant.eq(person) & drv.fold.eq(fold) & drv.role.eq('test'), 'unit_id']
        b = tr.loc[tr.participant.eq(person) & tr.fold.eq(fold) & tr.protocol.eq('folds_to_scene_blocks') & tr.role.eq('test'), 'unit_id']
        assert set(a) == set(b)

# Every random/geometric calibration selection is contained in its saved training pool.
selection = pd.read_csv(OFFSET / 'runs/driving/selections.csv.gz')
for row in selection.itertuples():
    pool = drv.loc[drv.participant.eq(row.participant) & drv.split_id.eq(row.split_id) & drv.role.eq('train'), 'unit_id']
    assert set(json.loads(row.unit_ids)) <= set(pool)
_, categories = driving_categories(scores['driving'], scores['transfer'])
keys = ['participant', 'category']
actual = categories.set_index(keys).sort_index()
expected = pd.read_csv(OFFSET / 'analysis/category_summary.csv').set_index(keys).sort_index()
assert actual.index.equals(expected.index)
np.testing.assert_allclose(actual[ACCURACY_COLUMNS], expected[ACCURACY_COLUMNS], atol=1e-12)
report = {'date': '2026-11-13', 'scenes': len(units), 'samples': len(samples), 'source_files_verified': len(hashes),
          'source_hashes': hashes, 'runs': checks, 'matched_test_scenes': True, 'train_test_overlap': 0,
          'driving_calibration_selections_checked': len(selection), 'category_summaries_reproduced': len(categories),
          'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(OFFSET.parent / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'source_hashes'}, indent=2))
