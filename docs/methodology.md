# Methodology, Scope & Assumptions

This note states how the ComplyForge assessment was produced, so the package can be
read with the same rigor an auditor would expect. It covers framework and versions,
scope, the rating scales, the scoring method, applicability decisions, and the
real-vs-synthetic data boundary.

## 1. Frameworks & versions

| Role | Standard | Version | Notes |
|---|---|---|---|
| Primary (certification) | ISO/IEC 27001 — Annex A | **2022** | 93 controls in 4 themes (Organizational 37, People 8, Physical 14, Technological 34). Control detail is elaborated in ISO/IEC 27002:2022. |
| Secondary (crosswalk) | NIST SP 800-53 | **Rev. 5** | Used for a best-effort control mapping (public-sector prospect request). |
| Reference (SSP format) | NIST SP 800-18 / FedRAMP SSP structure | current | Informs the structure of the sample SSP section only. |

**Control IDs and titles** are the official Annex A identifiers, used for reference
and interoperability. **Control descriptions are paraphrased in the author's own
words** — no copyrighted standard text is reproduced. Organizations performing a real
certification must work from a licensed copy of ISO/IEC 27001:2022 and 27002:2022.

## 2. Scope of the ISMS (as assessed)

> The ISMS covers the design, development, hosting, and operation of the **Sightline**
> SaaS platform, its supporting AWS cloud infrastructure (`us-east-1` / `us-west-2`),
> the corporate engineering office (Austin, TX), and the personnel and suppliers that
> operate the service.

**In scope:** production AWS environment; source code and CI/CD; identity and access;
customer and personal data processing; corporate endpoints and office; in-scope
suppliers/sub-processors.

**Out of scope / inherited:** AWS data-center physical and environmental controls
(inherited under the shared-responsibility model, evidenced by AWS attestations);
cardholder data (payments outsourced to Stripe — PCI SAQ-A).

## 3. Assessment approach

1. **Enumerate** all 93 Annex A (2022) controls.
2. **Decide applicability** for each control and record a justification (the Statement
   of Applicability). Controls made Not Applicable carry an explicit rationale.
3. **Assess implementation** against evidence available in Q3 2026.
4. **Identify gaps** for anything not fully implemented; describe the gap concretely.
5. **Rate residual risk** of each gap and assign an owner, remediation, and target
   date.
6. **Roll up** to family-level and overall readiness metrics.

This is a **first-party (internal) readiness assessment**, not a certification audit.
It is the pre-work that de-risks the Stage 1/Stage 2 audit.

## 4. Rating scales

### Implementation status
| Status | Meaning |
|---|---|
| **Implemented** | Control is designed and operating; adequate evidence exists. |
| **Partially Implemented** | Control is partly in place or inconsistently operated; a defined gap remains. |
| **Not Implemented** | Control is absent or not operating. |
| **Not Applicable** | Control does not apply to the ISMS scope; justification recorded in the SoA. |

### Risk rating of a gap
Severity reflects **likelihood × impact** of the residual exposure while the gap is
open, considering the data at risk (Restricted PII weighted highest).

| Rating | Guidance |
|---|---|
| **Critical** | Direct exposure of Restricted data or a control failure with immediate, high-impact consequences; fix before audit. |
| **High** | Significant weakness affecting core security objectives; likely an audit finding. |
| **Medium** | Moderate weakness; may be raised as a minor nonconformity or opportunity for improvement. |
| **Low** | Minor or procedural gap; low exposure. |

## 5. Scoring method (how the percentages are computed)

Percentages are computed over **applicable controls only** (Not Applicable controls
are excluded from the denominator).

**Weighted compliance score** (used for the headline and per-family charts):

```
score(control) = 1.0 (Implemented) | 0.5 (Partially Implemented) | 0.0 (Not Implemented)
weighted %     = 100 × Σ score(control) / (number of applicable controls)
```

The half-credit for "Partially Implemented" reflects that partial controls provide
real but incomplete assurance. A stricter **fully-implemented rate** (Implemented ÷
applicable) is also reported, so readers can see both the optimistic and conservative
view. All numbers in the report and README are generated from
[`build/compute_stats.py`](../build/compute_stats.py) — they cannot drift from the
workbook because both derive from the same dataset.

## 6. Applicability (Not Applicable) decisions

Because Sightline is a cloud-native, fully-remote SaaS with no owned data center and
no removable media, six controls are scoped Not Applicable. Each is defensible and
documented in the SoA:

| Control | Decision basis |
|---|---|
| A.7.6 Working in secure areas | No designated high-security processing zones/labs; all production in AWS. |
| A.7.10 Storage media | Removable media prohibited; USB mass-storage blocked by MDM; data resides in AWS managed services. |
| A.7.11 Supporting utilities | No owned processing facility; production utilities inherited from AWS. |
| A.7.12 Cabling security | No owned data-center cabling; office cabling carries no production/Restricted data. |
| A.8.23 Web filtering | Objective met by other controls (EDR web protection A.8.1, VPC egress A.8.20); no standalone web gateway. |
| A.8.30 Outsourced development | All development in-house; no outsourced/contract development. |

Knowing what does **not** apply — and why — is part of the competency this package
demonstrates. Applicability is reviewed if the environment changes (e.g., if
development is later outsourced, A.8.30 is re-scoped).

## 7. Real vs. synthetic data

| Real (cited) | Synthetic (invented) |
|---|---|
| ISO/IEC 27001:2022 Annex A control set (IDs & titles) | The company (Harborline) and product (Sightline) |
| NIST SP 800-53 Rev. 5 control identifiers | Implementation statuses, evidence, owners |
| SSP structure conventions (NIST 800-18 / FedRAMP) | Gaps, remediations, target dates, metrics |
| AWS shared-responsibility model concepts | Supplier list, architecture specifics |

No proprietary or copyrighted standard text is reproduced; requirements are
paraphrased. See [`../data/system_profile.md`](../data/system_profile.md) for the full
fictional system.

## 8. Limitations

- This is a portfolio artifact by a single author, not the output of an accredited
  certification body.
- Evidence artifacts are described, not attached (they would contain fictional
  operational data).
- The NIST crosswalk is a pragmatic mapping to *primary* related controls, not an
  exhaustive or authoritative equivalence.

## 9. How to regenerate

All artifacts are generated from one dataset. See the repository README for the exact
commands. Editing [`build/controls_data.py`](../build/controls_data.py) and re-running
the build scripts regenerates the workbook, tracker, figures, and statistics
consistently.
