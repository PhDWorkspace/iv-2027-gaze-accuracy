"""Verify refreshed model runs without changing the dataset or Horuspy."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from evaluation.offset_benchmark import ACCURACY_COLUMNS, make_splits, score_directions, summarize, test_weights
from evaluation.offset_data import GAZE_COLUMNS
from models.offset import MedianOffset
from run_benchmark import FEATURES, MODELS, load_inputs

DATA = Path('/home/william/data')
SCRATCH = Path('/scratch')
PAPER = Path('/paper')
ROOT = PAPER / 'evals/data/06_four_drivers/offset'
PEOPLE = ['william', 'katharina', 'stefan', 'constantin']
HASHES, REPORT, COVERAGE = {}, {}, []
INPUTS = {}
for name in ['transfer_regression', 'linear_runtime', 'ridge_20', 'ridge_80']:
    print('Auditing', name, flush=True)
    folder = SCRATCH / 'runs' / name
    protocol = json.loads((folder / 'protocol.json').read_text())
    spec = protocol['spec']
    original = json.loads((PAPER / 'evals/data/06_current_driving/specs' / f'{name}.json').read_text())
    original['participants'] = PEOPLE
    assert spec == original, name
    for source in protocol['sources']:
        p = Path(source['path'])
        if str(p) not in HASHES:
            HASHES[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
        assert HASHES[str(p)] == source['sha256'], p
    for p, expected in protocol['code_sha256'].items():
        assert hashlib.sha256((Path('/horuspy') / p).read_bytes()).hexdigest() == expected
    key = 'runtime' if spec.get('runtime_features') else 'transfer'
    if key not in INPUTS:
        cache = SCRATCH / f'inputs_{key}.pkl'
        if cache.exists():
            INPUTS[key] = pd.read_pickle(cache)
        else:
            INPUTS[key] = load_inputs(DATA, spec, DATA / 'gaze_accuracy/offset/units')[:2]
            pd.to_pickle(INPUTS[key], cache)
    units, samples = INPUTS[key]
    scores = pd.read_csv(folder / 'scores.csv')
    splits = pd.read_csv(folder / 'splits.csv')
    selections = pd.read_csv(folder / 'selections.csv')
    expected = pd.read_csv(folder / 'summary.csv').fillna({'group': ''}).set_index(['participant', 'protocol', 'model', 'method', 'group']).sort_index()
    actual = summarize(scores).set_index(['participant', 'protocol', 'model', 'method', 'group']).sort_index()
    assert actual.index.equals(expected.index)
    np.testing.assert_allclose(actual[ACCURACY_COLUMNS], expected[ACCURACY_COLUMNS], atol=1e-12)
    # Each model uses the same scene IDs, sample count and matched raw baseline within its split.
    for _, group in scores.groupby(['participant', 'split_id']):
        assert group.n_test_units.nunique() == group.n_test_samples.nunique() == 1
        assert np.isfinite(group[ACCURACY_COLUMNS].to_numpy()).all()
    # Recreate every saved split and independently replay one available split per person/protocol/model.
    replayed = 0
    for person in PEOPLE:
        pool = units.loc[units.participant.eq(person)]
        for pspec in spec['protocols']:
            generated = make_splits(pool, pspec, spec['seed'])
            chosen = False
            for number, split in enumerate(generated, 1):
                sid = f"{pspec['name']}/{number:04d}"
                saved = splits.loc[splits.participant.eq(person) & splits.split_id.eq(sid)]
                for role in ['train', 'test']:
                    assert set(saved.loc[saved.role.eq(role), 'unit_id']) == set(split[f'{role}_ids'])
                assert not set(split['train_ids']) & set(split['test_ids'])
                if chosen or not split['train_ids']:
                    continue
                chosen = True
                train = pool.set_index('unit_id', drop=False).loc[split['train_ids']]
                if train.domain.eq('chessboard').all():
                    assert train.complete.all()
                test = samples.loc[samples.unit_id.isin(split['test_ids'])]
                weights = test_weights(test)
                for m in [None, *spec['models']]:
                    label = 'raw' if m is None else m.get('label', m['name'])
                    row = scores.loc[scores.participant.eq(person) & scores.split_id.eq(sid) & scores.model.eq(label)].iloc[0]
                    if m is None:
                        directions = test[GAZE_COLUMNS].to_numpy(float)
                    else:
                        kwargs = {k: [c for f in v for c in FEATURES[f]] if k == 'features' else v for k, v in m.items() if k not in ['name', 'label']}
                        directions = MODELS[m['name']](train, samples.loc[samples.participant.eq(person)], **kwargs)(test)
                    values = score_directions(test, directions, weights)
                    np.testing.assert_allclose([values[c] for c in ACCURACY_COLUMNS], row[ACCURACY_COLUMNS].to_numpy(float), atol=1e-10)
                    replayed += 1
    for row in selections.itertuples():
        pool = splits.loc[splits.participant.eq(row.participant) & splits.split_id.eq(row.split_id) & splits.role.eq('train'), 'unit_id']
        assert set(json.loads(row.unit_ids)) == set(pool)
    # Participant-specific seeds mean adding P6 scenes/P8 cannot change P1/P2 results.
    old = pd.read_csv(PAPER / 'evals/data/06_current_driving/offset/runs' / name / 'summary.csv')
    keys = ['participant', 'protocol', 'model', 'method', 'group']
    a = scores.loc[scores.participant.isin(['william', 'katharina'])]
    a = summarize(a).fillna({'group': ''}).set_index(keys).sort_index()
    b = old.loc[old.participant.isin(['william', 'katharina'])].fillna({'group': ''}).set_index(keys).sort_index()
    assert a.index.equals(b.index)
    np.testing.assert_allclose(a[ACCURACY_COLUMNS], b[ACCURACY_COLUMNS], atol=1e-10)
    REPORT[name] = {'score_rows': len(scores), 'replayed_scores': replayed, 'split_identities_match': True,
                    'summary_reproduced': True, 'p1_p2_unchanged': True, 'calibration_selections': len(selections)}

# Runtime sample eligibility is measured explicitly, keeping the original feature filter.
u, s = INPUTS['transfer']
ru, rs = INPUTS['runtime']
for person in PEOPLE:
    a = s.loc[s.participant.eq(person) & s.domain.eq('driving')]
    b = rs.loc[rs.participant.eq(person)]
    assert set(a.unit_id) == set(b.unit_id)
    assert set(zip(b.recording_id, b.gaze_sample_id)) <= set(zip(a.recording_id, a.gaze_sample_id))
    COVERAGE.append({'participant': person, 'scenes': a.unit_id.nunique(), 'samples': len(a), 'runtime_samples': len(b), 'removed_samples': len(a)-len(b)})

# Source-trained models and velocity models share the established driving test scenes.
drv = pd.read_csv(ROOT / 'runs/driving/splits.csv.gz')
tr = pd.read_csv(SCRATCH / 'runs/transfer_regression/splits.csv')
rt = pd.read_csv(SCRATCH / 'runs/linear_runtime/splits.csv')
for person in PEOPLE:
    for fold in range(1, 6):
        target = set(drv.loc[drv.participant.eq(person) & drv.fold.eq(fold) & drv.role.eq('test'), 'unit_id'])
        for sp, protocol in [(tr, 'chessboard_to_driving'), (tr, 'driving_to_driving'), (rt, 'scene_blocks')]:
            actual = sp.loc[sp.participant.eq(person) & sp.fold.eq(fold) & sp.role.eq('test') & sp.protocol.eq(protocol), 'unit_id']
            assert set(actual) == target
# Principal median-offset rows reproduce the already audited 322-scene benchmark.
summary = pd.read_csv(SCRATCH / 'runs/transfer_regression/summary.csv')
category = pd.read_csv(ROOT / 'analysis/category_summary.csv')
for person in PEOPLE:
    for source, label in [('chessboard_to_driving', 'Chessboard E5 · pooled'), ('driving_to_driving', 'Driving · pooled 20%')]:
        a = summary.loc[summary.participant.eq(person) & summary.protocol.eq(source) & summary.model.eq('median')].iloc[0]
        b = category.loc[category.participant.eq(person) & category.category.eq(label)].iloc[0]
        np.testing.assert_allclose(a[ACCURACY_COLUMNS].to_numpy(float), b[ACCURACY_COLUMNS].to_numpy(float), atol=1e-10)

# Record fold-wise runtime improvements against the feature-matched median.
linear = pd.read_csv(SCRATCH / 'runs/linear_runtime/scores.csv')
folds = linear.pivot(index=['participant', 'fold'], columns='model', values=['median_error_deg', 'p90_error_deg'])
deltas = []
for person in PEOPLE:
    d = folds.loc[person]
    med = d['median_error_deg']['runtime'] < d['median_error_deg']['median']
    p90 = d['p90_error_deg']['runtime'] < d['p90_error_deg']['median']
    deltas.append({'participant': person, 'median_folds_better': int(med.sum()), 'p90_folds_better': int(p90.sum()), 'both_folds_better': int((med & p90).sum()), 'folds': len(d)})
report = {'date': '2026-11-13', 'runs': REPORT, 'source_files_verified': len(HASHES), 'source_hashes': HASHES,
          'runtime_coverage': COVERAGE, 'linear_velocity_fold_improvements': deltas, 'train_test_overlap': 0,
          'median_baselines_match_published_offset_benchmark': True, 'model_and_spec_changes': 'participants only',
          'audit_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(SCRATCH / 'verification.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='source_hashes'},indent=2))
