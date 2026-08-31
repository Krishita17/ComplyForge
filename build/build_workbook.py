# -*- coding: utf-8 -*-
"""Generate control_assessment_workbook.xlsx (the centerpiece).

    python build/build_workbook.py

Tabs:
  0. Read Me            – how to use the workbook, scope, legend
  1. Control Assessment – all 93 Annex A controls, fully assessed (filterable)
  2. Statement of Applicability – applicability decision + justification per control
  3. Summary by Family – counts + weighted score per theme, with charts
  4. Gap Register      – open gaps only, ranked by severity, with remediation
  5. ISO 27001 to NIST 800-53 crosswalk
"""
import os
from openpyxl import Workbook
from openpyxl.styles import (
    Font, PatternFill, Alignment, Border, Side, NamedStyle,
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList

import compute_stats as S
from controls_data import (
    CONTROLS, SYSTEM, FRAMEWORK, FRAMEWORK_SECONDARY, ASSESSMENT_DATE,
    THEME_ORDER, STATUS_ORDER, RISK_ORDER, IMPL, PART, NOIM, NA,
)

OUT = os.path.join(os.path.dirname(__file__), "..", "control_assessment_workbook.xlsx")

# --- palette -----------------------------------------------------------------
NAVY = "1F5C8B"
NAVY_D = "163F5F"
INK = "1F2933"
LIGHT = "EEF3F8"
WHITE = "FFFFFF"
STATUS_FILL = {
    IMPL: "C6E7DD", PART: "FCE8B8", NOIM: "F4C7C3", NA: "E2E5E9",
}
STATUS_FONT = {
    IMPL: "1E6B58", PART: "8A6100", NOIM: "9B2C22", NA: "5A626C",
}
RISK_FILL = {
    "Critical": "7B1E1E", "High": "C0392B", "Medium": "E0A200",
    "Low": "3A7BD5", "None": "FFFFFF", "N/A": "E2E5E9",
}
RISK_FONT = {
    "Critical": "FFFFFF", "High": "FFFFFF", "Medium": "3A2E00",
    "Low": "FFFFFF", "None": "1F2933", "N/A": "5A626C",
}

thin = Side(style="thin", color="D8DEE6")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
HDR_FONT = Font(name="Calibri", bold=True, color=WHITE, size=11)
TITLE_FONT = Font(name="Calibri", bold=True, color=NAVY_D, size=18)
SUB_FONT = Font(name="Calibri", color="5A626C", size=11)
WRAP_TOP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)


