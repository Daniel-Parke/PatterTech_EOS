#!/usr/bin/env python3
"""Criterion 9: the dosage field is labelled, says what to do, and holds on.

Three clauses against the delivered markup and scripts.

The label is read as a programmatic one: a `<label for>` pointing at
the field's id, or a label wrapped around it. An `aria-label` alone is
not accepted, because the brief has a pharmacist reading a dense screen
under fluorescent light and an invisible label is not a label to them.

The error message is found through `aria-describedby`,
`aria-errormessage` or an error container beside the field, and then
read for an instruction: a verb telling the pharmacist what to do next
rather than a noun telling them what happened. That clause is J5 in the
pack's own checks, filed there as judgement, and the keyword test here
is a proxy for a human read. It catches "Invalid input" and it would
accept a fluent sentence that says nothing useful, so a pass on this
clause is weaker than a pass on the other two.

The third clause, that a value survives a failed submit, is settled
structurally rather than by driving the form: a value bound back into
the field, or a submit handler that prevents the default and never
clears the field, or a test that names the behaviour. A handler that
resets the form fails outright, which is the defect the brief calls out
by name.
"""

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, SCRIPT_SUFFIXES, emit, read, rel,  # noqa: E402
                     scratch_dir, walk)

CID = "c9"

FIELD_TAGS = {"input", "select", "textarea"}
VOID = {"input", "img", "br", "hr", "meta", "link", "source", "col"}
DOSE = re.compile(r"dos", re.I)

INSTRUCTION = re.compile(
    r"\b(enter|type|use|choose|select|check|give|correct|add|remove|"
    r"re-?enter|retype|try|must be|should be|needs to be|between|"
    r"cannot be|no more than|at least)\b", re.I)

BINDING = re.compile(r"\{\{|\{[\w$.\[\]]+\}|\$\{|<%|@value|:value|v-model|"
                     r"bind:value", re.I)


class Markup(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": {k.lower(): (v or "")
                                      for k, v in attrs},
                "text": "", "parents": list(self.stack)}
        self.elements.append(node)
        if tag not in VOID:
            self.stack.append(len(self.elements) - 1)

    def handle_startendtag(self, tag, attrs):
        self.elements.append({"tag": tag,
                              "attrs": {k.lower(): (v or "") for k, v in attrs},
                              "text": "", "parents": list(self.stack)})

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.elements[self.stack[i]]["tag"] == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        for index in self.stack:
            self.elements[index]["text"] += data


def parse(text):
    doc = Markup()
    try:
        doc.feed(text)
    except Exception:  # noqa: BLE001 - malformed markup is still evidence
        pass
    return doc.elements


def identity(node):
    attrs = node["attrs"]
    return " ".join(attrs.get(key, "") for key in
                    ("id", "name", "class", "aria-label", "placeholder",
                     "data-field"))


def find_error_text(elements, field, scripts):
    """Text that could be the field's error message, best candidates first.

    Only error containers count, not every element the field describes
    itself by: a helpful hint above the field is not an error message,
    and reading one as the other would pass a screen whose rejection
    says "Invalid input".
    """
    ids = []
    for key in ("aria-errormessage", "aria-describedby"):
        ids += field["attrs"].get(key, "").split()
    texts = []
    for node in elements:
        node_id = node["attrs"].get("id", "")
        blob = node_id + " " + node["attrs"].get("class", "") + " " + \
            node["attrs"].get("role", "")
        if not re.search(r"error|invalid|alert", blob, re.I):
            continue
        if ids and node_id and node_id not in ids and \
                not re.search(r"summary|alert", blob, re.I):
            continue
        texts.append((node_id or blob.strip(),
                      " ".join(node["text"].split())))
    return texts + list(scripts)


def script_messages(scratch):
    """Message strings the scripts raise about the dose field.

    A string counts only where the handful of lines immediately above
    it, or the message itself, names the dose *and* says this is a
    rejection. The window is tight on purpose: a screen whose dose
    error is "Invalid input" should not pass on the strength of a
    well-written message belonging to the field below it, or of a line
    of working printed after a successful sum. Test files are skipped,
    because an assertion quoting a message is not the message.
    """
    out = []
    anchor = re.compile(r"\bdose\b", re.I)
    rejection = re.compile(r"error|invalid|reject|problem|not valid|"
                           r"fault|warn", re.I)
    for path in walk(scratch, SCRIPT_SUFFIXES | {".html", ".htm"}):
        if any(part.lower() in ("tests", "test", "spec", "__tests__")
               for part in path.parts):
            continue
        text = read(path)
        for m in re.finditer(r"[`'\"]([^`'\"\n]{18,200})[`'\"]", text):
            blob = m.group(1)
            window = text[max(0, m.start() - 140):m.start()] + blob
            if " " in blob and INSTRUCTION.search(blob) \
                    and anchor.search(window) and rejection.search(window):
                out.append((rel(scratch, path), blob))
    return out


