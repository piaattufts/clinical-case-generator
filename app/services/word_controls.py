"""Microsoft Word content controls for fillable validation casebooks.

python-docx does not create checkbox structured document tags. These helpers
write the OOXML that current desktop Word uses for a clickable checkbox
(w14:checkbox) and a short plain-text field (w:text). Reviewers do not need
macros, ActiveX, or document protection.
"""

from __future__ import annotations

import io
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

from docx.oxml import OxmlElement
from docx.oxml import ns as oxml_ns
from docx.oxml.ns import qn

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W14_NS = "http://schemas.microsoft.com/office/word/2010/wordml"
W15_NS = "http://schemas.microsoft.com/office/word/2012/wordml"
XML_NS = "http://www.w3.org/XML/1998/namespace"
FORM_COLOR = "2E75B6"
W15_DECLARATION = 'xmlns:w15="http://schemas.microsoft.com/office/word/2012/wordml"'

# python-docx only knows the prefixes in its own map. Word 2013 form
# appearance lives in the w15 namespace, so register it before building controls.
oxml_ns.nsmap["w15"] = W15_NS

CHECKBOX_FONT = "MS Gothic"
CHECKBOX_SIZE_PT = 14
TEXT_FONT = "Calibri"
TEXT_FIELD_SPACES = 36
UNCHECKED_CHAR = "\u2610"
CHECKED_CHAR = "\u2612"
BALLOT_CHARS = ("\u2610", "\u2611", "\u2612", "\u25A1", "\u25A2", "\u25FB")

_NEXT_ID: dict[int, int] = {}


def prepare_form_document(document: Any) -> None:
    """Make Word open this file as a current document, not a compatibility-mode file.

    python-docx writes compatibility mode 14. Desktop Word then shows the
    checkbox characters but does not treat them as form controls until the
    document is converted. Mode 16 is the current Word document format.
    """
    settings = document.settings.element
    for setting in settings.iter(qn("w:compatSetting")):
        if setting.get(qn("w:name")) == "compatibilityMode":
            setting.set(qn("w:val"), "16")


def finalize_word_form(path: Path) -> None:
    """Put the Word 2013 namespace on the document root after python-docx saves.

    Each control already declares xmlns:w15 locally. The root mc:Ignorable list
    also has to be able to name that prefix, and an undeclared prefix makes
    Word discard the form controls.
    """
    original = path.read_bytes()
    buffer = io.BytesIO()
    with (
        zipfile.ZipFile(io.BytesIO(original)) as source,
        zipfile.ZipFile(buffer, "w") as output,
    ):
        for info in source.infolist():
            payload = source.read(info.filename)
            if info.filename == "word/document.xml":
                payload = _declare_form_namespace(payload)
            output.writestr(info, payload)
    path.write_bytes(buffer.getvalue())


def _declare_form_namespace(payload: bytes) -> bytes:
    text = payload.decode("utf-8")
    text = text.replace(f' ns0:w15="{W15_NS}"', "")
    marker = "<w:document "
    begin = text.find(marker)
    if begin < 0:
        return text.encode("utf-8")
    end = text.find(">", begin)
    start = text[begin:end]
    if "xmlns:w15=" not in start:
        start = start.replace(marker, f"<w:document {W15_DECLARATION} ", 1)
    if 'mc:Ignorable="' in start and "w15" not in _ignorable_value(start):
        start = start.replace('mc:Ignorable="', 'mc:Ignorable="w15 ', 1)
    return (text[:begin] + start + text[end:]).encode("utf-8")


def _ignorable_value(start_tag: str) -> str:
    marker = 'mc:Ignorable="'
    begin = start_tag.find(marker)
    if begin < 0:
        return ""
    begin += len(marker)
    end = start_tag.find('"', begin)
    return start_tag[begin:end]


def append_checkbox(paragraph: Any, document: Any, *, tag: str, alias: str) -> None:
    """Append one unchecked Word checkbox content control to a paragraph."""
    paragraph._p.append(_checkbox_sdt(document, tag=tag, alias=alias))


