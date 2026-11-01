"""Generate the paper figures from saved evaluation outputs.

Usage: python scripts/make_figures.py /path/to/data

Reads only existing evaluation tables under <data>/controlled/evaluations and
<data>/driving/evaluations (nothing is recomputed or written to the dataset).
Writes PDFs to figures/ next to this script's parent directory.
Participants are pseudonymised for double-blind review (see PARTICIPANTS).
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path(sys.argv[1] if len(sys.argv) > 1 else "/home/william/data")
OUT = Path(__file__).resolve().parents[1] / "figures"
DRIVE = DATA / "driving/evaluations"
FACTORS = DATA / "controlled/evaluations/factor_analysis"

PARTICIPANTS = {"william": "P1", "William": "P1", "katharina": "P2", "Katharina Winter": "P2",
                "Kanak Mazumder": "P3", "Max Buettner": "P4", "Mohan Ramesh": "P5", "Stefan Englmeier": "P6"}
# Reference categorical slots 1-3 (validated all-pairs) plus neutral gray for raw gaze.
RAW, CHESS, DRIVING, EXTENDED = "#8a8985", "#eb6834", "#2a78d6", "#1baf7a"
INK, MUTED = "#0b0b0b", "#52514e"
MARKER = {"P1": "o", "P2": "s", "P3": "^", "P4": "v", "P5": "D", "P6": "P"}
COLUMN, FULL = 3.5, 7.16

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Nimbus Roman", "Times New Roman", "FreeSerif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 7, "axes.titlesize": 7, "axes.labelsize": 7, "xtick.labelsize": 6.5,
    "ytick.labelsize": 6.5, "legend.fontsize": 6.5, "axes.spines.top": False,
    "axes.spines.right": False, "axes.edgecolor": MUTED, "axes.linewidth": 0.6,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True, "axes.grid.axis": "y",
    "grid.color": "#e4e3df", "grid.linewidth": 0.5, "lines.linewidth": 1.4, "pdf.fonttype": 42,
})


def boxes(ax, groups, colors, labels):
    """Thin boxplot with jittered fold-level points."""
    bp = ax.boxplot(groups, widths=0.5, patch_artist=True, showfliers=False,
                    medianprops=dict(color=INK, linewidth=1), whiskerprops=dict(color=MUTED, linewidth=0.6),
                    capprops=dict(color=MUTED, linewidth=0.6), boxprops=dict(linewidth=0.6, color=MUTED))
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.35)
    rng = np.random.default_rng(0)
    for i, (values, color) in enumerate(zip(groups, colors), start=1):
        ax.scatter(i + rng.uniform(-0.12, 0.12, len(values)), values, s=5, color=color, zorder=3, linewidths=0)
    ax.set_xticks(range(1, len(labels) + 1), labels)


def fig_driving():
    """Fig. 2: raw vs chessboard vs driving correction, and reference-scene budget."""
    plot = pd.read_csv(DRIVE / "driving_offset_benchmark/boxplot_data.csv")
    summary = pd.read_csv(DRIVE / "driving_offset_benchmark/category_summary.csv")
    methods = [("Raw driving", "raw", RAW), ("Chessboard E4 · full 15", "1\nboard", CHESS),
               ("Chessboard E5 · pooled", "all\nboards", CHESS), ("Driving · single scene", "1\nscene", DRIVING),
               ("Driving · pooled 20%", "20%\nscenes", DRIVING)]
    shapes = {"Driving line · 2": (2, "line"), "Driving line · 3": (3, "line"), "Driving triangle · 3": (3, "triangle"),
              "Driving rectangle · 4": (4, "rectangle"), "Driving rectangle + center · 5": (5, "rect.+center")}
    fig, axes = plt.subplots(2, 2, figsize=(COLUMN, 3.3), gridspec_kw=dict(height_ratios=[1.15, 1]),
                             layout="constrained")
    for col, key in enumerate(["william", "katharina"]):
        ax = axes[0, col]
        rows = plot[plot.participant == key]
        boxes(ax, [rows[rows.category == m].median_error_deg.to_numpy() for m, _, _ in methods],
              [c for _, _, c in methods], [l for _, l, _ in methods])
        ax.set_title(f"{PARTICIPANTS[key]}", loc="left", fontweight="bold")
        ax.set_ylim(0, 4.6 if key == "william" else 2.6)
        ax = axes[1, col]
        s = summary[summary.participant == key].set_index("category")
        k = [1, 2, 3, 4, 5, 8]
        ax.plot(k, [s.loc[f"Driving random · {i}", "median_error_deg"] for i in k], color=DRIVING, marker="o",
                markersize=3, label="random scenes")
        for cat, (kk, name) in shapes.items():
            ax.scatter(kk + 0.12, s.loc[cat, "median_error_deg"], marker="x", s=14, color=INK, linewidths=0.8,
                       label="geometric layout" if cat == "Driving line · 2" else None, zorder=3)
        ax.axhline(s.loc["Driving · pooled 20%", "median_error_deg"], color=DRIVING, linestyle="--", linewidth=0.9,
                   label="pooled 20% scenes")
        ax.axhline(s.loc["Chessboard E5 · pooled", "median_error_deg"], color=CHESS, linestyle="--", linewidth=0.9,
                   label="boards pooled")
        ax.set_xticks(k)
        ax.set_xlabel("reference scenes $k$")
    axes[0, 0].set_ylabel("(a)  median error (°)")
    axes[1, 0].set_ylabel("(b)  median error (°)")
    fig.legend(*axes[1, 0].get_legend_handles_labels(), frameon=False, ncol=2, loc="outside lower center",
               handlelength=1.8, columnspacing=1.0)
    fig.savefig(OUT / "fig2_driving_correction.pdf")


def test_value(tests, participant, rq, comparison, metric="angular_error_median_deg"):
    row = tests[(tests.participant == participant) & (tests.rq == rq) & (tests.comparison == comparison)
                & (tests.metric == metric)]
    return row.iloc[-1] if len(row) else None


def fig_controlled():
    """Fig. 3: distance, robustness summary, lower-row precision, pursuit dispersion."""
    tests = pd.read_csv(FACTORS / "tests.csv")
    fig, axes = plt.subplots(1, 4, figsize=(FULL, 2.0), gridspec_kw=dict(width_ratios=[0.9, 1.25, 1.0, 0.7]),
                             layout="constrained")

    ax = axes[0]
    dist = pd.read_csv(FACTORS / "1_distance/levels.csv")
    dist = dist[(dist.view == "scope+experiment_distance_m") & ~dist.scope.str.contains("pilot")]
    for name, d in dist.groupby("participant"):
        p = PARTICIPANTS[name]
        ax.plot(d.experiment_distance_m, d.angular_error_median_deg_median, color=INK, marker=MARKER[p], markersize=3)
        ax.plot(d.experiment_distance_m, d.p_std_deg_median, color=MUTED, marker=MARKER[p], markersize=3,
                linestyle=":", linewidth=1)
        ax.annotate(p, (d.experiment_distance_m.iloc[-1], d.angular_error_median_deg_median.iloc[-1]),
                    xytext=(3, 0), textcoords="offset points", va="center", fontsize=6.5)
    ax.text(2.2, 0.62, "dispersion\n(dotted)", color=MUTED, fontsize=6)
    ax.set_xticks([1, 2, 4])
    ax.set_xlabel("viewing distance (m)")
    ax.set_ylabel("accuracy / dispersion (°)")
    ax.set_title("(a) distance", loc="left", fontweight="bold")

    ax = axes[1]
    levels = pd.read_csv(FACTORS / "4_illumination/levels.csv")
    levels = levels[levels.view == "condition"].pivot(index="participant", columns="condition",
                                                       values="angular_error_median_deg_median")
    env = pd.read_csv(FACTORS / "5_environment/levels.csv")
    env = env[(env.view == "date+environment") & (env.date == "2026-10-30")].set_index("environment")
    rows = []  # (label, participant, difference, significant)
    for name in ["William", "Katharina Winter"]:
        t = test_value(tests, name, "1_distance", "4 m − 1 m")
        if t is not None:
            rows.append(("4 m − 1 m", name, t.mean_difference_deg, t.p_holm < 0.05))
        else:
            t = test_value(tests, name, "1_distance", "experiment_distance_m: 1.0 / 2.0 / 4.0")
            d = dist[dist.participant == name].set_index("experiment_distance_m").angular_error_median_deg_median
            rows.append(("4 m − 1 m", name, d[4.0] - d[1.0], t.p_holm < 0.05))
    lower = tests[(tests.rq == "2_position") & (tests.comparison == "Lower − Upper")
                  & (tests.metric == "angular_error_median_deg")].groupby("participant").tail(1)
    rows += [("lower − upper", r.participant, r.mean_difference_deg, r.p_holm < 0.05) for r in lower.itertuples()]
    ecc = tests[(tests.rq == "2_position") & (tests.comparison == "20–30° − 0–10°")
                & (tests.metric == "angular_error_median_deg")]
    rows += [("ecc. 20–30° − 0–10°", r.participant, r.mean_difference_deg, r.p_holm < 0.05)
             for r in ecc.itertuples()]
    for name, r in levels.iterrows():
        p = test_value(tests, name, "4_illumination", "condition: Bright / Dark").p_holm
        rows.append(("dark − bright", name, r.Dark - r.Bright, p < 0.05))
    p = tests[(tests.rq == "5_environment") & (tests.n_units == 18)
              & (tests.metric == "angular_error_median_deg")].p_holm.iloc[0]
    rows.append(("outdoor − indoor", "William",
                 env.loc["Outdoor", "angular_error_median_deg_median"] - env.loc["Indoor", "angular_error_median_deg_median"],
                 p < 0.05))
    t = test_value(tests, "William", "8_drift", "Pass 2 − pass 1")
    rows.append(("pass 2 − pass 1", "William", t.mean_difference_deg, t.p_holm < 0.05))
    order = list(dict.fromkeys(r[0] for r in rows))
    for label, name, diff, significant in rows:
        y = len(order) - order.index(label)
        p = PARTICIPANTS[name]
        ax.scatter(diff, y, marker=MARKER[p], s=14, color=INK if significant else "white",
                   edgecolors=INK, linewidths=0.7, zorder=3)
    for p in MARKER:
        ax.scatter([], [], marker=MARKER[p], s=14, color="white", edgecolors=INK, linewidths=0.7, label=p)
    ax.legend(frameon=False, ncol=2, loc="lower left", handletextpad=0.1, columnspacing=0.5, borderaxespad=0.1)
    ax.axvline(0, color=MUTED, linewidth=0.7)
    ax.set_yticks(range(len(order), 0, -1), order)
    ax.grid(axis="x", color="#e4e3df", linewidth=0.5)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("Δ accuracy (°)")
    ax.set_title("(b) accuracy effects", loc="left", fontweight="bold")
    pd.DataFrame(rows, columns=["comparison", "participant", "difference_deg", "significant"]).assign(
        participant=lambda d: d.participant.map(PARTICIPANTS)).to_csv(OUT / "fig3b_data.csv", index=False)

    ax = axes[2]
    pos = pd.read_csv(FACTORS / "2_position/levels.csv")
    pos = pos[pos.view == "row"].pivot(index="participant", columns="row", values="p_rms_s2s_deg_median")
    pos.index = pos.index.map(PARTICIPANTS)
    pos = pos.sort_index()
    for i, (p, r) in enumerate(pos.iterrows()):
        ax.plot([i, i], [r.Upper, r.Lower], color=MUTED, linewidth=0.8)
        ax.scatter(i, r.Upper, s=12, color="white", edgecolors=INK, linewidths=0.7, zorder=3,
                   label="upper row" if i == 0 else None)
        ax.scatter(i, r.Lower, s=12, color=INK, zorder=3, label="lower row" if i == 0 else None)
    ax.set_xticks(range(len(pos)), pos.index)
    ax.set_ylabel("precision RMS-S2S (°)")
    ax.legend(frameon=False, loc="upper left", handletextpad=0.2, borderaxespad=0.1)
    ax.set_title("(c) lower-row precision", loc="left", fontweight="bold")

    ax = axes[3]
    pursuit = pd.read_csv(FACTORS / "6_pursuit/recordings.csv")
    groups = [pursuit[pursuit.task == t].residual_p_std_deg.to_numpy() for t in ["Static", "Pursuit"]]
    boxes(ax, groups, [RAW, INK], ["static", "pursuit"])
    ax.set_ylabel("residual dispersion (°)")
    ax.set_title("(d) pursuit", loc="left", fontweight="bold")
    fig.savefig(OUT / "fig3_controlled_factors.pdf")


def fig_transfer():
    """Fig. 4: extended correction vs driving median baseline, tails and subgroups."""
    rows = []
    for share in [20, 40, 60, 80]:
        seeds = pd.read_csv(DRIVE / f"ridge_offset/gaze_correction_{share}/per_seed.csv")
        means = seeds.groupby(["participant", "method"])[["median_error_deg", "p90_error_deg"]].mean().reset_index()
        rows.append(means.assign(share=share))
    scores = pd.concat(rows)
    scores.to_csv(OUT / "fig4ab_data.csv", index=False)
    tags = pd.read_csv(DRIVE / "ridge_offset/tags.csv")
    tags = tags[tags.share == 20]
    selected = [("gaze speed (third)", "high", "fast gaze"), ("gaze speed (third)", "low", "slow gaze"),
                ("ego motion", "moving", "ego moving"), ("ego motion", "stationary", "ego stationary"),
                ("relative motion", "approaching", "approaching target"),
                ("target distance (third)", "low", "near target"), ("target distance (third)", "medium", "medium distance"),
                ("target distance (third)", "high", "far target"),
                ("eye-image exposure", "largely_overexposed", "overexposed eye img.")]

    fig, axes = plt.subplots(1, 3, figsize=(FULL, 2.05), gridspec_kw=dict(width_ratios=[1, 1, 1.3]),
                             layout="constrained")
    for ax, metric, title in [(axes[0], "median_error_deg", "(a) median error"), (axes[1], "p90_error_deg", "(b) P90 error")]:
        for key, ls in [("william", "-"), ("katharina", "--")]:
            for method, color, name in [("median", DRIVING, "median offset"), ("selected", EXTENDED, "extended")]:
                d = scores[(scores.participant == key) & (scores.method == method)]
                ax.plot(d.share, d[metric], color=color, linestyle=ls, marker=MARKER[PARTICIPANTS[key]], markersize=3,
                        label=f"{PARTICIPANTS[key]} {name}")
        ax.set_xticks([20, 40, 60, 80])
        ax.set_xlabel("calibration scenes (%)")
        ax.set_ylabel("error (°)")
        ax.set_title(title, loc="left", fontweight="bold")
    fig.legend(*axes[0].get_legend_handles_labels(), frameon=False, ncol=4, loc="outside lower left",
               handlelength=2.2, columnspacing=1.0)
    axes[0].set_ylim(0.68, 0.86)
    axes[1].set_ylim(1.3, 1.75)

    ax = axes[2]
    for offset, key in [(-0.15, "william"), (0.15, "katharina")]:
        p = PARTICIPANTS[key]
        for i, (tag, level, _) in enumerate(selected):
            r = tags[(tags.participant == key) & (tags.tag == tag) & (tags.level == level)]
            if r.empty:
                continue
            r = r.iloc[0]
            y = len(selected) - i + offset
            ax.plot([0, r.error_change_pct], [y, y], color=MUTED, linewidth=0.6)
            ax.scatter(r.error_change_pct, y, marker=MARKER[p], s=13, color=INK if r.q_bh < 0.05 else "white",
                       edgecolors=INK, linewidths=0.7, zorder=3)
        ax.scatter([], [], marker=MARKER[p], s=13, color="white", edgecolors=INK, linewidths=0.7, label=p)
    ax.axvline(0, color=MUTED, linewidth=0.7)
    ax.set_yticks(range(len(selected), 0, -1), [s[2] for s in selected])
    ax.grid(axis="x", color="#e4e3df", linewidth=0.5)
    ax.grid(axis="y", visible=False)
    ax.set_xlabel("error change vs. median offset (%)")
    ax.legend(frameon=False, loc="lower left", handletextpad=0.2)
    ax.set_title("(c) scene subsets (20%)", loc="left", fontweight="bold")
    fig.savefig(OUT / "fig4_transfer.pdf")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    fig_driving()
    fig_controlled()
    fig_transfer()
