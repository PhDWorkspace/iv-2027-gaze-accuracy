"""One full-width figure on the controlled screen fixations (raw gaze, no offset correction):
(a) per-wearer angular error at 1 m: median with IQR handles over fixations (all 11 wearers)
(b, c) change from 1 m to 4 m in vertical bias and angular error (all 9 wearers with both distances)

Reads gaze_accuracy/factors/controlled/1_distance/fixations.csv (central_60, status ok). Unit for (b, c): one value per
recording (median over its fixations); per wearer and distance the median over recordings; 1 m recordings are kept only
from days that also have 4 m recordings, unless the wearer has no such day (then all; see same_day in the CSV).

Usage: python scripts/make_fig_distance_baseline.py --format ieee --column --out <dir>  (paper Fig. 3; copy of /home/william/data/illustration/distance_baseline/plot.py)
Usage: python plot.py [--data-root /home/william/data] [--out .] [--exclude P5] [--format ieee|springer] [--left error|offset] [--color] [--column]
"""
import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator

# Pseudonyms of the manuscript (scripts/make_section5.py)
PARTICIPANTS = {"William": "P1", "Katharina Winter": "P2", "Kanak Mazumder": "P3", "Max Buettner": "P4",
                "Mohan Ramesh": "P5", "Stefan Englmeier": "P6", "Sarah Joy": "P7", "Constantin Selzer": "P8",
                "Marilu Flores Turon Ramirez": "P9", "Sofia Elizabeth Moreno Reynaga": "P10",
                "Isabel Oliveira Trindade": "P11"}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
BLUE = "#2f6aa3"
# --color: one colour + marker per wearer. Hues = the eight validated categorical slots (dataviz palette); a scatter only
# separates three hues for colour-blind readers, so each wearer also gets a unique marker (P1-P6 = paper markers), and
# repeated hues (P9-P11) go to wearers far from their hue twin in panel (a).
HUES = dict(blue="#2a78d6", orange="#eb6834", aqua="#1baf7a", yellow="#eda100", magenta="#e87ba4", green="#008300",
            violet="#6250d6", red="#e34948")
WEARER_STYLE = {"P1": ("blue", "o"), "P2": ("orange", "s"), "P3": ("aqua", "^"), "P4": ("yellow", "v"),
                "P5": ("magenta", "D"), "P6": ("green", "P"), "P7": ("violet", "X"), "P8": ("red", "*"),
                "P9": ("green", "h"), "P10": ("yellow", "<"), "P11": ("violet", ">")}


def color(code, per_wearer):
    return HUES[WEARER_STYLE[code][0]] if per_wearer else BLUE


def marker(code, per_wearer):
    return WEARER_STYLE[code][1] if per_wearer else "o"


def marker_size(code, size, per_wearer=True):
    return size * 1.45 if per_wearer and WEARER_STYLE[code][1] == "*" else size  # the star reads small at equal size
ERROR, AZIMUTH, ELEVATION = "angular_error_median_deg", "bias_azimuth_deg", "bias_elevation_deg"
# Label positions (data coordinates, with a leader line) for wearers whose centres crowd; others sit right of the dot
LABEL_AT = {"P4": (2.3, 1.1), "P9": (2.3, 0.4), "P2": (2.3, -0.3), "P5": (-2.3, 0.6), "P8": (-2.3, -0.8),
            "P11": (-2.0, -1.9), "P3": (2.3, -1.3), "P10": (-2.6, -4.0), "P6": (2.3, -4.0)}


# Page formats: IEEE two-column (serif, 7 pt) and Springer double column (174 mm, sans serif Helvetica clone, 8 pt)
FORMATS = {
    "ieee": dict(width=7.16, height=2.1, family="serif", font="Nimbus Roman", files="NimbusRoman-*.otf", size=7,
                 tick=6.5, panel="({}) {}", suffix="", column_width=3.5, column_height=3.4),
    "springer": dict(width=174 / 25.4, height=2.35, family="sans-serif", font="Nimbus Sans", files="NimbusSans-*.otf",
                     size=8, tick=7.5, panel="{}   {}", suffix="_springer", column_width=84 / 25.4,
                     column_height=3.6),
}


