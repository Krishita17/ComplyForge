# -*- coding: utf-8 -*-
"""Compute assessment statistics from the master dataset.

Run directly to print the headline numbers used in the report and README:
    python build/compute_stats.py
"""
from collections import defaultdict, Counter
from controls_data import (
    CONTROLS, THEME_ORDER, STATUS_ORDER, RISK_ORDER,
    IMPL, PART, NOIM, NA,
)

# Weighted scoring: Implemented = 1.0, Partial = 0.5, Not Implemented = 0.
WEIGHT = {IMPL: 1.0, PART: 0.5, NOIM: 0.0}


def overall_counts():
    return Counter(c["status"] for c in CONTROLS)


def applicable_controls():
    return [c for c in CONTROLS if c["status"] != NA]


def compliance_score():
    """Weighted implementation score over applicable controls (%)."""
    app = applicable_controls()
    score = sum(WEIGHT[c["status"]] for c in app)
    return 100.0 * score / len(app), len(app)


def implemented_rate():
    """Fully-implemented over applicable controls (%)."""
    app = applicable_controls()
    impl = sum(1 for c in app if c["status"] == IMPL)
    return 100.0 * impl / len(app)


def by_theme():
    """Return dict theme -> {status: count, ..., 'applicable': n, 'score_pct': x}."""
    out = {}
    for theme in THEME_ORDER:
        rows = [c for c in CONTROLS if c["theme"] == theme]
        counts = Counter(c["status"] for c in rows)
        app = [c for c in rows if c["status"] != NA]
        score = sum(WEIGHT[c["status"]] for c in app)
        out[theme] = {
            "total": len(rows),
            IMPL: counts.get(IMPL, 0),
            PART: counts.get(PART, 0),
            NOIM: counts.get(NOIM, 0),
            NA: counts.get(NA, 0),
            "applicable": len(app),
            "score_pct": (100.0 * score / len(app)) if app else 0.0,
        }
    return out


def gaps():
    """All controls with an open gap (Partial or Not Implemented)."""
    return [c for c in CONTROLS if c["status"] in (PART, NOIM)]


def gaps_by_severity():
    return Counter(c["risk"] for c in gaps())


def severity_by_theme():
    """theme -> {risk: count} for the heatmap."""
    grid = {t: {r: 0 for r in RISK_ORDER} for t in THEME_ORDER}
    for c in gaps():
        if c["risk"] in RISK_ORDER:
            grid[c["theme"]][c["risk"]] += 1
    return grid


def ranked_gaps():
    """Gaps sorted by severity (Critical first) then control id."""
    order = {r: i for i, r in enumerate(RISK_ORDER)}
    return sorted(gaps(), key=lambda c: (order.get(c["risk"], 99), c["id"]))


if __name__ == "__main__":
    counts = overall_counts()
    score, napp = compliance_score()
    print("=" * 60)
    print("ComplyForge — Sightline ISO 27001:2022 readiness snapshot")
    print("=" * 60)
    print(f"Total Annex A controls           : {len(CONTROLS)}")
    print(f"Applicable                       : {napp}")
    print(f"Not Applicable                   : {counts.get(NA,0)}")
    print(f"Implemented                      : {counts.get(IMPL,0)}")
    print(f"Partially Implemented            : {counts.get(PART,0)}")
    print(f"Not Implemented                  : {counts.get(NOIM,0)}")
    print(f"Implemented rate (of applicable) : {implemented_rate():.1f}%")
    print(f"Weighted compliance score        : {score:.1f}%")
    print("-" * 60)
    print("By theme (weighted score %):")
    for t, d in by_theme().items():
        print(f"  {t:<16} {d['score_pct']:5.1f}%  "
              f"(I{d[IMPL]} P{d[PART]} N{d[NOIM]} NA{d[NA]}  n={d['total']})")
    print("-" * 60)
    print("Open gaps by severity:")
    for r in RISK_ORDER:
        print(f"  {r:<9}: {gaps_by_severity().get(r,0)}")
    print(f"  TOTAL open gaps: {len(gaps())}")
