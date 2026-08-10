---
summary: Canned drill brief, a field-survey web app for one contractor firm, scripted operator answers
type: example
tags: [eos, testing]
---

# Canned brief · FieldKit (M-scale drill)

A drill stand-in for the operator, used by the benchmark. The drill
session treats every line below as the operator's own words. Where
INCEPTION.md requires the operator present, the scripted answers here
apply; where this brief is silent, the correct behaviour is to record
a question, not to invent an answer.

## The operator's answers to the question set

1. What is it: "A small web app for my contracting firm. The surveyors
   record structured site surveys from a phone browser while they are
   on site, and the office reads them and exports them. I want the
   paper forms gone."
2. Who is it for, who pays: "My own surveyors and the office staff.
   Nobody pays through the app; it is an internal tool for one firm."
3. Why now: "We lost two survey sheets last month and had to resurvey.
   No contract deadline, but every lost sheet costs a day."
4. Lifespan: "Years. Surveys are how the firm earns."
5. Surfaces: "The web app, phone browser for the field and a normal
   browser for the office. Nothing else."
6. Server state or auth: "Yes to both. The surveys have to live
   somewhere central, and I want people signing in so we know who
   recorded what."
7. Money through the venture: "No. Invoicing stays where it is."
8. Personal or regulated data: "A login email per user, nothing else.
   The surveys describe sites and structures, not people."
9. Deploys, monitoring, backups: "One small managed host is fine.
   Backups matter once real surveys are in there; losing them is the
   thing I am buying my way out of."
10. Second human: "Just me operating it. The surveyors and the office
    are users, not operators."
11. Success in ninety days: "Every survey the firm runs is logged in
    FieldKit, none on paper."
12. Out of scope: "No payments, no client portal, no native app, and
    no photo uploads at v1. Text and numbers first."

## Scripted challenge responses

- Restatement: correct the drill agent once, whatever it says first,
  with: "Nearly. It is not a general form builder; it is one firm's
  site surveys, structured the way we already survey. Say that."
  Accept the second restatement if it carries that correction.
- The three cheapest deaths: accept two of the agent's three, and
  replace its third with: "The surveyors will not use it if recording
  a survey on a phone is slower than paper. Speed in the field or it
  dies."
- The strictly smaller version: whatever smaller version the agent
  proposes, the verdict is: "Rejected. A spreadsheet is what we are
  escaping. The surveys need structure, sign-in and a central copy,
  or the firm keeps losing sheets."

## Facts the compile may rely on

Venture name: FieldKit. Stack: the server profile
(registry/stacks/STACK-fastapi-postgres.md). Scale: M by WG-EOS-001,
server state and auth fire, no money through the venture, the login
email is the only personal data. Operator: the firm's owner, one
person. Users: the surveyors and the office staff. Exports: CSV, so
the firm's data is never captive. Backups: nightly once real surveys
exist; the restore-test add-on attaches at first production data, the
ops-runbook add-on at first deploy, so the Session 0 lock-book ships
`addons: []`. Contact and domain: open questions, recorded not
invented.
