# The First Year: an operating plan for a SaaS Operations seat

This is the day-1-to-month-12 version of the [30/60/90 in the README](README.md#the-306090-standing-the-lane-up-from-day-one),
written against a real publicly posted role: an **Application Administrator / IT Support Engineer**
seat that owns "SaaS Operations, the service-operator layer for the SaaS catalog":
app administration, license and seat operations, renewals and true-ups, the support
queue, SOC2 evidence and access reviews, Google Groups and Calendar resources,
Slack app installs and credential rotation, across a stack that names Gong,
1Password, MongoDB, and Vanta.

I ran the core of this lane in production for years at a public SaaS company. This document is
that experience laid out as a plan someone could hold me to: what gets stood up,
in what order, on what cadence, and how success gets measured. Every process named
here has a working counterpart in this repo (runbooks in [`runbook/`](runbook/),
automations in [`automations/`](automations/), all CI-gated), so the plan is not
aspiration: the machinery is already written down and running against fixtures.

---

## The shape of the year

| Quarter | Theme | The test at the end |
|---|---|---|
| Q1 (days 1-90) | **Learn the estate, stand up the foundations** | The renewal calendar is complete, the intake taxonomy is live, and nothing renews or gets audited as a surprise |
| Q2 (months 4-6) | **Make it run on rails: automation and rhythm** | Utilization review, reclamation cycle, and hygiene automations run monthly without being pushed |
| Q3 (months 7-9) | **Governance maturity: audit season, access reviews, non-human identities** | An evidence request is a same-week, reproducible motion, and every automation credential has an owner and an expiry |
| Q4 (months 10-12) | **Prove the lane survives without me** | Someone else covers the lane for a week from the runbook alone, and Finance gets a year-ahead renewal forecast |

---

## Q1, days 1-90: foundations (the README's 30/60/90, plus the detail)

The full 30/60/90 is in the [README](README.md#the-306090-standing-the-lane-up-from-day-one).
What it stands up, restated as the processes that exist by day 90:

1. **The estate inventory** (day 1-30): every app, its business owner, its admin
   credential, its contract, its renewal date, its user count. One source of truth,
   reviewed with IT Engineering and Security so the operate-vs-change boundary is
   agreed out loud, not assumed. Tiering follows: which apps are business-critical
   (break-glass documented), which are department tools, which are sprawl candidates.
2. **The intake taxonomy** ([`runbook/intake.md`](runbook/intake.md)): every queue
   escalation tagged from week one. Admin actions inside configured apps get done
   same-day in this lane; platform-level work routes to IT Engineering with context
   attached. The taxonomy is also the automation backlog: whatever repeats, ranks.
3. **The renewal calendar** ([`runbook/renewal-calendar.md`](runbook/renewal-calendar.md)):
   built from the contracts themselves in month one, then run on a T-120/T-90/T-60/T-30
   cadence keyed to NOTICE deadlines, not renewal dates (the notice deadline is the
   one that actually bites, and the negotiation-timing evidence says the earliest
   month is where the savings live: see [FIELD-GUIDE.md](FIELD-GUIDE.md)).
   [`automations/renewal_radar.py`](automations/renewal_radar.py) is the working model.
4. **The first utilization report, by hand** ([`automations/seat_report.py`](automations/seat_report.py)
   is the automated version): run manually first to learn where each platform's
   truth lives (Gong seat data, 1Password provisioning state, MongoDB org members,
   Vanta integration status), then automated once the data paths are proven.
5. **The evidence dry-run** ([`runbook/audit-evidence.md`](runbook/audit-evidence.md)):
   take the LAST audit's request list and produce the pack cold, before any auditor
   asks. Every gap found in the dry-run is fixed on my time instead of audit-season time.
6. **Vendor introductions**: a first call with every vendor CSM in the book, so the
   day-to-day contact relationship the role describes starts as a relationship, not
   a renewal-week scramble.

**Day-90 exit criteria:** calendar complete, taxonomy live and tagging real tickets,
first reclaim candidates identified, evidence dry-run finished with gaps closed,
top-ten request classes each have a runbook entry.

---

## Q2, months 4-6: automation and rhythm

7. **The monthly utilization review**: seat report runs monthly, reviewed with each
   app's business owner. Reclamation is **confirm-or-release, never surprise
   revocation**: managers see their own usage data and every seat gets a
   conversation, which is how a reclamation program spends zero trust. I ran
   license reclamation in production; it funded itself many times over.
8. **True-up preparation as a standing artifact**: before any true-up conversation,
   the utilization truth is already assembled. This lane never decides spend; it
   makes sure whoever does walks in with facts.
9. **Sprawl registers with governance at creation time**: Google Groups and Slack
   apps each get an intake form (purpose, owner, lifecycle) feeding a register that
   [`automations/groups_hygiene.py`](automations/groups_hygiene.py) and
   [`automations/slack_app_audit.py`](automations/slack_app_audit.py) check forever
   after: nesting depth, ownerless groups, external reach, orphaned app installs,
   over-broad scopes, and **credential age**, with rotation scheduled before expiry
   rather than after breakage. Google Calendar resources (rooms, shared calendars)
   join the same register: created with an owner, reviewed on the same cycle.
10. **The automation ladder, applied to the queue**: by month six, the top repetitive
    classes from the intake taxonomy are automated in order of the ladder the README
    describes: deterministic script first, app-native workflow second, AI-assisted
    only where ambiguity is the problem and a wrong answer is cheap. Every automation
    ships with its runbook entry and a least-privilege, read-only-where-possible credential.
11. **Vendor health and update coordination**: a change-calendar for vendor app
    updates, with user-facing impact communicated ahead of time in plain words.
    The measure: no user learns about a breaking vendor change from the breakage.

**Month-6 exit criteria:** reclamation has produced measurable recovered spend,
at least one full renewal has run the complete T-90/T-60/T-30 cadence, hygiene
automations run on schedule, and the KPI dashboard (below) exists.

---

## Q3, months 7-9: governance maturity

12. **The audit calendar, merged with Security**: SOC2 evidence requests mapped to
    a calendar the way renewals are. Vanta is the system of record: evidence tasks,
    monitored controls, and integration health get a weekly glance, not an
    audit-week panic. Scope and control ownership stay with Security and
    Compliance; this lane's job is making their evidence painless, manifested, and
    reproducible ([`automations/evidence_pack.py`](automations/evidence_pack.py)
    produces SHA-256-manifested packs for exactly this reason).
13. **Access-review execution as a playbook**: when access reviews run, this lane
    executes them on schedule: pull the rosters, chase the sign-offs, deliver the
    artifacts, log the removals. The playbook makes review N+1 cheaper than review N.
13b. **Deprovisioning verification loops**: SCIM fails silently, so "the IdP says
    removed" and "the app says removed" are different facts, and auditors sample
    the second one. Post-offboarding jobs query each connected app's API to confirm
    the account actually died; the long tail outside the IdP gets scheduled
    reconciliation instead.
14. **Non-human identity lifecycle**: by month nine, every service account, API
    token, and automation credential in the lane's estate has an owner, a scope, a
    creation record, and an expiry: the same joiner-mover-leaver discipline humans
    get. This includes the credentials behind AI agents and integrations, which is
    where sprawl is growing fastest in every company right now.
15. **App rationalization, proposed with facts**: the inventory plus a year of
    utilization data supports an overlap analysis (two tools doing one job) handed
    to whoever owns the spend decision. Facts first, opinions attached clearly as opinions.
16. **AI in the lane itself, with the safety ordering**: runbook drafting,
    ticket summarization, utilization narratives, and queue triage assistance are
    the right jobs for AI here (judgment stays human, wrong answers are cheap and
    visible). Provisioning, deprovisioning, and anything touching access stay
    deterministic. Using AI tools for productivity is part of the JD; using them
    with this ordering is what makes that safe. And any AI layer that reports a
    deflection number uses the strict definition: fully resolved, no human touch,
    no reopen within 72 hours: honest measurement before impressive measurement.

**Month-9 exit criteria:** one full audit cycle (or dry-run at full fidelity) has
run through the calendar without a fire drill, and the NHI register is complete.

---

## Q4, months 10-12: prove it survives

17. **The coverage test**: someone else runs the lane for a week from the runbook
    alone. Every question they have to ask a human is a runbook bug, filed and fixed.
    This is the difference between a lane and a person.
18. **The year-ahead renewal forecast**: Finance gets the next twelve months of
    renewals, notice deadlines, expected true-ups, and utilization trendlines in
    one artifact, a quarter before budget season needs it.
19. **The year-in-review**: KPIs against baseline, spend recovered, automations
    shipped, evidence turnaround trend, and the honest list of what didn't work.
20. **The year-two proposal**: informed by twelve months of taxonomy data: which
    request classes to automate next, whether a license-management platform earns
    its cost, and where self-service can replace tickets entirely.

---

## The measures that define success

| Metric | Baseline (day 30) | Year-one target |
|---|---|---|
| Renewal surprises (missed notice windows) | measured | **zero** |
| Seat utilization visibility | partial, manual | every tiered app, monthly, automated |
| Recovered spend from reclamation | none | measurable and reported quarterly |
| Evidence request turnaround | measured | same-week, reproducible, manifested |
| Runbook coverage of request classes | ~0 | top ten by day 90, expanding monthly |
| Automation credential hygiene | unknown | 100% owned, scoped, expiring |
| Lane survivability | single-person | one-week coverage test passed |

---

## How the posted JD maps to this plan (and to my record)

| The JD asks for | Where this plan answers it | The receipt behind it |
|---|---|---|
| Administer SaaS apps: roles, settings, troubleshooting at admin level | Q1 items 1-2; the operate-vs-change boundary | Years running admin-level SaaS operations at a public SaaS company; Okta Certified Administrator |
| License assignment, reclamation, utilization reporting (Gong, 1Password, MongoDB, Vanta) | Q1 item 4, Q2 items 7-8; `seat_report.py` | Built a license-utilization dashboard against vendor APIs and ran a portfolio-wide audit; the reclamation program funded itself many times over. Deployed a password manager company-wide |
| Ticket intake and execution from the support queue | Q1 item 2; `runbook/intake.md` | Led IT operations support: queue ownership, triage taxonomy, SLA program that moved compliance from 75 to 95+ |
| Identify repetitive work and automate it (scripts or app-native workflows) | Q2 item 10; the five automations in this repo | The third-repeat rule, practiced for years: production automations in identity workflows and Python |
| Monitor app health; route platform issues to IT Engineering | Q1 item 1 (boundary agreement); intake routing | The operate-vs-change discipline in `intake.md`, learned by running exactly that boundary in production |
| Renewal calendars and true-ups; vendor CSM contact | Q1 items 3, 6; Q2 items 8, 11; `renewal_radar.py` | Owned vendor relationships and renewals; renewal work grounded in utilization data |
| Pull SOC2 evidence; support access reviews | Q1 item 5, Q3 items 12-13; `evidence_pack.py` | Pulled SOC2 and SOX evidence across annual audit cycles (evidence side; scope and control ownership stayed with Security, same as this plan keeps it) |
| Google Groups and Calendar resources | Q2 item 9; `groups_hygiene.py` | Ran a Google Groups cleanup owner-by-owner in production, then made it permanent with an intake form: governance at creation time |
| Slack app installs and credential rotation | Q2 item 9; `slack_app_audit.py` | Slack Enterprise Grid administration; credential-expiry alerting built after living through an expired-token outage |
| Basic scripting (Bash or Python) | Every automation here is stdlib Python, CI-gated | This repo, plus [okta-as-code](https://github.com/emiliorobles24/okta-as-code) and [endpoints-as-code](https://github.com/emiliorobles24/endpoints-as-code) (portfolio builds, like this repo) |
| Documentation: runbooks, guides, KB articles | Items 2, 17; everything here ships a runbook | Turned resolved escalations into runbooks and KB articles as standard practice, for years |
| Calendar-driven work alongside ticket queues | Principle 4 in the README; the radar automations | Ran renewals and audit calendars beside a live queue; the radars exist so neither steals from the other |
| AI tools for productivity | Q3 item 16, with the deterministic-first safety ordering | Led an org-wide AI rollout with governance: provisioning, data boundaries, per-team enablement; build daily with Claude Code |

**Honest edges, stated plainly:** where I have not run a specific console named in
the posting (Gong admin, MongoDB Atlas org administration, Vanta), the plan
front-loads them: they are Q1 item-4 platforms, learned hands-on in the first
weeks the way I have learned every console I've administered. The lane transfers;
the menus are the easy part.

---

*Everything in this repo runs against fixtures with zero API keys, and CI gates
every push. The plan is the system; the automations are its working parts;
the runbooks are how someone else operates it; and [SAFETY.md](SAFETY.md) is
the rulebook for how any of it is allowed to act: every automation in this plan
sits at a declared Autonomy Level and earns promotion with evidence. That is
the standard I hold infrastructure to, and the standard I would bring to this seat.*
