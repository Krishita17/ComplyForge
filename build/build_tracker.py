# -*- coding: utf-8 -*-
"""Generate evidence_tracker.xlsx — the audit-evidence coordination artifact.

    python build/build_tracker.py

Maps each applicable control to the evidence needed, its owner, and tracks
collection status (Not Started -> Requested -> Received -> Validated) and
submission status to the auditor.
"""
import os
from collections import Counter
from datetime import date, timedelta
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList

from controls_data import CONTROLS, SYSTEM, ASSESSMENT_DATE, IMPL, PART, NOIM, NA

OUT = os.path.join(os.path.dirname(__file__), "..", "evidence_tracker.xlsx")

NAVY = "1F5C8B"; NAVY_D = "163F5F"; WHITE = "FFFFFF"
thin = Side(style="thin", color="D8DEE6")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
HDR_FILL = PatternFill("solid", fgColor=NAVY)
HDR_FONT = Font(bold=True, color=WHITE, size=11)
WRAP_TOP = Alignment(wrap_text=True, vertical="top")
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)

COLL_FILL = {
    "Validated": "C6E7DD", "Received": "CDE3F2", "Requested": "FCE8B8",
    "In Progress": "FCE8B8", "Not Started": "F4C7C3",
}
COLL_FONT = {
    "Validated": "1E6B58", "Received": "1F5C8B", "Requested": "8A6100",
    "In Progress": "8A6100", "Not Started": "9B2C22",
}
SUB_FILL = {"Submitted": "C6E7DD", "Ready to submit": "CDE3F2", "Pending": "E2E5E9"}
SUB_FONT = {"Submitted": "1E6B58", "Ready to submit": "1F5C8B", "Pending": "5A626C"}


def _evidence_type(text):
    t = text.lower()
    if any(k in t for k in ("log", "cloudtrail", "siem", "flow log")):
        return "Log export"
    if any(k in t for k in ("policy", "plan", "standard", "procedure", "register",
                            "schedule", "matrix", "manual", "ropa", "dpia", "notice")):
        return "Document"
    if any(k in t for k in ("config", "terraform", "baseline", "iac", "scan")):
        return "Configuration / scan"
    if any(k in t for k in ("report", "attestation", "soc 2", "pentest", "minutes")):
        return "Report / attestation"
    if any(k in t for k in ("record", "checklist", "completion", "acknowledge",
                            "training", "review", "ticket")):
        return "Record"
    return "Screenshot / export"


