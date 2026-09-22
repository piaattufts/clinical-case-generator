"""HTTP mock helpers. Fixture identifiers use the TEST_ prefix only."""

from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx

TEST_RXCUI = "TEST_RXCUI_1"
TEST_RXCUI_RELATED_IN = "TEST_RXCUI_IN"
TEST_RXCUI_RELATED_BN = "TEST_RXCUI_BN"
TEST_RXCUI_RELATED_DF = "TEST_RXCUI_DF"
TEST_RXCUI_WARFARIN = "TEST_RXCUI_W"
TEST_RXCUI_APIXABAN = "TEST_RXCUI_A"
TEST_RXCUI_IBU = "TEST_RXCUI_I"
TEST_RXCUI_COMBO = "TEST_RXCUI_COMBO"
TEST_RXCUI_COMBO_IN1 = "TEST_RXCUI_COMBO_IN1"
TEST_RXCUI_COMBO_IN2 = "TEST_RXCUI_COMBO_IN2"
TEST_LOINC = "TEST_LOINC_1"
TEST_ICD = "TEST_ICD_1"
TEST_UCUM = "TEST_U1"
TEST_UCUM_NO_FACTOR = "TEST_U2"
TEST_SYMPTOM_NAME = "TEST_symptom_1"
TEST_HPO_ID = "HP:TEST_1"
TEST_HPO_NAME = "TEST_orthopnea"
TEST_SET_ID = "TEST_SET_1"
TEST_RULE_CODE = "TEST_NO_DUAL_ANTICOAG"


def rxnorm_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        name = request.url.params.get("name") or ""
        if path.endswith("/version.json") or path.endswith("/version"):
            return httpx.Response(
                200, json={"version": "TEST_RXNORM_VERSION", "apiVersion": "TEST_API"}
            )
        if path.endswith("/drugs.json"):
            if "TEST_med" in name or name == "TEST_med":
                return httpx.Response(200, json=_drugs_payload())
            if "warfarin" in name.casefold():
                return httpx.Response(
                    200, json=_named_drug_payload(TEST_RXCUI_WARFARIN, "TEST_warfarin", "IN")
                )
            if "ibuprofen" in name.casefold():
                return httpx.Response(
                    200, json=_named_drug_payload(TEST_RXCUI_IBU, "TEST_ibuprofen", "IN")
                )
            if "TEST_combo" in name:
                return httpx.Response(200, json=_combo_drug_payload())
            return httpx.Response(200, json={"drugGroup": {"name": name, "conceptGroup": []}})
        if path.endswith("/rxcui.json"):
            if "TEST_med" in name:
                return httpx.Response(200, json={"idGroup": {"rxnormId": [TEST_RXCUI]}})
            return httpx.Response(200, json={"idGroup": {}})
        if f"/rxcui/{TEST_RXCUI_WARFARIN}/properties.json" in path:
            payload = _named_properties_payload(TEST_RXCUI_WARFARIN, "TEST_warfarin", "IN")
            return httpx.Response(200, json=payload)
        if f"/rxcui/{TEST_RXCUI_APIXABAN}/properties.json" in path:
            payload = _named_properties_payload(TEST_RXCUI_APIXABAN, "TEST_apixaban", "IN")
            return httpx.Response(200, json=payload)
        if f"/rxcui/{TEST_RXCUI_IBU}/properties.json" in path:
            payload = _named_properties_payload(TEST_RXCUI_IBU, "TEST_ibuprofen", "IN")
            return httpx.Response(200, json=payload)
        if f"/rxcui/{TEST_RXCUI_COMBO}/properties.json" in path:
            payload = _named_properties_payload(
                TEST_RXCUI_COMBO, "TEST_med / TEST_other", "SCD"
            )
            return httpx.Response(200, json=payload)
        if f"/rxcui/{TEST_RXCUI}/properties.json" in path:
            return httpx.Response(200, json=_properties_payload())
        if f"/rxcui/{TEST_RXCUI}/allProperties.json" in path:
            return httpx.Response(200, json=_all_properties_payload())
        related_paths = (
            f"/rxcui/{TEST_RXCUI}/related.json" in path,
            f"/rxcui/{TEST_RXCUI}/allrelated.json" in path,
            f"/rxcui/{TEST_RXCUI_WARFARIN}/related.json" in path,
            f"/rxcui/{TEST_RXCUI_WARFARIN}/allrelated.json" in path,
            f"/rxcui/{TEST_RXCUI_APIXABAN}/related.json" in path,
            f"/rxcui/{TEST_RXCUI_APIXABAN}/allrelated.json" in path,
            f"/rxcui/{TEST_RXCUI_IBU}/related.json" in path,
            f"/rxcui/{TEST_RXCUI_IBU}/allrelated.json" in path,
        )
        if any(related_paths):
            return httpx.Response(200, json=_related_payload())
        if f"/rxcui/{TEST_RXCUI_COMBO}/related.json" in path or (
            f"/rxcui/{TEST_RXCUI_COMBO}/allrelated.json" in path
        ):
            return httpx.Response(200, json=_combo_related_payload())
        if f"/rxcui/{TEST_RXCUI_WARFARIN}/allProperties.json" in path:
            return httpx.Response(200, json=_all_properties_payload())
        if f"/rxcui/{TEST_RXCUI_APIXABAN}/allProperties.json" in path:
            return httpx.Response(200, json=_all_properties_payload())
        if f"/rxcui/{TEST_RXCUI_IBU}/allProperties.json" in path:
            return httpx.Response(200, json=_all_properties_payload())
        if f"/rxcui/{TEST_RXCUI_COMBO}/allProperties.json" in path:
            return httpx.Response(200, json=_all_properties_payload())
        if path.endswith("/properties.json"):
            return httpx.Response(200, json={})
        return httpx.Response(404, json={"error": "TEST_not_found"})

    return httpx.MockTransport(handler)


