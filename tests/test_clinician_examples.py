"""Educational clinician-example snapshots are not blinded VAL study cases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1] / "docs" / "clinician_walkthrough" / "examples"


def _load(name: str) -> dict[str, Any]:
    payload = json.loads((ROOT / name).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(name)
    return payload


def test_educational_examples_are_not_study_val_ids() -> None:
    hf = _load("syn-000901.json")
    af = _load("syn-000902.json")
    cap = _load("syn-000903.json")
    injected = _load("syn-000904.json")
    assert hf["case_id_code"] == "SYN-000901"
    assert af["case_id_code"] == "SYN-000902"
    assert cap["case_id_code"] == "SYN-000903"
    assert injected["case_id_code"] == "SYN-000904"
    for payload in (hf, af, cap, injected):
        assert not str(payload["case_id_code"]).startswith("VAL-")
        assert "VAL-" not in json.dumps(payload)
    assert hf["clean_case"] is True
    assert af["clean_case"] is True
    assert cap["clean_case"] is True
    assert hf["diagnoses"][0]["icd10cm_code"] == "I50.20"
    assert af["diagnoses"][0]["icd10cm_code"] == "I48.0"
    assert cap["diagnoses"][0]["icd10cm_code"] == "J18.1"
    assert cap["specialty"] == "pulmonology"
    assert injected["clean_case"] is False
    assert injected["answer_keys"][0]["error_category"] == "f1_omission"
    assert injected["answer_keys"][0]["error_family"] == "family_1"
    assert injected["answer_keys"][0]["trigger_meds"][0]["rxcui"] == "1364435"
    assert hf["answer_keys"] == []
    assert "investigator" in (ROOT / "README.md").read_text(encoding="utf-8").casefold()
