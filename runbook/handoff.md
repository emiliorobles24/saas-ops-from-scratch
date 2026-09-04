# The Follow-the-Sun Handoff

How a globally distributed operations team passes work between timezones without
dropping anything. A handoff is the single most failure-prone moment in
distributed operations: whatever is ambiguous at the boundary becomes an incident
by morning. This runbook makes the handoff a PROTOCOL, not a vibe.

## The principle

**The receiving shift should never have to reconstruct context.** If the person
picking up a ticket, an incident, or a renewal task has to re-derive what
happened, the handoff failed, even if the note technically existed. Every
handoff is written for a reader who knows nothing and is mildly tired.

## The handoff note, one per shift boundary

Posted in the team channel at a fixed time, same format every day. Five
sections, empty sections stated as empty (silence is ambiguous; "none" is data):

```
HANDOFF: <region> → <region> · <date> · <author>

1. OPEN ESCALATIONS (anything a user is waiting on)
   - [ticket] one-line status · next action · owner-if-not-you · promised-by time

2. IN-FLIGHT CHANGES (anything half-done that touches shared systems)
   - what's changed so far · what remains · how to roll back if it breaks overnight

3. WATCHING (not broken, could break)
   - the thing · the signal that means act · what acting looks like

4. CALENDAR ITEMS LANDING IN YOUR SHIFT (renewals, evidence deadlines, vendor windows)

5. NONE-OF-THE-ABOVE: anything a tired reader should know anyway
```

## Severity carryover rules

- **Sev-high (user-blocking, exec-visible, or security-touching):** never handed
  off by note alone. Live handoff: a synchronous 5 minutes or a recorded voice
  note, plus the written entry. The sender stays reachable for 30 minutes after
  boundary.
- **In-flight irreversible work** (deletions, deprovisioning, data migration
  steps): not handed off at all. Either finish it in-shift or park it at a safe,
  documented checkpoint. An irreversible step should never straddle a timezone.
- **Everything else:** the note carries it. If the note can't carry it in five
  lines, it wasn't understood well enough to hand off; write the sixth line.

## The coverage matrix

A standing document (not per-shift) that answers "who has this hour": each
region's hours in UTC, the overlap windows (where live handoffs happen), the
on-call path when no region is awake, and per-system ownership when regional
depth differs (e.g., only one region has an Okta admin: the matrix says what
the others may safely do and what waits).

| | AMER | EMEA | APAC | Nobody awake |
|---|---|---|---|---|
| Hours (UTC) | 13:00-22:00 | 08:00-17:00 | 00:00-09:00 | 22:00-00:00 |
| Live handoff window | ← 16:00-17:00 → | ← 08:00-09:00 → | ← n/a → | on-call only |
| Full admin coverage | yes | partial (see matrix) | partial | break-glass doc |

(The hours above are the fixture example; the real matrix is the first thing a
new region's onboarding updates.)

## What makes this work in practice

1. **Fixed time, fixed format, no exceptions.** The value of a handoff note is
   90% predictability. A brilliant note at a random time is worse than an
   adequate note at the same time every day.
2. **The note is written DURING the shift, not at the end.** Keep it open as a
   scratchpad from hour one; the last 10 minutes are for editing, not recall.
3. **Receipt is explicit.** The receiving shift emoji-acks the note and asks
   questions in-thread within their first 30 minutes. An unacknowledged handoff
   escalates to a ping; a pattern of them escalates to the team lead.
4. **Handoff quality is reviewed like any other work product.** When an
   overnight incident traces to a handoff gap, the retro fixes the NOTE FORMAT
   (a new required line), not the person: kill the failure class.
5. **Every handoff feeds the runbook.** Anything explained twice across
   boundaries becomes a runbook entry, so the next handoff can link instead of
   explain: the third-repeat rule, applied to context itself.

## Why this is in a SaaS-operations repo

Renewals, audit evidence, and access reviews are calendar-driven work that does
not care which timezone is awake when the deadline lands. The radar automations
in [`automations/`](../automations/) surface the deadlines; this protocol is how
a distributed team makes sure a deadline surfaced in one region gets landed in
another. Calendar work plus queue work plus timezones is exactly where things
fall through, and the handoff note's section 4 is the stitch.
