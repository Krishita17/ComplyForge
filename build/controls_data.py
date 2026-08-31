# -*- coding: utf-8 -*-
"""
ComplyForge — master control dataset (single source of truth)
=============================================================

This module holds the full ISO/IEC 27001:2022 Annex A control assessment for the
fictional SaaS system "Sightline" (Harborline Technologies, Inc.), together with a
best-effort crosswalk to NIST SP 800-53 Rev. 5.

Every downstream artifact is generated from this file:
  - control_assessment_workbook.xlsx   (build/build_workbook.py)
  - evidence_tracker.xlsx              (build/build_tracker.py)
  - figures/*.png                      (build/build_figures.py)
  - reports/audit_readiness_report.md  (stats computed via build/compute_stats.py)

Framework source:  ISO/IEC 27001:2022, Annex A (93 controls, 4 themes).
Control titles are the official Annex A identifiers/titles used for reference only.
Control *descriptions* are paraphrased in the author's own words — the copyrighted
standard text is NOT reproduced. See docs/methodology.md for scope and assumptions.

Status vocabulary:  Implemented | Partially Implemented | Not Implemented | Not Applicable
Risk vocabulary  :  Critical | High | Medium | Low | None | N/A
"""

from datetime import date

ASSESSMENT_DATE = date(2026, 8, 30)
FRAMEWORK = "ISO/IEC 27001:2022, Annex A"
FRAMEWORK_SECONDARY = "NIST SP 800-53 Rev. 5 (crosswalk)"

# ---------------------------------------------------------------------------
# Fictional system profile (synthetic — see data/system_profile.md)
# ---------------------------------------------------------------------------
SYSTEM = {
    "company": "Harborline Technologies, Inc.",
    "product": "Sightline",
    "tagline": "Real-time supply-chain visibility & predictive-ETA SaaS for mid-market logistics",
    "environment": "AWS (us-east-1 primary, us-west-2 DR); multi-tenant; Kubernetes (EKS)",
    "certification_goal": "ISO/IEC 27001:2022 certification (Stage 1 Jan 2027, Stage 2 Mar 2027)",
    "assessment_window": "Q3 2026",
    "assessor": "Internal audit lead (first-party readiness assessment)",
    "scope_statement": (
        "The Information Security Management System (ISMS) covers the design, "
        "development, hosting and operation of the Sightline SaaS platform, its "
        "supporting AWS cloud infrastructure, the corporate engineering office "
        "(Austin, TX), and the personnel and suppliers that operate the service."
    ),
}

# Owners (roles, not individuals)
CISO = "Security Lead (CISO function)"
VPENG = "VP Engineering"
PLAT = "Platform / DevOps Lead"
SRE = "SRE Lead"
DPO = "Data Protection Officer"
LEGAL = "Legal & Compliance"
PEOPLE = "People Operations (HR)"
CTO = "CTO"
OFFICE = "Office Manager"
PRODUCT = "Head of Product"

# ---------------------------------------------------------------------------
# Helper to keep the 93 rows compact and consistent.
# ---------------------------------------------------------------------------
def C(cid, title, theme, desc, status, owner, evidence, nist,
      gap="—", remediation="—", target="—", risk="None"):
    return {
        "id": cid, "title": title, "theme": theme, "desc": desc,
        "status": status, "owner": owner, "evidence": evidence, "nist": nist,
        "gap": gap, "remediation": remediation, "target": target, "risk": risk,
    }


IMPL = "Implemented"
PART = "Partially Implemented"
NOIM = "Not Implemented"
NA = "Not Applicable"