def append_plain_text(paragraph: Any, document: Any, *, tag: str, alias: str) -> None:
    """Append one single-line plain-text content control to a paragraph."""
    paragraph._p.append(_plain_text_sdt(document, tag=tag, alias=alias))


def append_rich_text_field(cell: Any, document: Any, *, tag: str, alias: str, lines: int) -> None:
    """Append a multi-line rich-text content control inside a table cell."""
    cell._tc.append(_rich_text_sdt(document, tag=tag, alias=alias, lines=lines))


def _checkbox_sdt(document: Any, *, tag: str, alias: str) -> Any:
    half_points = str(CHECKBOX_SIZE_PT * 2)
    sdt = OxmlElement("w:sdt")
    properties = OxmlElement("w:sdtPr")
    properties.append(
        _run_properties(
            font=CHECKBOX_FONT,
            half_points=half_points,
            underline=False,
            east_asia_hint=True,
        )
    )
    properties.append(_string_element("w:alias", alias))
    properties.append(_string_element("w:tag", tag))
    properties.append(_string_element("w:id", _next_id(document)))
    _append_form_appearance(properties)
    checkbox = OxmlElement("w14:checkbox")
    checked = OxmlElement("w14:checked")
    checked.set(qn("w14:val"), "0")
    checked_state = OxmlElement("w14:checkedState")
    checked_state.set(qn("w14:val"), "2612")
    checked_state.set(qn("w14:font"), CHECKBOX_FONT)
    unchecked_state = OxmlElement("w14:uncheckedState")
    unchecked_state.set(qn("w14:val"), "2610")
    unchecked_state.set(qn("w14:font"), CHECKBOX_FONT)
    checkbox.append(checked)
    checkbox.append(checked_state)
    checkbox.append(unchecked_state)
    properties.append(checkbox)
    sdt.append(properties)
    sdt.append(OxmlElement("w:sdtEndPr"))
    sdt.append(_symbol_content(half_points))
    return sdt


def _plain_text_sdt(document: Any, *, tag: str, alias: str) -> Any:
    sdt = OxmlElement("w:sdt")
    properties = OxmlElement("w:sdtPr")
    properties.append(
        _run_properties(font=TEXT_FONT, half_points="22", underline=True, east_asia_hint=False)
    )
    properties.append(_string_element("w:alias", alias))
    properties.append(_string_element("w:tag", tag))
    properties.append(_string_element("w:id", _next_id(document)))
    _append_form_appearance(properties)
    text_mode = OxmlElement("w:text")
    text_mode.set(qn("w:multiLine"), "0")
    properties.append(text_mode)
    sdt.append(properties)
    sdt.append(OxmlElement("w:sdtEndPr"))
    content = OxmlElement("w:sdtContent")
    run = OxmlElement("w:r")
    run.append(
        _run_properties(font=TEXT_FONT, half_points="22", underline=True, east_asia_hint=False)
    )
    text = OxmlElement("w:t")
    text.set(qn("xml:space"), "preserve")
    text.text = " " * TEXT_FIELD_SPACES
    run.append(text)
    content.append(run)
    sdt.append(content)
    return sdt


def _rich_text_sdt(document: Any, *, tag: str, alias: str, lines: int) -> Any:
    sdt = OxmlElement("w:sdt")
    properties = OxmlElement("w:sdtPr")
    properties.append(_string_element("w:alias", alias))
    properties.append(_string_element("w:tag", tag))
    properties.append(_string_element("w:id", _next_id(document)))
    _append_form_appearance(properties)
    sdt.append(properties)
    sdt.append(OxmlElement("w:sdtEndPr"))
    content = OxmlElement("w:sdtContent")
    for _ in range(lines):
        paragraph = OxmlElement("w:p")
        run = OxmlElement("w:r")
        text = OxmlElement("w:t")
        text.set(qn("xml:space"), "preserve")
        text.text = " "
        run.append(text)
        paragraph.append(run)
        content.append(paragraph)
    sdt.append(content)
    return sdt