def style_header_row(ws, row, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=row, column=c)
        cell.fill = HDR_FILL
        cell.font = HDR_FONT
        cell.alignment = Alignment(horizontal="center", vertical="center",
                                   wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[row].height = 30


def banner(ws, title, subtitle, span):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    ws.cell(1, 1, title).font = TITLE_FONT
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    ws.cell(2, 1, subtitle).font = SUB_FONT
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 18


# =============================================================================
def sheet_readme(wb):
    ws = wb.active
    ws.title = "Read Me"
    ws.sheet_view.showGridLines = False
    banner(ws, "ComplyForge — Control Assessment Workbook",
           f"{SYSTEM['company']} · {SYSTEM['product']} · {FRAMEWORK}", 2)
    score, napp = S.compliance_score()
    rows = [
        ("", ""),
        ("System", f"{SYSTEM['product']} — {SYSTEM['tagline']}"),
        ("Operated by", SYSTEM["company"]),
        ("Environment", SYSTEM["environment"]),
        ("Primary framework", FRAMEWORK),
        ("Secondary reference", FRAMEWORK_SECONDARY),
        ("Assessment window", SYSTEM["assessment_window"]),
        ("Assessment date", ASSESSMENT_DATE.strftime("%d %b %Y")),
        ("Assessor", SYSTEM["assessor"]),
        ("Certification goal", SYSTEM["certification_goal"]),
        ("", ""),
        ("HEADLINE RESULTS", ""),
        ("Total Annex A controls", str(len(CONTROLS))),
        ("Applicable controls", str(napp)),
        ("Not applicable", str(S.overall_counts().get(NA, 0))),
        ("Implemented", str(S.overall_counts().get(IMPL, 0))),
        ("Partially implemented", str(S.overall_counts().get(PART, 0))),
        ("Not implemented", str(S.overall_counts().get(NOIM, 0))),
        ("Weighted compliance score", f"{score:.1f}%  (Implemented=1, Partial=0.5)"),
        ("Open gaps", f"{len(S.gaps())}  "
         f"(Critical {S.gaps_by_severity().get('Critical',0)}, "
         f"High {S.gaps_by_severity().get('High',0)}, "
         f"Medium {S.gaps_by_severity().get('Medium',0)}, "
         f"Low {S.gaps_by_severity().get('Low',0)})"),
        ("", ""),
        ("HOW TO USE THIS WORKBOOK", ""),
        ("Control Assessment", "The full register — every Annex A control with "
         "status, owner, evidence, gap, remediation and risk. Use the filter."),
        ("Statement of Applicability", "The formal SoA: applicability decision and "
         "justification for each control (required for certification)."),
        ("Summary by Family", "Counts and weighted score per control theme, with "
         "charts."),
        ("Gap Register", "Open gaps only, ranked by risk severity, with owners and "
         "target dates — the remediation worklist."),
        ("ISO to NIST Crosswalk", "Mapping of each Annex A control to primary NIST "
         "SP 800-53 Rev. 5 controls."),
        ("", ""),
        ("LEGEND — Status", "Implemented / Partially Implemented / Not Implemented "
         "/ Not Applicable"),
        ("LEGEND — Risk", "Critical / High / Medium / Low (severity of the residual "
         "gap)"),
        ("", ""),
        ("Note on data", "The control framework (IDs & titles) is real; all "
         "implementation statuses, evidence, owners, gaps and remediations are "
         "synthetic and describe a fictional company. Standard text is paraphrased, "
         "not reproduced. See docs/methodology.md."),
    ]
    r = 4
    for k, v in rows:
        kc = ws.cell(r, 1, k)
        vc = ws.cell(r, 2, v)
        vc.alignment = WRAP_TOP
        if k in ("HEADLINE RESULTS", "HOW TO USE THIS WORKBOOK") or k.startswith("LEGEND"):
            kc.font = Font(bold=True, color=NAVY_D, size=12)
        elif k == "System" or k == "Note on data":
            kc.font = Font(bold=True, color=INK)
        else:
            kc.font = Font(bold=True, color=INK)
        r += 1
    ws.column_dimensions["A"].width = 26
    ws.column_dimensions["B"].width = 96
    ws.freeze_panes = "A4"


# =============================================================================
def sheet_assessment(wb):
    ws = wb.create_sheet("Control Assessment")
    ws.sheet_view.showGridLines = False
    headers = ["Control ID", "Control Title", "Theme", "Control Objective (paraphrased)",
               "Status", "Control Owner", "Evidence / Artifact",
               "Gap / N-A Rationale", "Remediation Action", "Target Date",
               "Risk Rating", "NIST SP 800-53 Rev.5"]
    banner(ws, "Control Assessment — ISO/IEC 27001:2022 Annex A",
           f"{SYSTEM['product']} · {len(CONTROLS)} controls · assessed "
           f"{ASSESSMENT_DATE.strftime('%d %b %Y')}", len(headers))
    hdr_row = 4
    for i, h in enumerate(headers, 1):
        ws.cell(hdr_row, i, h)
    style_header_row(ws, hdr_row, len(headers))

    r = hdr_row + 1
    for c in CONTROLS:
        vals = [c["id"], c["title"], c["theme"], c["desc"], c["status"],
                c["owner"], c["evidence"], c["gap"], c["remediation"],
                c["target"], c["risk"], c["nist"]]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v)
            cell.border = BORDER
            cell.alignment = WRAP_TOP
        # ID bold
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D)
        ws.cell(r, 1).alignment = Alignment(vertical="top", horizontal="center")
        # status fill
        sc = ws.cell(r, 5)
        sc.fill = PatternFill("solid", fgColor=STATUS_FILL[c["status"]])
        sc.font = Font(bold=True, color=STATUS_FONT[c["status"]])
        sc.alignment = CENTER
        # risk fill
        rc = ws.cell(r, 11)
        rc.fill = PatternFill("solid", fgColor=RISK_FILL.get(c["risk"], "FFFFFF"))
        rc.font = Font(bold=True, color=RISK_FONT.get(c["risk"], "1F2933"))
        rc.alignment = CENTER
        ws.cell(r, 10).alignment = CENTER  # target date
        r += 1

    last = r - 1
    widths = [10, 30, 15, 46, 16, 22, 46, 46, 44, 12, 11, 22]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hdr_row}:{get_column_letter(len(headers))}{last}"
    ws.freeze_panes = f"C{hdr_row+1}"

    # data validation dropdowns (so the workbook is usable as a live tool)
    dv_status = DataValidation(type="list",
        formula1='"Implemented,Partially Implemented,Not Implemented,Not Applicable"',
        allow_blank=True)
    dv_risk = DataValidation(type="list",
        formula1='"Critical,High,Medium,Low,None,N/A"', allow_blank=True)
    ws.add_data_validation(dv_status)
    ws.add_data_validation(dv_risk)
    dv_status.add(f"E{hdr_row+1}:E{last}")
    dv_risk.add(f"K{hdr_row+1}:K{last}")
    return last


