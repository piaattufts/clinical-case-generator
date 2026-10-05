"""DOI and title normalization, plus importer behavior on synthetic exports."""

from __future__ import annotations

from pathlib import Path

from inthewild_review.config import ReviewLayout
from inthewild_review.importers import import_export, parse_bibtex, parse_ris, rebuild_normalized
from inthewild_review.io_utils import RawDataProtectionError, read_csv, write_csv
from inthewild_review.normalize import make_record_id, normalize_doi, normalize_title
from inthewild_review.schemas import NORMALIZED_FIELDS


def test_doi_normalization_strips_resolver_and_label() -> None:
    assert normalize_doi("https://doi.org/10.1000/XYZ") == "10.1000/xyz"
    assert normalize_doi("http://doi.org/10.1000/AbC") == "10.1000/abc"
    assert normalize_doi("doi:10.1000/XYZ") == "10.1000/xyz"
    assert normalize_doi("  10.1000/AbC  ") == "10.1000/abc"
    assert normalize_doi("https://dx.doi.org/10.1000/AbC") == "10.1000/abc"
    assert normalize_doi("DOI: 10.1000/AbC") == "10.1000/abc"
    assert normalize_doi("") == ""
    assert normalize_doi(None) == ""


def test_title_normalization_does_not_require_changing_the_original() -> None:
    original = "  Robot’s   Home—Work! "
    assert normalize_title(original) == "robot s home work"
    assert original == "  Robot’s   Home—Work! "
    assert normalize_title("Hello   World") == "hello world"
    assert normalize_title(None) == ""


def test_record_id_is_stable() -> None:
    first = make_record_id("scopus", "EID1", "10.1000/abc", "hello", "2014", "a.csv")
    second = make_record_id("scopus", "EID1", "10.1000/abc", "hello", "2014", "a.csv")
    other = make_record_id("pubmed", "EID1", "10.1000/abc", "hello", "2014", "a.csv")
    assert first == second
    assert first != other
    assert first.startswith("rec_")


def test_importer_preserves_raw_export_and_original_title(tmp_path: Path) -> None:
    raw = tmp_path / "data" / "raw" / "scopus" / "export.csv"
    raw.parent.mkdir(parents=True)
    content = (
        "Title,Authors,Year,Abstract,DOI,EID,Source title\n"
        '"  SYNTHETIC TEST FIXTURE Robot’s Home  ",Ada,2014,Abstract,'
        "https://doi.org/10.1000/ABC,EID-1,Journal\n"
    )
    raw.write_text(content, encoding="utf-8")
    before = raw.read_bytes()
    layout = ReviewLayout(tmp_path)
    import_export(layout, raw, "scopus")
    assert raw.read_bytes() == before
    rows = rebuild_normalized(layout)
    assert len(rows) == 1
    assert rows[0]["title"] == "  SYNTHETIC TEST FIXTURE Robot’s Home  "
    assert rows[0]["normalized_title"] == "synthetic test fixture robot s home"
    assert rows[0]["doi_raw"] == "https://doi.org/10.1000/ABC"
    assert rows[0]["doi_normalized"] == "10.1000/abc"
    assert rows[0]["origin"] == "database"
    with_raw_target = tmp_path / "data" / "raw" / "scopus" / "not_allowed.csv"
    try:
        write_csv(with_raw_target, rows, NORMALIZED_FIELDS, tmp_path)
    except RawDataProtectionError:
        pass
    else:
        raise AssertionError("write_csv wrote inside data/raw")
    assert not with_raw_target.exists()


def test_bibtex_and_ris_parse_synthetic_records() -> None:
    bibtex = parse_bibtex(
        """
        @article{synthetic2014,
          title = {SYNTHETIC TEST FIXTURE},
          author = {Ada Example},
          year = {2014},
          doi = {https://doi.org/10.1000/ABC}
        }
        """
    )
    assert bibtex[0]["title"] == "SYNTHETIC TEST FIXTURE"
    assert bibtex[0]["doi"] == "https://doi.org/10.1000/ABC"
    assert bibtex[0]["source_record_id"] == "synthetic2014"
    ris = parse_ris(
        "TY  - JOUR\nTI  - SYNTHETIC TEST FIXTURE\nAU  - Ada\nPY  - 2014\n"
        "DO  - 10.1000/abc\nER  - \n"
    )
    assert ris[0]["TI"] == "SYNTHETIC TEST FIXTURE"
    assert ris[0]["DO"] == "10.1000/abc"


def test_second_import_of_the_same_file_is_refused(tmp_path: Path) -> None:
    raw = tmp_path / "export.csv"
    raw.write_text("Title,Year\nSYNTHETIC TEST FIXTURE,2014\n", encoding="utf-8")
    layout = ReviewLayout(tmp_path)
    import_export(layout, raw, "generic")
    try:
        import_export(layout, raw, "generic")
    except FileExistsError:
        return
    raise AssertionError("The same export was imported twice")


def test_citation_chasing_records_remain_after_normalize(tmp_path: Path) -> None:
    from inthewild_review.citation_chasing import import_citation_edges

    layout = ReviewLayout(tmp_path)
    import_citation_edges(
        layout,
        [
            {
                "seed_record_id": "rec_seed",
                "citing_or_cited_record": "Smith2014",
                "direction": "BACKWARD",
                "iteration": "1",
                "parent_record": "rec_seed",
                "discovery_source": "reference list",
                "date_retrieved": "2026-10-05",
                "title": "SYNTHETIC TEST FIXTURE cited paper",
                "year": "2014",
            }
        ],
    )
    rows = rebuild_normalized(layout)
    chased = [row for row in rows if row["origin"] == "citation_chasing"]
    assert len(chased) == 1
    assert chased[0]["title"] == "SYNTHETIC TEST FIXTURE cited paper"
    assert chased[0].get("decision", "") == ""


def test_normalized_table_round_trip_keeps_columns(tmp_path: Path) -> None:
    layout = ReviewLayout(tmp_path)
    raw = tmp_path / "export.csv"
    raw.write_text(
        "Title,Year,DOI\nSYNTHETIC TEST FIXTURE,2014,doi:10.1000/ZZ\n",
        encoding="utf-8",
    )
    import_export(layout, raw, "generic")
    rebuild_normalized(layout)
    rows = read_csv(layout.normalized)
    assert set(NORMALIZED_FIELDS).issubset(rows[0])
    assert rows[0]["doi_normalized"] == "10.1000/zz"
