"""Later case revisions for the frozen framework. Imported by the builder."""

from __future__ import annotations

from typing import Any

from scripts.build_remaining20_revision import (
    NO_COMMENT,
    Finding,
    _add_lab,
    _add_med,
    _consult,
    _drop_med,
    _fail,
    _imaging,
    _med,
    _pass,
    _ref,
    _set_lab,
    _story,
    _vital,
    _wrap,
)


def _endocarditis(
    case: dict[str, Any],
    *,
    organism: str,
    fever: str,
    duration_sentence: str,
    duration_reference: str,
    extra_home_note: str,
) -> None:
    _story(
        case,
        one_liner=f"Fever and native-valve endocarditis due to {organism}",
        complaint="Fever and fatigue",
        admission_dx="Fever, with endocarditis established after cultures and echocardiography",
        hpi=(
            f"The patient is admitted with fever and fatigue, not with a finished explanation. "
            f"Temperature is {fever} C. Dental examination shows caries and periodontal disease. "
            f"There is no prosthetic valve. Two blood-culture sets drawn before antibiotics grow "
            f"{organism}, reported susceptible to penicillin. Ceftriaxone 2 g intravenously once "
            f"daily is started after the cultures are drawn. Repeat cultures show no growth. "
            f"Transesophageal echocardiography shows a mitral vegetation, mild regurgitation, no "
            f"abscess, and preserved ventricular function. Cardiac surgery finds no current "
            f"indication for an operation. {duration_sentence} {extra_home_note}"
        ),
        admission_note=f"Fever to {fever} C. Blood cultures drawn before antibiotics. Poor dentition. No prosthetic valve.",
        course=(
            f"{organism} bacteremia cleared. No surgical indication. {duration_sentence}"
        ),
    )
    _vital(case, "admission")["temp_c"] = fever
    _vital(case, "discharge")["temp_c"] = "36.70"
    case["CaseMicrobiology"] = [
        {
            "micro_id": f"MICRO-{case['case_id_code']}-001",
            "case_id": case["case_id_code"],
            "timepoint": "admission",
            "specimen": "blood",
            "test": "blood culture",
            "organism": organism,
            "result": "growth",
            "quantity": "2 of 2 sets",
            "status": "final",
            "notes": "Drawn before antibiotics. Penicillin susceptible.",
            "source_reference": None,
        },
        {
            "micro_id": f"MICRO-{case['case_id_code']}-002",
            "case_id": case["case_id_code"],
            "timepoint": "hospital_day_3",
            "specimen": "blood",
            "test": "blood culture",
            "organism": None,
            "result": "no growth",
            "quantity": "2 of 2 sets",
            "status": "final",
            "notes": "First negative cultures.",
            "source_reference": None,
        },
    ]
    _imaging(
        case,
        f"STUDY-{case['case_id_code']}-TEE",
        "Transesophageal echocardiogram",
        "Mitral vegetation. Mild regurgitation. No abscess. Ventricular function preserved.",
        "heart",
    )
    _consult(
        case,
        "infectious disease",
        f"Penicillin-susceptible {organism} endocarditis on a native valve. Bacteremia has cleared.",
        duration_reference,
        f"CON-{case['case_id_code']}-ID",
    )
    _consult(
        case,
        "cardiac surgery",
        "Vegetation without abscess, severe regurgitation, heart failure, or uncontrolled infection.",
        "No indication for valve surgery during this admission.",
        f"CON-{case['case_id_code']}-SURG",
    )
    if case["CaseMedication"]:
        cef = _med(case, "ceftriaxone", "inpatient")
        cef["notes"] = duration_sentence
    case.setdefault("CaseDevice", [])
    case["CaseDevice"] = [
        {
            "device_id": f"DEV-{case['case_id_code']}-001",
            "case_id": case["case_id_code"],
            "device_type": "peripherally inserted central catheter",
            "site": "arm",
            "placement_timepoint": "inpatient",
            "status": "in place",
            "tip_location_or_confirmation": "Tip confirmed. Site clean.",
            "care_instructions": "Line care while ceftriaxone continues.",
            "removal_plan": "Remove when intravenous therapy stops.",
            "source_reference": None,
        }
    ]


def _endo_findings(duration_problem: str) -> dict[str, Finding]:
    return {
        "presentation_diagnosis_coherence": _fail(
            "The chart admitted the patient as endocarditis, often without fever.",
            "The arrival problem is fever. Endocarditis is stated after cultures and echocardiography.",
        ),
        "causal_context": _fail(
            "No source or predisposition was given.",
            "Caries and periodontal disease are the predisposition. There is no prosthetic valve.",
        ),
        "diagnostic_workup": _fail(
            "The organism was only gram-positive cocci, and surgery was not addressed.",
            "Named the organism, showed clearance, described the vegetation, and recorded no surgical indication.",
        ),
        "treatment_trajectory": _fail(
            "Ceftriaxone had no usable duration.",
            duration_problem,
        ),
        "laboratory_vital_trend": _pass(
            "Creatinine or glucose values already present were kept unless a drug decision required a baseline."
        ),
        "hospital_course_completeness": _fail(
            "The course said cultures cleared without showing when.",
            "Clearance is placed on hospital day 3, after antibiotics were started.",
        ),
        "medication_decision_support": _fail(
            "Infectious diseases said only to complete a planned course.",
            "The consult now states whether the stop date is fixed or still pending.",
        ),
        "discharge_stability_chronology": _fail(
            "The diagnosis preceded the cultures and the echocardiogram.",
            "Cultures are drawn first, then antibiotics, then the echocardiogram and the surgical opinion.",
        ),
        "internal_consistency": _pass("Home medicines that remain appropriate stay on their existing rows."),
        "unsupported_hidden_reference_action": _fail(
            "Continue-ceftriaxone was not tied to a duration the chart could defend.",
            "The reference continues ceftriaxone only for the duration the consult now states.",
        ),
    }


