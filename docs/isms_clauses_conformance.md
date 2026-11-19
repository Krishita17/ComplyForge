# ISMS Management Clauses (4–10) — Conformance Checklist

ISO/IEC 27001:2022 certification audits **two** things: the Annex A controls *and* the
management-system requirements in **Clauses 4–10**. The control workbook covers Annex A;
this checklist covers the clauses. Without conforming to Clauses 4–10, an organization
cannot be certified even with strong technical controls.

**Legend:** ✅ Conformant · 🟡 Partial · 🔴 Nonconformant
**Scope:** Sightline SaaS ISMS · **Assessment:** Q3 2026 (synthetic, fictional company)

**Clause-level summary:** 23 of 34 line items conformant (68%), 10 partial, 1
nonconformant — consistent with the Annex A posture (strong foundations, gaps in
continuity testing, internal audit, and review cadence).

---

## Clause 4 — Context of the organization

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 4.1 | Understand the organization and its context | ✅ | Context analysis (market, cloud model, threat landscape) in ISMS manual. |
| 4.2 | Understand needs & expectations of interested parties | ✅ | Interested-parties register (customers, regulators, employees, AWS, investors). |
| 4.3 | Determine the scope of the ISMS | ✅ | Documented scope statement (see methodology §2); boundary defined. |
| 4.4 | Information security management system | 🟡 | ISMS established and operating; some processes not yet fully mature (reviews, internal audit). |

## Clause 5 — Leadership

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 5.1 | Leadership and commitment | ✅ | Management commitment statement; quarterly security steering committee. |
| 5.2 | Policy | ✅ | Board-approved Information Security Policy v3.1 (A.5.1). |
| 5.3 | Roles, responsibilities and authorities | ✅ | ISMS RACI; Security Lead and DPO appointed (A.5.2). |

## Clause 6 — Planning

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 6.1.1 | Actions to address risks and opportunities | ✅ | Risk management framework documented. |
| 6.1.2 | Information security risk assessment | ✅ | Risk register with 5×5 methodology ([`risk_register.xlsx`](../risk_register.xlsx)). |
| 6.1.3 | Information security risk treatment | 🟡 | Treatment plans defined; several high-priority treatments still in progress (see POA&M). |
| 6.1.3 d) | Statement of Applicability | ✅ | SoA produced for all 93 controls (workbook tab). |
| 6.2 | Information security objectives and planning | 🟡 | Objectives defined (metrics table); formal measurement cadence being established. |
| 6.3 | Planning of changes | ✅ | Change management process (A.8.32). |

## Clause 7 — Support

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 7.1 | Resources | ✅ | Security function resourced; budget approved for remediation. |
| 7.2 | Competence | 🟡 | Roles competency-mapped; role-based security training gap for engineers (A.6.3). |
| 7.3 | Awareness | ✅ | Annual awareness training, 96% completion (A.6.3). |
| 7.4 | Communication | ✅ | Internal/external security communication plan; reporting channels (A.6.8). |
| 7.5.1 | Documented information (general) | 🟡 | Core documents in place; labelling/classification of documents incomplete (A.5.13). |
| 7.5.2 | Creating and updating | ✅ | Document control standard (versioning, approval, review dates). |
| 7.5.3 | Control of documented information | ✅ | Access-controlled policy portal; version control. |

## Clause 8 — Operation

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 8.1 | Operational planning and control | ✅ | Documented operating procedures / runbooks (A.5.37). |
| 8.2 | Information security risk assessment (operational) | 🟡 | Risk assessment performed; periodic re-assessment cadence not yet enforced. |
| 8.3 | Information security risk treatment (operational) | 🟡 | Treatment underway; evidenced via POA&M and remediation roadmap. |

## Clause 9 — Performance evaluation

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 9.1 | Monitoring, measurement, analysis and evaluation | 🟡 | Automated control monitoring (Vanta) + security metrics; formal measurement plan maturing. |
| 9.2 | Internal audit | 🔴 | No internal audit programme executed yet; this readiness assessment is the precursor (A.5.35). **Nonconformity — scheduled.** |
| 9.3 | Management review | 🟡 | Steering committee meets; formal ISO-aligned management review (with required inputs/outputs) not yet run. |

## Clause 10 — Improvement

| # | Requirement | Status | Evidence / Note |
|---|---|---|---|
| 10.1 | Continual improvement | 🟡 | Improvement backlog exists; not yet driven by a formal review/audit cycle. |
| 10.2 | Nonconformity and corrective action | ✅ | Corrective-action process via POA&M ([`reports/poam.xlsx`](../reports/poam.xlsx)); incident postmortems (A.5.27). |

---

## Priority clause actions before certification

1. **9.2 Internal audit (Nonconformity):** charter and run a first internal audit of the
   ISMS before Stage 1 — this is mandatory for certification.
2. **9.3 Management review:** hold a formal management review covering the required
   inputs (audit results, risk status, objectives, improvement) and record outputs.
3. **6.1.3 / 8.3 Risk treatment:** close Wave 1 (Critical/High) treatments per the POA&M.
4. **6.2 Objectives:** finalize measurable objectives and the measurement plan (9.1).

These four items, plus the Annex A Wave 1 remediations, are the critical path to a
defensible Stage 2 audit in March 2027.
