# -*- coding: utf-8 -*-
"""Generate risk_register.xlsx — ISO/IEC 27001:2022 Clause 6.1 risk assessment.

    python build/build_risk_register.py

Tabs:
  0. Read Me        – method, scoring, scope
  1. Risk Register  – all risks, inherent & residual scoring, treatment, owner
  2. Risk Summary   – counts by band (inherent vs residual) + chart, top risks
"""
import os
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

from risk_data import RISKS, band, BAND_ORDER
from controls_data import SYSTEM, ASSESSMENT_DATE

OUT = os.path.join(os.path.dirname(__file__), "..", "risk_register.xlsx")

NAVY = "1F5C8B"; NAVY_D = "163F5F"; WHITE = "FFFFFF"; INK = "1F2933"
thin = Side(style="thin", color="D8DEE6")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
HDR_FONT = Font(bold=True, color=WHITE, size=11)
WRAP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
BAND_FILL = {"Critical": "7B1E1E", "High": "C0392B", "Medium": "E0A200", "Low": "2E8B7A"}
BAND_FONT = {"Critical": "FFFFFF", "High": "FFFFFF", "Medium": "3A2E00", "Low": "FFFFFF"}


def banner(ws, title, subtitle, span):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    ws.cell(1, 1, title).font = Font(bold=True, color=NAVY_D, size=18)
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
    ws.cell(2, 1, subtitle).font = Font(color="5A626C", size=11)


def hdr_row(ws, row, headers):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row, i, h)
        c.fill = HDR_FILL; c.font = HDR_FONT; c.alignment = CENTER; c.border = BORDER
    ws.row_dimensions[row].height = 30


def score_cell(ws, r, col, score):
    b = band(score)
    c = ws.cell(r, col, score)
    c.fill = PatternFill("solid", fgColor=BAND_FILL[b])
    c.font = Font(bold=True, color=BAND_FONT[b]); c.alignment = CENTER; c.border = BORDER


def sheet_readme(wb):
    ws = wb.active; ws.title = "Read Me"; ws.sheet_view.showGridLines = False
    banner(ws, "ComplyForge — Information Security Risk Register",
           f"{SYSTEM['product']} · ISO/IEC 27001:2022 Clause 6.1.2 / 6.1.3", 2)
    inh = Counter(band(r["l_inh"] * r["i_inh"]) for r in RISKS)
    res = Counter(band(r["l_res"] * r["i_res"]) for r in RISKS)
    rows = [
        ("", ""),
        ("Purpose", "Identify, analyse, evaluate and plan treatment of information "
         "security risks to the Sightline SaaS, per ISO/IEC 27001:2022 Clause 6.1."),
        ("Method", "Risk = Likelihood (1-5) x Impact (1-5). Scored both INHERENT "
         "(before current controls) and RESIDUAL (after current controls)."),
        ("Likelihood scale", "1 Rare · 2 Unlikely · 3 Possible · 4 Likely · 5 Almost certain"),
        ("Impact scale", "1 Insignificant · 2 Minor · 3 Moderate · 4 Major · 5 Severe"),
        ("Risk bands", "Low 1-4 · Medium 5-9 · High 10-14 · Critical 15-25"),
        ("Treatment options", "Modify (reduce) · Retain (accept) · Share (transfer) · Avoid"),
        ("Linkage", "Each risk links to the Annex A controls that treat it; see "
         "control_assessment_workbook.xlsx."),
        ("", ""),
        ("SNAPSHOT", ""),
        ("Total risks", str(len(RISKS))),
        ("Inherent (before controls)", f"Critical {inh['Critical']} · High {inh['High']} "
         f"· Medium {inh['Medium']} · Low {inh['Low']}"),
        ("Residual (after controls)", f"Critical {res['Critical']} · High {res['High']} "
         f"· Medium {res['Medium']} · Low {res['Low']}"),
        ("Assessment date", ASSESSMENT_DATE.strftime("%d %b %Y")),
        ("", ""),
        ("Note", "Synthetic risk data for a fictional company. Framework references "
         "are real. See docs/methodology.md."),
    ]
    r = 4
    for k, v in rows:
        kc = ws.cell(r, 1, k); vc = ws.cell(r, 2, v); vc.alignment = WRAP
        kc.font = Font(bold=True, color=NAVY_D if k in ("SNAPSHOT",) else INK)
        r += 1
    ws.column_dimensions["A"].width = 26; ws.column_dimensions["B"].width = 96