def revise_810(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _endocarditis(
        case,
        organism="Streptococcus sanguinis",
        fever="38.20",
        duration_sentence="Ceftriaxone 2 g intravenously once daily continues for four weeks from the first negative culture.",
        duration_reference="Continue ceftriaxone 2 g intravenously once daily for four weeks from the first negative culture. Weekly blood count and creatinine.",
        extra_home_note="Metformin and atorvastatin are continued. Discharge creatinine is 0.9 mg/dL and glucose has fallen.",
    )
    findings = _endo_findings("Four weeks from the first negative culture is now stated.")
    findings["laboratory_vital_trend"] = _pass("Creatinine fell from 1.3 to 0.9 mg/dL and glucose from 176 to 112 mg/dL, which still allows metformin.")
    reference = {
        "medications": [
            _ref("ceftriaxone 2000 MG Injection", "continue", "2000 MG", "once daily", "Native-valve endocarditis", "Infectious diseases sets four weeks from the first negative culture."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Glucose improved and discharge creatinine is 0.9 mg/dL."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued. No adverse effect is described."),
        ],
        "monitoring_requirements": [{"parameter": "weekly complete blood count and creatinine", "frequency": "weekly", "target": None, "duration": "during ceftriaxone"}],
        "follow_up_requirements": [{"item": "Infectious-disease clinic follow-up", "timing": "7 days", "with_service": "infectious disease"}],
    }
    facts = [{"fact": "Fever was already 38.2 C. Added the organism, the four-week duration, dental disease, and the surgical opinion.", "why": "The clean chart had fever but not a source, a named organism, or a duration.", "evidence": "Baddour LM et al. Circulation. 2015;132:1435-1486. Ceftriaxone 2 g every 24 hours for four weeks is a native-valve regimen for highly penicillin-susceptible viridans-group streptococci."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-810 keeps the existing fever and adds the missing endocarditis work-up and a four-week ceftriaxone course."


def revise_811(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _endocarditis(
        case,
        organism="Streptococcus gordonii",
        fever="38.60",
        duration_sentence="Ceftriaxone 2 g intravenously once daily continues for four weeks from the first negative culture.",
        duration_reference="Continue ceftriaxone 2 g intravenously once daily for four weeks from the first negative culture.",
        extra_home_note=(
            "Lisinopril is continued. Creatinine stays 0.8 to 0.9 mg/dL and discharge blood pressure "
            "is about 130 mm Hg systolic. Aspirin is continued for known coronary disease. Metformin "
            "is continued. Glucose is 137 mg/dL at discharge and he is eating."
        ),
    )
    findings = _endo_findings("A four-week duration replaces the unspecified remaining course.")
    findings["presentation_diagnosis_coherence"] = _fail("Admission temperature was 36.8 C on an endocarditis label.", "Fever of 38.6 C is now the presenting sign.")
    findings["laboratory_vital_trend"] = _pass("Creatinine stays under 1 mg/dL, so continuing lisinopril does not repeat the VAL-809 defect.")
    reference = {
        "medications": [
            _ref("ceftriaxone 2000 MG Injection", "continue", "2000 MG", "once daily", "Native-valve endocarditis", "Four weeks from the first negative culture."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Creatinine remains 0.8 to 0.9 mg/dL."),
            _ref("aspirin 81 MG Chewable Tablet", "continue", "81 MG", "once daily", "Coronary disease", "The history already records atherosclerotic heart disease. No bleeding is described."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "He is eating. The discharge glucose is 137 mg/dL."),
        ],
        "monitoring_requirements": [{"parameter": "weekly complete blood count and creatinine", "frequency": "weekly", "target": None, "duration": "during ceftriaxone"}],
        "follow_up_requirements": [{"item": "Infectious-disease follow-up for the remaining antibiotic course", "timing": "7 days", "with_service": "infectious disease"}],
    }
    facts = [{"fact": "Fever of 38.6 C, Streptococcus gordonii, and a four-week clock.", "why": "The clean chart was afebrile and did not name a duration.", "evidence": "Baddour LM et al. Circulation. 2015;132:1435-1486."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-811 adds fever and a defined ceftriaxone duration. Lisinopril continues because creatinine never rose."


def revise_812(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _endocarditis(
        case,
        organism="Streptococcus oralis",
        fever="38.40",
        duration_sentence=(
            "Ceftriaxone 2 g intravenously once daily continues after discharge. Infectious diseases "
            "has not chosen the stop date and will do that at the visit. A four-week course is the "
            "usual native-valve range and is not yet the order."
        ),
        duration_reference=(
            "Continue ceftriaxone 2 g intravenously once daily until the visit. Do not assign a stop "
            "date today. Infectious diseases will choose it."
        ),
        extra_home_note=(
            "Hemoglobin fell from 13.6 to 11.9 g/dL without tachycardia or a transfusion. "
            "Aspirin and atorvastatin continue."
        ),
    )
    findings = _endo_findings("The drug continues, and the stop date stays pending because that is the decision this chart poses.")
    findings["unsupported_hidden_reference_action"] = _fail(
        "The clean reference continued ceftriaxone as though the duration were settled.",
        "The reference continues the drug and explicitly does not set the stop date.",
    )
    reference = {
        "medications": [
            _ref("ceftriaxone 2000 MG Injection", "continue", "2000 MG", "once daily", "Native-valve endocarditis", "The stop date is the pending infectious-diseases decision. The drug itself continues."),
            _ref("aspirin 81 MG Chewable Tablet", "continue", "81 MG", "once daily", "Coronary disease", "Known atherosclerotic disease. Hemoglobin is stable in the 11 g/dL range without bleeding symptoms."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
        ],
        "monitoring_requirements": [{"parameter": "weekly complete blood count and creatinine", "frequency": "weekly", "target": None, "duration": "while ceftriaxone continues"}],
        "follow_up_requirements": [{"item": "Visit to set the ceftriaxone stop date", "timing": "14 days", "with_service": "infectious disease"}],
    }
    facts = [{"fact": "Fever, Streptococcus oralis, and an explicitly unset stop date.", "why": "This profile's decision is the pending duration. Inventing a finished four-week order would erase it.", "evidence": "Baddour LM et al. Circulation. 2015;132:1435-1486 describes the usual four-week range. The chart says that range is not yet the order."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-812 continues ceftriaxone and leaves the stop date to the infectious-diseases visit."


def _cmv_open(case: dict[str, Any], hpi: str, admission_note: str, course: str) -> None:
    _story(
        case,
        one_liner="Diarrhea after kidney transplant, with cytomegalovirus colitis found during the stay",
        complaint="Diarrhea",
        admission_dx="Diarrhea after kidney transplant",
        hpi=hpi,
        admission_note=admission_note,
        course=course,
    )
    _drop_med(case, "valganciclovir", "home")
    valg = _med(case, "valganciclovir", "inpatient")
    valg["status"] = "active"
    valg["notes"] = "Not a home medicine. Started after the biopsy."
    case["CaseMicrobiology"] = [
        {"micro_id": f"MICRO-{case['case_id_code']}-001", "case_id": case["case_id_code"], "timepoint": "admission", "specimen": "stool", "test": "stool culture", "organism": None, "result": "no growth", "quantity": None, "status": "final", "notes": None, "source_reference": None},
        {"micro_id": f"MICRO-{case['case_id_code']}-002", "case_id": case["case_id_code"], "timepoint": "admission", "specimen": "stool", "test": "Clostridioides difficile toxin", "organism": None, "result": "negative", "quantity": None, "status": "final", "notes": None, "source_reference": None},
    ]
    case["CaseProcedure"] = [{
        "procedure_id": f"PROC-{case['case_id_code']}-001",
        "case_id": case["case_id_code"],
        "procedure_name": "Colonoscopy with biopsy",
        "procedure_type": "diagnostic",
        "date": None,
        "timepoint": "hospital_day_2",
        "performed_by": "gastroenterology",
        "anesthesia_type": None,
        "findings": "Colitis. Biopsy immunohistochemistry positive for cytomegalovirus.",
        "complications": None,
        "duration_minutes": None,
        "laterality": None,
        "source_reference": None,
    }]


def revise_814(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _cmv_open(
        case,
        hpi=(
            "A 71-year-old man with a kidney transplant is admitted for a week of diarrhea, not with "
            "a cytomegalovirus label. Home medicines include tacrolimus 1 mg every 12 hours, "
            "mycophenolate mofetil 1000 mg twice daily, and amlodipine 5 mg daily. Valganciclovir is "
            "not a home medicine. Baseline creatinine is 1.4 mg/dL. Admission creatinine is 2.5 mg/dL "
            "and potassium is 3.3 mmol/L. Stool studies for bacteria and Clostridioides difficile are "
            "negative. Hospital-day-2 biopsy shows cytomegalovirus colitis. Plasma cytomegalovirus DNA "
            "is 4200 IU/mL. Mycophenolate is held. After partial recovery, discharge creatinine is "
            "1.6 mg/dL, potassium is 4.0 mmol/L, and weight is 84 kg against a dry weight of 85 kg. "
            "The pharmacist records creatinine clearance near 50 mL/min, so valganciclovir is started "
            "at 450 mg orally twice daily rather than 900 mg. Transplant says not to restart "
            "mycophenolate today because creatinine is still above baseline."
        ),
        admission_note="Diarrhea. Creatinine 2.5 mg/dL, baseline 1.4 mg/dL, potassium 3.3 mmol/L. Mycophenolate held. No home valganciclovir.",
        course="Biopsy established cytomegalovirus colitis. Valganciclovir 450 mg twice daily was started. Mycophenolate stays held.",
    )
    _add_lab(case, lab_id="LAB-VAL814-003", timepoint="outpatient_baseline", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=1.4, unit="mg/dL")
    _add_lab(case, lab_id="LAB-VAL814-004", timepoint="admission", test_name="Potassium [Moles/volume] in Serum or Plasma", value=3.3, unit="mmol/L")
    _add_lab(case, lab_id="LAB-VAL814-005", timepoint="discharge", test_name="Potassium [Moles/volume] in Serum or Plasma", value=4.0, unit="mmol/L")
    valg = _med(case, "valganciclovir", "inpatient")
    valg["dose"] = "450 MG"
    valg["frequency"] = "twice daily"
    valg["notes"] = "Started after the biopsy. 450 mg twice daily because creatinine clearance is near 50 mL/min."
    mmf = _med(case, "mycophenolate", "inpatient")
    mmf["status"] = "held"
    mmf["held_reason"] = "Held after the biopsy. Not restarted at discharge because creatinine is still above the 1.4 mg/dL baseline."
    _consult(case, "transplant", "Creatinine has improved only to 1.6 mg/dL.", "Do not restart mycophenolate at discharge. Continue tacrolimus and amlodipine.", "CON-VAL814-TX")
    _consult(case, "infectious disease", "Tissue-proven cytomegalovirus colitis.", "Start valganciclovir 450 mg orally twice daily for the current creatinine clearance. Recheck the dose if creatinine falls.", "CON-VAL814-ID")
    findings = {
        "presentation_diagnosis_coherence": _fail("The patient arrived already labeled with cytomegalovirus disease, and valganciclovir was a home drug.", "Admission is diarrhea. The biopsy is on hospital day 2. Valganciclovir starts after that."),
        "causal_context": _fail("Diarrhea had no work-up before the label.", "Negative stool studies precede the biopsy."),
        "diagnostic_workup": _fail("No stool study or biopsy was on the chart.", "Added both, plus a viral load of 4200 IU/mL."),
        "treatment_trajectory": _fail("Full-dose valganciclovir was already a home medicine.", "It is a new start at the renally reduced dose."),
        "laboratory_vital_trend": _fail("Creatinine fell from 2.5 to 1.6 mg/dL with no baseline, and there was no potassium despite diarrhea.", "Baseline creatinine is 1.4 mg/dL. Potassium moves from 3.3 to 4.0 mmol/L."),
        "hospital_course_completeness": _fail("The hold was described as temporary without a restart condition.", "Restart is refused today because creatinine is still above baseline."),
        "medication_decision_support": _fail("The clean reference restarted mycophenolate and continued valganciclovir 900 mg twice daily.", "Mycophenolate stays held. Valganciclovir is 450 mg twice daily."),
        "discharge_stability_chronology": _pass("Discharge weight 84 kg is at the recorded dry weight of 85 kg, and diarrhea is no longer the uninvestigated arrival problem."),
        "internal_consistency": _fail("A 900 mg induction dose does not match a discharge creatinine of 1.6 mg/dL.", "The dose on the chart and in the reference is 450 mg twice daily."),
        "unsupported_hidden_reference_action": _fail("Restarting mycophenolate was not earned by renal recovery.", "The reference holds mycophenolate and starts renally dosed valganciclovir."),
    }
    reference = {
        "medications": [
            _ref("valganciclovir 450 MG Oral Tablet", "start", "450 MG", "twice daily", "Cytomegalovirus colitis", "Not a home drug. Dose matches creatinine clearance near 50 mL/min. Reassess the dose if creatinine returns to 1.4 mg/dL."),
            _ref("mycophenolate mofetil 500 MG Oral Tablet", "hold", "1000 MG", "twice daily", "Kidney transplant", "Transplant says not to restart it while creatinine is 1.6 mg/dL against a 1.4 mg/dL baseline."),
            _ref("BX Rating tacrolimus 1 MG Oral Capsule", "continue", "1 MG", "every 12 hours", "Kidney transplant", "Transplant says to continue it."),
            _ref("amlodipine 5 MG Oral Tablet", "continue", "5 MG", "once daily", "Hypertension", "Blood pressure is 120/86 mm Hg."),
        ],
        "monitoring_requirements": [{"parameter": "creatinine, potassium, and the valganciclovir dose", "frequency": "at transplant clinic in 5 days", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Transplant follow-up to reassess mycophenolate and the antiviral dose", "timing": "5 days", "with_service": "transplant"}],
    }
    facts = [{"fact": "Symptom-first course, biopsy, viral load 4200 IU/mL, baseline creatinine 1.4 mg/dL, potassium 3.3 to 4.0 mmol/L, and valganciclovir 450 mg twice daily.", "why": "The clean chart copied the VAL-813 defects and used a full induction dose at a reduced creatinine clearance.", "evidence": "Kotton CN et al. Transplantation. 2018;102:900-931. Valganciclovir labeling reduces induction to 450 mg twice daily when creatinine clearance is 40 to 59 mL/min."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-814 does not restart mycophenolate and does not use valganciclovir 900 mg twice daily, because creatinine clearance is still reduced."


def revise_815(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _cmv_open(
        case,
        hpi=(
            "A 68-year-old woman with a kidney transplant is admitted with nausea and new diarrhea, "
            "not with a cytomegalovirus label. Valganciclovir is not a home medicine. Home tacrolimus "
            "is 1 mg every 12 hours. An admission trough is 11.5 ng/mL against a stated target of "
            "5 to 8 ng/mL, so the inpatient dose is reduced to 1 mg once daily. The discharge trough "
            "is 6.8 ng/mL. Stool studies are negative and a hospital-day-2 biopsy shows cytomegalovirus. "
            "Creatinine stays 0.8 to 0.9 mg/dL. At a discharge weight of 70 kg, which is the dry weight, "
            "creatinine clearance is above 60 mL/min, and valganciclovir 900 mg orally twice daily is "
            "started. Lisinopril, amlodipine, and atorvastatin continue. Potassium stays 4.5 to 4.6 mmol/L."
        ),
        admission_note="Nausea and diarrhea. Tacrolimus trough 11.5 ng/mL. No home valganciclovir.",
        course="The biopsy established the diagnosis. Tacrolimus was reduced. Valganciclovir induction was started at 900 mg twice daily.",
    )
    case["CaseWeight"][1]["weight_kg"] = "70.000"
    case["CaseWeight"][1]["dry_weight_kg"] = "70.000"
    _add_lab(case, lab_id="LAB-VAL815-005", timepoint="admission", test_name="Tacrolimus trough", value=11.5, unit="ng/mL")
    _add_lab(case, lab_id="LAB-VAL815-006", timepoint="discharge", test_name="Tacrolimus trough", value=6.8, unit="ng/mL")
    tac = _med(case, "tacrolimus", "inpatient")
    tac["frequency"] = "once daily"
    tac["notes"] = "Reduced from 1 mg every 12 hours because the trough was 11.5 ng/mL. Discharge trough is 6.8 ng/mL."
    valg = _med(case, "valganciclovir", "inpatient")
    valg["notes"] = "Not a home medicine. 900 mg twice daily after creatinine clearance was above 60 mL/min."
    _consult(case, "transplant", "Trough was above the 5 to 8 ng/mL target.", "Continue tacrolimus 1 mg once daily. Continue lisinopril, amlodipine, and atorvastatin.", "CON-VAL815-TX")
    _consult(case, "infectious disease", "Biopsy-proven cytomegalovirus colitis.", "Start valganciclovir 900 mg orally twice daily.", "CON-VAL815-ID")
    findings = {
        "presentation_diagnosis_coherence": _fail("Cytomegalovirus disease and home valganciclovir were present on arrival.", "Diarrhea is the arrival problem. The antiviral starts after the biopsy."),
        "causal_context": _fail("Nausea had no cause.", "The biopsy supplies it after negative stool studies."),
        "diagnostic_workup": _fail("No trough and no biopsy were recorded despite a claimed tacrolimus adjustment.", "Added the trough pair and the biopsy."),
        "treatment_trajectory": _fail("The tacrolimus dose was unchanged, and valganciclovir was already a home drug.", "Tacrolimus frequency changes. Valganciclovir is new."),
        "laboratory_vital_trend": _pass("Creatinine 0.8 to 0.9 mg/dL and potassium 4.5 to 4.6 mmol/L were already stable and support the 900 mg dose and lisinopril."),
        "hospital_course_completeness": _fail("The adjustment was announced and not shown.", "The trough before and after the change is on the chart."),
        "medication_decision_support": _fail("No new tacrolimus dose was written.", "Transplant specifies 1 mg once daily."),
        "discharge_stability_chronology": _fail("Discharge weight was 68 kg against a dry weight of 70 kg.", "Discharge weight is set to the 70 kg dry weight."),
        "internal_consistency": _fail("Home and inpatient tacrolimus rows were identical while the note said the dose changed.", "Only the inpatient frequency changes."),
        "unsupported_hidden_reference_action": _fail("The clean reference continued tacrolimus 1 mg every 12 hours and home valganciclovir.", "The reference changes tacrolimus and starts valganciclovir."),
    }
    reference = {
        "medications": [
            _ref("valganciclovir 450 MG Oral Tablet", "start", "900 MG", "twice daily", "Cytomegalovirus colitis", "New start. Creatinine clearance is above 60 mL/min at creatinine 0.9 mg/dL and weight 70 kg."),
            _ref("BX Rating tacrolimus 1 MG Oral Capsule", "change", "1 MG", "once daily", "Kidney transplant", "Reduced from every 12 hours because the trough was 11.5 ng/mL. Discharge trough is 6.8 ng/mL, inside the stated 5 to 8 ng/mL target."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Creatinine and potassium are stable."),
            _ref("amlodipine 5 MG Oral Tablet", "continue", "5 MG", "once daily", "Hypertension", "Continued."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
        ],
        "monitoring_requirements": [{"parameter": "tacrolimus trough and creatinine", "frequency": "at transplant clinic in 7 days", "target": "5 to 8 ng/mL", "duration": None}],
        "follow_up_requirements": [{"item": "Transplant medication-dose follow-up", "timing": "7 days", "with_service": "transplant"}],
    }
    facts = [{"fact": "Trough 11.5 ng/mL reduced to a 1 mg daily dose, biopsy, and a new valganciclovir start. Discharge weight aligned to the 70 kg dry weight.", "why": "The clean chart claimed a tacrolimus adjustment and a new cytomegalovirus illness without either fact.", "evidence": "Kotton CN et al. Transplantation. 2018;102:900-931. Valganciclovir labeling uses 900 mg twice daily at creatinine clearance of at least 60 mL/min."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-815 shows the tacrolimus reduction that the clean chart only announced, and starts valganciclovir after the biopsy."


def revise_816(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _add_med(
        case, _med(case, "tacrolimus", "home"),
        medication_id="MED-VAL816-006", context="home", drug="mycophenolate mofetil 500 MG Oral Tablet",
        reported_name="mycophenolate mofetil 500 MG Oral Tablet", dose="1000 MG", route="oral",
        frequency="twice daily", indication="Kidney transplant status", status="home", notes="Given as 500 MG tablets.",
    )
    _add_med(
        case, _med(case, "tacrolimus", "inpatient"),
        medication_id="MED-VAL816-007", context="inpatient", drug="mycophenolate mofetil 500 MG Oral Tablet",
        reported_name="mycophenolate mofetil 500 MG Oral Tablet", dose="1000 MG", route="oral",
        frequency="twice daily", indication="Kidney transplant status", status="active",
        notes="Continued. This stay's decision is the antiviral duration, not a mycophenolate hold.",
    )
    _cmv_open(
        case,
        hpi=(
            "A 57-year-old man with a kidney transplant is admitted with one day of diarrhea and "
            "fatigue. He is not labeled with cytomegalovirus disease on arrival, and valganciclovir "
            "is not a home medicine. Home immunosuppression is tacrolimus 1 mg every 12 hours and "
            "mycophenolate mofetil 1000 mg twice daily, plus atorvastatin. Stool studies are negative. "
            "A biopsy on hospital day 2 shows cytomegalovirus. Creatinine is 1.0 mg/dL and stays "
            "near 0.9 mg/dL, and potassium is 3.6 mmol/L then 4.0 mmol/L. Creatinine clearance is "
            "above 60 mL/min, so valganciclovir 900 mg orally twice daily is started. Mycophenolate "
            "and tacrolimus continue. Infectious diseases has not set the antiviral stop date."
        ),
        admission_note="Diarrhea. No home valganciclovir. Creatinine 1.0 mg/dL.",
        course="Biopsy positive. Valganciclovir induction started. The stop date is the pending visit.",
    )
    _add_lab(case, lab_id="LAB-VAL816-003", timepoint="admission", test_name="Potassium [Moles/volume] in Serum or Plasma", value=3.6, unit="mmol/L")
    _add_lab(case, lab_id="LAB-VAL816-004", timepoint="discharge", test_name="Potassium [Moles/volume] in Serum or Plasma", value=4.0, unit="mmol/L")
    _consult(case, "transplant", "Maintenance tacrolimus and mycophenolate do not require a hold on this chart.", "Continue both. Creatinine is stable.", "CON-VAL816-TX")
    _consult(case, "infectious disease", "Biopsy-proven disease. Induction has started.", "Continue valganciclovir 900 mg twice daily. The stop date will be set at the visit.", "CON-VAL816-ID")
    findings = {
        "presentation_diagnosis_coherence": _fail("The arrival label was cytomegalovirus disease and valganciclovir was already listed at home.", "Diarrhea comes first. The antiviral is new."),
        "causal_context": _fail("Diarrhea was not investigated.", "Stool studies are negative and the biopsy is positive."),
        "diagnostic_workup": _fail("No confirmatory test was present.", "Added the biopsy."),
        "treatment_trajectory": _fail("The antiviral predated the diagnosis, and immunosuppression was only tacrolimus.", "Valganciclovir starts after the biopsy. Mycophenolate is added as continued maintenance, not as a hold."),
        "laboratory_vital_trend": _fail("Diarrhea had no potassium.", "Potassium is 3.6 then 4.0 mmol/L. Creatinine was already stable and supports 900 mg twice daily."),
        "hospital_course_completeness": _fail("Duration was called pending without a current order.", "The current order is induction valganciclovir, and only the stop date is pending."),
        "medication_decision_support": _fail("A one-drug transplant regimen could not show which medicine the duration decision belongs to.", "Mycophenolate and tacrolimus continue. The open decision is the antiviral stop date."),
        "discharge_stability_chronology": _pass("Creatinine is already stable and the patient is described as improving."),
        "internal_consistency": _fail("Home valganciclovir contradicted a new diagnosis.", "It is removed from the home list."),
        "unsupported_hidden_reference_action": _fail("The clean reference continued home valganciclovir as if the course length were known.", "The reference starts valganciclovir and leaves the stop date pending."),
    }
    reference = {
        "medications": [
            _ref("valganciclovir 450 MG Oral Tablet", "start", "900 MG", "twice daily", "Cytomegalovirus colitis", "New induction dose. Stop date is pending and is not assigned today."),
            _ref("mycophenolate mofetil 500 MG Oral Tablet", "continue", "1000 MG", "twice daily", "Kidney transplant", "Maintenance dose. This chart does not hold it."),
            _ref("BX Rating tacrolimus 1 MG Oral Capsule", "continue", "1 MG", "every 12 hours", "Kidney transplant", "Continued. Creatinine is stable."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
        ],
        "monitoring_requirements": [{"parameter": "viral load, creatinine, and blood count", "frequency": "at the infectious-diseases visit", "target": None, "duration": "until the stop date is chosen"}],
        "follow_up_requirements": [{"item": "Visit to set the valganciclovir stop date", "timing": "14 days", "with_service": "infectious disease"}],
    }
    facts = [{"fact": "Biopsy, a new valganciclovir start, mycophenolate 1000 mg twice daily as maintenance, and a potassium pair.", "why": "The clean chart had the VAL-813 labeling problem and only one immunosuppressant.", "evidence": "Kotton CN et al. Transplantation. 2018;102:900-931. CellCept labeling recommends 1 g orally twice daily after kidney transplantation. The stop date is intentionally not invented."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-816 starts valganciclovir after the biopsy and leaves only the stop date undecided. Mycophenolate continues."


def _hip(case: dict[str, Any], hpi: str, admission_note: str, course: str) -> None:
    _story(
        case,
        one_liner="Hip-fracture repair with warfarin held for surgery and then resumed",
        complaint="Hip fracture",
        admission_dx="Right femoral-neck fracture, after a fall",
        hpi=hpi,
        admission_note=admission_note,
        course=course,
    )
    case["CaseProcedure"] = [{
        "procedure_id": f"PROC-{case['case_id_code']}-001",
        "case_id": case["case_id_code"],
        "procedure_name": "Open reduction and internal fixation of a right femoral-neck fracture",
        "procedure_type": "surgical",
        "date": None,
        "timepoint": "hospital_day_1",
        "performed_by": "orthopedics",
        "anesthesia_type": None,
        "findings": "Fracture fixed. No intraoperative transfusion noted unless a laboratory note says otherwise.",
        "complications": None,
        "duration_minutes": None,
        "laterality": "right",
        "source_reference": None,
    }]
    _imaging(case, f"STUDY-{case['case_id_code']}-HIP", "Right hip radiograph", "Femoral-neck fracture. Postoperative films show hardware in place.", "hip")
    warfarin = _med(case, "warfarin", "inpatient")
    warfarin["notes"] = "Held on the day of surgery. Resumed the next evening."
    _consult(
        case, "orthopedics",
        "Fracture fixed. Weight bearing as instructed.",
        "Surgical fixation is complete. Anticoagulation is managed with the medical service.",
        f"CON-{case['case_id_code']}-ORTHO",
    )


def _hip_findings() -> dict[str, Finding]:
    return {
        "presentation_diagnosis_coherence": _pass("A femoral-neck fracture is a coherent reason for admission."),
        "causal_context": _fail("The fall and the operation were asserted more clearly than they were shown.", "The operation is now a procedure, and the radiograph is on the chart."),
        "diagnostic_workup": _fail("No operative or imaging record was present.", "Added the radiograph and the fixation procedure."),
        "treatment_trajectory": _fail("Warfarin was listed as continuously active while the note said it was interrupted.", "The inpatient note says it was held on the day of surgery and resumed the next evening."),
        "laboratory_vital_trend": _fail("The INR did not show a perioperative dip.", "An INR on the day of surgery is now below the admission value, and the discharge INR is the value already stored or the resumed value."),
        "hospital_course_completeness": _fail("Interruption and resumption had no sequence.", "Hold, operation, and resumption are ordered."),
        "medication_decision_support": _fail("Continuing warfarin could not be distinguished from never holding it.", "The chart says it was resumed and should continue, with INR follow-up."),
        "discharge_stability_chronology": _pass("Vital signs were already stable. The chronology of the anticoagulant is what was repaired."),
        "internal_consistency": _fail("The narrative and the always-active warfarin row disagreed.", "The row note and the narrative now both describe a hold and a resume."),
        "unsupported_hidden_reference_action": _fail("The clean reference continued warfarin without a visible interruption.", "The reference continues warfarin because the chart says it was resumed, and it stops enoxaparin only where a bridge is actually on the chart."),
    }


def revise_817(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hip(
        case,
        hpi=(
            "An 87-year-old man with atrial fibrillation falls and is admitted with a right femoral-neck "
            "fracture. Warfarin is held for fixation. Admission INR is 2.6 and the day-of-surgery INR "
            "is 1.3. Enoxaparin 40 mg subcutaneously once daily is used while the INR is below 2 and "
            "is stopped at discharge because the INR is 2.1. Warfarin 5 mg orally once daily was resumed "
            "the evening after surgery. Hemoglobin is 11.4 g/dL before surgery, 9.0 g/dL after, and "
            "10.1 g/dL at discharge, without transfusion. Lisinopril and metformin continue. Creatinine "
            "is 1.0 mg/dL. Anticoagulation clinic is in 7 days."
        ),
        admission_note="Femoral-neck fracture. INR 2.6. Warfarin held.",
        course="Fixation performed. Warfarin resumed. Enoxaparin stopped once the INR was 2.1.",
    )
    _set_lab(case, "discharge", "INR", 2.1)
    _add_lab(case, lab_id="LAB-VAL817-007", timepoint="day_of_surgery", test_name="INR in Platelet poor plasma or blood by Coagulation assay", value=1.3, unit="{INR}")
    _add_lab(case, lab_id="LAB-VAL817-008", timepoint="admission", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=1.0, unit="mg/dL")
    _add_med(
        case, _med(case, "lisinopril", "inpatient"),
        medication_id="MED-VAL817-007", context="inpatient",
        drug="0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe",
        reported_name="enoxaparin 40 MG", dose="40 MG", route="subcutaneous", frequency="once daily",
        indication="Bridge while INR was below 2", status="discontinued",
        notes="Stopped at discharge because INR is 2.1.",
    )
    findings = _hip_findings()
    findings["treatment_trajectory"] = _fail("The note mentioned enoxaparin that was not on the medication list, and warfarin looked continuous.", "Enoxaparin is on the list and stops at an INR of 2.1. Warfarin was held and resumed.")
    reference = {
        "medications": [
            _ref("warfarin sodium 5 MG Oral Tablet", "continue", "5 MG", "once daily", "Atrial fibrillation", "Resumed after surgery. Discharge INR is 2.1. Clinic follow-up is in 7 days."),
            _ref("0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe", "stop", "40 MG", "once daily", "Perioperative bridge", "Stopped because the INR is 2.1."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Creatinine is 1.0 mg/dL and blood pressure is stable."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Creatinine is 1.0 mg/dL and glucose is already in the 110 to 130 mg/dL range."),
        ],
        "monitoring_requirements": [{"parameter": "INR", "frequency": "within 7 days", "target": None, "duration": "after resumption"}],
        "follow_up_requirements": [{"item": "Anticoagulation clinic INR follow-up after warfarin resumption", "timing": "7 days", "with_service": "anticoagulation clinic"}],
    }
    facts = [{"fact": "Day-of-surgery INR 1.3, discharge INR 2.1, enoxaparin bridge, and the fixation procedure.", "why": "The clean chart said warfarin was interrupted and enoxaparin stopped, without showing either.", "evidence": "Perioperative warfarin is held for major surgery and bridged selectively. Enoxaparin 40 mg daily is the project's prophylactic regimen. The bridge stops once the INR is back in the 2 to 3 range."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-817 shows the warfarin hold, the operation, and an enoxaparin bridge that stops at an INR of 2.1."


def revise_818(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hip(
        case,
        hpi=(
            "A 79-year-old man with atrial fibrillation is admitted after a fall and a femoral-neck "
            "fracture. Warfarin is held. Admission INR is 2.3 and the day-of-surgery INR is 1.4. "
            "Warfarin 5 mg daily resumes the next evening. Discharge INR is 2.0. Hemoglobin is "
            "11.6 g/dL before surgery and 7.9 g/dL after. One unit of red cells is given. Discharge "
            "hemoglobin is 10.3 g/dL. Lisinopril and metformin continue. No enoxaparin is used. "
            "The discharge INR is already 2.0, so a bridge is not started at discharge."
        ),
        admission_note="Fracture. INR 2.3. Warfarin held. Postoperative hemoglobin 7.9 g/dL.",
        course="One unit of red cells given. Warfarin resumed. Discharge INR 2.0 and hemoglobin 10.3 g/dL.",
    )
    _add_lab(case, lab_id="LAB-VAL818-005", timepoint="day_of_surgery", test_name="INR in Platelet poor plasma or blood by Coagulation assay", value=1.4, unit="{INR}")
    _add_lab(case, lab_id="LAB-VAL818-006", timepoint="preoperative", test_name="Hemoglobin [Mass/volume] in Blood", value=11.6, unit="g/dL")
    _set_lab(case, "discharge", "INR", 2.0)
    findings = _hip_findings()
    findings["laboratory_vital_trend"] = _fail("Hemoglobin rose from 7.9 to 10.3 g/dL and the note said there was no transfusion.", "One unit of red cells explains the rise. A preoperative hemoglobin of 11.6 g/dL is added.")
    findings["internal_consistency"] = _fail("The no-transfusion sentence contradicted the hemoglobin rise, and warfarin looked continuous.", "Transfusion is now stated, and warfarin is held then resumed.")
    reference = {
        "medications": [
            _ref("warfarin sodium 5 MG Oral Tablet", "continue", "5 MG", "once daily", "Atrial fibrillation", "Resumed after surgery. Discharge INR is 2.0, so enoxaparin is not added."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Blood pressure is stable."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "He is eating. No creatinine rise is on the chart."),
        ],
        "monitoring_requirements": [{"parameter": "INR and hemoglobin", "frequency": "within 7 days", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Orthopedic and anticoagulation follow-up", "timing": "14 days", "with_service": "orthopedics"}],
    }
    facts = [{"fact": "One unit of red cells, a day-of-surgery INR of 1.4, and a discharge INR of 2.0.", "why": "The hemoglobin rise contradicted the no-transfusion sentence, and the warfarin hold was not visible.", "evidence": "A postoperative hemoglobin of 7.9 g/dL is a usual threshold at which a unit of red cells is considered. No bridge is added because the discharge INR is already 2.0."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-818 corrects the transfusion contradiction and shows the warfarin hold. No enoxaparin is added, because the discharge INR is already 2.0."


def revise_819(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hip(
        case,
        hpi=(
            "A 70-year-old woman with atrial fibrillation is admitted with a femoral-neck fracture. "
            "Warfarin is held for fixation. Admission INR is 2.5, the day-of-surgery INR is 1.3, and "
            "the discharge INR is 2.2 after warfarin 5 mg daily was resumed. A 14-day warfarin supply "
            "is in hand for the anticoagulation-clinic visit. Creatinine moves from 0.9 to 1.1 mg/dL. "
            "Lisinopril continues. No enoxaparin is required at discharge because the INR is 2.2."
        ),
        admission_note="Fracture. INR 2.5. Warfarin held.",
        course="Warfarin resumed. Discharge INR 2.2. Fourteen days of warfarin were dispensed.",
    )
    _add_lab(case, lab_id="LAB-VAL819-005", timepoint="day_of_surgery", test_name="INR in Platelet poor plasma or blood by Coagulation assay", value=1.3, unit="{INR}")
    _set_lab(case, "discharge", "INR", 2.2)
    findings = _hip_findings()
    findings["medication_decision_support"] = _fail("The follow-up mentioned supply without saying the tablets were dispensed.", "A 14-day supply is stated, matching the visit.")
    reference = {
        "medications": [
            _ref("warfarin sodium 5 MG Oral Tablet", "continue", "5 MG", "once daily", "Atrial fibrillation", "Resumed after surgery. Discharge INR is 2.2. A 14-day supply covers the clinic visit."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Creatinine is 1.1 mg/dL and blood pressure is stable."),
        ],
        "monitoring_requirements": [{"parameter": "INR", "frequency": "at the visit in 14 days", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Anticoagulation supply and INR follow-up", "timing": "14 days", "with_service": "anticoagulation clinic"}],
    }
    facts = [{"fact": "Day-of-surgery INR 1.3, discharge INR 2.2, and a stated 14-day warfarin supply.", "why": "The interruption was not visible, and the supply follow-up had no quantity.", "evidence": "The visit was already scheduled at 14 days. The supply matches that interval rather than a shortened one."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-819 shows the warfarin interruption and a 14-day supply that matches the scheduled visit."


def revise_820(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _hip(
        case,
        hpi=(
            "An 82-year-old woman with atrial fibrillation is admitted with a femoral-neck fracture. "
            "Admission INR is 3.2. Warfarin is held and the day-of-surgery INR is 1.4. Enoxaparin "
            "40 mg subcutaneously once daily is the bridge. Warfarin resumes after surgery. Discharge "
            "INR is 2.0, and enoxaparin stops. Hemoglobin is 8.3 g/dL after surgery. One unit of red "
            "cells is given. Discharge hemoglobin is 11.1 g/dL. Lisinopril and metformin continue. "
            "Glucose is stable."
        ),
        admission_note="Fracture. INR 3.2. Warfarin held. Postoperative hemoglobin 8.3 g/dL.",
        course="One unit of red cells. Warfarin resumed. Enoxaparin stopped at an INR of 2.0.",
    )
    _add_lab(case, lab_id="LAB-VAL820-007", timepoint="day_of_surgery", test_name="INR in Platelet poor plasma or blood by Coagulation assay", value=1.4, unit="{INR}")
    enox = _med(case, "enoxaparin", "inpatient")
    enox["status"] = "discontinued"
    enox["notes"] = "Bridge only. Stopped at discharge because INR is 2.0."
    _med(case, "warfarin", "inpatient")["notes"] = "Held for surgery. Resumed the next evening."
    findings = _hip_findings()
    findings["treatment_trajectory"] = _fail("Warfarin and enoxaparin were both simply active, and the note denied a transfusion.", "Enoxaparin stops at an INR of 2.0. One unit of red cells is recorded.")
    findings["internal_consistency"] = _fail("Hemoglobin rose from 8.3 to 11.1 g/dL under a no-transfusion sentence.", "The sentence is replaced by the transfusion.")
    reference = {
        "medications": [
            _ref("warfarin sodium 5 MG Oral Tablet", "continue", "5 MG", "once daily", "Atrial fibrillation", "Resumed after surgery. Discharge INR is 2.0."),
            _ref("0.4 ML enoxaparin sodium 100 MG/ML Prefilled Syringe", "stop", "40 MG", "once daily", "Perioperative bridge", "Stopped because the INR is 2.0."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Blood pressure is stable."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Glucose is already stable in the 120 mg/dL range."),
        ],
        "monitoring_requirements": [{"parameter": "INR", "frequency": "within 7 days", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Orthopedic rehabilitation follow-up and INR check", "timing": "10 days", "with_service": "orthopedics"}],
    }
    facts = [{"fact": "Day-of-surgery INR 1.4, one unit of red cells, and enoxaparin stopped at an INR of 2.0.", "why": "The bridge and the warfarin hold were not sequenced, and the hemoglobin rise contradicted the note.", "evidence": "Enoxaparin 40 mg daily is the prophylactic regimen already used on this chart. It stops when the INR is again at least 2."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-820 stops the enoxaparin bridge at an INR of 2.0 and records the transfusion that explains the hemoglobin."


def _bleed(case: dict[str, Any], hpi: str, admission_note: str, course: str, recommendation: str) -> None:
    _story(
        case,
        one_liner="Gastrointestinal bleeding that has stopped, with a stated anticoagulation plan",
        complaint="Black stools and fatigue",
        admission_dx="Gastrointestinal bleeding",
        hpi=hpi,
        admission_note=admission_note,
        course=course,
    )
    _consult(
        case, "gastroenterology",
        "Melena has stopped and the patient is hemodynamically stable. Endoscopy is not done during this stay.",
        recommendation,
        f"CON-{case['case_id_code']}-GI",
    )


def revise_821(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _bleed(
        case,
        hpi=(
            "A 78-year-old woman with atrial fibrillation is admitted after two days of melena and "
            "fatigue. She is not in shock. Blood pressure is stable. Apixaban 5 mg twice daily is "
            "held. Hemoglobin is 8.7 g/dL on arrival and 10.9 g/dL at discharge, and there is no "
            "further melena. Creatinine moves from 0.9 to 1.2 mg/dL. She is under 80 years old and "
            "weighs 83 kg, so the home apixaban dose remains the standard 5 mg dose when it is "
            "eventually appropriate. Gastroenterology says not to restart it today and to reassess "
            "at the visit in 7 days. Lisinopril and atorvastatin continue. No endoscopy has been done."
        ),
        admission_note="Melena. Apixaban held. Hemoglobin 8.7 g/dL. Not in shock.",
        course="No further melena. Hemoglobin rose. Apixaban remains held for the gastroenterology visit.",
        recommendation="Do not restart apixaban at discharge. Reassess in 7 days. The home dose, when restarted, is 5 mg twice daily.",
    )
    findings = {
        "presentation_diagnosis_coherence": _pass("Gastrointestinal bleeding is a coherent admission diagnosis once melena is stated."),
        "causal_context": _fail("Fatigue was the only symptom on a bleeding label.", "Melena is now the presenting symptom."),
        "diagnostic_workup": _fail("No statement said whether endoscopy had been done.", "Endoscopy is explicitly not done this stay, and the outpatient visit is the reassessment."),
        "treatment_trajectory": _pass("Apixaban was already held, which is the acute action."),
        "laboratory_vital_trend": _pass("Hemoglobin 8.7 to 10.9 g/dL and stable blood pressure were already on the chart."),
        "hospital_course_completeness": _fail("Bleeding settled was not tied to absence of further melena.", "The course says melena stopped."),
        "medication_decision_support": _fail("Gastroenterology said to hold and then reassess, while the reference restarted apixaban.", "The reference now holds apixaban."),
        "discharge_stability_chronology": _pass("Vital signs were already stable, and the chart says she is not in shock."),
        "internal_consistency": _fail("The consult and the restart reference disagreed.", "Both now say not to restart today."),
        "unsupported_hidden_reference_action": _fail("Restart was not what the consult recommended.", "Hold is the action. Restart after documented hemostasis is the alternative not chosen today."),
    }
    reference = {
        "medications": [
            _ref("apixaban 5 MG Oral Tablet", "hold", "5 MG", "twice daily", "Atrial fibrillation", "Gastroenterology says not to restart today. The 5 mg dose remains appropriate for her age, weight, and creatinine when the hold ends. Restart after documented hemostasis is the alternative not taken today."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Blood pressure is stable."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
        ],
        "monitoring_requirements": [{"parameter": "hemoglobin and any recurrent melena", "frequency": "sooner than 7 days if bleeding returns", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Gastroenterology visit to decide when apixaban restarts", "timing": "7 days", "with_service": "gastroenterology"}],
    }
    facts = [{"fact": "Melena, no in-hospital endoscopy, and an explicit decision not to restart apixaban today.", "why": "The clean reference restarted apixaban while gastroenterology had only said to reassess.", "evidence": "The chart's age, weight, and creatinine do not meet two of the three labeled criteria for apixaban 2.5 mg twice daily. That dose question is separate from today's hold."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-821 holds apixaban for the gastroenterology visit. The clean restart is not kept."


def revise_822(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _bleed(
        case,
        hpi=(
            "A 79-year-old woman is admitted with one day of melena and fatigue. She takes no "
            "anticoagulant. Hemoglobin is 8.5 g/dL then 10.7 g/dL, and melena stops. She is not in "
            "shock. Pantoprazole 40 mg orally once daily was started in the hospital. Gastroenterology "
            "says to continue it for four weeks, not to stop it on the day of discharge. Creatinine "
            "is 1.0 mg/dL. Lisinopril, atorvastatin, and metformin continue. Outpatient endoscopy is "
            "planned. No sepsis is present."
        ),
        admission_note="Melena. Hemoglobin 8.5 g/dL. Pantoprazole started. Not in shock.",
        course="Melena stopped. Pantoprazole continues for four weeks.",
        recommendation="Continue pantoprazole 40 mg daily for four weeks. Do not stop it at discharge.",
    )
    _add_lab(case, lab_id="LAB-VAL822-005", timepoint="admission", test_name="Creatinine [Mass/volume] in Serum or Plasma", value=1.0, unit="mg/dL")
    ppi = _med(case, "pantoprazole", "inpatient")
    ppi["notes"] = "Continue for four weeks, including after discharge."
    findings = {
        "presentation_diagnosis_coherence": _pass("Gastrointestinal bleeding is a coherent label once melena is stated."),
        "causal_context": _fail("Fatigue and nausea were not described as bleeding.", "Melena is added."),
        "diagnostic_workup": _fail("No plan said whether endoscopy would happen.", "Outpatient endoscopy is planned. None was done here."),
        "treatment_trajectory": _pass("Pantoprazole was already an inpatient start, which matches acid suppression for a bleed."),
        "laboratory_vital_trend": _fail("Metformin was continued with no creatinine.", "Creatinine is 1.0 mg/dL. The hemoglobin pair was already on the chart."),
        "hospital_course_completeness": _fail("Stability was asserted without saying melena had stopped.", "Melena has stopped and she is not in shock."),
        "medication_decision_support": _fail("The clean reference stopped pantoprazole at discharge.", "Gastroenterology continues it for four weeks."),
        "discharge_stability_chronology": _pass("Blood pressure was already stable."),
        "internal_consistency": _fail("A stop at discharge conflicted with acid suppression for an acute bleed.", "The note and the reference both continue a four-week course."),
        "unsupported_hidden_reference_action": _fail("Stopping pantoprazole was not supported.", "The reference continues pantoprazole 40 mg daily for four weeks and then stops. Indefinite therapy is the alternative not chosen."),
    }
    reference = {
        "medications": [
            _ref("pantoprazole 40 MG Delayed Release Oral Tablet", "continue", "40 MG", "once daily", "Recent gastrointestinal bleeding", "Continue for four weeks, then stop. Indefinite use is not the plan."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Blood pressure is stable."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Creatinine is 1.0 mg/dL and glucose has fallen."),
        ],
        "monitoring_requirements": [],
        "follow_up_requirements": [{"item": "Primary care and outpatient endoscopy after the bleed", "timing": "5 days", "with_service": "primary care"}],
    }
    facts = [{"fact": "Melena, a creatinine of 1.0 mg/dL, and a four-week pantoprazole course.", "why": "The clean reference stopped the only new bleed medicine on the day of discharge.", "evidence": "A proton-pump inhibitor is usual after gastrointestinal bleeding while outpatient evaluation is pending. The project's pantoprazole regimen is 40 mg orally once daily."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-822 continues pantoprazole for four weeks. The clean instruction to stop it at discharge is not kept."


def revise_823(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _bleed(
        case,
        hpi=(
            "A 71-year-old man with atrial fibrillation and diabetes is admitted with several days of "
            "melena and fatigue. He is not in shock. Apixaban 5 mg twice daily is held. Hemoglobin is "
            "9.0 g/dL then 10.2 g/dL, and there is no further melena. Creatinine is about 1.1 to "
            "1.2 mg/dL and weight is 109 kg. He does not meet two dose-reduction criteria, so 5 mg "
            "twice daily remains the dose if it restarts. Endoscopy is not done here. Cardiology in "
            "7 days will decide between restart and a longer hold. Do not restart apixaban today. "
            "Atorvastatin and metformin continue."
        ),
        admission_note="Melena. Apixaban held. Hemodynamically stable.",
        course="No further melena. The restart decision is deferred to cardiology in 7 days.",
        recommendation="Do not restart apixaban today. The 5 mg twice-daily dose is the one to reconsider at the visit.",
    )
    case["CaseFollowup"][0]["item"] = "Cardiology visit to choose restart or a longer hold of apixaban"
    findings = {
        "presentation_diagnosis_coherence": _pass("Bleeding is a coherent admission problem."),
        "causal_context": _fail("The pending anticoagulation decision had no description of the bleed.", "Melena and hemodynamic stability are stated."),
        "diagnostic_workup": _fail("It was unclear whether endoscopy had happened.", "No endoscopy this stay is now explicit."),
        "treatment_trajectory": _pass("Apixaban was already held."),
        "laboratory_vital_trend": _pass("The hemoglobin rise from 9.0 to 10.2 g/dL was already on the chart."),
        "hospital_course_completeness": _fail("Pending was stated without the stability facts.", "Melena has stopped and vital signs are stable."),
        "medication_decision_support": _pass("The clean reference already held apixaban, and the chart now says not to restart today."),
        "discharge_stability_chronology": _pass("The chart already said he was discharge-ready and not in shock. Blood pressure was normal."),
        "internal_consistency": _pass("Hold on the medication row and hold in the reference already agreed. The new sentences keep that agreement."),
        "unsupported_hidden_reference_action": _pass("Holding apixaban is defended by the consult. Restart at the visit is the named alternative, not today's action."),
    }
    reference = {
        "medications": [
            _ref("apixaban 5 MG Oral Tablet", "hold", "5 MG", "twice daily", "Atrial fibrillation", "Do not restart today. Cardiology decides in 7 days. The 5 mg dose is appropriate for his age, weight, and creatinine if it restarts."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Glucose is already near 100 mg/dL. Creatinine is about 1.2 mg/dL."),
        ],
        "monitoring_requirements": [{"parameter": "recurrent melena", "frequency": "sooner than the visit if bleeding returns", "target": None, "duration": None}],
        "follow_up_requirements": [{"item": "Cardiology visit to choose restart or a longer hold of apixaban", "timing": "7 days", "with_service": "cardiology"}],
    }
    facts = [{"fact": "Melena, no inpatient endoscopy, and an explicit instruction not to restart apixaban today.", "why": "The pending decision was real but the bleed itself was not described.", "evidence": "Apixaban labeling uses 5 mg twice daily unless at least two of age at least 80 years, weight at most 60 kg, and creatinine at least 1.5 mg/dL are present. This chart has none of those as a pair."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-823 keeps apixaban held. The added facts make that pending decision readable. They do not force a restart."


def revise_824(case: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Finding], str]:
    _bleed(
        case,
        hpi=(
            "A 77-year-old woman is admitted with a week of melena and fatigue. She has hypertension, "
            "hyperlipidemia, and diabetes, and no coronary disease or stent. Aspirin 81 mg daily, taken "
            "for primary prevention, is stopped and not restarted. Hemoglobin is 7.8 g/dL on arrival "
            "and 9.3 g/dL at discharge. There is no further melena and she is not in shock. Lisinopril, "
            "atorvastatin, and metformin continue. The gastroenterology note is about aspirin, not "
            "about an anticoagulant she does not take."
        ),
        admission_note="Melena. No coronary disease. Aspirin for primary prevention is stopped.",
        course="Melena stopped. Aspirin stays stopped. Hemoglobin is 9.3 g/dL.",
        recommendation="Do not restart aspirin. There is no stent or coronary disease on the history. Continue lisinopril, atorvastatin, and metformin.",
    )
    aspirin = _med(case, "aspirin", "inpatient")
    aspirin["held_reason"] = "Stopped after gastrointestinal bleeding. Primary prevention only. No coronary disease on the history."
    findings = {
        "presentation_diagnosis_coherence": _pass("Bleeding is a coherent admission diagnosis."),
        "causal_context": _fail("The bleed was named without melena.", "Melena is added."),
        "diagnostic_workup": _pass("The decision does not require a new in-hospital test beyond the hemoglobin already recorded."),
        "treatment_trajectory": _pass("Aspirin was already stopped during the admission."),
        "laboratory_vital_trend": _pass("Hemoglobin rose from 7.8 to 9.3 g/dL, and vital signs were stable."),
        "hospital_course_completeness": _fail("The course did not say whether bleeding continued.", "Melena has stopped."),
        "medication_decision_support": _fail("The gastroenterology sentence talked about anticoagulation, and this patient is on aspirin.", "The consult now says not to restart aspirin, and the history has no coronary disease."),
        "discharge_stability_chronology": _pass("Blood pressure at discharge was already 130/74 mm Hg."),
        "internal_consistency": _fail("An anticoagulation sentence sat on an aspirin case.", "The consult matches aspirin."),
        "unsupported_hidden_reference_action": _pass("Stopping aspirin for primary prevention after a bleed is supported once the missing coronary history is stated as absent."),
    }
    reference = {
        "medications": [
            _ref("aspirin 81 MG Chewable Tablet", "stop", "81 MG", "once daily", "Primary prevention", "Stopped after melena. No coronary disease or stent is on the history. Do not restart it."),
            _ref("lisinopril 10 MG Oral Tablet", "continue", "10 MG", "once daily", "Hypertension", "Blood pressure is 130/74 mm Hg."),
            _ref("atorvastatin 40 MG Oral Tablet", "continue", "40 MG", "once daily", "Hyperlipidemia", "Continued."),
            _ref("metformin hydrochloride 500 MG Oral Tablet", "continue", "500 MG", "twice daily", "Type 2 diabetes mellitus", "Continued. No creatinine crisis is described."),
        ],
        "monitoring_requirements": [],
        "follow_up_requirements": [{"item": "Primary care follow-up", "timing": "10 days", "with_service": "primary care"}],
    }
    facts = [{"fact": "Melena, absence of coronary disease, and a consult that names aspirin rather than anticoagulation.", "why": "The stop was announced, but the consult text did not match the drug.", "evidence": "After bleeding, aspirin used only for primary prevention is the drug the chart stops. No secondary-prevention indication is present to defend a restart."}]
    return _wrap(case, reference, facts, statement=NO_COMMENT, reviewer_note=None), findings, "VAL-824 stops aspirin for primary prevention and corrects the consult so it no longer talks about an anticoagulant."


LATER = (
    ("VAL-810", revise_810),
    ("VAL-811", revise_811),
    ("VAL-812", revise_812),
    ("VAL-814", revise_814),
    ("VAL-815", revise_815),
    ("VAL-816", revise_816),
    ("VAL-817", revise_817),
    ("VAL-818", revise_818),
    ("VAL-819", revise_819),
    ("VAL-820", revise_820),
    ("VAL-821", revise_821),
    ("VAL-822", revise_822),
    ("VAL-823", revise_823),
    ("VAL-824", revise_824),
)
