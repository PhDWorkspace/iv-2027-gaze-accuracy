"""Generate Section VI (transfer to driving) figure, table and data exports.

Usage: python scripts/make_section6.py /path/to/data evals/data/06_transfer_regression_run

Reads only existing evaluation outputs (nothing in the dataset is written):
  <data>/gaze_accuracy/offset/analysis/category_summary.csv  fold-matched driving comparison (raw, chessboard, driving)
  <data>/gaze_accuracy/offset/analysis/tests.csv             paired scene-level tests (RQ1-RQ5)
  <data>/gaze_accuracy/offset/runs/driving/                  sparse in-situ references (k scenes, random/pattern)
  <data>/gaze_accuracy/offset/runs/ridge_20, ridge_80/       driving-trained ridge with runtime features
  <transfer_regression_dir>                                  horuspy spec transfer_regression.json (chessboard- and
                                                             driving-trained median/linear/ridge on the same scenes)
Writes figures/fig6_transfer.pdf, figures/tab_transfer_models.tex and evals/data/06_*.csv.
Participants: P1 william, P2 katharina, P6 stefan (codes as in Sections IV and V).
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data") / "gaze_accuracy/offset"
TRANSFER_REGRESSION = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("evals/data/06_transfer_regression_run")
ROOT = Path(__file__).resolve().parents[1]
FIG, EXPORT = ROOT / "figures", ROOT / "evals/data"
DRIVERS = {"william": "P1", "katharina": "P2", "stefan": "P6"}
COLORS = {"P1": "#2f6aa3", "P2": "#eb6834", "P6": "#1baf7a"}
MARKERS = {"P1": "o", "P2": "s", "P6": "^"}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
FULL, COLUMN = 7.16, 3.5
for f in Path("/usr/share/fonts").rglob("NimbusRoman-*.otf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Nimbus Roman", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 7, "axes.titlesize": 7, "axes.labelsize": 7,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.5,
    "lines.linewidth": 1.2, "pdf.fonttype": 42,
})
MODELS = [("median", "Median offset", "constant"), ("linear_position", "Linear", "position"),
          ("ridge_position", "Ridge", "position"), ("linear_position_pupil", "Linear", "position + pupil"),
          ("ridge_position_pupil", "Ridge", "position + pupil")]


def category_summary():
    cs = pd.read_csv(DATA / "analysis/category_summary.csv")
    cs.insert(0, "code", cs.participant.map(DRIVERS))
    return cs[cs.code.notna()]


def reference_folds():
    """Random k-scene offsets: mean over the 20 draws within each fold; geometric layouts per fold."""
    s = pd.read_csv(DATA / "runs/driving/scores.csv")
    s["code"] = s.participant.map(DRIVERS)
    rnd = s[s.selection == "random"].groupby(["code", "k", "fold"])[["median_error_deg", "p90_error_deg"]].mean()
    rnd = rnd.reset_index().assign(selection="random")
    pat = s[s.selection == "pattern"].groupby(["code", "pattern", "k", "fold"])[
        ["median_error_deg", "p90_error_deg"]].mean().reset_index().assign(selection="geometric")
    single = s[s.selection == "single"].groupby(["code", "fold"])[["median_error_deg", "p90_error_deg"]].mean()
    single = single.reset_index().assign(selection="single scene (each)", k=1)
    pooled = s[s.selection == "all"].groupby(["code", "fold"])[["median_error_deg", "p90_error_deg", "n_train_units"]
                                                               ].mean().reset_index().assign(selection="all (20%)")
    raw = s[s.selection == "none"].groupby(["code", "fold"])[["median_error_deg", "p90_error_deg"]].mean()
    raw = raw.reset_index().assign(selection="raw", k=0)
    return pd.concat([raw, single, rnd, pat, pooled], ignore_index=True)


def model_runs():
    """Chessboard- and driving-trained models on the same held-out driving scenes, plus driving ridge runs."""
    tr = pd.read_csv(TRANSFER_REGRESSION / "summary.csv")
    tr["code"] = tr.participant.map(DRIVERS)
    tr["source"] = tr.protocol.map({"chessboard_to_driving": "chessboard", "driving_to_driving": "driving"})
    scores = pd.read_csv(TRANSFER_REGRESSION / "scores.csv")
    scores["code"] = scores.participant.map(DRIVERS)
    folds = scores.pivot_table(index=["code", "protocol", "fold"], columns="model",
                               values=["median_error_deg", "p90_error_deg"])
    rows = []
    for (code, protocol), f in folds.groupby(level=[0, 1]):
        for model in f["median_error_deg"].columns:
            for metric in ("median_error_deg", "p90_error_deg"):
                d = f[metric][model] - f[metric]["median"]
                rows.append(dict(code=code, protocol=protocol, model=model, metric=metric,
                                 mean_vs_median=d.mean(), min_vs_median=d.min(), max_vs_median=d.max(),
                                 folds_better=int((d < 0).sum()), folds=len(d)))
    deltas = pd.DataFrame(rows)
    ridge = []
    for share, run in (("20%", "ridge_20"), ("80%", "ridge_80")):
        r = pd.read_csv(DATA / "runs" / run / "summary.csv").assign(calibration_share=share)
        r["code"] = r.participant.map(DRIVERS)
        ridge.append(r)
    return tr, deltas, pd.concat(ridge, ignore_index=True), scores


def same_test_scenes():
    """True if chessboard- and driving-trained models were scored on identical held-out scene sets per fold."""
    sp = pd.read_csv(TRANSFER_REGRESSION / "splits.csv.gz")
    test = sp[sp.role == "test"].groupby(["participant", "protocol", "fold"]).unit_id.apply(frozenset).unstack("protocol")
    train_drv = sp[(sp.role == "train") & (sp.protocol == "driving_to_driving")].groupby(
        ["participant", "fold"]).unit_id.apply(frozenset)
    overlap = sum(len(a & b) for a, b in zip(train_drv, test["driving_to_driving"].loc[train_drv.index]))
    return bool((test["chessboard_to_driving"] == test["driving_to_driving"]).all()), overlap


def figure(cs, ref, tr):
    fig, axes = plt.subplots(1, 2, figsize=(COLUMN, 1.9), layout="constrained", gridspec_kw=dict(width_ratios=[0.85, 1.15]))
    ax = axes[0]
    conditions = [("Raw driving", "none"), ("Chessboard E5 · pooled", "chess-\nboard"),
                  ("Driving · pooled 20%", "driving\n(20%)")]
    width = 0.26
    for j, (code, color) in enumerate(COLORS.items()):
        d = cs[cs.code == code].set_index("category")
        for i, (cat, _) in enumerate(conditions):
            x = i + (j - 1) * width
            med, p90 = d.loc[cat, "median_error_deg"], d.loc[cat, "p90_error_deg"]
            ax.vlines(x, med, p90, color=color, linewidth=0.8, alpha=0.6)
            ax.scatter(x, med, marker=MARKERS[code], s=10, color=color, zorder=3, label=code if i == 0 else None)
            ax.scatter(x, p90, marker="_", s=18, color=color, zorder=3)
    ax.set_xticks(range(len(conditions)), [c[1] for c in conditions])
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, 9)
    ax.set_ylabel("error (°)")
    ax.legend(loc="upper center", ncol=3, frameon=False, handletextpad=0.1, columnspacing=0.5, fontsize=6)
    ax.set_title("(a) offset source", loc="left")

    ax = axes[1]
    ks = [1, 2, 3, 4, 5, 8]
    for code, color in COLORS.items():
        r = ref[(ref.code == code) & (ref.selection == "random")]
        g = r.groupby("k").median_error_deg
        m = g.mean().reindex(ks)
        ax.fill_between(ks, g.min().reindex(ks), g.max().reindex(ks), color=color, alpha=0.15, linewidth=0)
        ax.plot(ks, m, color=color, marker=MARKERS[code], markersize=2.2, linewidth=1.0)
        pooled = cs[(cs.code == code) & (cs.category == "Driving · pooled 20%")].median_error_deg.iloc[0]
        chess = cs[(cs.code == code) & (cs.category == "Chessboard E5 · pooled")].median_error_deg.iloc[0]
        ax.scatter(10, pooled, marker=MARKERS[code], s=10, color=color, zorder=3)
        ax.axhline(chess, color=color, linestyle=(0, (3, 2)), linewidth=0.8)
    ax.set_xticks(ks + [10], [str(k) for k in ks] + ["20%"])
    ax.set_xlabel("driving reference scenes $k$")
    ax.set_ylabel("median error (°)")
    ax.set_ylim(0, None)
    ax.set_title("(b) in-situ references", loc="left")
    fig.savefig(FIG / "fig6_transfer.pdf")


def table(tr, linear):
    """Compact model table, linear models only (ridge results are kept in the md and data exports)."""
    rows = [("Chessboard", "median offset", tr[(tr.model == "median") & (tr.source == "chessboard")]),
            ("", "linear, position", tr[(tr.model == "linear_position") & (tr.source == "chessboard")]),
            ("", "linear, pos.\\,+\\,pupil", tr[(tr.model == "linear_position_pupil") & (tr.source == "chessboard")]),
            ("Driving", "median offset", tr[(tr.model == "median") & (tr.source == "driving")]),
            ("(20\\%)", "linear, position", tr[(tr.model == "linear_position") & (tr.source == "driving")]),
            ("", "linear, pos.\\,+\\,pupil", tr[(tr.model == "linear_position_pupil") & (tr.source == "driving")]),
            ("", "linear, pos.\\,+\\,velocity", linear[linear.model == "runtime"])]
    lines = [r"% Generated by scripts/make_section6.py (see evals/06_transfer_to_driving.md).",
             r"\begin{tabular}{@{}l@{\hskip 4pt}l@{\hskip 4pt}cc@{\hskip 5pt}cc@{\hskip 5pt}cc@{}}", r"\toprule",
             r" & & \multicolumn{2}{c}{P1} & \multicolumn{2}{c}{P2} & \multicolumn{2}{c}{P6} \\",
             r"\cmidrule(lr){3-4}\cmidrule(lr){5-6}\cmidrule(l){7-8}",
             r"Fitted on & Correction & Med. & P90 & Med. & P90 & Med. & P90 \\", r"\midrule"]
    for i, (src, name, d) in enumerate(rows):
        d = d.set_index("code")
        cells = " & ".join(f"{d.loc[c, 'median_error_deg']:.2f} & {d.loc[c, 'p90_error_deg']:.2f}" for c in DRIVERS.values())
        if i == 3:
            lines.append(r"\midrule")
        lines.append(f"{src} & {name} & {cells} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (FIG / "tab_transfer_models.tex").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    EXPORT.mkdir(parents=True, exist_ok=True)
    cs = category_summary()
    ref = reference_folds()
    tr, deltas, ridge, scores = model_runs()
    same, overlap = same_test_scenes()
    assert same and overlap == 0, (same, overlap)
    cs.to_csv(EXPORT / "06_driving_offset_by_category.csv", index=False, float_format="%.4f")
    ref.to_csv(EXPORT / "06_reference_count_per_fold.csv", index=False, float_format="%.4f")
    tr.to_csv(EXPORT / "06_model_comparison_summary.csv", index=False, float_format="%.4f")
    deltas.to_csv(EXPORT / "06_model_vs_median_per_fold.csv", index=False, float_format="%.4f")
    ridge.to_csv(EXPORT / "06_driving_ridge_runtime_features.csv", index=False, float_format="%.4f")
    tests = pd.read_csv(DATA / "analysis/tests.csv")
    tests[tests.participant.isin(DRIVERS)].assign(code=lambda t: t.participant.map(DRIVERS)).to_csv(
        EXPORT / "06_driving_scene_tests.csv", index=False)
    figure(cs, ref, tr)
    linear = pd.read_csv(ROOT / "evals/data/06_linear_runtime_run/share_20/summary.csv")
    linear["code"] = linear.participant.map(DRIVERS)
    linear.to_csv(EXPORT / "06_driving_linear_runtime_features.csv", index=False, float_format="%.4f")
    table(tr, linear)
    print("same held-out scenes for chessboard- and driving-trained models:", same, "| train/test overlap:", overlap)
