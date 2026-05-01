"""
MMI Kenya Pipeline — Unit Tests
================================
Tests for data cleaning, aggregation logic, payload building,
and SQL layer. Run with:  python -m pytest test_pipeline.py -v

Author: Alex Gatongo Arasa
"""

import sqlite3
import pytest
from kobo_to_dhis2_pipeline_v2 import (
    date_to_period,
    get_org_unit,
    safe_get,
    init_db,
    store_hts_submissions,
    store_mm_submissions,
    aggregate_hts_sql,
    aggregate_mm_sql,
    build_payload,
    DE,
)

# ── FIXTURES ──────────────────────────────────────────────────────────────────

@pytest.fixture
def db():
    """In-memory SQLite database — isolated per test, no files written."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    init_db.__wrapped__(conn) if hasattr(init_db, "__wrapped__") else None
    # Recreate tables directly for in-memory test DB
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS hts_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kobo_id TEXT, session_date TEXT, period TEXT,
            sub_location TEXT, org_unit_uid TEXT,
            hts_result TEXT, referral_outcome TEXT, art_initiated TEXT,
            pulled_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS mm_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kobo_id TEXT, contact_date TEXT, period TEXT,
            mm_sub_location TEXT, org_unit_uid TEXT, client_id TEXT,
            contact_duration_minutes INTEGER, cascade_status TEXT,
            infant_prophylaxis_given TEXT, eid_done TEXT,
            pulled_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS validation_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            form_type TEXT, kobo_id TEXT, error_type TEXT,
            error_detail TEXT, logged_at TEXT DEFAULT (datetime('now'))
        );
        CREATE TABLE IF NOT EXISTS import_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_at TEXT, dry_run INTEGER, status TEXT,
            imported INTEGER, updated INTEGER, ignored INTEGER,
            conflict_count INTEGER, total_values INTEGER, duration_sec INTEGER
        );
        CREATE TABLE IF NOT EXISTS import_conflicts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER REFERENCES import_log(id),
            object TEXT, value TEXT,
            logged_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    yield conn
    conn.close()


# ── date_to_period ─────────────────────────────────────────────────────────────

class TestDateToPeriod:

    def test_valid_date_returns_yearmonth(self):
        assert date_to_period("2024-03-15") == "202403"

    def test_datetime_string_truncated_correctly(self):
        assert date_to_period("2024-11-01T08:30:00") == "202411"

    def test_none_returns_none(self):
        assert date_to_period(None) is None

    def test_empty_string_returns_none(self):
        assert date_to_period("") is None

    def test_invalid_format_returns_none(self):
        assert date_to_period("15/03/2024") is None

    def test_december_boundary(self):
        assert date_to_period("2023-12-31") == "202312"

    def test_january_boundary(self):
        assert date_to_period("2024-01-01") == "202401"


# ── get_org_unit ───────────────────────────────────────────────────────────────

class TestGetOrgUnit:

    def test_known_location_returns_uid(self):
        uid = get_org_unit("korogocho")
        assert uid == "GRS012FGDSP"

    def test_known_location_mathare(self):
        uid = get_org_unit("mathare_north")
        assert uid == "GRS011FGHC1"

    def test_unknown_location_returns_none(self):
        assert get_org_unit("unknown_place") is None

    def test_empty_string_returns_none(self):
        assert get_org_unit("") is None

    def test_case_sensitive(self):
        # ORG_UNIT_MAP keys are lowercase — uppercase should fail
        assert get_org_unit("Korogocho") is None


# ── safe_get ───────────────────────────────────────────────────────────────────

class TestSafeGet:

    def test_existing_key(self):
        assert safe_get({"a": 1}, "a") == 1

    def test_missing_key_returns_default(self):
        assert safe_get({}, "missing") is None

    def test_missing_key_with_custom_default(self):
        assert safe_get({}, "missing", "N/A") == "N/A"

    def test_falsy_value_not_replaced_by_default(self):
        assert safe_get({"a": 0}, "a", 99) == 0

    def test_none_value_returned(self):
        assert safe_get({"a": None}, "a", "default") is None


# ── HTS SQL AGGREGATION ────────────────────────────────────────────────────────

class TestAggregateHtsSQL:

    def _load(self, db, rows):
        db.executemany("""
            INSERT INTO hts_submissions
                (kobo_id, session_date, period, sub_location, org_unit_uid,
                 hts_result, referral_outcome, art_initiated)
            VALUES (?,?,?,?,?,?,?,?)
        """, rows)
        db.commit()

    def test_basic_hts_tst_count(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "negative", None, None),
            ("2", "2024-03-05", "202403", "korogocho", "GRS012FGDSP", "positive", None, None),
        ])
        result = aggregate_hts_sql(db)
        assert result[("GRS012FGDSP", "202403")]["HTS_TST"] == 2

    def test_declined_excluded_from_hts_tst(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "negative", None, None),
            ("2", "2024-03-02", "202403", "korogocho", "GRS012FGDSP", "declined", None, None),
        ])
        result = aggregate_hts_sql(db)
        assert result[("GRS012FGDSP", "202403")]["HTS_TST"] == 1

    def test_hts_tst_pos_count(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "mukuru", "GRS013FGDHC", "positive", None, None),
            ("2", "2024-03-02", "202403", "mukuru", "GRS013FGDHC", "negative", None, None),
            ("3", "2024-03-03", "202403", "mukuru", "GRS013FGDHC", "positive", None, None),
        ])
        result = aggregate_hts_sql(db)
        assert result[("GRS013FGDHC", "202403")]["HTS_TST_POS"] == 2

    def test_hts_referral_count(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "positive", "accepted", None),
            ("2", "2024-03-02", "202403", "korogocho", "GRS012FGDSP", "positive", "declined", None),
        ])
        result = aggregate_hts_sql(db)
        assert result[("GRS012FGDSP", "202403")]["HTS_REFERRAL"] == 1

    def test_art_initiated_count(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "mukuru", "GRS013FGDHC", "positive", "accepted", "yes"),
            ("2", "2024-03-02", "202403", "mukuru", "GRS013FGDHC", "positive", "accepted", "no"),
        ])
        result = aggregate_hts_sql(db)
        assert result[("GRS013FGDHC", "202403")]["HTS_LINKED_30"] == 1

    def test_records_missing_period_excluded(self, db):
        self._load(db, [
            ("1", None, None, "korogocho", "GRS012FGDSP", "negative", None, None),
        ])
        result = aggregate_hts_sql(db)
        assert len(result) == 0

    def test_records_missing_org_unit_excluded(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "unknown", None, "negative", None, None),
        ])
        result = aggregate_hts_sql(db)
        assert len(result) == 0

    def test_multiple_periods_grouped_separately(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "negative", None, None),
            ("2", "2024-04-01", "202404", "korogocho", "GRS012FGDSP", "negative", None, None),
        ])
        result = aggregate_hts_sql(db)
        assert ("GRS012FGDSP", "202403") in result
        assert ("GRS012FGDSP", "202404") in result


# ── MM SQL AGGREGATION ─────────────────────────────────────────────────────────

class TestAggregateMmSQL:

    def _load(self, db, rows):
        db.executemany("""
            INSERT INTO mm_submissions
                (kobo_id, contact_date, period, mm_sub_location, org_unit_uid,
                 client_id, contact_duration_minutes, cascade_status,
                 infant_prophylaxis_given, eid_done)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, rows)
        db.commit()

    def test_mm_contacts_count(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "C001", 20, None, None, None),
            ("2", "2024-03-02", "202403", "korogocho", "GRS012FGDSP", "C002", 45, None, None, None),
        ])
        result = aggregate_mm_sql(db)
        assert result[("GRS012FGDSP", "202403")]["MM_CONTACTS"] == 2

    def test_mm_quality_threshold(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "mukuru", "GRS013FGDHC", "C001", 30, None, None, None),
            ("2", "2024-03-02", "202403", "mukuru", "GRS013FGDHC", "C002", 29, None, None, None),
            ("3", "2024-03-03", "202403", "mukuru", "GRS013FGDHC", "C003", 60, None, None, None),
        ])
        result = aggregate_mm_sql(db)
        # Only contacts >= 30 minutes count
        assert result[("GRS013FGDHC", "202403")]["MM_QUALITY"] == 2

    def test_pmtct_enrolled_deduplication(self, db):
        """Same client_id appearing twice in same period counts as 1 enrolled."""
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "C001", 20, None, None, None),
            ("2", "2024-03-10", "202403", "korogocho", "GRS012FGDSP", "C001", 35, None, None, None),  # repeat
            ("3", "2024-03-15", "202403", "korogocho", "GRS012FGDSP", "C002", 40, None, None, None),
        ])
        result = aggregate_mm_sql(db)
        assert result[("GRS012FGDSP", "202403")]["PMTCT_ENROLLED"] == 2  # C001 + C002

    def test_eid_eligible_count(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "mukuru", "GRS013FGDHC", "C001", 30, "eid_pending", None, None),
            ("2", "2024-03-02", "202403", "mukuru", "GRS013FGDHC", "C002", 30, "eid_done", None, "yes"),
            ("3", "2024-03-03", "202403", "mukuru", "GRS013FGDHC", "C003", 30, "delivered", None, None),
        ])
        result = aggregate_mm_sql(db)
        assert result[("GRS013FGDHC", "202403")]["EID_ELIGIBLE"] == 2  # eid_pending + eid_done
        assert result[("GRS013FGDHC", "202403")]["EID_DONE"] == 1

    def test_pmtct_cascade_requires_prophylaxis(self, db):
        self._load(db, [
            ("1", "2024-03-01", "202403", "korogocho", "GRS012FGDSP", "C001", 30, "delivered", "yes", None),
            ("2", "2024-03-02", "202403", "korogocho", "GRS012FGDSP", "C002", 30, "delivered", "no",  None),
        ])
        result = aggregate_mm_sql(db)
        assert result[("GRS012FGDSP", "202403")]["PMTCT_DELIVERY"] == 2
        assert result[("GRS012FGDSP", "202403")]["PMTCT_CASCADE"] == 1  # only C001


