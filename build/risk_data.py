# -*- coding: utf-8 -*-
"""
ComplyForge — Information Security Risk Register dataset
========================================================

Supports ISO/IEC 27001:2022 Clause 6.1.2 (information security risk assessment)
and 6.1.3 (risk treatment) for the fictional "Sightline" SaaS. Each risk is scored
on a 5x5 likelihood x impact matrix, both *inherent* (before current controls) and
*residual* (after current controls), with a treatment decision and owner.

Scoring:
  score = likelihood (1-5) x impact (1-5)  ->  1..25
  bands: Low 1-4 | Medium 5-9 | High 10-14 | Critical 15-25

Risks are linked to the Annex A controls in controls_data.py so the register and the
control assessment tell one coherent story.
"""

# Owners reuse the role vocabulary from the control assessment.
CISO = "Security Lead (CISO function)"
VPENG = "VP Engineering"
PLAT = "Platform / DevOps Lead"
SRE = "SRE Lead"
DPO = "Data Protection Officer"
LEGAL = "Legal & Compliance"

TREAT_MODIFY = "Modify (reduce)"
TREAT_RETAIN = "Retain (accept)"
TREAT_SHARE = "Share (transfer)"
TREAT_AVOID = "Avoid"


def R(rid, title, asset, threat, vuln, controls, li, ii, lr, ir,
      treatment, owner, status, target):
    return {
        "id": rid, "title": title, "asset": asset, "threat": threat,
        "vuln": vuln, "controls": controls,
        "l_inh": li, "i_inh": ii, "l_res": lr, "i_res": ir,
        "treatment": treatment, "owner": owner, "status": status,
        "target": target,
    }


