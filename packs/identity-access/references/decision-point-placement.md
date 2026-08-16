---
summary: The four points a decision needs, where each can sit, the four outcomes a decision has, and what happens when the decider is unreachable
type: guide
tags: [auth, arch]
kind: fact
scope: estate
volatility: slow
review: 2029-04
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
---

# Reference: where the authorisation decision point sits

Level 3 detail behind binding requirement B1 and behind the default of
one decision point. Read this when the check is about to be written in
more than one place, or when somebody proposes a policy service.

## Four points, and the value of naming them

The access control vocabulary that has lasted splits the job four ways
(XACML 3.0):

- The **enforcement point** asks the question and obeys the answer. It
  is the middleware, the decorator, the guard clause.
- The **decision point** answers it. It holds the rules and evaluates
  them.
- The **information point** supplies facts the rules need that the
  request did not carry: the record's owner, the person's department,
  the tenant's plan.
- The **administration point** is where the rules are written and
  changed.

The value is not the specification, which is thirteen years unrevised
and whose XML nobody should write today. It is that naming all four
makes it obvious when one of them is nowhere. A system whose
administration point is "edit the source and deploy" has one, and saying
so is more useful than pretending it does not exist. A system with no
information point is a system where every rule can only depend on what
happened to be in the request.

## Four outcomes, not two

A decision resolves to permit, deny, not-applicable or indeterminate
(XACML 3.0). The last two are the ones ad-hoc checks leave undefined,
and they are where the interesting failures live.

- **Not-applicable** means no rule matched. Under B1 this is a denial. A
  system where no matching rule means permitted has a deny-by-default
  policy in name only (OWASP authorization guidance).
- **Indeterminate** means evaluation failed: the information point was
  unreachable, an attribute was missing, the policy service timed out.
  This must also be a denial, and it must be visible, because a
  deny-on-error that is silent looks exactly like a correct refusal and
  will be diagnosed as a permissions bug for as long as it lasts.

Where more than one rule can apply, something has to say what happens
when they disagree. Deny wins is the sane default. Whatever is chosen,
it is a written choice, not an accident of evaluation order.

## Where the decision point can sit

**In process, as a library or a module.** One function every request
path calls. No network hop, no availability question, no version skew.
This is the right answer for a single application and it is the default
in `packs/identity-access/PACK.md`. Its limit is reuse: a second service
cannot call it without either duplicating the rules or taking a
dependency on the first service.

**At the gateway or edge.** Coarse decisions before the request reaches
the application: is this caller authenticated, does the token have the
right audience, is this route admin-only. Good for the coarse half and
structurally incapable of the fine half, because the gateway does not
know who owns record 4172. A gateway check is never the whole of B1.

**As a sidecar.** The rules run beside the service rather than inside
it. Buys one rule set across services in different languages, and keeps
the hop local. Costs a deployment unit per service and a distribution
mechanism for the rules.

**As a central service.** One decision service everything calls. Buys
one place to change a rule and one place to audit. Costs a dependency on
the request path, which is the property to think hardest about: the
best-documented system of this shape is inseparable from a globally
consistent database, a specialised set-computation index, request
hedging and per-client quotas, and its own authors report that hot
spots, where many objects indirectly depend on one heavily shared group,
are a critical availability problem (Zanzibar).

**As a central service holding the data too.** The relationship engines
go further and store the relations as well as the rules (OpenFGA). That
is the strongest version of one place to look, and it is also a second
source of truth that has to stay in step with the application's own
records for ever.

## The staleness question

Any decision point that is not in process, and any in-process one that
caches, can answer from data that is out of date. That is usually fine
and occasionally not: revoke someone's access and then add content, and
a stale check lets the removed person see the new content. The
best-documented answer makes the client do the work, storing an opaque
token with each content version and passing it back on the check so the
decision is evaluated no earlier than the content it protects
(Zanzibar). Note what that means for anyone adopting the pattern: the
guarantee is not a property of the service, it is a property of a client
that remembers to pass the token. A client that skips it loses the
property silently.

For a venture with one application and an in-process decision point,
none of this applies and the paragraph exists so that nobody buys the
machinery without buying the obligation.

## The short version

Start in process. Move outwards only when a second service needs the
same rules, or when a rule has to be changed by somebody who cannot
deploy. Whatever the shape, there is one of them, it fails closed, and
its failure is loud.
