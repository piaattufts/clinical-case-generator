# Answer-leak audit for version 3

Resident JSON files were scanned for direct discharge instructions.
A phrase that describes an inpatient event or a recorded order is clinical evidence.

| Case | Phrase checked | Classification |
| --- | --- | --- |
| VAL-801 | none of the direct-leak phrases | CLINICAL_EVIDENCE |
| VAL-802 | none of the direct-leak phrases | CLINICAL_EVIDENCE |
| VAL-803 | none of the direct-leak phrases | CLINICAL_EVIDENCE |
| VAL-805 | none of the direct-leak phrases | CLINICAL_EVIDENCE |
| VAL-809 | none of the direct-leak phrases | CLINICAL_EVIDENCE |
| VAL-813 | none of the direct-leak phrases | CLINICAL_EVIDENCE |

Reviewed strong hints that were removed: geriatrics telling the reader to use the verified list at discharge; the sentence that there is no reason to stop ibuprofen; the sentence that no discharge medicine is stopped; and the instruction to complete the planned parenteral course.

Remaining clinical wording that is not a discharge order: oral intake resumed; hydrochlorothiazide held during the admission while sodium was 128 mmol/L; inpatient furosemide recorded as 40 mg oral once daily; ceftriaxone administered during the admission; valganciclovir started after the viral-load result.

DIRECT_ANSWER_LEAK count: 0.