# =============================================================================
def sheet_soa(wb):
    ws = wb.create_sheet("Statement of Applicability")
    ws.sheet_view.showGridLines = False
    headers = ["Control ID", "Control Title", "Theme", "Applicable? (Y/N)",
               "Inclusion / Exclusion Justification", "Implementation Status",
               "Control Owner"]
    banner(ws, "Statement of Applicability (SoA)",
           f"{SYSTEM['product']} · {FRAMEWORK} · justification for each control's "
           f"applicability", len(headers))
    hdr = 4
    for i, h in enumerate(headers, 1):
        ws.cell(hdr, i, h)
    style_header_row(ws, hdr, len(headers))
    r = hdr + 1
    for c in CONTROLS:
        applicable = "N" if c["status"] == NA else "Y"
        if c["status"] == NA:
            justification = c["gap"]  # holds the N/A rationale
        else:
            justification = ("Applicable — relevant to the Sightline SaaS, its cloud "
                             "infrastructure, personnel and/or suppliers within the "
                             "ISMS scope.")
        vals = [c["id"], c["title"], c["theme"], applicable, justification,
                c["status"], c["owner"]]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v)
            cell.border = BORDER
            cell.alignment = WRAP_TOP
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D)
        ac = ws.cell(r, 4)
        ac.alignment = CENTER
        ac.fill = PatternFill("solid",
                              fgColor="E2E5E9" if applicable == "N" else "C6E7DD")
        ac.font = Font(bold=True,
                       color="5A626C" if applicable == "N" else "1E6B58")
        sc = ws.cell(r, 6)
        sc.fill = PatternFill("solid", fgColor=STATUS_FILL[c["status"]])
        sc.font = Font(bold=True, color=STATUS_FONT[c["status"]])
        sc.alignment = CENTER
        r += 1
    widths = [10, 30, 15, 14, 66, 20, 22]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hdr}:{get_column_letter(len(headers))}{r-1}"
    ws.freeze_panes = f"A{hdr+1}"


