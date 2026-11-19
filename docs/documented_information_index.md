# Documented Information Index (ISMS Document Register)

ISO/IEC 27001:2022 requires certain **documented information** to be maintained and
controlled (Clause 7.5). Auditors ask for this register early. It lists the mandatory
and supporting ISMS documents, their owner, and status for the Sightline ISMS.

**Status:** ✅ In place · 🟡 Draft / partial · 🔴 Not started
**Note:** Synthetic register for a fictional company; document *contents* are not
included — this is the index an audit lead maintains.

## Mandatory documented information (required by the standard)

| Ref | Document | Clause | Owner | Status |
|---|---|---|---|---|
| D-01 | ISMS scope | 4.3 | Security Lead | ✅ |
| D-02 | Information security policy | 5.2 | Security Lead | ✅ |
| D-03 | Information security risk assessment process | 6.1.2 | Security Lead | ✅ |
| D-04 | Information security risk treatment process | 6.1.3 | Security Lead | ✅ |
| D-05 | Statement of Applicability (SoA) | 6.1.3 d) | Security Lead | ✅ |
| D-06 | Information security objectives | 6.2 | Security Lead | 🟡 |
| D-07 | Evidence of competence | 7.2 | People Ops | ✅ |
| D-08 | Risk assessment results (risk register) | 8.2 | Security Lead | ✅ |
| D-09 | Risk treatment plan & results (POA&M) | 8.3 | Security Lead | 🟡 |
| D-10 | Monitoring & measurement results | 9.1 | Security Lead | 🟡 |
| D-11 | Internal audit programme & results | 9.2 | Security Lead | 🔴 |
| D-12 | Management review results | 9.3 | CTO / Security Lead | 🟡 |
| D-13 | Nonconformities & corrective actions | 10.2 | Security Lead | ✅ |

## Supporting operational documents (Annex A driven)

| Ref | Document | Related control | Owner | Status |
|---|---|---|---|---|
| D-20 | Acceptable Use Policy | A.5.10 | Security Lead | ✅ |
| D-21 | Access Control Policy | A.5.15 | Platform Lead | ✅ |
| D-22 | Cryptography / Key Management Standard | A.8.24 | Platform Lead | ✅ |
| D-23 | Incident Response Plan | A.5.24 | Security Lead | ✅ |
| D-24 | Business Continuity / DR Plan | A.5.29, A.5.30 | SRE Lead | 🟡 |
| D-25 | Supplier Security / TPRM Policy | A.5.19 | Legal & Compliance | ✅ |
| D-26 | Data Classification & Handling Standard | A.5.12 | DPO | 🟡 |
| D-27 | Secure Development Lifecycle Standard | A.8.25 | VP Engineering | 🟡 |
| D-28 | Secure Coding Standard | A.8.28 | VP Engineering | 🔴 |
| D-29 | Logging & Monitoring Standard | A.8.15, A.8.16 | SRE Lead | ✅ |
| D-30 | Data Retention & Deletion Schedule | A.5.33, A.8.10 | DPO | ✅ |
| D-31 | Privacy Policy / RoPA / DPIA | A.5.34 | DPO | ✅ |
| D-32 | Asset Management Policy & Inventory | A.5.9 | Platform Lead | ✅ |
| D-33 | Change Management Procedure | A.8.32 | Platform Lead | ✅ |
| D-34 | Vulnerability Management Standard | A.8.8 | Platform Lead | 🟡 |
| D-35 | Evidence Handling / Forensics Procedure | A.5.28 | Security Lead | 🔴 |
| D-36 | Remote Working Policy | A.6.7 | Security Lead | ✅ |
| D-37 | Cloud Security Standard (AWS) | A.5.23 | Platform Lead | ✅ |

## Gaps to close before Stage 1

- **D-11 Internal audit programme (🔴)** — mandatory; blocks certification.
- **D-28 Secure Coding Standard (🔴)** and **D-35 Evidence Handling (🔴)** — supporting
  documents tied to open Annex A gaps (A.8.28, A.5.28).
- Finalize drafts **D-06, D-09, D-10, D-12** (objectives, treatment plan, measurement,
  management review) to complete the mandatory set.