def apply_style(fmt):
    for f in Path("/usr/share/fonts").rglob(fmt["files"]):
        font_manager.fontManager.addfont(str(f))
    plt.rcParams.update({
        "font.family": fmt["family"], f"font.{fmt['family']}": [fmt["font"], "Arial", "DejaVu Sans" if fmt["family"] == "sans-serif" else "DejaVu Serif"],
        "mathtext.fontset": "stix" if fmt["family"] == "serif" else "stixsans", "font.size": fmt["size"],
        "axes.titlesize": fmt["size"], "axes.labelsize": fmt["size"], "xtick.labelsize": fmt["tick"],
        "ytick.labelsize": fmt["tick"], "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": MUTED, "axes.linewidth": 0.6, "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.grid": True, "axes.grid.axis": "x", "axes.axisbelow": True, "grid.color": GRID, "grid.linewidth": 0.5,
        "pdf.fonttype": 42,
    })


def load(root):
    fix = pd.read_csv(root / "gaze_accuracy/factors/controlled/1_distance/fixations.csv", low_memory=False)
    assert fix.status.eq("ok").all() and fix.selection_method.eq("central_60").all()
    fix["code"] = fix.participant.map(PARTICIPANTS)
    assert fix.code.notna().all(), f"no pseudonym for {set(fix.participant[fix.code.isna()])}"
    return fix


def baseline(fix):
    """Per wearer at 1 m: median and IQR of the fixation errors; recordings and days as context."""
    base = fix[fix.experiment_distance_m.eq(1.0)]
    stats = base.groupby("code").agg(median=(ERROR, "median"), q25=(ERROR, lambda v: v.quantile(.25)),
                                     q75=(ERROR, lambda v: v.quantile(.75)), fixations=(ERROR, "size"),
                                     recordings=("recording_name", "nunique"), days=("date", "nunique"))
    return stats.sort_values("median")


def baseline_offset(fix):
    """Per wearer at 1 m: median and IQR of the fixation biases, separately for azimuth and elevation."""
    base = fix[fix.experiment_distance_m.eq(1.0)]
    out = base.groupby("code").agg(fixations=(AZIMUTH, "size"))
    for name, column in (("azimuth", AZIMUTH), ("elevation", ELEVATION)):
        out[name] = base.groupby("code")[column].median()
        out[f"{name}_q25"], out[f"{name}_q75"] = (base.groupby("code")[column].quantile(q) for q in (.25, .75))
    return out


def distance_change(fix):
    """Per wearer with 1 m and 4 m: median over recordings at 4 m minus at 1 m (same-day 1 m where available)."""
    rec = (fix[fix.experiment_distance_m.isin([1.0, 4.0])]
           .groupby(["code", "recording_name", "date", "experiment_distance_m"])[[ERROR, ELEVATION]].median().reset_index())
    rows = []
    for code, r in rec.groupby("code"):
        far = r[r.experiment_distance_m.eq(4.0)]
        near = r[r.experiment_distance_m.eq(1.0)]
        if far.empty or near.empty:
            continue
        same_day = near[near.date.isin(far.date)]
        rows.append(dict(code=code, same_day=not same_day.empty, recordings_1m=len(same_day if len(same_day) else near),
                         recordings_4m=len(far), days_1m="/".join(sorted((same_day if len(same_day) else near).date.unique())),
                         days_4m="/".join(sorted(far.date.unique())),
                         **{f"{m}_{d}": v for m in (ERROR, ELEVATION) for d, v in
                            (("1m", (same_day if len(same_day) else near)[m].median()), ("4m", far[m].median()))}))
    out = pd.DataFrame(rows).set_index("code")
    for m in (ERROR, ELEVATION):
        out[f"{m}_change"] = out[f"{m}_4m"] - out[f"{m}_1m"]
    return out