def sheet_register(wb):
    ws = wb.create_sheet("Risk Register"); ws.sheet_view.showGridLines = False
    headers = ["Risk ID", "Risk Scenario", "Asset at Risk", "Threat", "Vulnerability",
               "Linked Controls", "Inh. L", "Inh. I", "Inh. Score", "Inh. Band",
               "Res. L", "Res. I", "Res. Score", "Res. Band", "Treatment",
               "Risk Owner", "Status", "Target"]
    banner(ws, "Risk Register", f"{SYSTEM['product']} · {len(RISKS)} risks · inherent "
           f"and residual scoring with treatment decisions", len(headers))
    hr = 4; hdr_row(ws, hr, headers)
    r = hr + 1
    for rk in RISKS:
        inh = rk["l_inh"] * rk["i_inh"]; res = rk["l_res"] * rk["i_res"]
        vals = [rk["id"], rk["title"], rk["asset"], rk["threat"], rk["vuln"],
                ", ".join(rk["controls"]), rk["l_inh"], rk["i_inh"], None, band(inh),
                rk["l_res"], rk["i_res"], None, band(res), rk["treatment"],
                rk["owner"], rk["status"], rk["target"]]
        for i, v in enumerate(vals, 1):
            c = ws.cell(r, i, v); c.border = BORDER
            c.alignment = CENTER if i in (7, 8, 11, 12, 18) else WRAP
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D); ws.cell(r, 1).alignment = CENTER
        score_cell(ws, r, 9, inh); score_cell(ws, r, 13, res)
        for col, bnd in ((10, band(inh)), (14, band(res))):
            c = ws.cell(r, col)
            c.fill = PatternFill("solid", fgColor=BAND_FILL[bnd])
            c.font = Font(bold=True, color=BAND_FONT[bnd]); c.alignment = CENTER
        r += 1
    widths = [8, 34, 24, 26, 30, 16, 6, 6, 9, 9, 6, 6, 9, 9, 16, 22, 20, 10]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hr}:{get_column_letter(len(headers))}{r-1}"
    ws.freeze_panes = f"B{hr+1}"
    dv = DataValidation(type="list",
        formula1='"Modify (reduce),Retain (accept),Share (transfer),Avoid"',
        allow_blank=True)
    ws.add_data_validation(dv); dv.add(f"O{hr+1}:O{r-1}")


def sheet_summary(wb):
    ws = wb.create_sheet("Risk Summary"); ws.sheet_view.showGridLines = False
    banner(ws, "Risk Summary", "Inherent vs residual risk profile and top residual risks", 5)
    inh = Counter(band(r["l_inh"] * r["i_inh"]) for r in RISKS)
    res = Counter(band(r["l_res"] * r["i_res"]) for r in RISKS)
    hr = 4
    hdr_row(ws, hr, ["Risk Band", "Inherent (before controls)", "Residual (after controls)"])
    r = hr + 1
    for b in BAND_ORDER:
        ws.cell(r, 1, b).border = BORDER
        ws.cell(r, 1).fill = PatternFill("solid", fgColor=BAND_FILL[b])
        ws.cell(r, 1).font = Font(bold=True, color=BAND_FONT[b])
        for col, src in ((2, inh), (3, res)):
            c = ws.cell(r, col, src.get(b, 0)); c.border = BORDER; c.alignment = CENTER
        r += 1
    ws.cell(r, 1, "TOTAL").font = Font(bold=True, color=WHITE)
    ws.cell(r, 1).fill = PatternFill("solid", fgColor=NAVY_D)
    ws.cell(r, 2, len(RISKS)).alignment = CENTER
    ws.cell(r, 3, len(RISKS)).alignment = CENTER
    for col in (2, 3):
        ws.cell(r, col).font = Font(bold=True)
    for i, w in enumerate([16, 24, 24], 1):
        ws.column_dimensions[get_column_letter(i)].width = w

    chart = BarChart(); chart.type = "col"; chart.title = "Inherent vs residual risk by band"
    chart.height = 8; chart.width = 15
    data = Reference(ws, min_col=2, max_col=3, min_row=hr, max_row=hr + len(BAND_ORDER))
    cats = Reference(ws, min_col=1, min_row=hr + 1, max_row=hr + len(BAND_ORDER))
    chart.add_data(data, titles_from_data=True); chart.set_categories(cats)
    chart.dLbls = DataLabelList(); chart.dLbls.showVal = True
    ws.add_chart(chart, "E4")

    # top residual risks
    top_row = r + 3
    ws.cell(top_row, 1, "Top residual risks").font = Font(bold=True, color=NAVY_D, size=13)
    hdr_row(ws, top_row + 1, ["Risk ID", "Scenario", "Residual Score", "Owner"])
    ranked = sorted(RISKS, key=lambda x: -(x["l_res"] * x["i_res"]))[:6]
    rr = top_row + 2
    for rk in ranked:
        res = rk["l_res"] * rk["i_res"]
        ws.cell(rr, 1, rk["id"]).border = BORDER
        ws.cell(rr, 1).font = Font(bold=True, color=NAVY_D); ws.cell(rr, 1).alignment = CENTER
        ws.cell(rr, 2, rk["title"]).border = BORDER; ws.cell(rr, 2).alignment = WRAP
        score_cell(ws, rr, 3, res)
        ws.cell(rr, 4, rk["owner"]).border = BORDER; ws.cell(rr, 4).alignment = WRAP
        rr += 1
    ws.column_dimensions["B"].width = 50; ws.column_dimensions["D"].width = 24


def main():
    wb = Workbook()
    sheet_readme(wb); sheet_register(wb); sheet_summary(wb)
    wb.save(OUT)
    print("wrote", os.path.relpath(OUT), "|", len(RISKS), "risks")


if __name__ == "__main__":
    main()