def _append_form_appearance(properties: Any) -> None:
    color = OxmlElement("w15:color")
    color.set(qn("w15:val"), FORM_COLOR)
    appearance = OxmlElement("w15:appearance")
    appearance.set(qn("w15:val"), "boundingBox")
    properties.append(color)
    properties.append(appearance)


def _symbol_content(half_points: str) -> Any:
    content = OxmlElement("w:sdtContent")
    run = OxmlElement("w:r")
    run.append(
        _run_properties(
            font=CHECKBOX_FONT,
            half_points=half_points,
            underline=False,
            east_asia_hint=True,
        )
    )
    text = OxmlElement("w:t")
    text.text = UNCHECKED_CHAR
    run.append(text)
    content.append(run)
    return content


def _run_properties(
    *,
    font: str,
    half_points: str,
    underline: bool,
    east_asia_hint: bool,
) -> Any:
    properties = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    for name in ("w:ascii", "w:hAnsi", "w:cs"):
        fonts.set(qn(name), font)
    if east_asia_hint:
        fonts.set(qn("w:eastAsia"), font)
        fonts.set(qn("w:hint"), "eastAsia")
    properties.append(fonts)
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), half_points)
    size_cs = OxmlElement("w:szCs")
    size_cs.set(qn("w:val"), half_points)
    properties.append(size)
    properties.append(size_cs)
    if underline:
        line = OxmlElement("w:u")
        line.set(qn("w:val"), "single")
        properties.append(line)
    return properties


def _string_element(tag: str, value: str) -> Any:
    element = OxmlElement(tag)
    element.set(qn("w:val"), value)
    return element


def _next_id(document: Any) -> str:
    key = id(document.element)
    current = _NEXT_ID.get(key, 1)
    _NEXT_ID[key] = current + 1
    return str(current)


def _clark(namespace: str, name: str) -> str:
    return f"{{{namespace}}}{name}"


@dataclass
class FormControlAudit:
    checkbox_controls: int = 0
    malformed_checkboxes: int = 0
    unchecked_checkboxes: int = 0
    checkboxes_by_case: dict[str, dict[str, int]] = field(default_factory=dict)
    plain_text_controls: int = 0
    malformed_plain_text: int = 0
    plain_text_by_case: dict[str, dict[str, int]] = field(default_factory=dict)
    static_ballot_glyphs: int = 0
    display_ballot_glyphs: int = 0
    wingdings_fonts: int = 0
    symbol_elements: int = 0
    macros: bool = False
    document_protection: bool = False
    activex_parts: int = 0
    duplicate_sdt_ids: int = 0
    w14_checkbox_start_tags: int = 0
    bounding_box_controls: int = 0
    rich_text_controls: int = 0
    compatibility_mode: str = ""
    xml_parts_well_formed: bool = False


def audit_form_controls(path: Path) -> FormControlAudit:
    """Inspect a DOCX package for checkbox SDTs and static ballot glyphs."""
    audit = FormControlAudit()
    with zipfile.ZipFile(path) as package:
        names = package.namelist()
        audit.macros = any(
            name.endswith("vbaProject.bin") or name.endswith("vbaData.xml") for name in names
        )
        audit.activex_parts = sum(1 for name in names if "activeX" in name or "ActiveX" in name)
        audit.xml_parts_well_formed = True
        for name in names:
            if not name.endswith((".xml", ".rels")):
                continue
            payload = package.read(name)
            try:
                root = ET.fromstring(payload)
            except ET.ParseError:
                audit.xml_parts_well_formed = False
                continue
            audit.document_protection = audit.document_protection or (
                root.find(f".//{_clark(W_NS, 'documentProtection')}") is not None
            )
            audit.static_ballot_glyphs += _static_ballot_count(root)
            audit.display_ballot_glyphs += _display_ballot_count(root)
            audit.symbol_elements += len(list(root.iter(_clark(W_NS, "sym"))))
            audit.wingdings_fonts += _wingdings_count(root)
            if name == "word/settings.xml":
                audit.compatibility_mode = _compatibility_mode(root)
            if name == "word/document.xml":
                _audit_document(root, audit)
                audit.w14_checkbox_start_tags = payload.count(b"<w14:checkbox")
    return audit