def loinc_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("CodeSystem/$lookup"):
            code = request.url.params.get("code") or ""
            if code != TEST_LOINC:
                return httpx.Response(404, json={"resourceType": "OperationOutcome"})
            return httpx.Response(200, json=_loinc_lookup_payload())
        if path.endswith("ValueSet/$expand"):
            filter_text = request.url.params.get("filter") or ""
            if filter_text.strip() == "":
                return httpx.Response(400, json={"resourceType": "OperationOutcome"})
            if "TEST_lab" in filter_text or filter_text == TEST_LOINC:
                return httpx.Response(200, json=_loinc_expand_payload())
            return httpx.Response(
                200,
                json={"resourceType": "ValueSet", "expansion": {"contains": []}},
            )
        return httpx.Response(404, json={"resourceType": "OperationOutcome"})

    return httpx.MockTransport(handler)


def ucum_transport(xml_text: str) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("ucum-essence.xml") or "ucum-essence.xml" in str(request.url):
            return httpx.Response(200, text=xml_text, headers={"Content-Type": "application/xml"})
        return httpx.Response(404, text="TEST_not_found")

    return httpx.MockTransport(handler)


def icd10cm_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        parsed = urlparse(str(request.url))
        params = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        terms = params.get("terms", "")
        if "TEST" not in terms and terms != TEST_ICD:
            return httpx.Response(200, json=[0, [], None, []])
        return httpx.Response(
            200,
            json=[
                1,
                [TEST_ICD],
                None,
                [[TEST_ICD, "TEST_exact description from source"]],
            ],
        )

    return httpx.MockTransport(handler)


