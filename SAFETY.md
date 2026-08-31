# The Safety Model

How this lane makes changes without breaking things, and how automation earns
trust before it earns autonomy. IT operations is a high-blast-radius job: the
systems here touch every employee's access, every device, and the company's
audit posture. A safety model is not overhead for this work; it IS the work.

---

## The four rules every change follows

1. **Know the blast radius before you touch anything.** Every change names, out
   loud, who and what it can affect if it goes wrong: one user, one department,
   or everyone. The bigger the radius, the slower and more witnessed the change.
2. **Reversible-first.** Prefer the change you can undo. Speed on reversible
   things, deliberation on irreversible ones: a rollout can be walked back, a
   deleted account's data or a leaked credential cannot. Anything irreversible
   gets a second person and a written rollback-or-recovery note BEFORE it ships.
3. **Least privilege, for humans AND automations.** Every credential is scoped
   to the minimum it needs (read-only unless writing is the job), owned by a
   named person, and expiring. The [okta-as-code CLI](https://github.com/emiliorobles24/okta-as-code/tree/main/cli)
   demonstrates the pattern: secrets fetched at runtime from a vault, never
   stored, and the tool is incapable of writing by design.
4. **Verify, don't trust.** Deprovisioning gets checked at the app, not assumed
   from the IdP. Automations get their outputs sampled. Metrics use strict
   definitions (a deflection = resolved, no human touch, no reopen in 72 hours).
   "The system says it worked" is a hypothesis, not evidence.

---

## Autonomy Levels: how an automation earns trust

Borrowed from staged-safety thinking: an automation's permission to act scales
with the evidence it has earned, never with enthusiasm. Every automation in this
repo and in the [first-year plan](FIRST-YEAR-PLAN.md) sits at a declared level,
and promotion requires proof.

| Level | What it may do | What promotion requires |
|---|---|---|
| **AL0 · Observe** | Read-only: reports, dashboards, radar alerts. (Every automation in this repo is AL0.) | Nothing: this is where everything starts |
| **AL1 · Suggest** | Propose actions for a human to execute: "these 14 seats are reclaim candidates" | AL0 history showing its findings are accurate (sampled against reality) |
| **AL2 · Execute reversible, gated** | Perform undoable actions with a dry-run default, an explicit `--apply` flag, per-run logging, and a human approval | A tested rollback path, an audit log, and an error budget: unexplained failures demote it back to AL1 |
| **AL3 · Execute on schedule** | Run approved reversible actions unattended (e.g., flag-then-reclaim license policy with grace periods) | Months of clean AL2 history, monitoring that pages a human on anomaly, and a kill switch anyone on the team can pull |

**No automation ever reaches "irreversible, unattended."** Deactivating people,
deleting data, and revoking access at scale keep a human decision in the loop
permanently. That is a design position, not a maturity gap.

---

## Where AI is allowed in the lane, and where it is not

The ordering from the [README principles](README.md#the-principles-the-lane-runs-on),
made explicit as a safety boundary:

**AI is welcome where ambiguity is the problem and a wrong answer is cheap and
visible:** drafting runbooks, summarizing tickets, triage suggestions, writing
report narratives, first-pass evidence gathering. Human judgment reviews the
output; the human owns the result.

**AI never decides access.** Provisioning, deprovisioning, permission grants,
and anything touching money or user data run deterministically: same input,
same output, auditable line by line. An access decision you cannot replay is
an access decision you cannot defend to an auditor, or to the person affected.

**AI agents are identities, with the same lifecycle as humans.** Any agent or
automation gets a named owner, scoped credentials, an expiry, and an entry in
the non-human-identity register (first-year plan, Q3). Agent tools that can
act destructively are annotated and gated behind confirmation, never auto-fired.

**Retrieved content is data, not instructions.** Any AI reading tickets,
documents, or emails treats their contents as material to analyze, never as
commands to follow: the prompt-injection rule. A helpbot that takes orders
from the documents it reads is an incident waiting for a scheduler.

**Metrics stay honest.** AI-assisted work reports strict-definition outcomes.
Publishing a number the data cannot defend is a safety failure of a quieter
kind: it breaks the trust every other control depends on.

---

## Change safety, the working checklist

Before any change to a shared system, five questions, answerable in one line each:

1. Blast radius: who does this touch if it goes wrong?
2. Reversal: what is the undo, and has it been tried?
3. Witness: who else knows this is happening? (Scaled to radius: FYI for small, approval for large.)
4. Evidence: what will show it worked, and what will page us if it did not?
5. Timing: is this the right moment? (Never large-radius changes at 4:59pm Friday.)

Every incident feeds back: the fix kills the failure CLASS, not the instance,
and the checklist grows only when an incident proves it needs to. A checklist
that grows any other way becomes wallpaper.

---

*Why this document exists: I ran the small version of this discipline in
production for years (the credential-expiry alerting in these repos exists
because an undocumented token once expired on me in production), and the
companies doing the best work on AI safety have convinced me the same idea
scales: capability should never outrun the evidence that it is safe. That
belief is cheap to say and expensive to practice; this file is the practice.*