def _audit_document(root: ET.Element, audit: FormControlAudit) -> None:
    body = root.find(_clark(W_NS, "body"))
    if body is None:
        return
    case_id = "COVER"
    checkbox_counts: dict[str, Counter[str]] = defaultdict(Counter)
    text_counts: dict[str, Counter[str]] = defaultdict(Counter)
    seen_ids: list[str] = []
    paragraph_tag = _clark(W_NS, "p")
    for child in list(body):
        if child.tag == paragraph_tag and _style(child) == "Heading1":
            heading = _text(child)
            if heading.startswith("CASE VAL-"):
                case_id = heading.removeprefix("CASE ").strip()
        for control in child.iter(_clark(W_NS, "sdt")):
            properties = control.find(_clark(W_NS, "sdtPr"))
            if properties is None:
                continue
            tag = _attribute(properties.find(_clark(W_NS, "tag")), "val")
            seen_ids.append(_attribute(properties.find(_clark(W_NS, "id")), "val"))
            if _has_bounding_box(properties):
                audit.bounding_box_controls += 1
            if properties.find(_clark(W14_NS, "checkbox")) is not None:
                audit.checkbox_controls += 1
                checkbox_counts[case_id][tag] += 1
                if _checkbox_well_formed(control):
                    if _checked_value(control) in {"0", "false", "off"}:
                        audit.unchecked_checkboxes += 1
                else:
                    audit.malformed_checkboxes += 1
            elif properties.find(_clark(W_NS, "text")) is not None:
                audit.plain_text_controls += 1
                text_counts[case_id][tag] += 1
                if not _plain_text_well_formed(control):
                    audit.malformed_plain_text += 1
            else:
                audit.rich_text_controls += 1
    audit.checkboxes_by_case = {key: dict(value) for key, value in checkbox_counts.items()}
    audit.plain_text_by_case = {key: dict(value) for key, value in text_counts.items()}
    populated = [item for item in seen_ids if item]
    audit.duplicate_sdt_ids = len(populated) - len(set(populated))
    if len(populated) != len(seen_ids):
        audit.duplicate_sdt_ids += len(seen_ids) - len(populated)


def _checkbox_well_formed(control: ET.Element) -> bool:
    properties = control.find(_clark(W_NS, "sdtPr"))
    if properties is None:
        return False
    checkbox = properties.find(_clark(W14_NS, "checkbox"))
    if checkbox is None:
        return False
    checked = checkbox.find(_clark(W14_NS, "checked"))
    checked_state = checkbox.find(_clark(W14_NS, "checkedState"))
    unchecked_state = checkbox.find(_clark(W14_NS, "uncheckedState"))
    if checked is None or checked_state is None or unchecked_state is None:
        return False
    if _w14(checked, "val") not in {"0", "1", "false", "true", "off", "on"}:
        return False
    if _w14(checked_state, "val") != "2612" or _w14(checked_state, "font") != CHECKBOX_FONT:
        return False
    if _w14(unchecked_state, "val") != "2610" or _w14(unchecked_state, "font") != CHECKBOX_FONT:
        return False
    if not _attribute(properties.find(_clark(W_NS, "tag")), "val"):
        return False
    if not _attribute(properties.find(_clark(W_NS, "id")), "val"):
        return False
    if not _has_bounding_box(properties):
        return False
    content = control.find(_clark(W_NS, "sdtContent"))
    if content is None:
        return False
    display = "".join(node.text or "" for node in content.iter(_clark(W_NS, "t")))
    checked_value = _checked_value(control)
    if checked_value in {"0", "false", "off"} and display != UNCHECKED_CHAR:
        return False
    if checked_value in {"1", "true", "on"} and display != CHECKED_CHAR:
        return False
    expected_size = str(CHECKBOX_SIZE_PT * 2)
    sizes = [
        size.get(_clark(W_NS, "val"))
        for size in control.iter(_clark(W_NS, "sz"))
    ]
    return bool(sizes) and all(size == expected_size for size in sizes)


