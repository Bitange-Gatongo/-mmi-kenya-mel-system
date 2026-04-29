# Community HTS Register — XLSForm Documentation

## Purpose

Data collection instrument for Community Health Volunteers (CHVs) conducting
HIV Testing Services (HTS) at community testing points in Nairobi County
informal settlements. Designed to capture individual client testing encounters
and support 30-day linkage tracking for HIV-positive individuals.

---

## Deployment Context

| Item | Detail |
|---|---|
| **Program** | MMI Kenya HIV/PMTCT Community Health Program |
| **Data collectors** | Trained CHVs at community testing points |
| **Collection mode** | KoBoToolbox Collect app — Android tablet |
| **Connectivity** | Offline-capable — submits when connectivity available |
| **Language** | English (Swahili translation recommended for field deployment) |
| **Average completion time** | 4–6 minutes per client encounter |

---

## Form Structure — 6 Sections

### Section 1 — Form Metadata (automatic)
Captures device ID, username, start/end timestamps, and GPS coordinates
automatically. No interviewer input required. Enables data quality monitoring
— falsified submissions detectable through GPS clustering and timestamp analysis.

### Section 2 — Session Information
Date, sub-location, testing modality, CHV identity. Provides the organizational
context linking the record to a specific facility, period, and data collector.

### Section 3 — Client Demographics
Age, age group, gender, first-test status, key population status, pregnancy
and breastfeeding status. Gender questions have relevant conditions — pregnancy
and breastfeeding questions only appear for female clients.

### Section 4 — HIV Testing
Test result, confirmatory test completion, result receipt, counselling
completion. Second test question only appears when result is positive —
enforcing the national testing algorithm requirement.

### Section 5 — Referral and Linkage
Referral outcome, facility, slip number, appointment date, client phone number,
barriers. Entire section only appears when result is positive. Phone number
validated against Kenya mobile format (07XXXXXXXX or 01XXXXXXXX).

### Section 6 — Quality Assurance
Consent verification, privacy confirmation, supervisor comments. Non-negotiable
fields ensuring ethical data collection standards are documented per encounter.

---

## Variable Reference

| Variable | Type | Description | DHIS2 mapping |
|---|---|---|---|
| `session_date` | date | Date of testing session | Period (YYYYMM) |
| `sub_location` | select_one | Testing point sub-location | Org unit UID |
| `hts_result` | select_one | HIV test result | HTS_TST / HTS_TST_POS |
| `referral_outcome` | select_one | Referral acceptance status | HTS_REFERRAL |
| `art_initiated` | select_one | ART initiation at facility | HTS_LINKED_30 |
| `client_age` | integer | Client age in years | Age disaggregation |
| `client_gender` | select_one | Client gender | Sex disaggregation |
| `kp_status` | select_one | Key population type | KP disaggregation |
| `gps_location` | geopoint | GPS coordinates of testing point | Quality assurance |

---

## Key Design Decisions

**Client ID not client name**
All records use a program-assigned client ID. Names are never recorded on the
digital form — protecting client confidentiality if a device is lost or
accessed without authorization. Names are recorded in a separate secure
paper register linked to the client ID.

**GPS on every record**
GPS coordinates are captured at session start for every form submission.
The pipeline cross-references GPS coordinates against expected testing point
locations during data quality review — enabling detection of falsified
submissions where an interviewer completes forms without conducting visits.

**Declined tests excluded from HTS_TST**
Per PEPFAR MER guidance, clients who decline testing are not counted in
HTS_TST. The pipeline aggregation explicitly excludes records where
`hts_result = declined` from the HTS_TST count.

**Phone number constraint**
Client phone numbers are validated using a regex constraint requiring Kenya
mobile format. This ensures follow-up contacts for positive clients are
actionable — preventing invalid numbers from entering the linkage tracking
system.

---

## Skip Logic Summary

| Question | Appears when |
|---|---|
| Pregnancy status | `client_gender = female` |
| Breastfeeding status | `client_gender = female AND pregnant = no` |
| Second test done | `hts_result = positive` |
| Result received | `hts_result ≠ declined` |
| Counselling done | `hts_result ≠ declined` |
| Entire referral section | `hts_result = positive` |
| Referral facility name | `referral_outcome = accepted` |
| Referral slip number | `referral_outcome = accepted` |
| Appointment date | `referral_outcome = accepted` |
| Client phone | `referral_outcome = accepted` |
| Linkage barriers | `referral_outcome = declined` |
| Follow-up section | `hts_result = positive AND referral_outcome = accepted` |
| ART number | `art_initiated = yes` |

---

## Constraint Validation

| Field | Constraint | Error message |
|---|---|---|
| `client_age` | >= 10 AND <= 80 | Age must be between 10 and 80 |
| `session_date` | <= today() | Date cannot be in the future |
| `appointment_date` | > session_date | Appointment must be after today's session |
| `client_phone` | regex Kenya mobile format | Enter valid Kenya number (07/01XXXXXXXX) |
| `art_number` | string-length >= 8 | ART number must be at least 8 characters |

---

## Version History

| Version | Date | Changes |
|---|---|---|
| v1.0 | 2024-01-01 | Initial deployment version |

---

## Deployment Instructions

1. Download `mmi_hts_v1.xlsx`
2. Log into KoBoToolbox at kf.kobotoolbox.org
3. Click **New** → **Upload an XLSForm**
4. Upload the file — resolve any validation errors
5. Click **Deploy**
6. Install KoBoToolbox Collect on CHV Android devices
7. Log in with CHV KoBoToolbox credentials
8. Download the form to device
9. Test all skip logic paths before field deployment
10. Delete test submissions before going live