def tracking_transport(calls: list[str]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(500, text="TEST_should_not_be_called")

    return httpx.MockTransport(handler)


def conditions_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        parsed = urlparse(str(request.url))
        params = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        terms = params.get("terms", "")
        if "TEST_symptom" in terms:
            return httpx.Response(200, json=_conditions_payload())
        return httpx.Response(200, json=[0, [], {}, []])

    return httpx.MockTransport(handler)


def hpo_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        parsed = urlparse(str(request.url))
        params = {key: values[-1] for key, values in parse_qs(parsed.query).items()}
        terms = params.get("terms", "")
        if "orthopnea" in terms.casefold() or "TEST_orthopnea" in terms:
            return httpx.Response(
                200,
                json=[
                    1,
                    [TEST_HPO_NAME],
                    {
                        "id": [TEST_HPO_ID],
                        "name": [TEST_HPO_NAME],
                        "synonyms": [["orthopnea"]],
                    },
                    [[TEST_HPO_ID, TEST_HPO_NAME]],
                ],
            )
        return httpx.Response(200, json=[0, [], {}, []])

    return httpx.MockTransport(handler)


def dailymed_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if path.endswith("/spls.json"):
            rxcui = request.url.params.get("rxcui") or ""
            return httpx.Response(
                200,
                json={"data": [{"setid": TEST_SET_ID, "title": f"TEST_label for {rxcui}"}]},
            )
        if TEST_SET_ID in path and path.endswith(".xml"):
            return httpx.Response(
                200,
                text=_dailymed_spl_xml(),
                headers={"Content-Type": "application/xml"},
            )
        if TEST_SET_ID in path and path.endswith(".json"):
            return httpx.Response(415, text="TEST_json_not_supported")
        return httpx.Response(404, json={"error": "TEST_not_found"})

    return httpx.MockTransport(handler)


def rxclass_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        rxcui = request.url.params.get("rxcui") or ""
        return httpx.Response(
            200,
            json={
                "rxclassDrugInfoList": {
                    "rxclassDrugInfo": [
                        {
                            "minConcept": {"rxcui": rxcui},
                            "rxclassMinConceptItem": {
                                "classId": "TEST_CLASS_1",
                                "className": "Anticoagulants",
                                "classType": "ATC1-4",
                            },
                            "rela": "has_ATC",
                        }
                    ]
                }
            },
        )

    return httpx.MockTransport(handler)


def official_shaped_ucum_xml() -> str:
    return """<?xml version="1.0" encoding="ascii"?>
<root xmlns="http://unitsofmeasure.org/ucum-essence" version="TEST_UCUM_2">
   <prefix Code="TEST_k" CODE="TEST_K">
      <name>TEST_prefix</name>
      <value value="1e3">1000</value>
   </prefix>
   <unit Code="TEST_U1" CODE="TEST_U1">
      <name>TEST unit one</name>
      <property>TEST_quantity</property>
      <value Unit="TEST_CANON" UNIT="TEST_CANON" value="9.25">9.25</value>
   </unit>
   <unit Code="TEST_U2" CODE="TEST_U2">
      <name>TEST unit two</name>
      <property>TEST_quantity</property>
      <value Unit="TEST_CANON" UNIT="TEST_CANON">no numeric factor</value>
   </unit>
</root>
"""


def _named_drug_payload(rxcui: str, name: str, tty: str) -> dict[str, Any]:
    return {
        "drugGroup": {
            "name": name,
            "conceptGroup": [
                {
                    "tty": tty,
                    "conceptProperties": {
                        "rxcui": rxcui,
                        "name": name,
                        "synonym": name,
                        "tty": tty,
                        "suppress": "N",
                    },
                }
            ],
        }
    }


def _named_properties_payload(rxcui: str, name: str, tty: str) -> dict[str, Any]:
    return {
        "properties": {
            "rxcui": rxcui,
            "name": name,
            "synonym": name,
            "tty": tty,
            "suppress": "N",
        }
    }


def _conditions_payload() -> list[Any]:
    return [
        1,
        [TEST_SYMPTOM_NAME],
        {
            "primary_name": [TEST_SYMPTOM_NAME],
            "synonyms": [["TEST_synonym"]],
            "icd10cm": [[{"code": TEST_ICD, "name": "TEST_exact description from source"}]],
        },
        [[TEST_SYMPTOM_NAME, "TEST_consumer"]],
    ]


def _dailymed_spl_xml() -> str:
    return """<?xml version="1.0" encoding="UTF-8"?>
<document xmlns="urn:hl7-org:v3">
  <title>TEST_label</title>
  <component>
    <structuredBody>
      <component>
        <section>
          <code code="34067-9" displayName="INDICATIONS &amp; USAGE SECTION"/>
          <title>Indications and Usage</title>
          <text>Indicated for edema associated with heart failure.</text>
        </section>
      </component>
      <component>
        <section>
          <code code="34071-1" displayName="WARNINGS SECTION"/>
          <title>Warnings</title>
          <text>Avoid concomitant use with another anticoagulant.
          Monitor INR and prothrombin time.</text>
        </section>
      </component>
      <component>
        <section>
          <code code="34070-3" displayName="CONTRAINDICATIONS SECTION"/>
          <title>Contraindications</title>
          <text>Do not use with another oral anticoagulant.</text>
        </section>
      </component>
      <component>
        <section>
          <code code="34068-7" displayName="DOSAGE &amp; ADMINISTRATION SECTION"/>
          <title>Dosage and Administration</title>
          <text>Dose according to INR.</text>
        </section>
      </component>
      <component>
        <section>
          <code displayName="ACTIVE INGREDIENT SECTION"/>
          <title>Active Ingredient</title>
          <text>TEST_ingredient</text>
        </section>
      </component>
    </structuredBody>
  </component>
</document>
"""


def _combo_drug_payload() -> dict[str, Any]:
    return {
        "drugGroup": {
            "name": "TEST_combo",
            "conceptGroup": [
                {
                    "tty": "SCD",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_COMBO,
                        "name": "TEST_med / TEST_other Oral Tablet",
                        "synonym": "TEST_combo",
                        "tty": "SCD",
                        "suppress": "N",
                    },
                },
                {
                    "tty": "IN",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI,
                        "name": "TEST_med branded product",
                        "synonym": "TEST_med",
                        "tty": "IN",
                        "suppress": "N",
                    },
                },
            ],
        }
    }