def _plain_text_well_formed(control: ET.Element) -> bool:
    properties = control.find(_clark(W_NS, "sdtPr"))
    content = control.find(_clark(W_NS, "sdtContent"))
    if properties is None or content is None:
        return False
    if properties.find(_clark(W_NS, "text")) is None:
        return False
    if not _has_bounding_box(properties):
        return False
    if not _attribute(properties.find(_clark(W_NS, "tag")), "val"):
        return False
    texts = list(content.iter(_clark(W_NS, "t")))
    if len(texts) != 1:
        return False
    node = texts[0]
    return node.text == " " * TEXT_FIELD_SPACES and node.get(_clark(XML_NS, "space")) == "preserve"


def _has_bounding_box(properties: ET.Element) -> bool:
    appearance = properties.find(_clark(W15_NS, "appearance"))
    return appearance is not None and _w15(appearance, "val") == "boundingBox"


def _compatibility_mode(settings: ET.Element) -> str:
    for setting in settings.iter(_clark(W_NS, "compatSetting")):
        if setting.get(_clark(W_NS, "name")) == "compatibilityMode":
            return setting.get(_clark(W_NS, "val")) or ""
    return ""


def _checked_value(control: ET.Element) -> str:
    properties = control.find(_clark(W_NS, "sdtPr"))
    if properties is None:
        return ""
    checkbox = properties.find(_clark(W14_NS, "checkbox"))
    if checkbox is None:
        return ""
    checked = checkbox.find(_clark(W14_NS, "checked"))
    if checked is None:
        return ""
    return _w14(checked, "val")


def _static_ballot_count(root: ET.Element) -> int:
    parents = _parents(root)
    count = 0
    sdt_tag = _clark(W_NS, "sdt")
    for node in root.iter(_clark(W_NS, "t")):
        hits = _ballot_hits(node.text or "")
        if hits == 0 or _has_ancestor(node, sdt_tag, parents):
            continue
        count += hits
    return count


def _display_ballot_count(root: ET.Element) -> int:
    parents = _parents(root)
    count = 0
    sdt_tag = _clark(W_NS, "sdt")
    for node in root.iter(_clark(W_NS, "t")):
        hits = _ballot_hits(node.text or "")
        if hits and _has_ancestor(node, sdt_tag, parents):
            count += hits
    return count


def _ballot_hits(value: str) -> int:
    return sum(value.count(character) for character in BALLOT_CHARS)


def _wingdings_count(root: ET.Element) -> int:
    count = 0
    for node in root.iter():
        for attribute, value in node.attrib.items():
            if attribute.endswith("}ascii") or attribute.endswith("}hAnsi") or "font" in attribute:
                if "wingding" in value.lower():
                    count += 1
    return count


def _parents(root: ET.Element) -> dict[ET.Element, ET.Element]:
    parents: dict[ET.Element, ET.Element] = {}
    for node in root.iter():
        for child in list(node):
            parents[child] = node
    return parents


def _has_ancestor(node: ET.Element, tag: str, parents: dict[ET.Element, ET.Element]) -> bool:
    current: ET.Element | None = node
    while current is not None:
        if current.tag == tag:
            return True
        current = parents.get(current)
    return False


def _style(paragraph: ET.Element) -> str:
    properties = paragraph.find(_clark(W_NS, "pPr"))
    if properties is None:
        return ""
    return _attribute(properties.find(_clark(W_NS, "pStyle")), "val")


def _text(element: ET.Element) -> str:
    return "".join(node.text or "" for node in element.iter(_clark(W_NS, "t")))


def _attribute(element: ET.Element | None, name: str) -> str:
    if element is None:
        return ""
    return element.get(_clark(W_NS, name)) or ""


def _w14(element: ET.Element, name: str) -> str:
    return element.get(_clark(W14_NS, name)) or ""


def _w15(element: ET.Element, name: str) -> str:
    return element.get(_clark(W15_NS, name)) or ""