# ── PAYLOAD BUILDER ────────────────────────────────────────────────────────────

class TestBuildPayload:

    def test_zero_values_excluded(self):
        hts = {("GRS012FGDSP", "202403"): {"HTS_TST": 5, "HTS_TST_POS": 0}}
        mm  = {}
        payload = build_payload(hts, mm, "default_coc")
        de_keys = [v["dataElement"] for v in payload["dataValues"]]
        assert DE["HTS_TST"] in de_keys
        assert DE["HTS_TST_POS"] not in de_keys  # zero excluded

    def test_payload_structure(self):
        hts = {("GRS012FGDSP", "202403"): {"HTS_TST": 3}}
        payload = build_payload(hts, {}, "HllvX50cXC0")
        dv = payload["dataValues"][0]
        assert dv["orgUnit"]    == "GRS012FGDSP"
        assert dv["period"]     == "202403"
        assert dv["value"]      == "3"
        assert dv["categoryOptionCombo"] == "HllvX50cXC0"

    def test_values_cast_to_string(self):
        hts = {("GRS012FGDSP", "202403"): {"HTS_TST": 10}}
        payload = build_payload(hts, {}, "coc")
        assert isinstance(payload["dataValues"][0]["value"], str)

    def test_empty_aggregation_returns_empty_payload(self):
        payload = build_payload({}, {}, "coc")
        assert payload["dataValues"] == []
