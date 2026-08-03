---
summary: FieldKit venture brief, a field-survey web app for one contractor firm, the business truth
type: template
tags: [eos]
compiled_from: kernel/templates/VENTURE_BRIEF.tpl.md
---

# FieldKit · Venture brief

Business truth, written at Session 0 from the interview and kept
current by the venture. Every fact here is the operator's; the agent
transcribed and challenged, never invented. If this file and reality
disagree, fix this file.

## What it is

A small field-survey web app for one contracting firm. Surveyors
record structured site surveys from a phone browser while on site; the
office reads them in a normal browser and exports them as CSV. It is
an internal tool for the firm's own surveyors and office staff, built
to retire the paper survey sheets the firm keeps losing.

- One line: every site survey recorded once, centrally, by a signed-in
  surveyor, and exportable by the office.
- Who it serves: the firm's surveyors in the field and the office
  staff. Nobody pays through the app; it is internal to one firm.
- Why now: two survey sheets were lost last month and the sites had to
  be resurveyed. No contract deadline, but every lost sheet costs a
  day.

## The challenge record (anti-sycophancy, mandatory)

- Restated and corrected: the first restatement said a general form
  builder; the operator corrected it once. It is one firm's site
  surveys, structured the way the firm already surveys. The second
  restatement carried the correction and was accepted.
- The three cheapest ways this dies: the central copy is lost or never
  trusted, so paper quietly returns; the office cannot get data out,
  so exports happen by retyping; and, in the operator's words, "The
  surveyors will not use it if recording a survey on a phone is slower
  than paper. Speed in the field or it dies."
- The strictly smaller version, and the verdict on it (adopted or
  rejected, in the operator's words): a shared spreadsheet was
  proposed. "Rejected. A spreadsheet is what we are escaping. The
  surveys need structure, sign-in and a central copy, or the firm
  keeps losing sheets."

## Scale and triggers

Ruled by WG-EOS-001 into the lock-book header. Triggers present at
Session 0: server state and auth. No money through the venture; the
login email per user is the only personal data. The rescale conditions
to watch: money arriving, more personal data appearing, a second human
joining as operator, ops burden growing past one small managed host.

## Constraints

- Time: no contract deadline; every lost paper sheet costs a day.
- Money and spend rule: one small managed host; the operator sets the
  monthly spend budget in `org/QUESTIONS.md` before the first deploy.
- People and approvals: the firm's owner operates and approves
  everything; surveyors and office staff are users, not operators.
- Agreements in force (contracts, heads of terms): none.

## Success in ninety days

Every survey the firm runs is logged in FieldKit, none on paper.

## Out of scope (explicit)

No payments, no client portal, no native app, no photo uploads at v1.
Text and numbers first.
