# Intake: how work enters the lane, and where the lane ends

The SaaS-admin lane receives work from three doors: **tickets escalated out of
the support queue**, **calendar-driven work** (renewals, audits, reviews), and
**things the automations surface** (reclaim candidates, hygiene findings,
rotation due). Everything gets a ticket; the queue is the system of record.

## The taxonomy (write it down on day one, refine forever)

| Class | Examples | Handled by |
|---|---|---|
| Admin action | role grant, settings change the app supports, admin-level troubleshooting | This lane, same day |
| Access request | seat request, group membership | This lane, against policy; sponsor/manager approval where required |
| Platform change | SSO/SCIM config, new integration, new-app intake | **Routed to IT Engineering** with context attached |
| Vendor motion | renewal, true-up, CSM escalation | This lane prepares; Procurement/Finance decide |
| Audit request | evidence pull, access-review support | This lane executes; Security/Compliance own scope |

## The boundary rule

The most important judgment in the lane: **know when a request crosses from
operating a system into changing it.** Operating = actions the app's admin
model already supports. Changing = anything touching identity plumbing,
integrations, or platform configuration. Route changes to the owning team
with everything they need (what was asked, what you checked, why it's
platform-level), so the handoff lands warm.

## Governance at creation time

Anything that can sprawl gets an intake form at creation, not a cleanup
project later. The pattern I ran in production for Google Groups: a required
form capturing **purpose, temporary-or-permanent (with expiry), and the
manager**. Those answers feed a register (see `fixtures/group_register.json`)
that the hygiene automation checks reality against forever after. The same
pattern extends to new SaaS app requests and Slack app installs.

## Every third repeat becomes automation

If the queue hands you the same request a third time, it stops being a ticket
and becomes a script, an app-native workflow, or an AI-assisted tool, chosen
in that order: deterministic first, agents only where a wrong answer is cheap.
The `automations/` folder is this rule, applied.

## Everything ships a runbook

A resolved escalation that lives in one person's head leaves when they do.
Every new request class gets a runbook entry the first time it's solved.
