# Eligibility criteria

Status: taken from the implementation brief. Confirm against `InTheWild_Review_Methods.docx` before screening. This file does not resolve open protocol questions.

## Include when all of these are supported by the report

- The system is a physically embodied social robot.
- People interact with it.
- The interaction is naturalistic in the sense below, or it is repeated everyday-use interaction as defined below.
- There is an identifiable interaction situation. The authors do not have to call it a scenario.
- The report is primary research rather than a review, commentary, or protocol-only paper.
- Setting, duration, and interaction structure can be extracted. Poor reporting of other variables is not a reason to exclude.

## Naturalistic or in-the-wild interaction

Any one of the following is enough:

1. Interaction in the intended use setting. Examples named in the brief: private home, care home, hospital, school, museum, shop, workplace, public space.
2. Interaction in a purpose-built high-fidelity environment that is used as the target setting, such as a furnished test house.
3. Repeated interaction in a laboratory: more than one session with the same participants, explicitly framed as everyday use.

Do not exclude a paper only because the authors use the word laboratory.

## Not eligibility thresholds

- Physical fidelity: how closely the physical environment resembles intended use.
- Contextual fidelity: how closely participant role, goals, and activities resemble actual use.

Record both during extraction. A low value on either one does not automatically exclude the study.

## Scenario

A scenario is a structured representation or enactment of a human–robot situation that contains enough contextual information to situate robot behaviour within a use or evaluation context.

Code an explicit scenario when the paper presents one. Code an implicit scenario when the deployment itself enacts an everyday activity. Use `UNCLEAR` for scenario explicitness when the coder cannot tell which of those applies. That value is not the same as `NOT_REPORTED_OR_UNCLEAR` on a yes/no field.

## Conceptual scenario papers

Whether a conceptual scenario contribution is included on its own, without an evaluation, is unresolved. Do not invent a local rule. Leave the record as MAYBE or discuss it in the decision log before excluding it for that reason alone.

## Title and abstract exclusion codes

Use one code when the decision is EXCLUDE. Definitions and the instruction not to treat a laboratory label as sufficient for `N1_NOT_NATURALISTIC` are in `protocol/screening_manual.md`.

## Full text

Inclusion at full text requires the report to confirm:

- a physically embodied social robot
- human participant interaction
- a naturalistic setting or repeated sessions as defined above
- an identifiable interaction situation
- enough reporting to extract setting, duration, and interaction structure

If the full text does not say, code `UNCLEAR`. Do not fill `YES` or `NO` from the title, from other papers, or from what the robot is generally known to do.