CONTROLS = [
    # =====================================================================
    # A.5 — Organizational controls (37)
    # =====================================================================
    C("A.5.1", "Policies for information security", "Organizational",
      "Maintain a set of information-security policies, approved by management, "
      "published to staff, and reviewed at planned intervals.",
      IMPL, CISO,
      "Information Security Policy v3.1 (board-approved 2026-02); policy portal "
      "in Confluence with read-acknowledgement records for all staff.",
      "PL-1, PM-1"),

    C("A.5.2", "Information security roles and responsibilities", "Organizational",
      "Define and allocate information-security responsibilities across the "
      "organization.",
      IMPL, CISO,
      "ISMS roles-and-responsibilities matrix (RACI); job descriptions for "
      "Security Lead and DPO; org chart.",
      "PM-2, PL-9, PS-2"),

    C("A.5.3", "Segregation of duties", "Organizational",
      "Separate conflicting duties and areas of responsibility to reduce the risk "
      "of unauthorized or unintentional modification or misuse.",
      PART, VPENG,
      "Deploy pipeline requires PR review + separate approver; but in a 25-person "
      "eng team several staff hold both developer and production-admin roles.",
      "AC-5",
      gap="Residual SoD conflicts: 4 engineers can both author and approve/deploy "
          "production change in emergency-access path; no documented compensating "
          "review log.",
      remediation="Formalize SoD conflict matrix; route emergency changes through "
                  "break-glass approval with mandatory post-hoc review.",
      target="Dec 2026", risk="Medium"),

    C("A.5.4", "Management responsibilities", "Organizational",
      "Require all personnel to apply information security per established policies "
      "and procedures.",
      IMPL, CISO,
      "Management commitment statement in ISMS manual; quarterly security steering "
      "committee minutes.",
      "PM-2, PL-4"),

    C("A.5.5", "Contact with authorities", "Organizational",
      "Maintain appropriate contact with relevant authorities.",
      IMPL, LEGAL,
      "Authority-contact register (state AG breach-notification contact, CISA, "
      "local law enforcement, EU lead supervisory authority).",
      "IR-6, IR-6(3)"),

    C("A.5.6", "Contact with special interest groups", "Organizational",
      "Maintain contact with special interest groups, security forums and "
      "professional associations.",
      IMPL, CISO,
      "Membership records: Cloud Security Alliance, OWASP local chapter, sector "
      "ISAC subscription; feeds routed to #sec-intel Slack.",
      "PM-15, SI-5"),

    C("A.5.7", "Threat intelligence", "Organizational",
      "Collect and analyse information about information-security threats to "
      "produce actionable threat intelligence.",
      PART, CISO,
      "Consumes CISA KEV and MDR-vendor threat feeds; no documented process to "
      "triage, contextualize and action strategic/operational threat intel.",
      "RA-3(3), PM-16, SI-5",
      gap="Threat intel is consumed ad hoc; no defined tactical/operational/"
          "strategic tiers, ownership, or feedback into risk assessment.",
      remediation="Stand up a lightweight threat-intel procedure; assign owner; "
                  "map feeds to KEV-driven patch prioritization.",
      target="Feb 2027", risk="Medium"),

    C("A.5.8", "Information security in project management", "Organizational",
      "Integrate information security into project management.",
      PART, PRODUCT,
      "Security review is a checklist item in the product RFC template, but is "
      "skipped for smaller projects; no gate enforcing sign-off.",
      "SA-3, PL-2",
      gap="Security requirements not consistently addressed for non-major "
          "projects; no evidence of security sign-off on 3 of last 8 launches.",
      remediation="Make security-impact assessment a mandatory RFC gate with "
                  "recorded Security Lead sign-off.",
      target="Jan 2027", risk="Medium"),

    C("A.5.9", "Inventory of information and other associated assets", "Organizational",
      "Develop and maintain an inventory of information and associated assets, "
      "including owners.",
      IMPL, PLAT,
      "CMDB in Vanta + AWS resource tagging policy (owner/data-class tags "
      "enforced via SCP); quarterly reconciliation report.",
      "CM-8, PM-5"),

    C("A.5.10", "Acceptable use of information and other associated assets",
      "Organizational",
      "Identify, document and implement rules for acceptable use of information "
      "and assets.",
      IMPL, CISO,
      "Acceptable Use Policy v2.0 acknowledged at onboarding and annually.",
      "PL-4, AC-8"),

    C("A.5.11", "Return of assets", "Organizational",
      "Ensure personnel return organizational assets on termination or change of "
      "employment.",
      IMPL, PEOPLE,
      "Offboarding checklist in HRIS (BambooHR) with asset-return step; MDM "
      "remote-wipe records.",
      "PS-4, PS-5"),

    C("A.5.12", "Classification of information", "Organizational",
      "Classify information according to security needs based on confidentiality, "
      "integrity, availability and stakeholder requirements.",
      PART, DPO,
      "4-tier classification scheme defined (Public/Internal/Confidential/"
      "Restricted); applied to key data stores but not to all documents/repos.",
      "RA-2, MP-1",
      gap="Classification not consistently applied to unstructured data "
          "(shared drives, wiki); no automated tagging.",
      remediation="Complete data-classification sweep of shared drives; add "
                  "classification banner requirement to document templates.",
      target="Feb 2027", risk="Medium"),

    C("A.5.13", "Labelling of information", "Organizational",
      "Develop and implement procedures for information labelling per the "
      "classification scheme.",
      NOIM, DPO,
      "No operational labelling mechanism in place.",
      "MP-3",
      gap="Labelling procedure not implemented; classified information is not "
          "labelled in documents, email, or datasets.",
      remediation="Define labelling procedure; enable Google Workspace labels / "
                  "document headers tied to classification tiers.",
      target="Mar 2027", risk="Medium"),

    C("A.5.14", "Information transfer", "Organizational",
      "Apply rules, procedures and agreements for secure information transfer "
      "internally and externally.",
      IMPL, CISO,
      "Data-transfer standard (TLS-only, approved channels); customer DPAs and "
      "Standard Contractual Clauses for EU transfers.",
      "AC-4, SC-8, SC-8(1)"),

    C("A.5.15", "Access control", "Organizational",
      "Establish and implement rules to control physical and logical access based "
      "on business and security requirements.",
      IMPL, PLAT,
      "Access Control Policy v2.2; role-based access model documented; "
      "least-privilege standard.",
      "AC-1, AC-2, AC-3, AC-6"),

    C("A.5.16", "Identity management", "Organizational",
      "Manage the full life cycle of identities.",
      IMPL, PLAT,
      "Okta as IdP; joiner-mover-leaver automation via SCIM; unique IDs; service "
      "accounts inventoried.",
      "IA-2, IA-4, AC-2"),

    C("A.5.17", "Authentication information", "Organizational",
      "Control allocation and management of authentication information (passwords, "
      "secrets, keys).",
      IMPL, PLAT,
      "Password policy (NIST-aligned) enforced in Okta; secrets in AWS Secrets "
      "Manager + HashiCorp Vault; no hard-coded credentials (gitleaks in CI).",
      "IA-5, IA-5(1)"),

    C("A.5.18", "Access rights", "Organizational",
      "Provision, review, modify and remove access rights per the access-control "
      "policy.",
      PART, PLAT,
      "Provisioning/deprovisioning automated; but periodic access recertification "
      "is irregular — last full user-access review was 9 months ago.",
      "AC-2, AC-2(3), AC-6(7)",
      gap="No enforced quarterly access review cadence; privileged and third-party "
          "access not recertified within policy interval.",
      remediation="Implement quarterly access-recertification campaigns in Vanta; "
                  "start with privileged and production access.",
      target="Nov 2026", risk="High"),

    C("A.5.19", "Information security in supplier relationships", "Organizational",
      "Define and implement processes to manage security risks from supplier use "
      "of the organization's assets.",
      IMPL, LEGAL,
      "Third-Party Risk Management Policy; vendor security review before "
      "onboarding; vendor inventory with tiering.",
      "SR-3, SA-9, SA-4"),

    C("A.5.20", "Addressing information security within supplier agreements",
      "Organizational",
      "Establish and agree relevant security requirements with each supplier.",
      IMPL, LEGAL,
      "Master service agreements include security addendum and DPA; sub-processor "
      "list maintained.",
      "SR-3, SA-9, SA-4"),

    C("A.5.21", "Managing information security in the ICT supply chain",
      "Organizational",
      "Manage security risks associated with the ICT products and services supply "
      "chain.",
      PART, PLAT,
      "Container base images pinned and scanned; but Software Bill of Materials "
      "(SBOM) generation is not standardized across services.",
      "SR-2, SR-3, SR-4, SR-11",
      gap="No consistent SBOM across all microservices; upstream dependency "
          "provenance not verified for all components.",
      remediation="Generate CycloneDX SBOMs in CI for all services; adopt "
                  "signed-artifact verification (Sigstore/cosign).",
      target="Feb 2027", risk="Medium"),

    C("A.5.22", "Monitoring, review and change management of supplier services",
      "Organizational",
      "Regularly monitor, review, evaluate and manage change in supplier security "
      "practice and service delivery.",
      PART, LEGAL,
      "Critical suppliers reviewed at renewal; but annual security re-review is "
      "not consistently performed for tier-2 vendors.",
      "SR-6, SA-9(1)",
      gap="Supplier re-assessment cadence not consistently met; SOC 2 reports not "
          "collected for all critical sub-processors.",
      remediation="Automate annual vendor re-review and SOC 2 collection reminders "
                  "in TPRM tool.",
      target="Apr 2027", risk="Low"),

    C("A.5.23", "Information security for use of cloud services", "Organizational",
      "Establish processes for acquisition, use, management and exit of cloud "
      "services per security requirements.",
      IMPL, PLAT,
      "Cloud Security Standard (AWS); CSP shared-responsibility matrix; AWS SOC 2 "
      "/ ISO 27001 attestations on file; exit plan documented.",
      "SA-9, SA-9(5), AC-20"),

    C("A.5.24", "Information security incident management planning and preparation",
      "Organizational",
      "Plan and prepare for incident management by defining processes, roles and "
      "responsibilities.",
      IMPL, CISO,
      "Incident Response Plan v2.0; severity matrix; on-call rotation; MDR "
      "provider runbooks.",
      "IR-1, IR-8"),

    C("A.5.25", "Assessment and decision on information security events",
      "Organizational",
      "Assess information-security events and decide whether to categorize them as "
      "incidents.",
      IMPL, SRE,
      "Event-triage runbook; severity classification criteria; PagerDuty + "
      "security event queue.",
      "IR-4, IR-5, AU-6"),

    C("A.5.26", "Response to information security incidents", "Organizational",
      "Respond to incidents per documented procedures.",
      IMPL, CISO,
      "Incident-specific runbooks (account compromise, data exposure, ransomware); "
      "2 tabletop exercises in 2026 with records.",
      "IR-4, IR-6"),

    C("A.5.27", "Learning from information security incidents", "Organizational",
      "Use knowledge from incidents to strengthen controls.",
      PART, CISO,
      "Blameless postmortems for SEV1/2; but no periodic trend analysis feeding "
      "control improvements.",
      "IR-4(1)",
      gap="Postmortem actions tracked per-incident but not aggregated into "
          "recurring-theme analysis or control-improvement backlog.",
      remediation="Add quarterly incident-trend review; link recurring findings to "
                  "risk register.",
      target="Mar 2027", risk="Low"),

    C("A.5.28", "Collection of evidence", "Organizational",
      "Establish procedures for identification, collection, acquisition and "
      "preservation of evidence.",
      NOIM, CISO,
      "No formal digital-evidence / chain-of-custody procedure exists.",
      "AU-11, IR-4, AU-10",
      gap="No documented forensic evidence-collection or chain-of-custody "
          "procedure; risk to legal defensibility of incident evidence.",
      remediation="Author evidence-handling procedure; pre-stage forensic capture "
                  "tooling and retention for CloudTrail/EDR data.",
      target="Feb 2027", risk="Medium"),

    C("A.5.29", "Information security during disruption", "Organizational",
      "Plan how to maintain information security at an appropriate level during "
      "disruption.",
      PART, SRE,
      "Business Continuity Plan drafted; security-during-disruption provisions "
      "identified but not exercised.",
      "CP-2, CP-2(3)",
      gap="BCP is in draft and unratified; security controls during degraded "
          "operation not tested; no defined minimum security baseline for "
          "contingency mode.",
      remediation="Ratify BCP; define contingency security baseline; include in "
                  "next continuity exercise.",
      target="Dec 2026", risk="High"),

    C("A.5.30", "ICT readiness for business continuity", "Organizational",
      "Plan, implement, maintain and test ICT readiness for business continuity.",
      PART, SRE,
      "Multi-AZ architecture and cross-region backups exist; DR runbook written; "
      "but no full region-failover test has been executed against RTO/RPO.",
      "CP-2, CP-10, CP-4",
      gap="RTO (4h) / RPO (1h) defined but never validated by full DR failover "
          "test; DR exercise overdue.",
      remediation="Execute full us-east-1 to us-west-2 failover game-day; document "
                  "results vs RTO/RPO; remediate gaps.",
      target="Dec 2026", risk="High"),

    C("A.5.31", "Legal, statutory, regulatory and contractual requirements",
      "Organizational",
      "Identify, document and keep current the legal, statutory, regulatory and "
      "contractual requirements relevant to information security.",
      IMPL, LEGAL,
      "Legal & regulatory register (GDPR, CCPA/CPRA, state breach laws, contractual "
      "security obligations); reviewed semi-annually.",
      "PL-1, SA-4, PM-9"),

    C("A.5.32", "Intellectual property rights", "Organizational",
      "Implement procedures to protect intellectual property rights.",
      IMPL, LEGAL,
      "Open-source usage policy; license scanning (FOSSA) in CI; software asset "
      "register.",
      "CM-10, CM-10(1)"),

    C("A.5.33", "Protection of records", "Organizational",
      "Protect records from loss, destruction, falsification, unauthorized access "
      "and release.",
      IMPL, DPO,
      "Records-retention schedule; immutable audit logs (S3 Object Lock); "
      "financial/legal record protection.",
      "AU-9, AU-11, SI-12"),

    C("A.5.34", "Privacy and protection of PII", "Organizational",
      "Identify and meet requirements for the preservation of privacy and "
      "protection of personal identifiable information.",
      IMPL, DPO,
      "Privacy program; RoPA (Records of Processing); DPIA for ETA-prediction "
      "model; data-subject-request workflow; privacy notice.",
      "PT-1, PT-2, PT-3, PT-5"),

    C("A.5.35", "Independent review of information security", "Organizational",
      "Review the organization's approach to information security independently at "
      "planned intervals.",
      PART, CISO,
      "This first-party readiness assessment is the initial independent-style "
      "review; no prior independent review and no established cadence.",
      "CA-2, CA-7, PM-14",
      gap="No established independent-review cadence; prior to this assessment no "
          "independent review had been performed.",
      remediation="Charter annual independent review (internal audit + external "
                  "assessor at certification); schedule in ISMS calendar.",
      target="Mar 2027", risk="Low"),

    C("A.5.36", "Compliance with policies, rules and standards for information "
      "security", "Organizational",
      "Regularly review compliance with the organization's own security policies "
      "and standards.",
      PART, CISO,
      "Vanta continuously monitors ~80 automated checks; but manual policy-"
      "compliance reviews (procedural controls) are not scheduled.",
      "CA-2, PM-14, CA-7",
      gap="Procedural (non-automatable) policy compliance not periodically "
          "reviewed; no internal control self-assessment calendar.",
      remediation="Establish internal control self-assessment schedule for "
                  "procedural controls.",
      target="Apr 2027", risk="Low"),

    C("A.5.37", "Documented operating procedures", "Organizational",
      "Document operating procedures and make them available to personnel who need "
      "them.",
      IMPL, SRE,
      "Runbook library in Confluence (deployments, backup/restore, incident, "
      "on-call); version-controlled.",
      "SA-5, CM-9"),

    # =====================================================================
    # A.6 — People controls (8)
    # =====================================================================
    C("A.6.1", "Screening", "People",
      "Perform background verification checks on candidates commensurate with "
      "business requirements and perceived risks.",
      IMPL, PEOPLE,
      "Pre-employment background checks (Checkr) for all hires; records retained "
      "in HRIS; enhanced checks for privileged roles.",
      "PS-3, PS-3(1)"),

    C("A.6.2", "Terms and conditions of employment", "People",
      "State personnel and organizational information-security responsibilities in "
      "employment agreements.",
      IMPL, PEOPLE,
      "Employment contracts include security & confidentiality clauses; contractor "
      "agreements mirror them.",
      "PS-6, PL-4"),

    C("A.6.3", "Information security awareness, education and training", "People",
      "Provide appropriate security awareness, education and training with regular "
      "updates.",
      PART, PEOPLE,
      "Annual security-awareness training (KnowBe4) with 96% completion; but no "
      "role-based secure-development training and phishing simulations are ad hoc.",
      "AT-2, AT-3, AT-2(1)",
      gap="No role-based training for developers/admins; phishing-simulation "
          "program not run on a regular cadence.",
      remediation="Add annual secure-coding training for engineers; schedule "
                  "quarterly phishing simulations.",
      target="Feb 2027", risk="Low"),

    C("A.6.4", "Disciplinary process", "People",
      "Formalize and communicate a disciplinary process to act against personnel "
      "who commit security violations.",
      IMPL, PEOPLE,
      "Disciplinary process in employee handbook; referenced in AUP; HR case-"
      "handling procedure.",
      "PS-8"),

    C("A.6.5", "Responsibilities after termination or change of employment",
      "People",
      "Define, enforce and communicate security responsibilities that remain valid "
      "after termination or change of employment.",
      IMPL, PEOPLE,
      "Offboarding procedure revokes access same-day; continuing-confidentiality "
      "clause; exit acknowledgement.",
      "PS-4, PS-5"),

    C("A.6.6", "Confidentiality or non-disclosure agreements", "People",
      "Identify, document and regularly review NDA requirements.",
      IMPL, LEGAL,
      "NDAs signed by employees, contractors and relevant third parties; template "
      "reviewed by counsel.",
      "PS-6"),

    C("A.6.7", "Remote working", "People",
      "Implement security measures for personnel working remotely.",
      IMPL, PLAT,
      "Remote-work security standard; company-managed laptops (JAMF/Intune MDM); "
      "full-disk encryption; VPN/ZTNA for admin access.",
      "AC-17, AC-17(1), PL-4"),

    C("A.6.8", "Information security event reporting", "People",
      "Provide a mechanism for personnel to report observed or suspected security "
      "events in a timely manner.",
      PART, CISO,
      "#security-report Slack channel and security@ inbox exist; but no defined "
      "SLA, ticketing, or awareness of the reporting path for all staff.",
      "IR-6, AT-2",
      gap="Reporting channels exist but lack an SLA and formal intake/triage "
          "workflow; ~30% of staff unaware of the path (survey).",
      remediation="Publish reporting SLA; route to ticketed intake; reinforce in "
                  "awareness training.",
      target="Jan 2027", risk="Low"),

    # =====================================================================
    # A.7 — Physical controls (14)
    # =====================================================================
    C("A.7.1", "Physical security perimeters", "Physical",
      "Define and use security perimeters to protect areas that contain "
      "information and associated assets.",
      IMPL, OFFICE,
      "Austin office in access-controlled building; badge perimeter; data-center "
      "perimeter inherited from AWS (SOC 2 / ISO 27001 attestation).",
      "PE-3, PE-6"),

    C("A.7.2", "Physical entry", "Physical",
      "Protect secure areas by appropriate entry controls and access points.",
      IMPL, OFFICE,
      "Badge-access system with logs; visitor sign-in and escort policy; "
      "reception control.",
      "PE-2, PE-3"),

    C("A.7.3", "Securing offices, rooms and facilities", "Physical",
      "Design and implement physical security for offices, rooms and facilities.",
      IMPL, OFFICE,
      "Lockable server/network closet (office switch gear only); restricted rooms; "
      "no production data stored on-premises.",
      "PE-3, PE-5"),

    C("A.7.4", "Physical security monitoring", "Physical",
      "Continuously monitor premises for unauthorized physical access.",
      PART, OFFICE,
      "Office CCTV at entrances; but no monitored intrusion alarm and camera "
      "footage retention is undocumented.",
      "PE-6, PE-6(1)",
      gap="No monitored alarm service; CCTV retention period and review process "
          "not documented.",
      remediation="Contract monitored alarm; document CCTV retention (30 days) and "
                  "review responsibilities.",
      target="Mar 2027", risk="Low"),

    C("A.7.5", "Protecting against physical and environmental threats", "Physical",
      "Design and implement protection against physical and environmental threats.",
      IMPL, OFFICE,
      "Fire detection/suppression and environmental controls in office (landlord); "
      "data-center environmental protection inherited from AWS.",
      "PE-13, PE-14, PE-15"),

    C("A.7.6", "Working in secure areas", "Physical",
      "Design and implement security measures for working in secure areas.",
      NA, OFFICE,
      "N/A — Sightline operates no designated high-security processing zones or "
      "labs; all production processing occurs in AWS. No on-premises secure area "
      "handles Restricted data, so specific secure-area working procedures do not "
      "apply. (Applicability reviewed 2026-08; SoA §A.7.6.)",
      "PE-3",
      risk="N/A"),

    C("A.7.7", "Clear desk and clear screen", "Physical",
      "Define and enforce clear-desk rules for papers and media and clear-screen "
      "rules for information-processing facilities.",
      PART, OFFICE,
      "Clear-screen enforced via MDM auto-lock; clear-desk policy exists but "
      "enforcement is inconsistent and unaudited.",
      "AC-11, MP-2",
      gap="Clear-desk compliance not audited; occasional printed shipment "
          "manifests left at desks (spot check).",
      remediation="Quarterly clear-desk walk-through; secure-print + shredding "
                  "reinforcement.",
      target="Feb 2027", risk="Low"),

    C("A.7.8", "Equipment siting and protection", "Physical",
      "Site and protect equipment securely.",
      IMPL, OFFICE,
      "Only end-user laptops and office network gear on premises; positioned to "
      "reduce risk; servers reside in AWS.",
      "PE-18"),

    C("A.7.9", "Security of assets off-premises", "Physical",
      "Protect off-site assets.",
      PART, PLAT,
      "Laptops MDM-enrolled and encrypted; but no full asset-tracking/geolocation "
      "and off-site asset register incomplete.",
      "PE-17, MP-5",
      gap="Off-premises asset register incomplete; no lost-device tracking beyond "
          "remote wipe; ~10% of laptops missing last-seen data.",
      remediation="Reconcile MDM inventory; enable device location/lost-mode; "
                  "complete off-site asset register.",
      target="Jan 2027", risk="Low"),

    C("A.7.10", "Storage media", "Physical",
      "Manage storage media through acquisition, use, transport and disposal per "
      "the classification scheme.",
      NA, PLAT,
      "N/A — Removable storage media are prohibited and USB mass-storage is blocked "
      "by MDM policy; all data resides in AWS managed services. No removable media "
      "lifecycle to manage. (Applicability reviewed 2026-08; SoA §A.7.10.)",
      "MP-2, MP-4, MP-6, MP-7",
      risk="N/A"),

    C("A.7.11", "Supporting utilities", "Physical",
      "Protect information-processing facilities from power failures and other "
      "disruptions caused by failures in supporting utilities.",
      NA, OFFICE,
      "N/A — No organization-owned information-processing facility. Production "
      "supporting utilities (power, cooling, redundancy) are inherited from AWS "
      "under the shared-responsibility model (AWS SOC 2 report on file). Office "
      "utilities support end-user devices only, not information processing. "
      "(Applicability reviewed 2026-08; SoA §A.7.11.)",
      "PE-9, PE-11, PE-12",
      risk="N/A"),

    C("A.7.12", "Cabling security", "Physical",
      "Protect cabling carrying power, data or supporting information services from "
      "interception, interference or damage.",
      NA, OFFICE,
      "N/A — No organization-owned data-center cabling. Production network cabling "
      "is AWS-managed (inherited). Office structured cabling carries no production "
      "or Restricted data. (Applicability reviewed 2026-08; SoA §A.7.12.)",
      "PE-4, PE-9",
      risk="N/A"),

    C("A.7.13", "Equipment maintenance", "Physical",
      "Maintain equipment correctly to ensure availability, integrity and "
      "confidentiality of information.",
      IMPL, PLAT,
      "Laptop refresh cycle and vendor maintenance for office gear; data-center "
      "equipment maintenance inherited from AWS.",
      "MA-2, MA-4"),

    C("A.7.14", "Secure disposal or re-use of equipment", "Physical",
      "Verify equipment containing storage media is sanitized before disposal or "
      "re-use.",
      PART, PLAT,
      "MDM remote-wipe on decommission and disk encryption reduce risk; but no "
      "certificates of data destruction retained for disposed laptops.",
      "MP-6, MP-6(1)",
      gap="No documented sanitization verification or certificates of destruction "
          "for disposed/returned devices.",
      remediation="Adopt certified ITAD vendor; retain certificates of "
                  "destruction; log sanitization in asset register.",
      target="Feb 2027", risk="Low"),

    # =====================================================================
    # A.8 — Technological controls (34)
    # =====================================================================
    C("A.8.1", "User endpoint devices", "Technological",
      "Protect information stored on, processed by or accessible via user endpoint "
      "devices.",
      IMPL, PLAT,
      "MDM (JAMF/Intune) baseline; full-disk encryption; EDR (CrowdStrike); "
      "screen-lock; endpoint compliance gates ZTNA access.",
      "AC-19, SC-28, SI-3"),

    C("A.8.2", "Privileged access rights", "Technological",
      "Restrict and manage allocation and use of privileged access rights.",
      PART, PLAT,
      "AWS admin via SSO roles with MFA; production access needs approval; but "
      "some standing admin access remains and no session recording / JIT for all "
      "privileged paths.",
      "AC-6, AC-6(1), AC-6(5), AC-2(7)",
      gap="Standing privileged access to production for 6 accounts; no just-in-time "
          "elevation or privileged-session logging for database break-glass.",
      remediation="Adopt JIT elevation (AWS IAM Identity Center + approval); remove "
                  "standing admin; enable session logging.",
      target="Dec 2026", risk="High"),

    C("A.8.3", "Information access restriction", "Technological",
      "Restrict access to information and associated assets per the access-control "
      "policy.",
      IMPL, VPENG,
      "Application RBAC; per-tenant row-level isolation enforced and tested; "
      "least-privilege data access; deny-by-default.",
      "AC-3, AC-6, AC-24"),

    C("A.8.4", "Access to source code", "Technological",
      "Appropriately manage read and write access to source code, development "
      "tools and software libraries.",
      IMPL, VPENG,
      "GitHub with SSO/SAML; branch protection; CODEOWNERS; least-privilege repo "
      "roles; no direct main commits.",
      "AC-3, CM-5, SA-10"),

    C("A.8.5", "Secure authentication", "Technological",
      "Implement secure authentication technologies and procedures based on access "
      "restrictions and the access-control policy.",
      IMPL, PLAT,
      "SSO everywhere; phishing-resistant MFA (WebAuthn/FIDO2) for admins; TOTP for "
      "users; session controls; brute-force lockout.",
      "IA-2, IA-2(1), IA-2(2), IA-2(8)"),

    C("A.8.6", "Capacity management", "Technological",
      "Monitor and adjust the use of resources in line with capacity requirements.",
      IMPL, SRE,
      "Kubernetes HPA/cluster autoscaling; capacity dashboards; forecasting; alert "
      "thresholds on saturation.",
      "SC-5, AU-4, CP-2(2)"),

    C("A.8.7", "Protection against malware", "Technological",
      "Protect against malware, supported by user awareness.",
      IMPL, PLAT,
      "EDR on endpoints; container image scanning (Trivy) blocking on critical; "
      "email malware filtering (Google Workspace).",
      "SI-3, SI-3(1), SI-8"),

    C("A.8.8", "Management of technical vulnerabilities", "Technological",
      "Obtain information about technical vulnerabilities, evaluate exposure and "
      "take appropriate measures.",
      PART, PLAT,
      "Snyk (dependencies), AWS Inspector (hosts/images) and quarterly external "
      "scans run; but patch/remediation SLAs are defined yet not consistently met.",
      "RA-5, RA-5(2), SI-2, SI-2(3)",
      gap="Remediation SLA (Critical 7d / High 30d) missed for ~35% of findings; "
          "no single tracked vulnerability-remediation backlog with aging.",
      remediation="Consolidate findings into one backlog with SLA aging; enforce "
                  "KEV-first prioritization; monthly exec metric.",
      target="Nov 2026", risk="High"),

    C("A.8.9", "Configuration management", "Technological",
      "Establish, document, implement, monitor and review configurations of "
      "hardware, software, services and networks.",
      PART, PLAT,
      "Infrastructure as Code (Terraform) with peer review; hardening baselines "
      "(CIS) applied; but drift detection is not enabled across all accounts.",
      "CM-2, CM-3, CM-6, CM-6(1)",
      gap="Configuration drift not continuously detected in all AWS accounts; no "
          "automated remediation of out-of-baseline resources.",
      remediation="Enable AWS Config conformance packs + drift alerts across all "
                  "accounts; auto-remediate high-risk drift.",
      target="Jan 2027", risk="Medium"),

    C("A.8.10", "Information deletion", "Technological",
      "Delete information stored in systems, devices or any other media when no "
      "longer required.",
      PART, DPO,
      "Retention schedule defined; customer-data deletion on offboarding performed "
      "but partly manual; backup expiry automated.",
      "SI-12, MP-6, AU-11",
      gap="Tenant-offboarding deletion is a manual runbook step; no automated "
          "verification that all data stores (incl. logs/derived data) are purged.",
      remediation="Automate tenant-deletion workflow with completion evidence "
                  "across all stores; verify against RoPA.",
      target="Feb 2027", risk="Medium"),

    C("A.8.11", "Data masking", "Technological",
      "Use data masking per the access-control and business requirements, taking "
      "account of applicable legislation.",
      NOIM, VPENG,
      "No masking/pseudonymization in non-production; production copies with real "
      "customer PII have been used to seed staging.",
      "SC-28, AC-4, PT-3",
      gap="Real customer PII present in staging/non-prod without masking — elevated "
          "exposure and privacy risk; violates data-minimization intent.",
      remediation="Implement synthetic/masked data-generation for non-prod; purge "
                  "existing PII from staging; block prod-to-nonprod data copies.",
      target="Nov 2026", risk="High"),

    C("A.8.12", "Data leakage prevention", "Technological",
      "Apply data-leakage-prevention measures to systems, networks and devices "
      "that process, store or transmit sensitive information.",
      NOIM, CISO,
      "No dedicated DLP tooling for email, endpoints or cloud storage.",
      "AC-4, SC-7(10), SI-4(4)",
      gap="No DLP coverage for egress channels (email, SaaS, endpoint); reliance on "
          "policy only; limited detection of sensitive-data exfiltration.",
      remediation="Deploy DLP for Google Workspace + endpoints; start with "
                  "detect-only on Restricted data patterns.",
      target="Mar 2027", risk="Medium"),

    C("A.8.13", "Information backup", "Technological",
      "Maintain and regularly test backup copies of information, software and "
      "systems per the backup policy.",
      IMPL, SRE,
      "Automated RDS snapshots + PITR; S3 cross-region replication with "
      "versioning/Object Lock; monthly restore tests with records.",
      "CP-9, CP-9(1), CP-10"),

    C("A.8.14", "Redundancy of information processing facilities", "Technological",
      "Implement information-processing facilities with sufficient redundancy to "
      "meet availability requirements.",
      IMPL, SRE,
      "Multi-AZ deployments; stateless services behind load balancers; managed "
      "database HA (Multi-AZ RDS).",
      "CP-2(2), SC-6, CP-10"),

    C("A.8.15", "Logging", "Technological",
      "Produce, store, protect and analyse logs that record activities, exceptions, "
      "faults and other relevant events.",
      IMPL, SRE,
      "CloudTrail (all accounts), VPC flow logs, app/audit logs centralized in a "
      "SIEM; log integrity via S3 Object Lock; 400-day retention.",
      "AU-2, AU-3, AU-6, AU-9, AU-11"),

    C("A.8.16", "Monitoring activities", "Technological",
      "Monitor networks, systems and applications for anomalous behaviour and take "
      "appropriate actions to evaluate potential incidents.",
      PART, CISO,
      "24/7 MDR monitors infrastructure and endpoint telemetry; but application-"
      "layer security monitoring (abuse, authz anomalies) has coverage gaps.",
      "SI-4, SI-4(2), AU-6, AU-6(1)",
      gap="Limited application-layer detections (business-logic abuse, tenant "
          "boundary anomalies); alerting tuned mostly to infra/endpoint.",
      remediation="Add application-layer detections and tenant-isolation anomaly "
                  "alerts to SIEM; define use-case coverage matrix.",
      target="Feb 2027", risk="Medium"),

    C("A.8.17", "Clock synchronization", "Technological",
      "Synchronize clocks of information-processing systems to approved time "
      "sources.",
      IMPL, SRE,
      "Amazon Time Sync Service (NTP) across fleet; consistent UTC timestamps in "
      "logs verified.",
      "AU-8, AU-8(1)"),

    C("A.8.18", "Use of privileged utility programs", "Technological",
      "Restrict and tightly control the use of utility programs capable of "
      "overriding system and application controls.",
      PART, PLAT,
      "Admin tooling limited to authorized staff; but no formal inventory or "
      "logging of powerful CLI/utility usage on production hosts.",
      "AC-6(9), AC-6(10), CM-7",
      gap="No inventory or dedicated logging of privileged utility usage; reliance "
          "on general admin controls.",
      remediation="Inventory privileged utilities; restrict via allow-listing; log "
                  "and alert on their use.",
      target="Apr 2027", risk="Low"),

    C("A.8.19", "Installation of software on operational systems", "Technological",
      "Implement procedures and measures to securely manage software installation "
      "on operational systems.",
      IMPL, PLAT,
      "Immutable infrastructure; no manual installs on production; deployments via "
      "signed CI artifacts; container image allow-list.",
      "CM-7, CM-11, CM-5, SI-7"),

    C("A.8.20", "Networks security", "Technological",
      "Secure, manage and control networks and network devices to protect "
      "information in systems and applications.",
      IMPL, PLAT,
      "VPC with private subnets; security groups (deny-by-default); managed WAF; "
      "TLS termination; no public database exposure.",
      "SC-7, SC-7(3), SC-7(5), AC-4"),

    C("A.8.21", "Security of network services", "Technological",
      "Identify, implement and monitor security mechanisms, service levels and "
      "requirements of network services.",
      IMPL, PLAT,
      "Network-service security requirements documented; TLS 1.2+; managed "
      "load-balancer/CDN with security SLAs; DDoS protection (Shield).",
      "SC-7, SA-9, CA-3"),

    C("A.8.22", "Segregation of networks", "Technological",
      "Segregate groups of information services, users and information systems in "
      "networks.",
      IMPL, PLAT,
      "Environment and tier segmentation (VPC/subnets, security groups); prod "
      "isolated from dev/test; namespace network policies in EKS.",
      "SC-7, SC-7(21), AC-4"),

    C("A.8.23", "Web filtering", "Technological",
      "Manage access to external websites to reduce exposure to malicious content.",
      NA, PLAT,
      "N/A — No centralized corporate web gateway/proxy operates. The control "
      "objective is met through other controls: endpoint DNS/web protection is "
      "delivered by EDR (A.8.1) and server egress is constrained by VPC egress "
      "controls (A.8.20). Standalone web filtering is therefore not applicable as a "
      "separate control. (Applicability reviewed 2026-08; SoA §A.8.23.)",
      "SC-7(8), SC-18",
      risk="N/A"),

    C("A.8.24", "Use of cryptography", "Technological",
      "Define and implement rules for effective use of cryptography, including key "
      "management.",
      IMPL, PLAT,
      "Cryptography standard (TLS 1.2+ in transit, AES-256 at rest); AWS KMS "
      "customer-managed keys with rotation; no deprecated ciphers (config-scanned).",
      "SC-13, SC-12, SC-12(2), SC-28(1)"),

    C("A.8.25", "Secure development life cycle", "Technological",
      "Establish and apply rules for the secure development of software and "
      "systems.",
      PART, VPENG,
      "SDLC uses PR review, CI checks and a security checklist; but a formal, "
      "documented secure-SDLC standard with defined security gates is not ratified.",
      "SA-3, SA-15, SA-8",
      gap="Secure-SDLC practices exist informally; no ratified standard mapping "
          "security activities/gates to each SDLC phase.",
      remediation="Author and ratify Secure SDLC standard; define phase gates "
                  "(threat modeling, SAST, review).",
      target="Feb 2027", risk="Medium"),

    C("A.8.26", "Application security requirements", "Technological",
      "Identify, specify and approve information-security requirements when "
      "developing or acquiring applications.",
      IMPL, PRODUCT,
      "Security requirements captured in RFC/PRD templates (authz, data-class, "
      "logging, privacy); OWASP ASVS-aligned checklist for new features.",
      "SA-4, SA-8, SA-15"),

    C("A.8.27", "Secure system architecture and engineering principles",
      "Technological",
      "Establish, document, maintain and apply principles for engineering secure "
      "systems.",
      IMPL, CTO,
      "Documented architecture principles (defense-in-depth, least privilege, "
      "zero-trust for admin, tenant isolation); architecture review for new "
      "services.",
      "SA-8, SA-8(1), PL-8"),

    C("A.8.28", "Secure coding", "Technological",
      "Apply secure-coding principles to software development.",
      PART, VPENG,
      "Linters, dependency scanning and code review in place; but no documented "
      "secure-coding standard and SAST is not enforced as a merge gate.",
      "SA-11, SA-11(1), SA-15(5)",
      gap="No formal secure-coding standard; SAST runs advisory-only, not blocking; "
          "inconsistent developer secure-coding guidance.",
      remediation="Adopt secure-coding standard (language-specific); enable SAST as "
                  "blocking gate for high-severity findings.",
      target="Feb 2027", risk="Medium"),

    C("A.8.29", "Security testing in development and acceptance", "Technological",
      "Define and implement security-testing processes in the development life "
      "cycle.",
      PART, VPENG,
      "Annual third-party penetration test; dependency/container scanning in CI; "
      "but DAST is partial and no security acceptance gate before release.",
      "SA-11, CA-8, SA-11(8)",
      gap="No consistent DAST coverage; no defined security acceptance criteria "
          "gating releases; pentest findings remediation not SLA-tracked.",
      remediation="Add DAST to pre-prod pipeline; define release security-"
                  "acceptance gate; track pentest findings to closure.",
      target="Dec 2026", risk="High"),

    C("A.8.30", "Outsourced development", "Technological",
      "Direct, monitor and review outsourced system-development activity.",
      NA, VPENG,
      "N/A — All software development is performed in-house by employed engineers. "
      "Sightline uses no outsourced or contract development houses, so outsourced-"
      "development oversight controls do not apply. (Applicability reviewed 2026-08; "
      "if outsourcing is later adopted this control will be re-scoped. SoA §A.8.30.)",
      "SA-4, SA-10, SR-3",
      risk="N/A"),

    C("A.8.31", "Separation of development, test and production environments",
      "Technological",
      "Separate and secure development, testing and production environments.",
      IMPL, PLAT,
      "Separate AWS accounts per environment; no shared credentials; promotion via "
      "CI only; network isolation between environments.",
      "CM-4, CM-4(1), SC-7"),

    C("A.8.32", "Change management", "Technological",
      "Subject changes to information-processing facilities and systems to change-"
      "management procedures.",
      IMPL, PLAT,
      "Change management via pull requests + CI/CD with approvals; change log; "
      "emergency-change procedure; rollback plans.",
      "CM-3, CM-3(2), CM-4, SA-10"),

    C("A.8.33", "Test information", "Technological",
      "Appropriately select, protect and manage test information.",
      NOIM, VPENG,
      "Test/staging environments have been seeded from production data containing "
      "real customer PII without protection.",
      "SA-15(9), PT-3, SC-28",
      gap="Production customer PII used as test data in staging without masking or "
          "controls — critical privacy and confidentiality exposure.",
      remediation="Prohibit prod data in test; replace with synthetic/masked "
                  "datasets; purge existing test PII and add pipeline guardrails.",
      target="Nov 2026", risk="Critical"),

    C("A.8.34", "Protection of information systems during audit testing",
      "Technological",
      "Plan and agree audit tests and other assurance activities involving "
      "operational systems with management to protect systems.",
      IMPL, CISO,
      "Audit/assessment activities scoped and scheduled with owners; read-only, "
      "time-boxed audit accounts; assurance-testing procedure.",
      "AU-5, CA-2, RA-5(4)"),
]

# ---------------------------------------------------------------------------
# Sanity check on load
# ---------------------------------------------------------------------------
assert len(CONTROLS) == 93, f"Expected 93 controls, got {len(CONTROLS)}"
_ids = [c["id"] for c in CONTROLS]
assert len(set(_ids)) == 93, "Duplicate control IDs detected"

THEME_ORDER = ["Organizational", "People", "Physical", "Technological"]
STATUS_ORDER = [IMPL, PART, NOIM, NA]
RISK_ORDER = ["Critical", "High", "Medium", "Low"]
