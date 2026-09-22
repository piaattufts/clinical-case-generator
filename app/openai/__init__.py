"""OpenAI integration.

Narrative assembly may run only after canonical concepts are selected in Python.
Raw MIMIC rows, notes, and patient-level data are never sent.
"""

from app.openai.narrative import CaseNarrative, assemble_narrative

__all__ = ["CaseNarrative", "assemble_narrative"]
