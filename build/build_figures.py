# -*- coding: utf-8 -*-
"""Generate all figures for the ComplyForge package into ../figures/.

    python build/build_figures.py
"""
import os
from datetime import date
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap

import compute_stats as S
from controls_data import (
    CONTROLS, THEME_ORDER, RISK_ORDER, IMPL, PART, NOIM, NA, SYSTEM,
)

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

# --- palette -----------------------------------------------------------------
INK = "#1F2933"
GRID = "#D8DEE6"
STATUS_COLOR = {IMPL: "#2E8B7A", PART: "#E0A200", NOIM: "#C0392B", NA: "#9AA0A6"}
SEV_COLOR = {"Critical": "#7B1E1E", "High": "#C0392B",
             "Medium": "#E0A200", "Low": "#3A7BD5"}
BRAND = "#1F5C8B"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "text.color": INK,
    "xtick.color": INK,
    "ytick.color": INK,
    "axes.titleweight": "bold",
    "figure.dpi": 140,
})


def _save(fig, name):
    path = os.path.join(FIG_DIR, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", os.path.relpath(path))


def _footer(fig):
    fig.text(0.01, 0.005,
             f"ComplyForge · {SYSTEM['product']} · ISO/IEC 27001:2022 Annex A · "
             f"assessment {SYSTEM['assessment_window']}",
             fontsize=7, color="#7A828C", ha="left")


# 1) Compliance by control family (headline) ---------------------------------
def fig_compliance_by_family():
    data = S.by_theme()
    themes = THEME_ORDER
    scores = [data[t]["score_pct"] for t in themes]
    overall, _ = S.compliance_score()

    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    bars = ax.bar(themes, scores, width=0.62, color=BRAND, edgecolor="white",
                  zorder=3)
    for b, s in zip(bars, scores):
        ax.text(b.get_x() + b.get_width() / 2, s + 1.5, f"{s:.0f}%",
                ha="center", va="bottom", fontweight="bold")
    ax.axhline(overall, color="#C0392B", ls="--", lw=1.4, zorder=4)
    ax.text(len(themes) - 0.45, overall + 1.5,
            f"overall {overall:.0f}%", color="#C0392B", fontweight="bold",
            ha="right", fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Weighted implementation score")
    ax.set_title("Compliance by control theme  (ISO/IEC 27001:2022 Annex A)")
    ax.yaxis.grid(True, color=GRID, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    # subtitle counts
    labels = [f"{data[t]['applicable']} applicable" for t in themes]
    ax.set_xticks(range(len(themes)))
    ax.set_xticklabels([f"{t}\n({l})" for t, l in zip(themes, labels)])
    _footer(fig)
    _save(fig, "01_compliance_by_family.png")


# 2) Status breakdown donut ---------------------------------------------------
def fig_status_donut():
    counts = S.overall_counts()
    order = [IMPL, PART, NOIM, NA]
    vals = [counts.get(s, 0) for s in order]
    colors = [STATUS_COLOR[s] for s in order]

    fig, ax = plt.subplots(figsize=(6.8, 5.2))
    wedges, _ = ax.pie(vals, colors=colors, startangle=90,
                       wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2))
    total = sum(vals)
    ax.text(0, 0.12, f"{total}", ha="center", va="center",
            fontsize=30, fontweight="bold")
    ax.text(0, -0.16, "Annex A controls", ha="center", va="center",
            fontsize=10, color="#5A626C")
    labels = [f"{s}  —  {v}  ({100*v/total:.0f}%)" for s, v in zip(order, vals)]
    ax.legend(wedges, labels, loc="center", bbox_to_anchor=(0.5, -0.06),
              frameon=False, ncol=2, fontsize=9, handlelength=1.1)
    ax.set_title("Implementation status across all controls", pad=14)
    _footer(fig)
    _save(fig, "02_status_breakdown.png")


# 3) Gap-severity heatmap (theme x severity) ---------------------------------
def fig_gap_heatmap():
    grid = S.severity_by_theme()
    themes = THEME_ORDER
    sevs = RISK_ORDER  # Critical, High, Medium, Low
    matrix = [[grid[t][s] for s in sevs] for t in themes]

    cmap = LinearSegmentedColormap.from_list(
        "cf", ["#FBFCFD", "#F3C9C3", "#D65C4E", "#7B1E1E"])
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    vmax = max(max(r) for r in matrix) or 1
    im = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    ax.set_xticks(range(len(sevs)))
    ax.set_xticklabels(sevs)
    ax.set_yticks(range(len(themes)))
    ax.set_yticklabels(themes)
    for i in range(len(themes)):
        for j in range(len(sevs)):
            v = matrix[i][j]
            ax.text(j, i, str(v), ha="center", va="center",
                    color="white" if v > vmax * 0.55 else INK,
                    fontweight="bold")
    ax.set_title("Open gaps — count by control theme × risk severity")
    ax.set_xticks([x - 0.5 for x in range(1, len(sevs))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(themes))], minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)
    cbar = fig.colorbar(im, ax=ax, shrink=0.8)
    cbar.set_label("number of gaps", fontsize=9)
    _footer(fig)
    _save(fig, "03_gap_severity_heatmap.png")


# 4) Remediation roadmap timeline --------------------------------------------
_MONTHS = {
    "Nov 2026": date(2026, 11, 15), "Dec 2026": date(2026, 12, 15),
    "Jan 2027": date(2027, 1, 15), "Feb 2027": date(2027, 2, 15),
    "Mar 2027": date(2027, 3, 15), "Apr 2027": date(2027, 4, 15),
    "May 2027": date(2027, 5, 15),
}


def fig_roadmap():
    g = S.ranked_gaps()
    # order rows by target date then severity
    sev_rank = {r: i for i, r in enumerate(RISK_ORDER)}
    rows = sorted(g, key=lambda c: (_MONTHS[c["target"]], sev_rank[c["risk"]]))
    y = list(range(len(rows)))
    start = date(2026, 8, 30)

    fig, ax = plt.subplots(figsize=(10.5, 9.5))
    for i, c in enumerate(rows):
        end = _MONTHS[c["target"]]
        ax.barh(i, (end - start).days, left=mdates.date2num(start),
                height=0.55, color=SEV_COLOR[c["risk"]], edgecolor="white",
                zorder=3)
        ax.text(mdates.date2num(end) + 3, i,
                f"{c['id']}", va="center", fontsize=7.5, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{c['id']}  {c['title'][:34]}" for c in rows], fontsize=7.6)
    ax.invert_yaxis()
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
    ax.set_xlim(mdates.date2num(start), mdates.date2num(date(2027, 5, 31)))

    # certification milestones
    for d, lbl in [(date(2027, 1, 15), "Stage 1 audit"),
                   (date(2027, 3, 15), "Stage 2 audit")]:
        ax.axvline(mdates.date2num(d), color=BRAND, ls="--", lw=1.3, zorder=5)
        ax.text(mdates.date2num(d), -1.2, lbl, color=BRAND, fontsize=8,
                ha="center", fontweight="bold")
    ax.set_title("Remediation roadmap — gap closure target dates vs certification "
                 "milestones", pad=26)
    ax.xaxis.grid(True, color=GRID, zorder=0)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    legend = [Patch(facecolor=SEV_COLOR[r], label=r) for r in RISK_ORDER]
    ax.legend(handles=legend, title="Gap severity", loc="lower right",
              frameon=True, fontsize=8.5)
    _footer(fig)
    _save(fig, "04_remediation_roadmap.png")


# 5) Overall readiness gauge --------------------------------------------------
def fig_readiness_gauge():
    score, _ = S.compliance_score()
    fig, ax = plt.subplots(figsize=(6.4, 3.7), subplot_kw={"aspect": "equal"})
    import numpy as np
    # semicircle gauge
    theta = np.linspace(np.pi, 0, 100)
    ax.plot(np.cos(theta), np.sin(theta), color=GRID, lw=16, solid_capstyle="round")
    filled = np.linspace(np.pi, np.pi - np.pi * score / 100, 100)
    color = "#2E8B7A" if score >= 75 else ("#E0A200" if score >= 50 else "#C0392B")
    ax.plot(np.cos(filled), np.sin(filled), color=color, lw=16,
            solid_capstyle="round")
    ax.text(0, 0.12, f"{score:.0f}%", ha="center", fontsize=34, fontweight="bold")
    ax.text(0, -0.16, "weighted ISMS readiness", ha="center", fontsize=10,
            color="#5A626C")
    ax.text(-1, -0.12, "0%", ha="center", fontsize=8, color="#7A828C")
    ax.text(1, -0.12, "100%", ha="center", fontsize=8, color="#7A828C")
    ax.set_xlim(-1.25, 1.25)
    ax.set_ylim(-0.35, 1.2)
    ax.axis("off")
    ax.set_title("Overall audit readiness", pad=2)
    _footer(fig)
    _save(fig, "05_readiness_gauge.png")


if __name__ == "__main__":
    fig_compliance_by_family()
    fig_status_donut()
    fig_gap_heatmap()
    fig_roadmap()
    fig_readiness_gauge()
    print("All figures generated.")