def draw_baseline(ax, stats, panel, per_wearer=False):
    y = np.arange(len(stats))
    for i, (code, r) in enumerate(stats.iterrows()):
        ax.errorbar(r["median"], i, xerr=[[r["median"] - r.q25], [r.q75 - r["median"]]], fmt=marker(code, per_wearer),
                    color=color(code, per_wearer), markersize=marker_size(code, 3.5, per_wearer), elinewidth=0.9, capsize=2.2,
                    capthick=0.9)
    ax.set_yticks(y, stats.index)
    ax.set_ylim(len(stats) - 0.5, -0.5)
    ax.set_xlim(0, None)
    ax.set_xlabel("angular error at 1 m (°)")
    ax.set_title(panel.format("a", "Baseline error"), loc="left", fontweight="bold")


def draw_offset(ax, offset, panel, per_wearer=False):
    """Median per wearer with an IQR cross (azimuth horizontal, elevation vertical), equal axis scale."""
    ax.axhline(0, color=MUTED, lw=0.6, ls=(0, (3, 2)), zorder=1)
    ax.axvline(0, color=MUTED, lw=0.6, ls=(0, (3, 2)), zorder=1)
    for code, r in offset.iterrows():
        c = color(code, per_wearer)
        ax.errorbar(r.azimuth, r.elevation, fmt="none", ecolor=c, elinewidth=1.0 if per_wearer else 0.9,
                    alpha=0.55 if per_wearer else 0.45, capsize=0, zorder=2,
                    xerr=[[r.azimuth - r.azimuth_q25], [r.azimuth_q75 - r.azimuth]],
                    yerr=[[r.elevation - r.elevation_q25], [r.elevation_q75 - r.elevation]])
        ax.plot(r.azimuth, r.elevation, marker(code, per_wearer), color=c, markersize=marker_size(code, 3.8) if per_wearer else 2.8,
                markeredgecolor="white", markeredgewidth=0.4 if per_wearer else 0, zorder=3)
    size = plt.rcParams["xtick.labelsize"] - 0.5
    for code, r in offset.iterrows():
        if per_wearer:  # the legend identifies wearers
            continue
        if code in LABEL_AT:
            x, y = LABEL_AT[code]
            ax.annotate(code, (r.azimuth, r.elevation), xytext=(x, y), fontsize=size, va="center",
                        ha="left" if x > r.azimuth else "right", zorder=5,
                        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.4, shrinkA=1, shrinkB=1.5))
        else:
            ax.annotate(code, (r.azimuth, r.elevation), xytext=(4, 3), textcoords="offset points", fontsize=size,
                        va="bottom", zorder=5)
    ax.set_aspect("equal", adjustable="datalim")
    ax.xaxis.set_major_locator(MultipleLocator(2))
    ax.yaxis.set_major_locator(MultipleLocator(2))
    ax.grid(False)
    ax.set_xlabel("azimuth bias (°, + right)")
    ax.set_ylabel("elevation bias (°, + up)")
    ax.set_title(panel.format("a", "Gaze offset at 1 m"), loc="left", fontweight="bold")


def draw_change(axes, change, panel, per_wearer=False):
    """(b) vertical bias and (c) angular error change, wearers sorted by the vertical-bias change."""
    change = change.sort_values(f"{ELEVATION}_change")
    y = np.arange(len(change))
    for ax, metric, title in ((axes[0], ELEVATION, panel.format("b", "Vertical bias")), (axes[1], ERROR, panel.format("c", "Angular error"))):
        ax.barh(y, change[f"{metric}_change"], height=0.62, color=[color(c, per_wearer) for c in change.index])
        ax.axvline(0, color=MUTED, lw=0.6)
        ax.set_title(title, loc="left", fontweight="bold")
        ax.set_xlabel("change 1 → 4 m (°)")
        lim = np.abs(change[f"{metric}_change"]).max() * 1.15
        ax.set_xlim(-lim, lim)
    axes[0].set_yticks(y, change.index)
    axes[0].set_ylim(len(change) - 0.5, -0.5)


