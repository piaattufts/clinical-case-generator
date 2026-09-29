# Prompt used to generate the CliniProof Word review package

This is the prompt used to generate the resident/clinician-facing Word exports in this directory. It is retained for methodological transparency and reproducibility.

The prompt controls rendering and export only. It does not constitute the clinical source of truth; the active structured case datasets remain the source of truth.

## Exact prompt

````text
You are working in:
`https://github.com/piaattufts/clinical-case-generator`
# Goal
Create polished Microsoft Word `.docx` documents that I can send directly to the resident reviewers.
I need THREE deliverables:
1. **Balanced case set**
   * one DOCX containing all current balanced cases
2. **Seed-guided case set**
   * one DOCX containing all current seed-guided cases
3. **Resident validation codebook**
   * one DOCX explaining how residents should read and validate the cases
The cases must be presented in a **human-readable clinical chart format**, similar in readability and organization to the original resident seed cases.
They must NOT look like JSON exports.
Most importantly:
# DO NOT HALLUCINATE OR ADD CLINICAL INFORMATION
This is an export/rendering task.
Do not invent, infer, repair, embellish, or medically complete any case while creating the Word documents.
Every patient-specific clinical fact in the DOCX must come directly from the current active case data in the repository.
If a field is absent in the source case:
* omit that subsection when appropriate, or
* state `Not specified` only if that is already the rendering convention.
Do NOT use medical knowledge to fill missing information.
Do NOT add a medication, diagnosis, lab, procedure, monitoring plan, follow-up appointment, symptom, allergy, dose, route, frequency, or clinical rationale that is not present in the case source.
---
# 1. Determine the current active datasets first
Do not blindly rely on old version names.
Inspect:
* root README
* `data/README.md`
* `data/case_sets/README.md`
* active case-set manifests
* active validation registry
* balanced case-set README
* seed-guided case-set README
Identify the two CURRENT prospective case sets.
I expect them to correspond to approximately:
* `CLINIPROOF_BALANCED_V4`
* VAL-701–VAL-724
and:
* `CLINIPROOF_SEEDCASES_V3`
* VAL-801–VAL-824
But use the repository as the source of truth.
If the current batch codes or paths have changed, use the current active versions and report the exact values.
Do not export archived or superseded cases.
---
# 2. Source-of-truth rule
For each case, establish ONE canonical source of truth.
Prefer the current structured active case artifact used to generate the resident-readable export.
The DOCX renderer must derive its contents from that source.
Do NOT manually copy information from:
* old README examples
* old archived case sets
* teaching cases
* investigator notes
* historical JSON
* old seed examples
unless those are explicitly part of the current active case.
The resident seed examples are design inputs for the seed-guided generator. They are NOT the source of patient facts for the current VAL cases.
---
# 3. Do not use LLM generation for the DOCX
The Word documents must be produced deterministically from existing repository data.
Do NOT call OpenAI or another LLM to:
* summarize a case
* rewrite a hospital course
* create an HPI
* infer a diagnosis
* explain a medication
* construct a discharge plan
* improve clinical wording
* fill missing sections
Use Python or another deterministic document-generation library.
`python-docx` is appropriate.
The DOCX step must be:
```text
existing case data
        ↓
deterministic renderer
        ↓
Word document
```
NOT:
```text
existing case
        ↓
LLM rewriting
        ↓
Word document
```
---
# 4. Required output files
Create:
```text
exports/word/
    CliniProof_Balanced_Case_Set.docx
    CliniProof_Seed_Guided_Case_Set.docx
    CliniProof_Resident_Validation_Codebook.docx
```
Use more specific batch-coded filenames too if useful, but also create or preserve these simple names for distribution.
For example:
```text
CliniProof_Balanced_CLINIPROOF_BALANCED_V4.docx
CliniProof_Seed_Guided_CLINIPROOF_SEEDCASES_V3.docx
```
Do not create dozens of individual DOCX files unless there is a strong reason.
The principal deliverable should be one document per dataset.
---
# 5. Balanced case-set DOCX
The first page should contain:
# CliniProof Balanced Structured Case Set
Then:
* Batch code
* Case range
* Number of cases
* Status
* Generation approach
* Date of export
Add a short statement:
> These are synthetic clinical cases generated for medication-reconciliation and transition-of-care assessment. They are currently intended for clinician/resident review and validation.
Do not discuss archives.
Do not discuss old versions.
Do not expose answer keys.
---
# 6. Seed-guided case-set DOCX
First page:
# CliniProof Resident-Seed-Guided Case Set
Then:
* Batch code
* Case range
* Number of cases
* Status
* Generation approach
* Date of export
Add a brief explanation:
> This case set was developed using six resident-provided clinical examples as design inputs. Those examples were abstracted into clinical archetypes and used to generate new synthetic encounters. The current cases are not copies of the original resident cases.
Do not put the original resident cases into this document.
Do not copy patient-specific details from the original examples unless they independently exist in the generated VAL case.
---
# 7. Word case format
Each case should begin on a NEW PAGE.
Use a clean Word heading:
```text
VAL-701
```
or the actual case ID.
Under it, present the case as a clinical chart.
Use approximately this structure, but render only fields actually supported by the current case schema.
## Patient overview
Include available items such as:
* Age
* Sex/gender
* Weight
* Clinical setting/specialty
* Admission diagnosis
* Disposition
Do not invent missing demographics.
---
## Reason for hospitalization
Use available fields:
* Chief complaint
* Presenting symptoms
* Symptom duration
* Symptom course
* History of present illness
Do not generate an HPI if none exists.
---
## Relevant medical history
Present:
* relevant diagnoses
* past medical history
* relevant chronic conditions
* allergies if present
* social context if present and clinically relevant
Do not write generic filler.
---
## Hospital course
Present the hospital-course text exactly from the active case source, apart from deterministic formatting cleanup such as whitespace.
Do not summarize it.
Do not add interpretations.
---
## Admission clinical status
### Vital signs
Use a readable table.
For example:
| Measure        | Value |
| -------------- | ----- |
| Blood pressure | ...   |
| Heart rate     | ...   |
Only include available values.
### Laboratory findings
Use:
| Laboratory test | Result | Unit |
| --------------- | -----: | ---- |
If the case distinguishes admission versus subsequent/discharge values, preserve that temporal distinction exactly.
Do not combine results from different timepoints.
---
## Discharge / most recent clinical status
Present available:
* vital signs
* labs
* weight
* symptoms
* relevant clinical state
Preserve source timepoints.
---
# 8. Medication tables
This section is critical.
The Word export must clearly separate:
## Home medications
## Medications during hospitalization
## Discharge medications
Use readable tables.
Suggested columns:
| Medication | Dose | Route | Frequency | Indication / relevant note |
| ---------- | ---- | ----- | --------- | -------------------------- |
Use the exact current case values.
DO NOT:
* correct doses
* standardize frequencies from medical knowledge
* substitute brand/generic names unless already represented
* infer missing indications
* infer route
* infer why a medication was held
* add monitoring
If structured dose, route, frequency, indication, or temporal role exists, use it exactly.
---
# 9. Medication reconciliation
If the current resident-visible case includes medication reconciliation information, render it in its own section:
## Medication reconciliation
Examples of source-supported items may include:
* medication-history source
* patient participation
* caregiver involvement
* pharmacy confirmation
* pharmacist involvement
Do not convert investigator metadata into resident-facing prose.
---
# 10. Monitoring and follow-up
Keep these distinct.
## Monitoring
Render ONLY monitoring tasks present in the current case.
## Follow-up
Render ONLY appointments/follow-up present in the current case.
Do not infer that an anticoagulation appointment automatically means a lab order.
Do not infer missing monitoring.
Do not repair a deliberately missing monitoring plan.
This is essential because missing monitoring may itself be an assessment target.
---
# 11. Discharge instructions
Render the existing resident-visible discharge instructions.
Do NOT add:
* recommendations
* explanations
* medication corrections
* warnings not present in the source
* interpretation of the intended assessment issue
---
# 12. Other clinical information
Where available, include structured subsections such as:
## Imaging
## Procedures
## Consultations
## Microbiology
## Other results
Use the actual case content only.
---
# 13. Preserve ambiguity when it is part of the case
This is very important.
Do NOT "fix" a case during export simply because something looks incomplete.
For example, if a resident is supposed to detect:
* missing monitoring
* inadequate supply
* unresolved restart decision
* medication omission
* wrong frequency
* unintended continuation
the Word document must preserve the actual resident-facing state.
The renderer must not accidentally reveal or correct the intended target.
---
# 14. No answer keys in the case DOCX files
The two resident-facing case-set documents must NEVER expose:
* intended error category
* error family
* clean expected value
* injected value
* correct action
* answer key
* control/error-bearing flag
* target field
* investigator note
* expected discharge state
* hidden assessment metadata
Do not label cases as:
```text
CONTROL
ERROR
F1
F2
OMISSION
MONITORING ERROR
```
The residents must receive only the clinical chart.
---
# 15. Codebook DOCX
Create:
`CliniProof_Resident_Validation_Codebook.docx`
This should be concise but complete.
It should explain the review process without revealing case-specific answers.
Suggested structure:
# CliniProof Resident Validation Codebook
## Purpose
Explain briefly that the cases are synthetic inpatient cases designed for medication-reconciliation and transition-of-care assessment.
Residents are being asked to determine whether each case is clinically coherent and usable for the planned dashboard/study.
---
## The two case sets
Explain:
### Balanced structured set
Generated from predefined structured clinical profiles to provide controlled coverage across several inpatient scenarios.
### Resident-seed-guided set
Generated from clinical archetypes abstracted from six resident-provided example cases.
Clarify:
> The generated cases are new synthetic encounters and are not copies of the resident-provided source cases.
Do not say one approach is better.
---
# 16. How this connects to the dashboard
Include a short section:
## How these cases connect to the CliniProof dashboard
Explain simply:
The same underlying case structure is intended to populate the dashboard.
Residents using the dashboard will review different parts of the synthetic chart, including:
* clinical presentation
* medical history
* laboratory results
* home medication list
* inpatient medication list
* discharge medication list
* monitoring
* follow-up
* discharge information
The current Word documents let the reviewers validate the clinical content before those cases are administered through the dashboard.
The dashboard is the presentation/interaction layer.
The case generator provides the underlying clinical content and concealed scoring reference.
Do NOT claim dashboard features that are not currently implemented.
If particular dashboard functionality remains planned, explicitly say:
`planned`
rather than describing it as completed.
---
# 17. Explain medication reconciliation simply
Add:
## What to look for when reading a case
Explain that medication reconciliation involves comparing:
```text
Home medications
        ↓
Medications during hospitalization
        ↓
Discharge medications
```
while also considering:
* indication
* dose
* route
* frequency
* intentional holds/stops
* newly started medications
* monitoring
* supply
* restart decisions
* follow-up
Do not tell the reviewers which problem exists in any individual case.
---
# 18. Validation rubric
The codebook must explain C1–C5.
Use the current repository's definitions as the source of truth.
Do not invent new criteria.
## C1 — Clinical plausibility
Does this reasonably represent an inpatient clinical encounter?
Where the existing rubric contains domains, preserve them:
* presentation and demographics
* fit between presentation and diagnosis
* vital signs
* laboratory findings
* medication regimen
* hospital course
* consistency across the chart
* discharge plan and follow-up
Use the existing response scale exactly if it is already defined in the current codebook/rubric.
Do not change scoring.
---
## C2 — Intended assessment problem
Does the case actually contain the medication-reconciliation or transition-of-care problem it was designed to assess?
This criterion may require investigator-side reference information during formal validation.
Do not reveal the target in the general resident codebook.
If these residents are acting as clinician validators and therefore will receive the target separately, explain that this information will be provided through the validation packet rather than embedded in the blinded case.
---
## C3 — Detectability
Could an internal-medicine resident identify and resolve the problem using only the information available in the case?
Ask reviewers to consider:
* enough evidence
* missing information
* ambiguity
* answer-revealing cues
---
## C4 — Absence of competing problems
Apart from the intended problem, is there another clinically meaningful medication-reconciliation or transition-of-care problem that could reasonably be interpreted as an alternative assessment target?
---
## C5 — Expected learner difficulty
Ask reviewers for a provisional expert estimate.
Clearly explain:
> Actual case difficulty will ultimately be determined from resident performance rather than expert judgment alone.
---
# 19. Recommendation
Use the current recommendation categories exactly.
Expected:
* Accept
* Revise
* Exclude
If repository wording differs, use the repository wording.
---
# 20. Optional free-text comments
The codebook should encourage reviewers to identify:
* exact clinical concern
* case section
* medication/lab/problem involved
* suggested correction where appropriate
But the DOCX must not require them to rewrite the whole case.
---
# 21. Codebook must not become an answer key
The codebook may describe TYPES of possible medication-reconciliation problems.
It must NOT map:
```text
VAL-701 → omission
VAL-702 → monitoring
...
```
No individual case targets.
No clean/error labels.
No answer-key table.
---
# 22. Make the Word documents look professional
Use consistent styles:
* Title
* Heading 1
* Heading 2
* Heading 3
* normal body text
* readable tables
Use:
* page numbers
* footer with CliniProof and batch name
* table of contents if practical
* page break before every case
* reasonable margins
* readable font
* consistent spacing
Do not overdesign.
This is a clinical research document.
---
# 23. Use the seed-case readability as the model
The active generated cases should read like the original resident-provided seed cases in the sense that they should feel like understandable clinical cases rather than database exports.
This means:
* meaningful clinical headings
* paragraphs where narrative fields exist
* readable medication tables
* readable laboratory tables
* temporal organization
* no JSON braces
* no raw internal field names unless clinically useful
* no schema clutter
But DO NOT rewrite current VAL cases to imitate facts from the seed cases.
Match the presentation, not the content.
---
# 24. Hallucination-prevention QA
This is mandatory.
After generating each DOCX, perform a programmatic verification against the canonical source.
For every VAL case verify:
### Identity
* correct VAL ID
* exactly once in the correct document
* no missing cases
* no duplicate cases
### Clinical fields
For every rendered patient-specific fact, confirm it exists in the source.
Check at minimum:
* age
* sex
* weight
* diagnosis
* symptoms
* PMH
* vitals
* lab names
* lab values
* lab units
* medications
* dose
* route
* frequency
* indication
* medication temporal role
* monitoring
* follow-up
* disposition
* imaging
* procedures
* consultations
The test should fail if the renderer contains a patient-specific fact that cannot be traced to the source case.
---
# 25. Medication-level exactness test
Create an automated comparison for each case:
```text
source home medication set
vs
DOCX-rendered home medication set
source inpatient medication set
vs
DOCX-rendered inpatient medication set
source discharge medication set
vs
DOCX-rendered discharge medication set
```
Compare:
* medication identity
* dose
* route
* frequency
All must match.
If they do not match, fail the export.
Do not silently repair them.
---
# 26. Numeric exactness
No numeric patient-specific values may be invented or altered by formatting.
For example:
```text
source potassium = 3.4 mmol/L
```
must not become:
```text
3.5 mmol/L
```
Likewise:
* creatinine
* INR
* hemoglobin
* weight
* blood pressure
* heart rate
* temperature
* oxygen saturation
Preserve appropriate source precision.
Do not add reference ranges unless they already exist in the source.
---
# 27. Text fidelity
Narrative sections may receive only minimal deterministic formatting changes:
Allowed:
* whitespace normalization
* bullet formatting
* paragraph breaks
* table conversion
* capitalization of headings
Not allowed:
* summarization
* paraphrasing patient-specific content
* making prose "more medically correct"
* replacing terminology
* inserting explanatory clinical sentences
The Word export should preserve source meaning exactly.
---
# 28. No old bad examples
Do not use the older teaching snapshots as templates for clinical content.
In particular, do not accidentally reintroduce older problems such as:
* outdated medication doses
* once-daily apixaban examples
* old metoprolol formulations
* old ceftriaxone route/dose examples
* historical incomplete medication regimens
Use only the current active case source.
---
# 29. Investigator artifacts remain separate
Do not place the investigator answer key in these three documents.
If it is useful to create an investigator DOCX later, leave the existing structured investigator artifacts unchanged.
For this task the three deliverables are:
```text
BALANCED CASES
SEED-GUIDED CASES
RESIDENT VALIDATION CODEBOOK
```
No answer-key document.
---
# 30. Render and visually inspect DOCX files
After creation:
1. open or render each DOCX to PDF/images if available
2. inspect several pages from beginning, middle, and end
3. verify tables do not overflow
4. verify headings are not orphaned
5. verify a case does not accidentally begin halfway through the previous case
6. verify medication tables are readable
7. verify long clinical text wraps normally
Specifically visually inspect at least:
* first balanced case
* middle balanced case
* final balanced case
* first seed-guided case
* middle seed-guided case
* final seed-guided case
* codebook first page
* C1–C5 section
---
# 31. Create a traceability report
Also produce a plain Markdown or text QA report:
```text
exports/word/DOCX_EXPORT_QA.md
```
Include:
## Balanced set
* batch
* expected case count
* exported case count
* missing cases
* duplicate cases
* medication mismatches
* numeric mismatches
* unsupported/generated facts
* result: PASS/FAIL
## Seed-guided set
same fields.
## Codebook
* source documentation used
* scoring/rubric fidelity
* answer-key leakage check
* result
A PASS requires:
```text
unsupported/generated patient-specific facts = 0
```
---
# 32. Tests
Add deterministic tests for the Word exporter.
At minimum:
1. correct active batch selected
2. archived cases excluded
3. all balanced VAL IDs exported once
4. all seed-guided VAL IDs exported once
5. no answer-key fields in resident DOCX
6. medication fields exactly match source
7. lab numeric values exactly match source
8. current monitoring/follow-up exactly preserved
9. no LLM/API call during DOCX generation
10. codebook definitions match current clinical-validation documentation
11. all DOCX files open successfully
12. no raw JSON is shown in the case document
13. no current case is silently modified during export
Run the repository test suite as well.
---
# 33. Do not change case content during this task
This task should not trigger another round of case generation.
Do NOT regenerate the 48 active cases just to make the Word files.
Do NOT change the random seed.
Do NOT alter case content to improve formatting.
Do NOT alter batch membership.
Do NOT modify the answer key.
If a genuine source-case problem is discovered during export:
1. stop treating it as a formatting issue
2. document the case ID and exact problem in the QA report
3. leave the source case unchanged
4. report it to me
Do not silently fix it inside the DOCX.
This is critical for provenance.
---
# 34. Final document names
The final files should be easy for me to send to residents:
```text
CliniProof_Balanced_Case_Set.docx
CliniProof_Seed_Guided_Case_Set.docx
CliniProof_Resident_Validation_Codebook.docx
```
---
# 35. Final report to me
When finished, report:
## Data source
1. balanced batch code
2. balanced VAL range
3. seed-guided batch code
4. seed-guided VAL range
5. canonical source files used
## Balanced DOCX
6. output path
7. number of cases
8. case IDs
9. medication fidelity result
10. numeric fidelity result
11. unsupported-fact count
## Seed-guided DOCX
12. output path
13. number of cases
14. case IDs
15. medication fidelity result
16. numeric fidelity result
17. unsupported-fact count
## Codebook
18. output path
19. source documentation used
20. C1–C5 fidelity check
21. answer-key leakage result
22. dashboard wording checked against implemented/planned status
## QA
23. DOCX rendering/visual inspection result
24. automated test result
25. full repository test result
26. QA report path
Finally answer these four questions:
### A
Did every patient-specific fact in the two case-set DOCX files originate from the current active case source?
### B
Did the DOCX exporter add or infer any clinical information?
### C
Do the medication lists, doses, routes, frequencies, labs, monitoring and follow-up exactly match the current source cases?
### D
Are the documents ready to send to residents without exposing investigator answer keys?
A, C and D must be `YES`.
B must be `NO`.
If that is not true, do not report the export as complete.
````
