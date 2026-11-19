# -*- coding: utf-8 -*-
"""Generate reports/poam.xlsx — Plan of Action & Milestones (POA&M).

    python build/build_poam.py

A POA&M is the NIST/FedRAMP artifact that tracks each identified weakness to closure:
the weakness, source, risk, remediation, resources, milestones, and status. Here it is
derived directly from the open gaps in the control assessment so the two never diverge.
"""
import os
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

import compute_stats as S
from controls_data import SYSTEM, ASSESSMENT_DATE

OUT = os.path.join(os.path.dirname(__file__), "..", "reports", "poam.xlsx")

NAVY = "1F5C8B"; NAVY_D = "163F5F"; WHITE = "FFFFFF"
thin = Side(style="thin", color="D8DEE6")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
HDR_FONT = Font(bold=True, color=WHITE, size=11)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
RISK_FILL = {"Critical": "7B1E1E", "High": "C0392B", "Medium": "E0A200", "Low": "3A7BD5"}
RISK_FONT = {"Critical": "FFFFFF", "High": "FFFFFF", "Medium": "3A2E00", "Low": "FFFFFF"}
STATUS_FILL = {"Open": "F4C7C3", "In Progress": "FCE8B8", "Planned": "E2E5E9"}
STATUS_FONT = {"Open": "9B2C22", "In Progress": "8A6100", "Planned": "5A626C"}

# Milestones per severity (illustrative, derived from target dates)
MILESTONES = {
    "Critical": "M1 Purge & block (wk 2) · M2 Masked data live (wk 4) · M3 Validate (wk 6)",
    "High": "M1 Design (wk 2) · M2 Implement (wk 5) · M3 Verify & evidence (wk 8)",
    "Medium": "M1 Plan (wk 3) · M2 Implement (wk 7) · M3 Evidence (wk 10)",
    "Low": "M1 Plan (wk 4) · M2 Implement (wk 9) · M3 Close (wk 12)",
}
RESOURCES = {
    "Critical": "Eng + Security (high priority, exec-sponsored)",
    "High": "Owning team + Security review",
    "Medium": "Owning team (scheduled)",
    "Low": "Owning team (BAU backlog)",
}


def _status(control):
    if control["risk"] in ("Critical", "High"):
        return "In Progress"
    if control["risk"] == "Medium":
        return "Planned"
    return "Planned"


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    wb = Workbook(); ws = wb.active; ws.title = "POA&M"
    ws.sheet_view.showGridLines = False
    headers = ["POA&M ID", "Weakness / Deficiency", "Control ID", "Control Title",
               "Source", "Risk Rating", "Remediation / Corrective Action",
               "Resources Required", "Milestones", "Point of Contact",
               "Original Detection", "Scheduled Completion", "Status"]
    ws.merge_cells("A1:M1")
    ws.cell(1, 1, "ComplyForge — Plan of Action & Milestones (POA&M)").font = \
        Font(bold=True, color=NAVY_D, size=18)
    ws.merge_cells("A2:M2")
    ws.cell(2, 1, f"{SYSTEM['product']} · {len(S.gaps())} open weaknesses tracked to "
            f"closure · NIST/FedRAMP-style").font = Font(color="5A626C", size=11)
    hr = 4
    for i, h in enumerate(headers, 1):
        c = ws.cell(hr, i, h); c.fill = HDR_FILL; c.font = HDR_FONT
        c.alignment = CENTER; c.border = BORDER
    ws.row_dimensions[hr].height = 30

    r = hr + 1
    for n, c in enumerate(S.ranked_gaps(), 1):
        st = _status(c)
        vals = [f"POAM-{n:03d}", c["gap"], c["id"], c["title"],
                "Internal readiness assessment (Q3 2026)", c["risk"],
                c["remediation"], RESOURCES[c["risk"]], MILESTONES[c["risk"]],
                c["owner"], ASSESSMENT_DATE.strftime("%d %b %Y"), c["target"], st]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v); cell.border = BORDER; cell.alignment = WRAP
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D); ws.cell(r, 1).alignment = CENTER
        ws.cell(r, 3).font = Font(bold=True, color=NAVY_D); ws.cell(r, 3).alignment = CENTER
        rc = ws.cell(r, 6); rc.fill = PatternFill("solid", fgColor=RISK_FILL[c["risk"]])
        rc.font = Font(bold=True, color=RISK_FONT[c["risk"]]); rc.alignment = CENTER
        sc = ws.cell(r, 13); sc.fill = PatternFill("solid", fgColor=STATUS_FILL[st])
        sc.font = Font(bold=True, color=STATUS_FONT[st]); sc.alignment = CENTER
        ws.cell(r, 12).alignment = CENTER
        r += 1
    widths = [10, 46, 10, 26, 24, 11, 48, 26, 40, 22, 14, 14, 13]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hr}:{get_column_letter(len(headers))}{r-1}"
    ws.freeze_panes = f"C{hr+1}"
    dv = DataValidation(type="list",
        formula1='"Open,Planned,In Progress,Completed,Risk Accepted"', allow_blank=True)
    ws.add_data_validation(dv); dv.add(f"M{hr+1}:M{r-1}")
    wb.save(OUT)
    print("wrote", os.path.relpath(OUT), "|", r - hr - 1, "POA&M items")


if __name__ == "__main__":
    main()