def _combo_related_payload() -> dict[str, Any]:
    return {
        "relatedGroup": {
            "conceptGroup": [
                {
                    "tty": "IN",
                    "conceptProperties": [
                        {
                            "rxcui": TEST_RXCUI_COMBO_IN1,
                            "name": "TEST_med",
                            "tty": "IN",
                            "suppress": "N",
                        },
                        {
                            "rxcui": TEST_RXCUI_COMBO_IN2,
                            "name": "TEST_other",
                            "tty": "IN",
                            "suppress": "N",
                        },
                    ],
                }
            ]
        }
    }


def _drugs_payload() -> dict[str, Any]:
    return {
        "drugGroup": {
            "name": "TEST_med",
            "conceptGroup": [
                {
                    "tty": "SBD",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI,
                        "name": "TEST_med branded product",
                        "synonym": "TEST_brand",
                        "tty": "SBD",
                        "suppress": "N",
                    },
                }
            ],
        }
    }


def _properties_payload() -> dict[str, Any]:
    return {
        "properties": {
            "rxcui": TEST_RXCUI,
            "name": "TEST_med branded product",
            "synonym": "TEST_brand",
            "tty": "SBD",
            "suppress": "N",
        }
    }


def _all_properties_payload() -> dict[str, Any]:
    return {
        "propConceptGroup": {
            "propConcept": [
                {
                    "propCategory": "NAMES",
                    "propName": "RxNorm Name",
                    "propValue": "TEST_med branded product",
                },
                {
                    "propCategory": "ATTRIBUTES",
                    "propName": "AVAILABLE_STRENGTH",
                    "propValue": "TEST_strength",
                },
            ]
        }
    }


def _related_payload() -> dict[str, Any]:
    return {
        "allRelatedGroup": {
            "rxcui": TEST_RXCUI,
            "conceptGroup": [
                {
                    "tty": "IN",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_RELATED_IN,
                        "name": "TEST_ingredient",
                        "tty": "IN",
                        "suppress": "N",
                    },
                },
                {
                    "tty": "BN",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_RELATED_BN,
                        "name": "TEST_brand_name",
                        "tty": "BN",
                        "suppress": "N",
                    },
                },
                {
                    "tty": "DF",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_RELATED_DF,
                        "name": "TEST_dose_form",
                        "tty": "DF",
                        "suppress": "N",
                    },
                },
            ],
        },
        "relatedGroup": {
            "conceptGroup": [
                {
                    "tty": "IN",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_RELATED_IN,
                        "name": "TEST_ingredient",
                        "tty": "IN",
                        "suppress": "N",
                    },
                },
                {
                    "tty": "BN",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_RELATED_BN,
                        "name": "TEST_brand_name",
                        "tty": "BN",
                        "suppress": "N",
                    },
                },
                {
                    "tty": "DF",
                    "conceptProperties": {
                        "rxcui": TEST_RXCUI_RELATED_DF,
                        "name": "TEST_dose_form",
                        "tty": "DF",
                        "suppress": "N",
                    },
                },
            ]
        },
    }


def _loinc_lookup_payload() -> dict[str, Any]:
    return {
        "resourceType": "Parameters",
        "parameter": [
            {"name": "name", "valueString": "LOINC"},
            {"name": "version", "valueString": "TEST_LOINC_VERSION"},
            {"name": "display", "valueString": "TEST_lab long name"},
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "COMPONENT"},
                    {"name": "value", "valueString": "TEST_component"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "PROPERTY"},
                    {"name": "value", "valueString": "TEST_property"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "TIME_ASPCT"},
                    {"name": "value", "valueString": "TEST_time"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "SYSTEM"},
                    {"name": "value", "valueString": "TEST_system"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "SCALE_TYP"},
                    {"name": "value", "valueString": "TEST_scale"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "METHOD_TYP"},
                    {"name": "value", "valueString": "TEST_method"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "CLASS"},
                    {"name": "value", "valueString": "TEST_class"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "SHORTNAME"},
                    {"name": "value", "valueString": "TEST_short"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "LONG_COMMON_NAME"},
                    {"name": "value", "valueString": "TEST_lab long name"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "STATUS"},
                    {"name": "value", "valueString": "ACTIVE"},
                ],
            },
            {
                "name": "property",
                "part": [
                    {"name": "code", "valueCode": "EXAMPLE_UCUM_UNITS"},
                    {"name": "value", "valueString": "TEST_mg/dL;TEST_mmol/L"},
                ],
            },
        ],
    }


def _loinc_expand_payload() -> dict[str, Any]:
    return {
        "resourceType": "ValueSet",
        "expansion": {
            "version": "TEST_LOINC_VERSION",
            "contains": [
                {
                    "system": "http://loinc.org",
                    "code": TEST_LOINC,
                    "display": "TEST_lab long name",
                }
            ],
        },
    }
