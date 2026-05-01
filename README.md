<div align="center">

# Alex Gatongo Arasa
### Health Informatics & MEAL Professional | Clinical Officer | DHIS2 Specialist

*Bridging frontline clinical practice and data systems to make health program evidence actionable*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-arasa-316b54214)
[![Portfolio](https://img.shields.io/badge/Portfolio-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://gatongoalex.netlify.app)
[![DHIS2](https://img.shields.io/badge/DHIS2_Certified-1A73E8?style=for-the-badge&logo=databricks&logoColor=white)](#certifications)

</div>

---

## Who I Am

I am a registered Clinical Officer based in Nairobi, Kenya, with hands-on experience in HIV/PMTCT care, community health, and facility-level program delivery. Over the past two years I have systematically built a parallel expertise in health informatics and monitoring, evaluation, and learning — not as a theoretical pursuit, but by building real systems that solve real data problems in the Kenyan health context.

I design and implement end-to-end data pipelines, configure DHIS2 for program-specific indicator tracking, and translate clinical program logic into structured M&E frameworks. My work sits at the intersection of two roles that are usually separate — MEAL practitioner and health informatics technician — and I bring both to every project.

---

## ⚡ Key Achievements

- 🔁 **Built a production-grade KoBo → DHIS2 pipeline** for an HIV/PMTCT program portfolio — handling form design, data cleaning, SQL aggregation, UID validation, dry-run pre-checks, and automated import logging
- 📊 **Configured DHIS2 end-to-end** — data elements, indicators, category combos, org unit hierarchies, validation rules, and program dashboards for Garissa County and MMI Kenya contexts
- 🗺️ **Built a GIS malaria burden mapping dashboard** for Garissa County using DHIS2 Maps and real facility-level data
- 📋 **Designed full M&E frameworks** for HIV, PMTCT, and NCD programs including Theory of Change, log frames, indicator matrices, DQA protocols, and PEPFAR MER alignment (TX_CURR, TX_PVLS, HTS, KP)
- 🎓 **6 DHIS2 Academy certifications** — Aggregate Customization, Data Analysis, Data Capture & Validation, Event Configuration, Planning & Budgeting, and Tracker
- 📝 **Registered Clinical Officer** — active PMTCT and HTS program experience at facility level, giving my data systems clinical credibility that pure informaticians lack

---

## 🔁 Featured Project: KoBo → DHIS2 Automated Data Pipeline

> *Solving the data silos that make health programs fly blind*

Most health programs collect data at the community level and aggregate it manually — weeks later, in spreadsheets, by programme officers who are already stretched thin. This pipeline automates that entire cycle.

### Data Flow

```mermaid
flowchart TD
    A[🏥 Community Health Workers\nKoBoToolbox ODK Forms] -->|Paginated API pull\nToken auth| B

    B[🐍 Python Cleaning Layer\nField validation · Period parsing\nOrg unit mapping · Error flagging]

    B -->|Cleaned records| C[(🗄️ SQLite Database\nhts_submissions\nmm_submissions\nvalidation_errors\nimport_log\nimport_conflicts)]

    C -->|SQL aggregation queries\nCOUNT · GROUP BY · DISTINCT| D

    D[📦 Payload Builder\nDataElement UIDs\nCategoryOptionCombo UIDs\nOrgUnit UIDs · Period strings]

    D -->|UID validation against\nDHIS2 metadata API| E{✅ UIDs Valid?}

    E -->|No — abort| F[❌ Validation Error Log\nWritten to DB]
    E -->|Yes| G

    G[🔍 DHIS2 Dry Run\ndryRun=true\nNo data committed]

    G -->|Conflicts found — abort| H[⚠️ Conflict Log\nimport_conflicts table]
    G -->|Clean — proceed| I

    I[✅ DHIS2 Live Import\ndataValueSets API\nFull import summary parsed]

    I --> J[📊 DHIS2 Dashboard\nIndicator visualisations\nFacility comparisons\nTrend analysis]

    style A fill:#E8F5E9,stroke:#388E3C
    style C fill:#E3F2FD,stroke:#1976D2
    style J fill:#FFF3E0,stroke:#F57C00
    style F fill:#FFEBEE,stroke:#D32F2F
    style H fill:#FFEBEE,stroke:#D32F2F
    style I fill:#E8F5E9,stroke:#388E3C
```

### What Makes This Pipeline Professional-Grade

| Layer | What it does | Why it matters |
|---|---|---|
| **SQL storage** | All raw submissions stored in SQLite before aggregation | Creates an auditable data trail — every record, every run |
| **SQL aggregation** | Indicators computed via GROUP BY queries, DISTINCT for deduplication | Reproducible, queryable, not locked in pandas memory |
| **UID validation** | Checks all dataElement and orgUnit UIDs against live DHIS2 metadata | Catches category combo mismatches before any import attempt |
| **Dry run** | `dryRun=true` pre-check — DHIS2 validates without committing | Zero risk of partial imports or silent failures |
| **Import log** | Every run logged to `import_log` with full conflict detail | Program managers have a queryable audit trail |
| **Env credentials** | No hardcoded secrets — all credentials via environment variables | Production-safe, shareable codebase |

### Indicators Tracked

**HTS (Community HIV Testing):** `HTS_TST` · `HTS_TST_POS` · `HTS_REFERRAL` · `HTS_LINKED_30`

**PMTCT / Mentor Mother:** `PMTCT_ENROLLED` · `PMTCT_CASCADE` · `PMTCT_DELIVERY` · `MM_CONTACTS` · `MM_QUALITY` · `EID_ELIGIBLE` · `EID_DONE`

### Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![KoBoToolbox](https://img.shields.io/badge/KoBoToolbox-5C9EDB?style=flat-square&logoColor=white)
![DHIS2](https://img.shields.io/badge/DHIS2_API-1A73E8?style=flat-square&logoColor=white)

📁 **[View pipeline code →](kobo_to_dhis2_pipeline_v2.py)**

---

## 📂 Portfolio Projects

### 🗺️ Garissa County Malaria GIS Burden Dashboard
Facility-level malaria burden mapping for Garissa County using DHIS2 Maps. Visualises case distribution across 5 health facilities, supporting targeted intervention planning in a high-burden arid-zone context.

`DHIS2 Maps` `GIS` `Malaria` `Garissa County`

📁 **[garissa_malaria_gis →](https://github.com/Bitange-Gatongo/garissa_malaria_gis)**

---

### ✅ HMIS Data Quality Assurance Framework
A structured DQA methodology for health management information systems — covering completeness, timeliness, accuracy, and internal consistency checks. Built around PEPFAR DQA standards and Kenya NASCOP reporting requirements.

`DHIS2` `DQA` `PEPFAR` `NASCOP` `KenyaEMR`

📁 **[hmis-dqa-framework →](https://github.com/Bitange-Gatongo/hmis-dqa-framework)**

---

### 💊 NCD Tracker — DHIS2 Programme Configuration
A DHIS2 Tracker programme for non-communicable disease patient follow-up — covering hypertension, diabetes, and chronic respiratory disease. Includes enrolment logic, program rules, indicators, and a facility-level management dashboard.

`DHIS2 Tracker` `NCD` `Program Rules` `Indicators`

📁 **[ncd_tracker_DHIS2 →](https://github.com/Bitange-Gatongo/ncd_tracker_DHIS2)**

---

## 🛠️ Technical Stack

### Health Data Systems
![DHIS2](https://img.shields.io/badge/DHIS2-1A73E8?style=flat&logo=databricks&logoColor=white)
![KoBoToolbox](https://img.shields.io/badge/KoBoToolbox-5C9EDB?style=flat&logoColor=white)
![KenyaEMR](https://img.shields.io/badge/KenyaEMR-009688?style=flat&logoColor=white)
![ODK](https://img.shields.io/badge/ODK-FF7043?style=flat&logoColor=white)

### Programming & Data
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-003B57?style=flat&logo=sqlite&logoColor=white)
![R](https://img.shields.io/badge/R-276DC3?style=flat&logo=r&logoColor=white)
![Excel](https://img.shields.io/badge/Excel-217346?style=flat&logo=microsoft-excel&logoColor=white)

### M&E Frameworks & Standards
![PEPFAR](https://img.shields.io/badge/PEPFAR_MER-C62828?style=flat&logoColor=white)
![GESI](https://img.shields.io/badge/GESI%2FUSAID_ADS205-7B1FA2?style=flat&logoColor=white)
![RBM](https://img.shields.io/badge/Results_Based_Management-00695C?style=flat&logoColor=white)
![LogFrame](https://img.shields.io/badge/LogFrame%2FToC-F57F17?style=flat&logoColor=white)

---

## 🎓 Certifications

| Certification | Issuer | Focus |
|---|---|---|
| DHIS2 Aggregate Customization | DHIS2 Academy | System configuration, data elements, indicators |
| DHIS2 Data Analysis | DHIS2 Academy | Pivot tables, charts, dashboards |
| DHIS2 Data Capture & Validation | DHIS2 Academy | Data entry, validation rules, quality |
| DHIS2 Event Configuration | DHIS2 Academy | Event programs, program rules |
| DHIS2 Planning & Budgeting | DHIS2 Academy | Organisational planning modules |
| DHIS2 Tracker Configuration | DHIS2 Academy | Individual-level program tracking |
| Afya Bora M&E Programme | Afya Bora | Applied M&E for health programs |

---

## ⚙️ Setup — Run the Pipeline Locally

```bash
# 1. Clone the repository
git clone https://github.com/Bitange-Gatongo/Bitange-Gatongo.git
cd Bitange-Gatongo

# 2. Install dependencies
pip install requests

# 3. Set credentials as environment variables (never hardcode)
export KOBO_API_TOKEN="your_kobo_token_here"
export DHIS2_USERNAME="admin"
export DHIS2_PASSWORD="district"
export DHIS2_BASE_URL="http://localhost:8080"   # or your remote instance

# 4. Ensure DHIS2 is running
# Local: Docker on port 8080
# Remote: set DHIS2_BASE_URL to your instance URL

# 5. Run the pipeline
python kobo_to_dhis2_pipeline_v2.py
```

### What the pipeline creates

```
mmi_pipeline.db       ← SQLite database (submissions, aggregations, import logs)
pipeline.log          ← Full run log with timestamps
```

### Query your data after a run

```sql
-- Check import history
SELECT run_at, status, imported, updated, conflict_count
FROM import_log ORDER BY run_at DESC;

-- See all conflicts from the last run
SELECT ic.object, ic.value
FROM import_conflicts ic
JOIN import_log il ON ic.run_id = il.id
ORDER BY il.run_at DESC LIMIT 20;

-- HTS aggregation by period
SELECT org_unit_uid, period, COUNT(*) as hts_tst
FROM hts_submissions
WHERE hts_result != 'declined' AND period IS NOT NULL
GROUP BY org_unit_uid, period;
```

---

## 📍 Context

Based in **Nairobi, Kenya** · Open to remote and field-based roles across East Africa

Currently targeting MEAL Officer, Health Informatics Officer, and HMIS roles with NGOs, UN agencies, and Ministry of Health implementing partners — particularly USAID, Global Fund, and UN-funded programs operating in Kenya.

---

<div align="center">

*"Good health data doesn't just happen. It is designed, cleaned, validated, and structured — before it ever reaches a dashboard."*

**[Portfolio](https://gatongoalex.netlify.app) · [LinkedIn](https://linkedin.com/in/alex-arasa-316b54214) · [Email](mailto:arasalex25@gmail.com)**

</div>