def clears_the_field(scratch):
    reset = re.compile(r"(\w[\w.\[\]]{0,30})\.reset\(\)|"
                       r"([\w.\[\]]{1,40})\.value\s*=\s*(''|\"\"|``|null)")
    for path in walk(scratch, SCRIPT_SUFFIXES | {".html", ".htm"}):
        text = read(path)
        for m in reset.finditer(text):
            target = (m.group(1) or m.group(2) or "").lower()
            if re.search(r"form|dose|field|input|amount", target):
                return rel(scratch, path), m.group(0)
    return None


def main():
    scratch = scratch_dir()
    pages = walk(scratch, {".html", ".htm"})
    if not pages:
        emit(CID, FAIL,
             "no page in the delivered tree, so there is no dosage entry "
             "field to inspect")

    field = page_path = elements = None
    for path in pages:
        found = parse(read(path))
        for node in found:
            if node["tag"] in FIELD_TAGS and DOSE.search(identity(node)):
                field, page_path, elements = node, path, found
                break
        if field:
            break
    if field is None:
        emit(CID, FAIL,
             "no dosage entry field: no input, select or textarea in %d "
             "page(s) is identified as a dose" % len(pages))

    where = rel(scratch, page_path)
    field_id = field["attrs"].get("id", "")
    labelled = None
    for index, node in enumerate(elements):
        if node["tag"] != "label":
            continue
        text = " ".join(node["text"].split())
        if not text:
            continue
        if field_id and node["attrs"].get("for", "") == field_id:
            labelled = "label for=%r" % field_id
            break
        if index in field["parents"]:
            labelled = "a label wrapped around the field"
            break
    if labelled is None:
        if field["attrs"].get("aria-label"):
            emit(CID, FAIL,
                 "%s: the dosage field carries only an aria-label, which is "
                 "not a visible explicit label" % where)
        emit(CID, FAIL,
             "%s: the dosage field (id=%r) has no explicit label"
             % (where, field_id or "unset"))

    messages = find_error_text(elements, field, script_messages(scratch))
    actionable = [(node_id, text) for node_id, text in messages
                  if text and INSTRUCTION.search(text)
                  and len(text.split()) >= 4]
    if not actionable:
        seen = [t for _, t in messages if t][:3]
        emit(CID, FAIL,
             "%s: no error message beside the dosage field says what to do "
             "next; found %s"
             % (where, ("%r" % seen) if seen else "no error text at all"))

    cleared = clears_the_field(scratch)
    if cleared:
        emit(CID, FAIL,
             "%s clears the entry on submit (%s), so a rejected dose has to "
             "be retyped" % (cleared[0], cleared[1]))

    survives = None
    if BINDING.search(field["attrs"].get("value", "")) or \
            any(key in field["attrs"] for key in
                (":value", "v-model", "bind:value", "@value")):
        survives = "the field's value is bound back from state"
    if survives is None:
        for path in walk(scratch, SCRIPT_SUFFIXES | {".html", ".htm"}):
            if "preventdefault" in read(path).lower():
                survives = ("%s prevents the default submit and never clears "
                            "the field" % rel(scratch, path))
                break
    if survives is None:
        for path in walk(scratch, SCRIPT_SUFFIXES | {".py"}):
            text = read(path).lower()
            if "dos" in text and "value" in text and \
                    re.search(r"invalid|error|reject|fail", text):
                survives = "%s tests the value after a rejected submit" \
                    % rel(scratch, path)
                break
    if survives is None:
        emit(CID, FAIL,
             "%s: nothing shows the entered dose surviving a failed submit: "
             "no value binding, no prevented default, no test" % where)

    emit(CID, PASS,
         "%s: the dosage field has %s, its error message says what to do "
         "next (%r), and %s"
         % (where, labelled, actionable[0][1][:90], survives))


if __name__ == "__main__":
    main()