def _status_map(control):
    """Deterministic, realistic collection + submission status per control."""
    cid = control["id"]
    seed = sum(ord(x) for x in cid)
    st = control["status"]
    if st == IMPL:
        coll = "Validated" if seed % 10 < 7 else "Received"
    elif st == PART:
        coll = ["Received", "Requested", "In Progress"][seed % 3]
    elif st == NOIM:
        coll = "Not Started"
    else:
        coll = "Not Started"
    if coll == "Validated":
        sub = "Submitted" if seed % 3 else "Ready to submit"
    elif coll == "Received":
        sub = "Ready to submit"
    else:
        sub = "Pending"
    return coll, sub


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Evidence Tracker"
    ws.sheet_view.showGridLines = False

    headers = ["Evidence ID", "Control ID", "Control Title", "Evidence Required",
               "Evidence Type", "Evidence Owner", "Collection Status",
               "Submission Status", "Requested On", "Due Date", "Notes"]
    ws.merge_cells("A1:K1")
    ws.cell(1, 1, "ComplyForge — Evidence Collection Tracker").font = \
        Font(bold=True, color=NAVY_D, size=18)
    ws.merge_cells("A2:K2")
    ws.cell(2, 1, f"{SYSTEM['product']} · ISO/IEC 27001:2022 certification evidence "
            f"· maintained by the audit lead").font = \
        Font(color="5A626C", size=11)
    hdr = 4
    for i, h in enumerate(headers, 1):
        ws.cell(hdr, i, h)
    for c in range(1, len(headers) + 1):
        cell = ws.cell(hdr, c)
        cell.fill = HDR_FILL; cell.font = HDR_FONT
        cell.alignment = CENTER; cell.border = BORDER
    ws.row_dimensions[hdr].height = 30

    requested = ASSESSMENT_DATE
    r = hdr + 1
    n = 0
    coll_counter = Counter()
    applicable = [c for c in CONTROLS if c["status"] != NA]
    for c in applicable:
        n += 1
        coll, sub = _status_map(c)
        coll_counter[coll] += 1
        # due date: gapped controls due at their remediation target-ish; others rolling
        if c["status"] in (PART, NOIM):
            due = c["target"]
        else:
            due = (requested + timedelta(days=21 + (n % 4) * 7)).strftime("%d %b %Y")
        notes = ("Evidence will be produced on remediation completion."
                 if c["status"] == NOIM else
                 ("Partial evidence on file; completeness pending remediation."
                  if c["status"] == PART else "Current-period evidence on file."))
        vals = [f"EV-{n:03d}", c["id"], c["title"], c["evidence"],
                _evidence_type(c["evidence"]), c["owner"], coll, sub,
                requested.strftime("%d %b %Y"), due, notes]
        for i, v in enumerate(vals, 1):
            cell = ws.cell(r, i, v)
            cell.border = BORDER; cell.alignment = WRAP_TOP
        ws.cell(r, 1).font = Font(bold=True, color=NAVY_D)
        ws.cell(r, 1).alignment = CENTER
        ws.cell(r, 2).font = Font(bold=True, color=NAVY_D)
        cc = ws.cell(r, 7)
        cc.fill = PatternFill("solid", fgColor=COLL_FILL[coll])
        cc.font = Font(bold=True, color=COLL_FONT[coll]); cc.alignment = CENTER
        sc = ws.cell(r, 8)
        sc.fill = PatternFill("solid", fgColor=SUB_FILL[sub])
        sc.font = Font(bold=True, color=SUB_FONT[sub]); sc.alignment = CENTER
        ws.cell(r, 9).alignment = CENTER
        ws.cell(r, 10).alignment = CENTER
        r += 1
    last = r - 1
    for i, w in enumerate([11, 10, 30, 48, 20, 22, 16, 16, 14, 14, 40], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.auto_filter.ref = f"A{hdr}:K{last}"
    ws.freeze_panes = f"C{hdr+1}"

    dv_coll = DataValidation(type="list",
        formula1='"Not Started,Requested,In Progress,Received,Validated"',
        allow_blank=True)
    dv_sub = DataValidation(type="list",
        formula1='"Pending,Ready to submit,Submitted"', allow_blank=True)
    ws.add_data_validation(dv_coll); ws.add_data_validation(dv_sub)
    dv_coll.add(f"G{hdr+1}:G{last}"); dv_sub.add(f"H{hdr+1}:H{last}")

    # --- summary sheet ---
    s = wb.create_sheet("Collection Summary")
    s.sheet_view.showGridLines = False
    s.merge_cells("A1:C1")
    s.cell(1, 1, "Evidence Collection — Status Summary").font = \
        Font(bold=True, color=NAVY_D, size=16)
    order = ["Validated", "Received", "In Progress", "Requested", "Not Started"]
    s.cell(3, 1, "Collection Status").font = Font(bold=True, color=WHITE)
    s.cell(3, 2, "Count").font = Font(bold=True, color=WHITE)
    s.cell(3, 3, "% of applicable").font = Font(bold=True, color=WHITE)
    for c in range(1, 4):
        s.cell(3, c).fill = HDR_FILL; s.cell(3, c).alignment = CENTER
        s.cell(3, c).border = BORDER
    rr = 4
    tot = sum(coll_counter.values())
    for k in order:
        v = coll_counter.get(k, 0)
        s.cell(rr, 1, k).border = BORDER
        s.cell(rr, 1).fill = PatternFill("solid", fgColor=COLL_FILL[k])
        s.cell(rr, 1).font = Font(bold=True, color=COLL_FONT[k])
        s.cell(rr, 2, v).border = BORDER; s.cell(rr, 2).alignment = CENTER
        s.cell(rr, 3, f"{100*v/tot:.0f}%").border = BORDER
        s.cell(rr, 3).alignment = CENTER
        rr += 1
    s.cell(rr, 1, "TOTAL (applicable controls)").font = Font(bold=True, color=WHITE)
    s.cell(rr, 1).fill = PatternFill("solid", fgColor=NAVY_D)
    s.cell(rr, 2, tot).font = Font(bold=True, color=WHITE)
    s.cell(rr, 2).fill = PatternFill("solid", fgColor=NAVY_D)
    s.cell(rr, 2).alignment = CENTER
    s.cell(rr, 3, "100%").font = Font(bold=True, color=WHITE)
    s.cell(rr, 3).fill = PatternFill("solid", fgColor=NAVY_D)
    s.cell(rr, 3).alignment = CENTER
    for i, w in enumerate([26, 10, 16], 1):
        s.column_dimensions[get_column_letter(i)].width = w

    chart = BarChart(); chart.type = "bar"
    chart.title = "Evidence collection status"
    chart.height = 7.5; chart.width = 15
    dref = Reference(s, min_col=2, min_row=3, max_row=3 + len(order))
    cats = Reference(s, min_col=1, min_row=4, max_row=3 + len(order))
    chart.add_data(dref, titles_from_data=True); chart.set_categories(cats)
    chart.dLbls = DataLabelList(); chart.dLbls.showVal = True
    chart.legend = None
    s.add_chart(chart, "E3")

    wb.save(OUT)
    print("wrote", os.path.relpath(OUT), "| evidence items:", n)
    print("collection status:", dict(coll_counter))


if __name__ == "__main__":
    main()
