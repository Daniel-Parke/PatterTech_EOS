"""Evidence ledger intake: the fragment sweep and the study path.

The two intakes share one ledger and one dedup rule, and the rule is
the URL. That is what lets the Study workflow put two lenses over one
source without the source arriving in the ledger twice.
"""

import json
import sys
from datetime import date
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools import import_fragments as imp  # noqa: E402

TODAY = date(2026, 8, 10)

BASE_RECORD = {
    "id": "EV-0001",
    "source": "An existing document",
    "url": "https://example.invalid/paper",
    "kind": "controlled",
    "publication_status": "peer-reviewed",
    "study_design": None, "population": None, "model": None,
    "benchmark": None,
    "version_or_commit": "v1",
    "licence": "CC-BY-4.0",
    "access_date": "2026-08-01",
    "maintenance": "stable",
    "finding": "Something was measured",
    "applicability_limits": "One population",
    "counter_evidence": None,
    "cited_by": [],
    "review": "2027-01",
}


def _ledger(tmp_path, records=None):
    path = tmp_path / "evidence.json"
    path.write_text(json.dumps({
        "version": 1, "generated": "2026-08-03", "note": "test ledger",
        "records": records if records is not None else [dict(BASE_RECORD)],
    }, indent=1) + "\n", encoding="utf-8", newline="\n")
    return path


def _study_argv(url, source="FieldKit, the product", **over):
    argv = ["study", "--source", source, "--url", url,
            "--version", "3.2.1", "--licence", "proprietary, read-only study",
            "--finding", "The onboarding asks one question at a time",
            "--limits", "Consumer app, not a back office",
            "--maintenance", "active"]
    for key, value in over.items():
        argv += ["--" + key.replace("_", "-"), value]
    return argv


# --- the generated date -------------------------------------------------


def test_generated_is_the_date_of_the_write(tmp_path):
    """It was the literal string 2026-08-03, written on every save
    whatever the date, so the ledger's header aged backwards the moment
    anything was imported into it."""
    path = _ledger(tmp_path)
    ledger = json.loads(path.read_text(encoding="utf-8"))
    imp.write_ledger(ledger, ledger["records"], path, today=TODAY)
    written = json.loads(path.read_text(encoding="utf-8"))
    assert written["generated"] == "2026-08-10"
    assert written["research_cutoff"] == "2026-08-01"


def test_generated_moves_with_a_second_write(tmp_path):
    """Two writes on two days leave two dates, which is the whole point
    of the field."""
    path = _ledger(tmp_path)
    ledger = json.loads(path.read_text(encoding="utf-8"))
    imp.write_ledger(ledger, ledger["records"], path, today=TODAY)
    imp.write_ledger(ledger, ledger["records"], path,
                     today=date(2026, 9, 1))
    assert json.loads(path.read_text(encoding="utf-8"))["generated"] == \
        "2026-09-01"


# --- study intake -------------------------------------------------------


def test_study_intake_adds_one_row_with_the_next_id(tmp_path):
    path = _ledger(tmp_path)
    assert imp.main(_study_argv("https://fieldkit.invalid/app") +
                    ["--dry-run"]) == 0
    assert json.loads(path.read_text(encoding="utf-8"))["records"] == \
        [BASE_RECORD]  # dry run wrote nothing

    ledger = json.loads(path.read_text(encoding="utf-8"))
    row, created = imp.study_intake(
        ledger["records"],
        {"source": "FieldKit", "url": "https://fieldkit.invalid/app"})
    assert created is True
    assert row["id"] == "EV-0002"
    assert row["cited_by"] == []


def test_two_lenses_on_one_source_share_one_evidence_row(tmp_path):
    """One evidence row per source, two lesson rows citing it. The lens
    is not part of the dedup key, because the source is the thing the
    ledger records."""
    path = _ledger(tmp_path)
    assert imp.main(_study_argv("https://fieldkit.invalid/app")) == 0
    first = json.loads(path.read_text(encoding="utf-8"))
    assert [r["id"] for r in first["records"]] == ["EV-0001", "EV-0002"]

    # The second lens over the same source, run again.
    assert imp.main(_study_argv(
        "https://fieldkit.invalid/app",
        finding="Errors are written in the second person")) == 0
    second = json.loads(path.read_text(encoding="utf-8"))
    assert [r["id"] for r in second["records"]] == ["EV-0001", "EV-0002"]
    assert second["records"][1]["finding"] == \
        "The onboarding asks one question at a time"


@pytest.mark.parametrize("variant", [
    "http://fieldkit.invalid/app",
    "https://www.fieldkit.invalid/app/",
    "https://fieldkit.invalid/app/",
])
def test_dedup_normalises_the_url(tmp_path, variant):
    records = [dict(BASE_RECORD, id="EV-0001",
                    url="https://fieldkit.invalid/app")]
    row, created = imp.study_intake(records, {"source": "again",
                                              "url": variant})
    assert created is False
    assert row["id"] == "EV-0001"
    assert len(records) == 1


def test_a_study_source_without_a_url_is_refused():
    """The URL is the dedup key, so a row without one cannot be
    deduplicated and would arrive twice on the next study."""
    with pytest.raises(ValueError):
        imp.study_intake([], {"source": "a thing with no address"})


def test_the_study_row_validates_against_the_evidence_schema(tmp_path):
    jsonschema = pytest.importorskip("jsonschema")
    path = _ledger(tmp_path)
    assert imp.main(_study_argv("https://fieldkit.invalid/app")) == 0
    doc = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(
        (REPO / "kernel" / "schemas" / "evidence.schema.json")
        .read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(doc)
    row = doc["records"][1]
    assert row["publication_status"] == "artefact"
    assert row["kind"] == "exemplar"
    assert row["study_design"] is None
    assert row["review"] == "on-change-of:FieldKit, the product"


def test_a_top_level_dry_run_still_reaches_the_study_path(tmp_path, monkeypatch):
    """A subparser default overwrites the value the top-level flag set,
    so --dry-run before the subcommand would have written the ledger it
    was told not to touch."""
    path = _ledger(tmp_path)
    monkeypatch.setattr(imp, "LEDGER", path)
    before = path.read_text(encoding="utf-8")
    assert imp.main(["--dry-run"] + _study_argv("https://x.invalid/y")) == 0
    assert path.read_text(encoding="utf-8") == before


@pytest.fixture(autouse=True)
def _ledger_under_test(tmp_path, monkeypatch):
    """Every test writes its own ledger, never registry/evidence.json."""
    monkeypatch.setattr(imp, "LEDGER", tmp_path / "evidence.json")