# =============================================================================
def sheet_summary(wb):
    ws = wb.create_sheet("Summary by Family")
    ws.sheet_view.showGridLines = False
    banner(ws, "Summary by Control Family",
           f"{SYSTEM['product']} · implementation status & weighted score per theme",
           7)
    data = S.by_theme()
    hdr = 4
    headers = ["Control Theme", "Implemented", "Partial", "Not Implemented",
               "Not Applicable", "Applicable", "Weighted Score %"]
    for i, h in enumerate(headers, 1):
        ws.cell(hdr, i, h)
    style_header_row(ws, hdr, len(headers))
    r = hdr + 1
    for t in THEME_ORDER:
        d = data[t]
        row = [t, d[IMPL], d[PART], d[NOIM], d[NA], d["applicable"],
               round(d["score_pct"], 1)]
        for i, v in enumerate(row, 1):
            cell = ws.cell(r, i, v)
            cell.border = BORDER
            cell.alignment = CENTER if i > 1 else WRAP_TOP
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D)
        r += 1
    # totals row
    counts = S.overall_counts()
    score, napp = S.compliance_score()
    total_row = ["TOTAL", counts.get(IMPL, 0), counts.get(PART, 0),
                 counts.get(NOIM, 0), counts.get(NA, 0), napp, round(score, 1)]
    for i, v in enumerate(total_row, 1):
        cell = ws.cell(r, i, v)
        cell.border = BORDER
        cell.font = Font(bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY_D)
        cell.alignment = CENTER if i > 1 else Alignment(vertical="center")
    total_line = r
    for i, w in enumerate([18, 13, 10, 16, 15, 12, 16], 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    # --- charts ---
    # stacked bar of statuses per theme
    bar = BarChart()
    bar.type = "col"
    bar.grouping = "stacked"
    bar.overlap = 100
    bar.title = "Status mix by control theme"
    bar.height = 8.5
    bar.width = 16
    data_ref = Reference(ws, min_col=2, max_col=5, min_row=hdr, max_row=hdr + 4)
    cats = Reference(ws, min_col=1, min_row=hdr + 1, max_row=hdr + 4)
    bar.add_data(data_ref, titles_from_data=True)
    bar.set_categories(cats)
    bar.y_axis.title = "controls"
    ws.add_chart(bar, "A" + str(total_line + 3))

    # weighted score column chart
    sc = BarChart()
    sc.type = "col"
    sc.title = "Weighted implementation score by theme (%)"
    sc.height = 8.5
    sc.width = 12
    sc_ref = Reference(ws, min_col=7, min_row=hdr, max_row=hdr + 4)
    sc.add_data(sc_ref, titles_from_data=True)
    sc.set_categories(cats)
    sc.y_axis.scaling.max = 100
    sc.dLbls = DataLabelList()
    sc.dLbls.showVal = True
    ws.add_chart(sc, "A" + str(total_line + 20))


# =============================================================================
def sheet_gaps(wb):
    ws = wb.create_sheet("Gap Register")
    ws.sheet_view.showGridLines = False
    headers = ["Rank", "Control ID", "Control Title", "Theme", "Status",
               "Risk Rating", "Gap Description", "Remediation Action",
               "Control Owner", "Target Date"]
    banner(ws, "Gap Register — open findings ranked by risk",
           f"{SYSTEM['product']} · {len(S.gaps())} open gaps · remediation worklist",
           len(headers))
    hdr = 4
    for i, h in enumerate(headers, 1):
        ws.cell(hdr, i, h)
    style_header_row(ws, hdr, len(headers))
    r = hdr + 1
    for rank, c in enumerate(S.ranked_gaps(), 1):
        vals = [rank, c["id"], c["title"], c["theme"], c["status"], c["risk"],
                c["gap"], c["remediation"], c["owner"], c["target"]]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v)
            cell.border = BORDER
            cell.alignment = WRAP_TOP
        ws.cell(r, 1).alignment = CENTER
        ws.cell(r, 2).font = Font(bold=True, color=NAVY_D)
        rc = ws.cell(r, 6)
        rc.fill = PatternFill("solid", fgColor=RISK_FILL[c["risk"]])
        rc.font = Font(bold=True, color=RISK_FONT[c["risk"]])
        rc.alignment = CENTER
        sc = ws.cell(r, 5)
        sc.fill = PatternFill("solid", fgColor=STATUS_FILL[c["status"]])
        sc.font = Font(bold=True, color=STATUS_FONT[c["status"]])
        sc.alignment = CENTER
        ws.cell(r, 10).alignment = CENTER
        r += 1
    for i, w in enumerate([6, 10, 28, 15, 20, 11, 50, 50, 22, 12], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hdr}:{get_column_letter(len(headers))}{r-1}"
    ws.freeze_panes = f"C{hdr+1}"


# =============================================================================
def sheet_crosswalk(wb):
    ws = wb.create_sheet("ISO to NIST Crosswalk")
    ws.sheet_view.showGridLines = False
    headers = ["ISO 27001:2022 Control", "Control Title", "Theme",
               "NIST SP 800-53 Rev.5 (primary mappings)"]
    banner(ws, "Crosswalk — ISO/IEC 27001:2022 Annex A to NIST SP 800-53 Rev. 5",
           "Best-effort mapping to primary NIST controls (see methodology for basis)",
           len(headers))
    hdr = 4
    for i, h in enumerate(headers, 1):
        ws.cell(hdr, i, h)
    style_header_row(ws, hdr, len(headers))
    r = hdr + 1
    for c in CONTROLS:
        vals = [c["id"], c["title"], c["theme"], c["nist"]]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v)
            cell.border = BORDER
            cell.alignment = WRAP_TOP
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D)
        r += 1
    for i, w in enumerate([20, 34, 16, 40], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hdr}:{get_column_letter(len(headers))}{r-1}"
    ws.freeze_panes = f"A{hdr+1}"


def main():
    wb = Workbook()
    sheet_readme(wb)
    sheet_assessment(wb)
    sheet_soa(wb)
    sheet_summary(wb)
    sheet_gaps(wb)
    sheet_crosswalk(wb)
    wb.save(OUT)
    print("wrote", os.path.relpath(OUT))


if __name__ == "__main__":
    main()
