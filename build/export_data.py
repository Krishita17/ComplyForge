# -*- coding: utf-8 -*-
"""Export machine-readable copies of the assessment data.

    python build/export_data.py

Produces:
  data/controls_export.csv   – all 93 controls, one row each
  data/crosswalk.csv         – ISO 27001:2022 -> NIST 800-53 Rev.5 mapping
  data/risk_register.csv     – the risk register
  data/assessment_summary.json – headline stats + per-theme + gaps (drives the dashboard)
"""
import os
import csv
import json

import compute_stats as S
from controls_data import CONTROLS, SYSTEM, FRAMEWORK, ASSESSMENT_DATE, THEME_ORDER
from risk_data import RISKS, band

DATA = os.path.join(os.path.dirname(__file__), "..", "data")


def export_controls():
    path = os.path.join(DATA, "controls_export.csv")
    cols = ["id", "title", "theme", "status", "owner", "evidence", "gap",
            "remediation", "target", "risk", "nist", "desc"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for c in CONTROLS:
            w.writerow(c)
    print("wrote", os.path.relpath(path))


def export_crosswalk():
    path = os.path.join(DATA, "crosswalk.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["iso_27001_2022", "title", "theme", "nist_800_53_r5"])
        for c in CONTROLS:
            w.writerow([c["id"], c["title"], c["theme"], c["nist"]])
    print("wrote", os.path.relpath(path))


def export_risks():
    path = os.path.join(DATA, "risk_register.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "scenario", "asset", "threat", "vulnerability",
                    "linked_controls", "inherent_L", "inherent_I", "inherent_score",
                    "inherent_band", "residual_L", "residual_I", "residual_score",
                    "residual_band", "treatment", "owner", "status", "target"])
        for r in RISKS:
            inh = r["l_inh"] * r["i_inh"]; res = r["l_res"] * r["i_res"]
            w.writerow([r["id"], r["title"], r["asset"], r["threat"], r["vuln"],
                        " ".join(r["controls"]), r["l_inh"], r["i_inh"], inh,
                        band(inh), r["l_res"], r["i_res"], res, band(res),
                        r["treatment"], r["owner"], r["status"], r["target"]])
    print("wrote", os.path.relpath(path))


def export_summary_json():
    path = os.path.join(DATA, "assessment_summary.json")
    score, napp = S.compliance_score()
    counts = S.overall_counts()
    summary = {
        "system": SYSTEM,
        "framework": FRAMEWORK,
        "assessment_date": ASSESSMENT_DATE.isoformat(),
        "totals": {
            "controls": len(CONTROLS),
            "applicable": napp,
            "implemented": counts.get("Implemented", 0),
            "partial": counts.get("Partially Implemented", 0),
            "not_implemented": counts.get("Not Implemented", 0),
            "not_applicable": counts.get("Not Applicable", 0),
            "weighted_compliance_pct": round(score, 1),
            "implemented_rate_pct": round(S.implemented_rate(), 1),
            "open_gaps": len(S.gaps()),
        },
        "gaps_by_severity": dict(S.gaps_by_severity()),
        "by_theme": {t: {k: v for k, v in d.items()} for t, d in S.by_theme().items()},
        "theme_order": THEME_ORDER,
        "controls": [
            {"id": c["id"], "title": c["title"], "theme": c["theme"],
             "status": c["status"], "owner": c["owner"], "risk": c["risk"],
             "gap": c["gap"] if c["status"] in ("Partially Implemented",
                                                "Not Implemented") else "",
             "remediation": c["remediation"], "target": c["target"],
             "nist": c["nist"]}
            for c in CONTROLS
        ],
        "risks": [
            {"id": r["id"], "title": r["title"], "owner": r["owner"],
             "inherent": r["l_inh"] * r["i_inh"], "residual": r["l_res"] * r["i_res"],
             "inherent_band": band(r["l_inh"] * r["i_inh"]),
             "residual_band": band(r["l_res"] * r["i_res"]),
             "treatment": r["treatment"], "controls": r["controls"]}
            for r in RISKS
        ],
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print("wrote", os.path.relpath(path))


if __name__ == "__main__":
    export_controls()
    export_crosswalk()
    export_risks()
    export_summary_json()
