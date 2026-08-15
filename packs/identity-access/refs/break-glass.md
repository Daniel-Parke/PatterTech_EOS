---
summary: The emergency access path, why it exists, the eight properties that make it work, and the trade it makes
type: guide
tags: [auth, security, ops]
kind: fact
scope: estate
volatility: slow
review: 2029-03
sources: [EV-0517, EV-0518, EV-0519, EV-0520, EV-0521, EV-0522, EV-0523, EV-0524, EV-0525, EV-0526, EV-0527, EV-0528, EV-0529, EV-0530, EV-0531]
---

# Reference: break-glass and the privileged path

Level 3 detail behind binding requirement B4. Read this when setting up
administrative access, and again the first time somebody asks for a
support view that reads a customer's records.

## Why the path exists

Everything that makes ordinary access safe can also lock everybody out.
The scenarios are ordinary rather than dramatic (Entra emergency access
guidance): the identity provider is unavailable and sign-in redirects
nowhere; the second factor everybody registered is a device or a network
that is also down; the one person who held the top-level role has left;
an approval workflow requires an approver and there is no approver left
who can approve. None of these is an attack. All of them end with nobody
able to administer the system.

So the choice is not whether to have an emergency path. It is whether
the one you have was designed or improvised.

## The eight properties

Taken from the vendor guidance and stripped of the product (Entra
emergency access guidance):

1. **At least two credentials.** One lost credential must not be a
   lockout.
2. **No dependency on the identity provider.** Provider outage is one of
   the reasons the path exists, so a break-glass account federated
   through the provider is decorative. This is the rule GD-IDENT-003
   points here for.
3. **Held by the organisation, not by a person.** Not somebody's
   personal administrator login, and not tied to an individual's phone.
   Where a venture is one person, that means the credential survives
   that person's device, which is a physical storage question rather
   than a technical one.
4. **A different authentication method from the everyday one.** If
   normal administration uses an application on a phone, the emergency
   path uses a hardware key. One method failing must not take out both.
   Phishing resistance means the authenticator is bound to the session,
   so a code somebody reads and retypes does not count, however many
   digits it has (NIST SP 800-63B-4).
5. **Standing privilege, not requested privilege.** The approval
   machinery may be exactly what is broken.
6. **An alert on every sign-in.** Not a log line somebody could read. An
   alert that reaches a person.
7. **A review after every use** that reaches one of three verdicts: a
   drill, a real emergency, or misuse. The review reads what the session
   actually did, not only that it happened.
8. **A test on a schedule**, at least every ninety days, that the
   credential still works, the alert still fires, and the people who
   would need it still know how. An untested emergency path is a
   credential that will fail at the only moment it matters.

## The trade it makes

These accounts are deliberately excluded from the controls that restrict
everybody else, because those controls are what might be failing (Entra
emergency access guidance). That is the trade stated plainly:
break-glass buys availability by giving up prevention, and pays for it
with detection. Properties 6, 7 and 8 are therefore not optional extras.
They are the whole of what makes the exclusion defensible.

If a venture cannot do the alerting and the review, it does not have a
break-glass path. It has an unmonitored administrator account.

## The rest of the privileged path

Break-glass is the sharpest case, not the only one. B4 covers every
route that reaches data or actions it does not own, and the two that
appear in almost every product are:

- **The administrator view**, which reads across tenants. It is a
  cross-tenant read with a friendly name, and it is the one route B2
  cannot cover, because it is supposed to cross the boundary.
- **Support impersonation**, where a member of staff acts as a customer.
  The record it leaves has to say who really acted, not only whose
  account it looked like, or the audit trail records the customer doing
  something the customer did not do.

Both get the same treatment: named in a list a person can read, a record
per use carrying who, when, what for and what was reached, and a review
that somebody actually does. The customer-facing half of this is worth
stating too, and it is a product decision rather than a technical one:
whether the customer is told when their data was read by staff.

## What this reference does not cover

Approval before a consequential external action, which is the security
and privacy pack's B6 and lives in `packs/security-privacy/PACK.md`. The
two are easy to confuse. B6 asks whether an action may be taken at all.
B4 asks whether the person taking it is on a path that should be
watched. A break-glass session doing something irreversible is subject
to both.