def plot(left, change, out, name, fmt, per_wearer=False, column=False):
    """left: baseline error table (1D handles) or baseline offset table (2D crosses); per_wearer: colours + legend;
    column: single-column layout, (a) on top and (b, c) below."""
    ellipses = "azimuth" in left
    height = (fmt["column_height"] if column else fmt["height"]) + (0.3 if per_wearer else 0)  # room for the legend
    if column:
        fig = plt.figure(figsize=(fmt["column_width"], height), layout="constrained")
        grid = fig.add_gridspec(2, 2, height_ratios=[1.15, 1])
        axes = [fig.add_subplot(grid[0, :]), fig.add_subplot(grid[1, 0]), fig.add_subplot(grid[1, 1])]
    else:
        fig, axes = plt.subplots(1, 3, figsize=(fmt["width"], height), layout="constrained",
                                 gridspec_kw=dict(width_ratios=[0.55 if ellipses else 1, 0.9, 0.9]))
    (draw_offset if ellipses else draw_baseline)(axes[0], left, fmt["panel"], per_wearer)
    axes[2].sharey(axes[1])
    axes[2].tick_params(axis="y", labelleft=False)
    draw_change(axes[1:], change, fmt["panel"], per_wearer)
    for ax in axes[0 if not ellipses else 1:]:
        ax.tick_params(axis="y", length=0)
    if per_wearer:
        codes = sorted(set(left.index) | set(change.index), key=lambda c: int(c[1:]))
        handles = [Line2D([], [], marker=marker(c, True), color=color(c, True), linestyle="", markersize=marker_size(c, 4.2),
                          markeredgecolor="white", markeredgewidth=0.4, label=c) for c in codes]
        fig.legend(handles=handles, ncol=len(handles) if not column else 6, loc="outside lower center", frameon=False, handletextpad=0.1,
                   columnspacing=1.0)
    return save(fig, out, name)


def save(fig, out, name):
    fig.savefig(out / f"{name}.pdf")
    fig.savefig(out / f"{name}.png", dpi=300)
    plt.close(fig)
    return out / f"{name}.pdf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", type=Path, default=Path("/home/william/data"))
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--exclude", nargs="*", default=[], help="pseudonyms to drop from every panel, e.g. P5")
    ap.add_argument("--format", choices=FORMATS, default="ieee")
    ap.add_argument("--left", choices=["error", "offset"], default="error",
                    help="panel a: 1 m angular error with IQR handles, or azimuth/elevation bias with IQR crosses")
    ap.add_argument("--color", action="store_true", help="one colour + marker per wearer, shared legend")
    ap.add_argument("--column", action="store_true", help="single-column layout: (a) on top, (b, c) below")
    args = ap.parse_args()
    fmt = FORMATS[args.format]
    apply_style(fmt)
    fix = load(args.data_root)
    fix = fix[~fix.code.isin(args.exclude)]
    suffix = "".join(f"_without_{code}" for code in args.exclude)
    stats, change = (baseline_offset if args.left == "offset" else baseline)(fix), distance_change(fix)
    stats.to_csv(args.out / f"baseline_{args.left}{suffix}.csv", float_format="%.4f")
    change.to_csv(args.out / f"distance_change{suffix}.csv", float_format="%.4f")
    left = "_offset" if args.left == "offset" else ""
    name = f"figure{left}{'_color' if args.color else ''}{suffix}{'_column' if args.column else ''}{fmt['suffix']}"
    print(plot(stats, change, args.out, name, fmt, args.color, args.column))
    print(stats.round(2).to_string(), change.filter(regex="change|same_day|recordings").round(2).to_string(), sep="\n\n")


if __name__ == "__main__":
    main()
