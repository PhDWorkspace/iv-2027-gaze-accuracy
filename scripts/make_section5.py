"""Generate Section V (controlled investigation) figure, tables and data exports.

Usage: python scripts/make_section5.py /path/to/data [regression_summary_dir]

Reads only existing evaluation outputs under <data>/gaze_accuracy (nothing in the dataset is written):
  factors/controlled/1_distance/fixations.csv   static screen fixations (central_60, status ok), all participants
  factors/controlled/*/levels.csv, tests.csv    factor levels and Holm-corrected tests
  factors/controlled/6_pursuit/recordings.csv   pursuit vs static (target-relative dispersion)
  offset/runs/regression_chessboard/            controlled correction benchmark (summary.csv, scores.csv)
regression_summary_dir overrides the benchmark folder (used for the 2026-11-05 12:48 snapshot, see evals/README.md).

Writes figures/fig5_controlled.pdf, figures/tab_section5_factors.tex, figures/tab_regression.tex and the
plotted/tabulated values to evals/data/*.csv. Needs pandas and matplotlib (e.g. the horuspy-dev image).
Participants are pseudonymised (P1-P11, see PARTICIPANTS); P1-P6 keep the codes used in Sections IV and VI.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data") / "gaze_accuracy"
FACTORS = DATA / "factors/controlled"
REGRESSION = Path(sys.argv[2]) if len(sys.argv) > 2 else DATA / "offset/runs/regression_chessboard"
ROOT = Path(__file__).resolve().parents[1]
FIG, EXPORT = ROOT / "figures", ROOT / "evals/data"

PARTICIPANTS = {"William": "P1", "Katharina Winter": "P2", "Kanak Mazumder": "P3", "Max Buettner": "P4",
                "Mohan Ramesh": "P5", "Stefan Englmeier": "P6", "Sarah Joy": "P7", "Constantin Selzer": "P8",
                "Marilu Flores Turon Ramirez": "P9", "Sofia Elizabeth Moreno Reynaga": "P10",
                "Isabel Oliveira Trindade": "P11"}
BENCHMARK = {"william": "P1", "katharina": "P2", "stefan": "P6", "sarah": "P7"}
METRICS = {"angular_error_median_deg": "error", "bias_azimuth_deg": "azimuth", "bias_elevation_deg": "elevation",
           "p_std_deg": "pstd", "p_rms_s2s_deg": "s2s", "pupil_mm": "pupil"}
ALPHA = 0.05

INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
DIST = {1.0: "#1d4f91", 2.0: "#5f95cf", 4.0: "#b5cdea", 5.0: "#d9e5f3"}
ACCENT, ACCENT2, BLUE = "#eb6834", "#1baf7a", "#2f6aa3"
COLUMN, FULL = 3.5, 7.16
for f in Path("/usr/share/fonts").rglob("NimbusRoman-*.otf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Nimbus Roman", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 7, "axes.titlesize": 7, "axes.labelsize": 7,
    "xtick.labelsize": 6.5, "ytick.labelsize": 6.5, "legend.fontsize": 6.5, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "xtick.color": MUTED,
    "ytick.color": MUTED, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "lines.linewidth": 1.2,
    "pdf.fonttype": 42,
})


def code(name):
    return PARTICIPANTS[name]


def order(codes):
    return sorted(codes, key=lambda c: int(c[1:]))


# ----------------------------------------------------------------------------- data
def recordings():
    """V-A unit table: one row per static screen recording, metric medians over its central_60 fixations."""
    fix = pd.read_csv(FACTORS / "1_distance/fixations.csv", low_memory=False)
    fix["pupil_mm"] = pd.to_numeric(fix.pupil_mm, errors="coerce")
    rec = (fix.groupby(["participant", "recording_name", "date", "experiment_distance_m", "experiment_config_id"], dropna=False)
           [list(METRICS)].median().rename(columns=METRICS).reset_index())
    rec["fixations"] = fix.groupby("recording_name").size().reindex(rec.recording_name).to_numpy()
    rec["offset_norm"] = np.hypot(rec.azimuth, rec.elevation)
    rec.insert(0, "code", rec.participant.map(PARTICIPANTS))
    return rec.rename(columns={"experiment_distance_m": "distance_m", "experiment_config_id": "board_config"})


def participants(rec):
    """Per participant: median and IQR across recordings, all distances and 1 m only (equal weight per recording)."""
    out = []
    for scope, sub in (("all distances", rec), ("1 m", rec[rec.distance_m == 1.0])):
        for (c, name), d in sub.groupby(["code", "participant"]):
            row = dict(code=c, participant=name, scope=scope, recordings=len(d), days=d.date.nunique(),
                       distances="/".join(f"{x:g}" for x in sorted(d.distance_m.unique())))
            for m in ["error", "azimuth", "elevation", "offset_norm", "pstd", "s2s", "pupil"]:
                row[f"{m}_median"] = d[m].median()
                row[f"{m}_q25"], row[f"{m}_q75"] = d[m].quantile([0.25, 0.75])
            row["offset_share"] = row["offset_norm_median"] / row["error_median"]
            out.append(row)
    return pd.DataFrame(out).sort_values(["scope", "code"], key=lambda s: s.map(
        lambda v: int(v[1:]) if isinstance(v, str) and v.startswith("P") else v))


def distance_levels():
    lv = pd.read_csv(FACTORS / "1_distance/levels.csv")
    lv = lv[lv.view == "experiment_distance_m"].copy()
    lv.insert(0, "code", lv.participant.map(PARTICIPANTS))
    keep = ["code", "participant", "experiment_distance_m", "recordings", "instances", "fixations"]
    keep += [c for c in lv.columns if c.endswith(("_median", "_q25", "_q75"))]
    return lv[keep].rename(columns={"experiment_distance_m": "distance_m"})


def section_tests():
    """All Holm-corrected tests of the factors discussed in Section V (valid_fraction omitted)."""
    t = pd.read_csv(FACTORS / "tests.csv")
    t = t[t.metric != "valid_fraction"].copy()
    t.insert(0, "code", t.participant.map(PARTICIPANTS))
    t["significant"] = t.p_holm < ALPHA
    return t


def secondary_levels():
    frames = []
    for folder, view in [("4_illumination", "condition"), ("5_environment", "environment"),
                         ("5_environment", "date+environment"), ("7_session", "date")]:
        lv = pd.read_csv(FACTORS / folder / "levels.csv")
        lv = lv[lv.view == view].copy()
        lv.insert(0, "factor", folder)
        frames.append(lv)
    lv = pd.concat(frames, ignore_index=True)
    lv.insert(1, "code", lv.participant.map(PARTICIPANTS))
    keep = ["factor", "code", "participant", "view", "condition", "environment", "date", "recordings"]
    keep += [c for c in lv.columns if c.endswith("_median")]
    return lv[[c for c in keep if c in lv.columns]]


def regression():
    summary = pd.read_csv(REGRESSION / "summary.csv")
    scores = pd.read_csv(REGRESSION / "scores.csv")
    folds = scores.pivot_table(index=["participant", "split_id"], columns="model", values="median_error_deg")
    rows = []
    for (p, model), d in summary.groupby(["participant", "model"]):
        f = folds.loc[p]
        delta = f[model] - f["median"]
        rows.append(dict(code=BENCHMARK[p], model=model, median_error_deg=d.median_error_deg.iloc[0],
                         p90_error_deg=d.p90_error_deg.iloc[0], fold_min=f[model].min(), fold_max=f[model].max(),
                         delta_vs_median_mean=delta.mean(), delta_vs_median_min=delta.min(),
                         delta_vs_median_max=delta.max(), folds_better_than_median=int((delta < 0).sum()),
                         folds=len(delta)))
    splits = pd.read_csv(REGRESSION / "splits.csv")
    splits["recording"] = splits.unit_id.str.split("/").str[0]
    sets = splits.groupby(["participant", "split_id", "role"]).recording.apply(set).unstack()
    overlap = sum(len(a & b) for a, b in zip(sets.train, sets.test))
    n = sets.map(len).groupby("participant").agg(["min", "max"])
    return pd.DataFrame(rows), overlap, n


# ----------------------------------------------------------------------------- figure
def figure(rec, dist):
    """(a) accuracy per wearer at 1 m, (b) signed 2D offset per wearer at 1 m, (c) vertical offset vs distance."""
    fig, axes = plt.subplots(1, 3, figsize=(FULL, 2.1), layout="constrained",
                             gridspec_kw=dict(width_ratios=[1.3, 1.0, 0.95]))
    base = rec[rec.distance_m == 1.0]
    stats = base.groupby("code").agg(n=("error", "size"), med=("error", "median"), lo=("error", "min"),
                                     hi=("error", "max"), q25=("error", lambda v: v.quantile(.25)),
                                     q75=("error", lambda v: v.quantile(.75)), az=("azimuth", "median"),
                                     el=("elevation", "median"),
                                     az25=("azimuth", lambda v: v.quantile(.25)), az75=("azimuth", lambda v: v.quantile(.75)),
                                     el25=("elevation", lambda v: v.quantile(.25)), el75=("elevation", lambda v: v.quantile(.75)))
    stats = stats.sort_values("med")
    stats.to_csv(EXPORT / "fig5ab_data.csv", float_format="%.4f")

    ax = axes[0]  # (a) median with interquartile whiskers (caps) across recordings
    x = np.arange(len(stats))
    multi = stats.n.to_numpy() > 1
    ax.errorbar(x[multi], stats.med[multi], yerr=[(stats.med - stats.q25)[multi], (stats.q75 - stats.med)[multi]],
                fmt="o", color=BLUE, markersize=4, elinewidth=1.0, capsize=2.5, capthick=1.0, zorder=3)
    ax.scatter(x[~multi], stats.med[~multi], s=16, facecolor="white", edgecolor=BLUE, linewidth=1.0, zorder=4)
    ax.set_xticks(range(len(stats)), [f"{c}\n{int(r.n)}" for c, r in stats.iterrows()])
    ax.tick_params(axis="x", length=0, labelsize=6)
    ax.set_xlim(-0.6, len(stats) - 0.4)
    ax.set_ylim(0, None)
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("median angular error (°)")
    ax.set_title("(a) accuracy per wearer (1 m; n = recordings)", loc="left")

    ax = axes[1]  # (b) signed offsets, IQR across recordings as error bars
    ax.axhline(0, color=MUTED, linewidth=0.6, linestyle=(0, (3, 2)))
    ax.axvline(0, color=MUTED, linewidth=0.6, linestyle=(0, (3, 2)))
    multi = stats[stats.n > 1]
    ax.errorbar(multi.az, multi.el, xerr=[multi.az - multi.az25, multi.az75 - multi.az],
                yerr=[multi.el - multi.el25, multi.el75 - multi.el], fmt="none", ecolor=BLUE, elinewidth=0.7,
                alpha=0.6, zorder=2)
    ax.scatter(stats.az, stats.el, s=16, color=BLUE, zorder=3)
    nudges = {"P2": (2, 6), "P9": (4, -6), "P5": (-12, -4), "P4": (-12, 3), "P8": (-12, -3), "P3": (4, 3),
              "P11": (4, -4)}
    for c, r in stats.iterrows():
        ax.annotate(c, (r.az, r.el), xytext=nudges.get(c, (4, 0)), textcoords="offset points", fontsize=6,
                    va="center")
    lim = 1.6
    ax.set_xlim(-lim, lim)
    ax.set_xlabel("azimuth offset (°, + right)")
    ax.set_ylabel("elevation offset (°, + up)")
    ax.grid(False)
    ax.set_title("(b) signed offset per wearer (1 m)", loc="left")

    ax = axes[2]  # (c) distance response of the vertical offset
    for c, d in dist[dist.distance_m <= 4].groupby("code"):
        if len(d) < 2:
            continue
        color = ACCENT if c == "P7" else ACCENT2 if c == "P5" else INK
        ax.plot(d.distance_m, d.bias_elevation_deg_median, color=color, marker="o", markersize=2.5,
                linewidth=1.0 if color == INK else 1.3, alpha=0.85)
        dy = {"P7": 4, "P5": -4, "P8": 3, "P9": -3}.get(c, 0)
        ax.annotate(c, (d.distance_m.iloc[-1], d.bias_elevation_deg_median.iloc[-1]), xytext=(3, dy),
                    textcoords="offset points", va="center", fontsize=6, color=color)
    ax.axhline(0, color=MUTED, linewidth=0.6, linestyle=(0, (3, 2)))
    ax.set_xticks([1, 2, 4])
    ax.set_xlim(0.8, 4.7)
    ax.set_xlabel("viewing distance (m)")
    ax.set_ylabel("elevation offset (°, + up)")
    ax.set_title("(c) vertical offset vs. distance", loc="left")
    fig.savefig(FIG / "fig5_controlled.pdf")


# ----------------------------------------------------------------------------- tables
def fmt(x, sign=False):
    return f"{x:+.2f}" if sign else f"{x:.2f}"


def factor_table(rec, dist, tests, sec):
    def sig(name, rq, metric, scope=None, comparison=None):
        t = tests[(tests.participant == name) & (tests.rq == rq) & (tests.metric == metric)]
        if scope:
            t = t[t.scope.str.startswith(scope)]
        if comparison:
            t = t[t.comparison.str.startswith(comparison)]
        return bool(len(t)) and bool(t.significant.iloc[-1])

    def recs(folder, name="fixations.csv"):
        return pd.read_csv(FACTORS / folder / name, usecols=["recording_name", "participant"]).drop_duplicates()

    d = dist[dist.distance_m <= 4]
    shift = d.groupby("code").apply(lambda g: g.sort_values("distance_m").bias_elevation_deg_median.iloc[-1]
                                    - g.sort_values("distance_m").bias_elevation_deg_median.iloc[0]
                                    if len(g) > 1 else np.nan, include_groups=False).dropna()
    down = int((shift < 0).sum())
    dist_recs = recs("1_distance")
    pos_recs = recs("2_position")
    paired = tests[(tests.participant == "William") & (tests.comparison.str.startswith("4 m − 1 m"))
                   ].set_index("metric")
    sig_el = [code(n) for n in PARTICIPANTS if sig(n, "1_distance", "bias_elevation_deg", "all days")]
    sig_pstd = [code(n) for n in PARTICIPANTS if sig(n, "1_distance", "p_std_deg", "all days")]
    pos = tests[(tests.rq == "2_position") & (tests.comparison == "Lower − Upper") & (tests.scope == "board row")]
    pos_el = pos[pos.metric == "bias_elevation_deg"].set_index("code")
    pos_err = pos[pos.metric == "angular_error_median_deg"].set_index("code")
    bin_el = tests[(tests.rq == "2_position") & (tests.comparison == "Lower − Upper")
                   & tests.scope.str.startswith("same") & (tests.metric == "bias_elevation_deg") & tests.significant]
    bin_err = tests[(tests.rq == "2_position") & (tests.comparison == "Lower − Upper")
                    & tests.scope.str.startswith("same") & (tests.metric == "angular_error_median_deg")
                    & tests.significant]
    pos_prec = [code(n) for n in PARTICIPANTS if sig(n, "2_position", "p_std_deg", "board row", "Lower − Upper")]
    ill = sec[(sec.factor == "4_illumination")].pivot_table(index="code", columns="condition",
                                                            values=["pupil_mm_median", "bias_elevation_deg_median"])
    dpupil = ill["pupil_mm_median"]["Dark"] - ill["pupil_mm_median"]["Bright"]
    ill_sig = [code(n) for n in PARTICIPANTS if any(sig(n, "4_illumination", m) for m in
                                                     ["angular_error_median_deg", "bias_azimuth_deg",
                                                      "bias_elevation_deg", "p_std_deg", "p_rms_s2s_deg"])]
    pupil_sig = [code(n) for n in PARTICIPANTS if sig(n, "4_illumination", "pupil_mm")]
    env = sec[(sec.factor == "5_environment") & (sec.view == "environment")].set_index("environment")
    pur = pd.read_csv(FACTORS / "6_pursuit/recordings.csv").groupby("task")
    pur_m = pur[["angular_error_median_deg", "residual_p_std_deg"]].median()
    ses = sec[(sec.factor == "7_session") & (sec.participant == "William")].set_index("date")
    aug = ses.loc[[i for i in ses.index if i.startswith("2026-08")], "bias_elevation_deg_median"]
    late = ses.loc[[i for i in ses.index if not i.startswith("2026-08")], "bias_elevation_deg_median"]
    drift = tests[(tests.rq == "8_drift")]
    n_pos = pos_recs.participant.nunique()
    n_tested_pos = pos.participant.nunique()

    S = r"$^*$"
    neg = pos_el.mean_difference_deg[pos_el.mean_difference_deg < 0]
    rows = [
        ("Distance", f"1/2/4\\,m; {len(shift)} part. with $\\geq$2 distances, "
                     f"{dist_recs[dist_recs.participant.map(PARTICIPANTS).isin(shift.index)].shape[0]} rec.",
         f"gaze moves down with distance in {down} of {len(shift)}{S} ({', '.join(sig_el)}); "
         f"P1 paired 1$\\to$4\\,m: error {fmt(paired.loc['angular_error_median_deg', 'mean_difference_deg'], True)}\\dg{{}}{S}. "
         f"Accuracy worsens or improves with the initial offset (P7: "
         f"{d[(d.code == 'P7') & (d.distance_m == 1)].angular_error_median_deg_median.iloc[0]:.2f}$\\to$"
         f"{d[(d.code == 'P7') & (d.distance_m == 4)].angular_error_median_deg_median.iloc[0]:.2f}\\dg{{}}{S})",
         f"dispersion lower at 2--4\\,m ({', '.join(sig_pstd)}{S})"),
        ("Field position", f"rows/columns at 1\\,m; {n_pos} part., {len(pos_recs)} rec.",
         f"lower row lower by {-neg.max():.2f}--{-neg.min():.2f}\\dg{{}} "
         f"in {int((pos_el.mean_difference_deg < 0).sum())} of {n_tested_pos} "
         f"({', '.join(sorted(set(bin_el.code), key=lambda c: int(c[1:])))}{S}); error "
         f"{'/'.join(sorted(set(bin_err.code), key=lambda c: int(c[1:])))} worse{S}, P7 better; "
         f"eccentricity confounded with row",
         f"lower-row dispersion higher only for {', '.join(pos_prec)}{S}"),
        ("Bright / dark", f"1\\,m; {ill.shape[0]} part., {len(recs('4_illumination'))} rec.",
         f"pupil +{dpupil.min():.1f}--{dpupil.max():.1f}\\,mm ({', '.join(pupil_sig)}{S}); "
         f"no detected change in error or offset" + (f" (except {', '.join(ill_sig)})" if ill_sig else ""),
         "no detected change"),
        ("Indoor / outdoor", f"printed board; P1, {len(recs('5_environment'))} rec.",
         f"pupil {env.loc['Indoor', 'pupil_mm_median']:.1f}$\\to${env.loc['Outdoor', 'pupil_mm_median']:.1f}\\,mm{S}; "
         f"error {env.loc['Indoor', 'angular_error_median_deg_median']:.2f}$\\to$"
         f"{env.loc['Outdoor', 'angular_error_median_deg_median']:.2f}\\dg{{}}, n.s.",
         f"dispersion {env.loc['Indoor', 'p_std_deg_median']:.2f}$\\to${env.loc['Outdoor', 'p_std_deg_median']:.2f}"
         f"\\dg{{}}{S} (all days; n.s. same day)"),
        ("Smooth pursuit", "P1, {} pursuit / {} static rec.".format(
            *pd.read_csv(FACTORS / "6_pursuit/recordings.csv").task.value_counts()[["Pursuit", "Static"]]),
         f"error {pur_m.loc['Static', 'angular_error_median_deg']:.2f} vs.\\ "
         f"{pur_m.loc['Pursuit', 'angular_error_median_deg']:.2f}\\dg{{}} (static vs.\\ pursuit)",
         f"target-relative dispersion {pur_m.loc['Static', 'residual_p_std_deg']:.2f}$\\to$"
         f"{pur_m.loc['Pursuit', 'residual_p_std_deg']:.2f}\\dg{{}}{S}"),
        ("Repetition", f"P1, {len(recs('8_drift'))} rec., up to 8 per day",
         "no drift detected" + ("" if not drift.significant.any() else " (exceptions)"), "no change detected"),
        ("Between days", f"P1 {len(ses)} days, P2 2 days",
         f"P1 elevation ${aug.max():.1f}$ to ${aug.min():.1f}$\\dg{{}} (Aug.) vs.\\ ${late.max():.1f}$ to ${late.min():.1f}$\\dg{{}}"
         f"{S}$^\\dagger$; P2 no detected change",
         f"P1 differed{S}$^\\dagger$"),
    ]
    lines = [r"% Generated by scripts/make_section5.py from gaze_accuracy/factors/controlled.",
             r"\begin{tabular}{@{}p{0.08\textwidth}p{0.15\textwidth}p{0.46\textwidth}p{0.225\textwidth}@{}}",
             r"\toprule", r"Factor & Coverage & Accuracy and signed offset & Dispersion and precision \\",
             r"\midrule"]
    lines += [" & ".join(r"\raggedright " + c for c in r) + r" \tabularnewline" for r in rows]
    lines += [r"\bottomrule", r"\end{tabular}"]
    (FIG / "tab_section5_factors.tex").write_text("\n".join(lines).replace("…", "--") + "\n")


def regression_table(reg):
    models = [("raw", "Raw"), ("median", "Median"), ("linear_position", "Pos."),
              ("linear_position_pupil", "Pos.+pupil"), ("linear_position_distance", "Pos.+dist.")]
    lines = [r"% Generated by scripts/make_section5.py from offset/runs/regression_chessboard (see evals/README.md).",
             r"\begin{tabular}{@{}l" + "c" * len(models) + "@{}}", r"\toprule",
             " & " + " & ".join(m[1] for m in models) + r" \\", r"\midrule"]
    for c in ["P1", "P2", "P6", "P7"]:
        r = reg[reg.code == c].set_index("model")
        cells = []
        for m, _ in models:
            v = f"{r.loc[m, 'median_error_deg']:.2f}"
            if m not in ("raw", "median") and r.loc[m, "folds_better_than_median"] == r.loc[m, "folds"]:
                v = r"\textbf{" + v + "}"
            cells.append(v)
        lines.append(f"{c} & " + " & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (FIG / "tab_regression.tex").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    FIG.mkdir(exist_ok=True)
    EXPORT.mkdir(parents=True, exist_ok=True)
    rec = recordings()
    part = participants(rec)
    dist = distance_levels()
    tests = section_tests()
    sec = secondary_levels()
    reg, overlap, nsplit = regression()
    assert overlap == 0, "a recording contributes to both training and testing"
    rec.to_csv(EXPORT / "va_recordings.csv", index=False, float_format="%.4f")
    part.to_csv(EXPORT / "va_participants.csv", index=False, float_format="%.4f")
    dist.to_csv(EXPORT / "vb_distance_levels.csv", index=False, float_format="%.4f")
    tests.to_csv(EXPORT / "vb_tests.csv", index=False)
    sec.to_csv(EXPORT / "vb_secondary_levels.csv", index=False, float_format="%.4f")
    reg.to_csv(EXPORT / "vc_regression.csv", index=False, float_format="%.4f")
    nsplit.to_csv(EXPORT / "vc_split_recordings.csv")
    figure(rec, dist)
    factor_table(rec, dist, tests, sec)
    regression_table(reg)
    print("recordings", len(rec), "participants", rec.code.nunique(), "train/test overlap", overlap)