RISKS = [
    R("R-01", "Exposure of customer & driver PII held unmasked in non-production",
      "Restricted PII (driver identity, location), Confidential customer PII",
      "Compromise of a lower-trust staging environment; insider access",
      "Production PII copied into staging without masking; no non-prod data controls",
      ["A.8.33", "A.8.11", "A.5.34"], 4, 5, 1, 5, TREAT_MODIFY, VPENG,
      "Treatment in progress", "Nov 2026"),

    R("R-02", "Unauthorized production change via standing privileged access",
      "Production AWS environment, customer data",
      "Malicious or mistaken use of privileged credentials",
      "Standing admin for 6 accounts; no just-in-time elevation or session logging",
      ["A.8.2", "A.5.18"], 3, 4, 2, 4, TREAT_MODIFY, PLAT,
      "Treatment in progress", "Dec 2026"),

    R("R-03", "Exploitation of an unpatched known vulnerability",
      "Internet-facing services, container images, hosts",
      "External attacker exploiting a known/listed (KEV) vulnerability",
      "Remediation SLA missed for ~35% of findings; no single aged backlog",
      ["A.8.8", "A.5.7"], 4, 4, 2, 4, TREAT_MODIFY, PLAT,
      "Treatment in progress", "Nov 2026"),

    R("R-04", "Prolonged outage or data loss from an unvalidated DR capability",
      "Sightline platform availability; customer data",
      "Regional AWS failure, data corruption, or ransomware",
      "RTO/RPO never validated by full failover; BCP unratified",
      ["A.5.30", "A.5.29", "A.8.13", "A.8.14"], 2, 5, 2, 4, TREAT_MODIFY, SRE,
      "Treatment in progress", "Dec 2026"),

    R("R-05", "Workforce account takeover via phishing",
      "SSO identities, corporate and cloud access",
      "Credential phishing / social engineering",
      "Role-based training & phishing simulations not run on a regular cadence",
      ["A.8.5", "A.6.3", "A.5.16"], 3, 4, 2, 3, TREAT_MODIFY, CISO,
      "Partially treated", "Feb 2027"),

    R("R-06", "Insider misuse enabled by inadequate access reviews",
      "Customer data, source code, production systems",
      "Malicious insider or accumulated excess privilege",
      "Access recertification irregular; residual segregation-of-duties conflicts",
      ["A.5.18", "A.5.3", "A.8.3"], 3, 4, 2, 3, TREAT_MODIFY, PLAT,
      "Treatment in progress", "Nov 2026"),

    R("R-07", "Sensitive-data exfiltration through unmonitored egress",
      "Confidential & Restricted data",
      "Insider or compromised account exfiltrating data",
      "No DLP coverage on email, SaaS, or endpoints",
      ["A.8.12", "A.5.14"], 3, 4, 2, 3, TREAT_MODIFY, CISO,
      "Planned", "Mar 2027"),

    R("R-08", "Software supply-chain compromise via third-party dependencies",
      "Build pipeline, deployed services",
      "Malicious or vulnerable upstream dependency / build tampering",
      "No standardized SBOM; artifact provenance not verified for all components",
      ["A.5.21", "A.8.8", "A.8.19"], 3, 4, 2, 3, TREAT_MODIFY, PLAT,
      "Planned", "Feb 2027"),

    R("R-09", "Cloud misconfiguration exposing data or services",
      "AWS resources (S3, RDS, IAM, security groups)",
      "Attacker discovering a misconfigured / drifted resource",
      "Configuration drift not continuously detected across all accounts",
      ["A.8.9", "A.5.23", "A.8.20"], 3, 4, 2, 3, TREAT_MODIFY, PLAT,
      "Partially treated", "Jan 2027"),

    R("R-10", "Cross-tenant data access (tenant isolation failure)",
      "Multi-tenant customer data",
      "Application flaw breaking logical tenant boundaries",
      "Application-layer monitoring for isolation anomalies incomplete",
      ["A.8.3", "A.8.22", "A.8.16"], 2, 5, 1, 5, TREAT_MODIFY, VPENG,
      "Partially treated", "Feb 2027"),

    R("R-11", "Breach at a supplier or sub-processor",
      "Data shared with Okta, Stripe, MDR, SIEM, Google Workspace",
      "Compromise of a critical supplier processing Sightline data",
      "Annual supplier re-review inconsistent; SOC 2 reports not fully collected",
      ["A.5.19", "A.5.20", "A.5.22"], 3, 4, 2, 3, TREAT_MODIFY, LEGAL,
      "Partially treated", "Apr 2027"),

    R("R-12", "Non-compliance with GDPR / CCPA obligations",
      "Personal data of EU and California data subjects",
      "Regulatory action or data-subject complaint",
      "Classification/labelling incomplete; tenant-deletion partly manual",
      ["A.5.34", "A.8.10", "A.5.12", "A.5.31"], 3, 4, 2, 3, TREAT_MODIFY, DPO,
      "Partially treated", "Feb 2027"),

    R("R-13", "Ransomware or malware impacting operations",
      "Endpoints, build systems, production",
      "Ransomware via phishing, compromised dependency, or exposed service",
      "Residual gaps in patching and application-layer detection",
      ["A.8.7", "A.8.1", "A.8.13"], 3, 4, 2, 3, TREAT_SHARE, CISO,
      "Partially treated (cyber-insurance)", "Dec 2026"),

    R("R-14", "Loss or theft of a workforce device",
      "Corporate laptops (MDM-managed)",
      "Device lost, stolen, or left unattended",
      "Off-premises asset register incomplete; no device location/lost-mode",
      ["A.7.9", "A.8.1", "A.7.7"], 2, 3, 1, 3, TREAT_MODIFY, PLAT,
      "Partially treated", "Jan 2027"),

    R("R-15", "Undetected security incident at the application layer",
      "Application, customer data",
      "Business-logic abuse or authorization anomaly going unnoticed",
      "SIEM alerting tuned mainly to infra/endpoint; app-layer coverage gaps",
      ["A.8.16", "A.5.25", "A.8.15"], 3, 4, 2, 3, TREAT_MODIFY, CISO,
      "Treatment in progress", "Feb 2027"),

    R("R-16", "Leakage of secrets or credentials in code / CI",
      "API keys, database credentials, KMS keys",
      "Accidental commit or exposure of a secret",
      "Residual reliance on scanning; secret-handling not fully hardened in CI",
      ["A.5.17", "A.8.4", "A.8.31"], 2, 4, 1, 4, TREAT_MODIFY, VPENG,
      "Partially treated", "Feb 2027"),

    R("R-17", "Release of insecure software to production",
      "Sightline application",
      "Vulnerability shipped due to missing security gate",
      "No ratified secure-SDLC; SAST advisory-only; no release security gate",
      ["A.8.29", "A.8.25", "A.8.28"], 3, 4, 2, 3, TREAT_MODIFY, VPENG,
      "Treatment in progress", "Dec 2026"),

    R("R-18", "Loss of evidential integrity during an incident",
      "Audit logs, forensic evidence",
      "Inability to preserve defensible evidence after an incident",
      "No forensic evidence-collection / chain-of-custody procedure",
      ["A.5.28", "A.8.15", "A.5.33"], 2, 3, 1, 3, TREAT_MODIFY, CISO,
      "Planned", "Feb 2027"),

    R("R-19", "Failure to meet breach-notification timelines",
      "Regulatory & contractual notification obligations",
      "Late or missed notification to regulators/customers after a breach",
      "IR plan strong, but evidence handling and authority contacts under-exercised",
      ["A.5.24", "A.5.5", "A.5.26"], 2, 4, 1, 4, TREAT_MODIFY, LEGAL,
      "Partially treated", "Jan 2027"),

    R("R-20", "Key-person dependency / duties concentration",
      "Critical operational knowledge and access",
      "Loss or unavailability of a key individual",
      "Small team; residual segregation-of-duties conflicts; documentation gaps",
      ["A.5.3", "A.5.2", "A.5.37"], 2, 3, 2, 2, TREAT_MODIFY, CISO,
      "Partially treated", "Mar 2027"),
]

assert len({r["id"] for r in RISKS}) == len(RISKS), "Duplicate risk IDs"


def band(score):
    if score >= 15:
        return "Critical"
    if score >= 10:
        return "High"
    if score >= 5:
        return "Medium"
    return "Low"


BAND_ORDER = ["Critical", "High", "Medium", "Low"]
