# Field Guide: how the best-run companies do SaaS operations

The research-backed companion to [FIRST-YEAR-PLAN.md](FIRST-YEAR-PLAN.md). The plan
says what I would do; this document says what the evidence says works, drawn from
a multi-source research sweep across public company handbooks and engineering
blogs (GitLab, Netflix, Google, Salesforce, Spotify, Figma, Block, Shopify),
customer case studies, analyst research, auditor-side guidance, and the annual
industry indexes (Okta, BetterCloud, Zylo, Productiv, Flexera, Torii, Gartner).

Two honesty rules throughout: statistics from vendors who sell the fix are marked
**[vendor]**, and where the sources flatly disagree, the disagreement is kept and
stated rather than averaged away (section 5).

---

## 1 · The practices, by maturity stage

### Foundation (the plan's Q1)

- **A SaaS system of record with named accountability per app**: business owner,
  technical owner, at least two provisioners/deprovisioners, data classification,
  auth method, criticality tier. GitLab requires exactly these fields for every
  app in its registry. Nothing downstream works without this table: Adobe's
  discovery found 2,600 apps against an estimated 1,800, a 44% blind spot at a
  software company, and orgs underestimate their true app count by roughly 2x
  **[vendor: Zylo]**.
- **Layered discovery, because every method has a blind spot**: SSO logs miss
  non-federated apps, expense mining misses free tools, network scans miss remote
  work. Mature programs layer several signals continuously; email-based discovery
  alone surfaced 32,000+ apps other methods missed **[vendor: Nudge Security]**.
- **HRIS → IdP → SCIM as the joiner-mover-leaver spine.** The single dominant
  pattern everywhere: Xero eliminated 95% of manual HR-to-IT lifecycle tasks and
  automated 90% of day-one apps via Workday-to-Okta; Sendbird reaches a
  30-minute onboarding (BambooHR + Okta + Jamf DEP); GitLab polls Workday for
  terminations every 15 minutes. The counterfactual: 58% of companies fail to
  equip new hires by day one **[vendor: BetterCloud]**.
- **Role-based baseline entitlements, auto-granted; everything else is a request.**
  GitLab auto-generates the day-two access request from the Workday job title;
  baseline needs no approvals, extras do. Removes approval load from the routine 80%.
- **Offboarding SLAs you can meet, then instrument**: GitLab cuts critical systems
  (IdP, Slack, password manager) within 24 hours, everything within 5 days, with
  named deprovisioners attesting per system. SOC 2 auditors sample terminations
  against YOUR stated SLA, so the SLA you write is the SLA you get audited
  against. 33% of orgs have had ex-employees retain access past 24 hours, and 18%
  trace a breach to one **[vendor: BetterCloud / Beyond Identity]**.
- **Seat reclamation as the first ROI project.** The one finding every index
  agrees on: somewhere between a quarter and half of purchased seats sit idle
  (Gartner ~25%; Zylo 36-53% across years; Flexera 50%+) **[all vendor except
  Gartner]**. Adobe reclaimed 20,000+ licenses for $60M in savings and avoidance.
  Reclamation funds the function's credibility for everything else.

### Rhythm (the plan's Q2)

- **Renewals surface at T-120, keyed to the NOTICE deadline, not the renewal
  date.** At enterprise scale renewals arrive roughly one per business day
  (211-247/year **[vendor: Zylo]**). Negotiations opened ~6 months out saved up
  to 39% versus 14% when opened 30 days out **[vendor: Vendr]**. Tier vendors:
  strategic vendors get 180-day prep and quarterly reviews; transactional stays light.
- **Continuous, policy-driven reclamation instead of cleanup sprints**:
  role-tiered idle thresholds (e.g., 60-day flag, 90-day reclaim), grace periods,
  downgrade-before-revoke, and auto-restore if the user returns. Always
  reclaim-before-buy.
- **A standard clause sheet before you need it**: true-down rights (absent from
  60-75% of reviewed order forms **[vendor]**), uplift caps (11-16% list-price
  inflation is the current norm, and AI products are re-pricing at 20-37% uplifts
  **[vendor: Vertice/Tropic]**), auto-renewal converted to opt-in, pre-negotiated
  overage rates.
- **Renewals as a cross-functional triad**: IT brings inventory and usage truth,
  procurement owns terms, finance owns budget. 69% of orgs buy jointly; only 17%
  leave it to IT alone **[vendor: BetterCloud]**. Business units control 70-81%
  of SaaS spend **[vendor: Zylo]**, which is why showback beats mandates.

### Governance (the plan's Q3)

- **Risk-tiered access-review cadence, published with named owners**: privileged
  monthly, SOX/sensitive quarterly, standard semi-annual (GitLab's model, with
  7-day manager validation and escalation at day 10). The stakes: user access
  review failures are now the number-one driver of qualified SOC 2 opinions, and
  identity-lifecycle items are ~44% of all exceptions (CBIZ 2024 benchmark of 193
  reports, a CPA firm, not a vendor).
- **Engineer against rubber-stamping**: enrich every review item with last-used
  date and peer comparison; move toward exception-only reviews. A healthy
  campaign revokes 10-20%; below 5% signals rubber-stamping, above 30% signals
  broken provisioning upstream.
- **Evidence as a byproduct, never archaeology**: system-generated listings with
  timestamps and completeness proofs (row counts, hashes), produced by the normal
  motion of the work. GitLab's evidence spec requires exactly this;
  auditor-side guidance is blunt: undocumented means it never happened.
- **Verify deprovisioning, don't trust it.** SCIM fails silently on rate limits
  and API errors; run post-offboarding verification loops that query each app's
  API to confirm the account actually died. Industry telemetry still finds ~2.5%
  of active seats assigned to offboarded users **[vendor: Torii]**, and 30-40% of
  enterprise apps sit outside the IdP entirely **[vendor: Stitchflow]**.
- **A single intake gate for new software, faster than expensing**: one request
  fanned out to security/legal/finance/procurement lanes in parallel with
  published SLAs. Snowflake's version gave pre-approval visibility over $3.7B in
  spend; Coinbase cut intake resolution from ~45 days to ~22. The gate only holds
  if it is genuinely easier than a corporate card.
- **Absorb shadow IT and shadow AI rather than only blocking**: employee-chosen
  tools show HIGHER engagement than IT-procured ones **[vendor: Productiv]**, and
  72% of GenAI use runs through personal accounts **[vendor: Reco]**. The winning
  move is migration into SSO-enforced enterprise tenants plus an approved
  catalog, Netflix's context-over-control culture and Adobe's internal app store
  being the two articulations.
- **Buy compliance automation, but design the program yourself**: 40-60% of SOC 2
  controls remain human process no platform runs **[vendor-adjacent: GRC
  consultancy]**. Named control owners before the platform arrives, not after.

### Scale (the plan's Q4 and beyond)

- **Self-service everything self-serviceable**: ChargePoint absorbed 80%+ of
  500-600 monthly access tickets into a self-service front door; GitLab runs an
  app-store front door as primary; Google's Grab-and-Go laptop racks recovered
  ~10% of technician time; Netflix vends peripherals with zero approvals.
- **AI deflection with strict definitions**: define deflection as fully resolved,
  no human touch, no reopen within 72 hours. Spotify's internal assistant (AiKA)
  cut internal support tickets by ~50% at maturity; but vendor deflection claims
  run ~10 points hotter than strict like-for-like measurement, and the honest
  year-one expectation is 20-35%.
- **An agentic operations layer, humans reviewing dispositions**: Figma's
  orchestrator-plus-subagents stack resolved complex alerts 70% faster with 20%
  fewer on-call pages; Anthropic's internal CLUE platform cut alert false
  positives from ~33% to 7% and removed ~1,870 hours of manual work in a month;
  OpenAI's internal data agent was built by two engineers in three months and
  serves 4,000+ employees daily. The pattern: small team, scoped tool access,
  human sign-off on anything destructive.
- **Insource the thin glue**: Shopify replaced an enterprise iPaaS with a
  homegrown integration layer run by two developers (18 integrations in year
  one). AI-written code has moved build-vs-buy decisively toward build for
  connective tissue.

---

## 2 · Named companies, one line each

| Company | The takeaway |
|---|---|
| **GitLab** | The most complete public reference implementation: registry, role-based baselines, 15-minute termination polling, 24h/5d offboarding SLAs, tiered access reviews, evidence spec. All public in their handbook |
| **Adobe** | The rationalization benchmark: 2,600 apps discovered vs 1,800 estimated, 7 sales platforms to 1, 20,000+ licenses reclaimed, $60M saved, internal app store ended card-swipe SaaS |
| **Xero** | JML automation benchmark: Workday→Okta, 95% of manual lifecycle work eliminated, 90% of day-one apps automated |
| **Snowflake** | Single intake gate over $3.7B of spend; one go-live email; $305M saved |
| **Coinbase** | Intake resolution ~45 days → ~22, deployed in 90 days |
| **ChargePoint** | Self-service absorbed 80%+ of access tickets; 100+ apps connected across five compliance frameworks in under 3 months |
| **Spotify** | AiKA internal AI assistant: ~50% internal ticket reduction, used by 87% of developers |
| **Figma** | The mid-size agentic-ops template: orchestrator + scoped sub-agents over Okta/EDR/SIEM, 70% faster complex-alert resolution |
| **Block** | The enterprise MCP governance template: curated in-house-only server catalog to 12,000 employees in ~2 months, read-only vs destructive tool annotation, OAuth in system keychains |
| **Anthropic** | CLUE: Claude as first-pass triage with human-reviewed dispositions, false positives 33%→7%; internal research shows Claude in ~59% of work while engineers still fully delegate only a minority of tasks: **active supervision is the operating model even at the frontier** |
| **Netflix / Google / Salesforce** | The service-culture end: zero-approval vending, Grab-and-Go, "Customer Zero" IT running on its own agent platform |
| **Klarna (caution)** | The famous "replaced Salesforce/Workday with AI" story was really vendor consolidation plus internal glue, and the CEO said the coverage embarrassed him. Loud rip-and-replace claims deserve autopsy before imitation |

---

## 3 · The numbers worth carrying in your head

- Idle seats: **~25% (Gartner) to ~50% (vendor indexes)** of purchased licenses. The honest citation is the range with the denominator stated.
- Average large-org SaaS waste: **~$20M/year**; ~$1,700 wasted per employee per year **[vendor: Zylo/Flexera]**.
- Renewals: **roughly one per business day** at enterprise scale; **6-months-early negotiation saves up to 39% vs 14% at 30 days** **[vendor: Vendr]**.
- SaaS list-price inflation ~**11-16%/yr**, with **AI products re-pricing at 20-37% uplifts** **[vendor: Vertice/Tropic]**.
- SOC 2: **qualified-opinion rate 10.9% and rising; access-review failures are the #1 driver; ~44% of all exceptions are identity-lifecycle** (CBIZ CPA-firm benchmark, neutral).
- Offboarding: manual runs **~7 hours per leaver across 15+ systems**; only ~25% of orgs automate it; **2.5% of active seats belong to already-offboarded users** **[vendor]**.
- Machine identities outnumber humans **~45:1**; **82% of orgs run AI agents, 44% have policies for them** **[vendor: SailPoint/Sysdig]**.
- Healthy access-review revocation rate: **10-20% per campaign** (below 5% = rubber-stamping; above 30% = broken provisioning upstream).
- AI helpdesk deflection, strictly defined: **20-35% year one, 40-60% best-in-class**; discount vendor claims ~10 points.

---

## 4 · What I would build moving forward

**Year one** is [FIRST-YEAR-PLAN.md](FIRST-YEAR-PLAN.md), and the research
validated its skeleton nearly item for item (registry first, JML SLAs,
reclamation as first ROI, notice-deadline-keyed renewal calendar, tiered reviews,
evidence-as-byproduct, self-service front door). Three places the evidence
UPGRADED the plan, adopted and noted transparently:

1. **Renewal surfacing moved from T-90 to T-120**, because the negotiation-timing data (39% vs 14%) says the extra month is where the money is.
2. **A deprovisioning verification loop** added to the governance quarter: SCIM's silent failures mean "the IdP says removed" and "the app says removed" are different facts, and auditors sample the second one.
3. **Deflection metrics hardened to the strict definition** (no human touch, no reopen in 72h) before any AI support layer reports a number.

**Year two:**
- The consolidated intake gate (Snowflake/Coinbase pattern), wired so approval CREATES the registry record.
- Continuous policy-driven license optimization: portfolio-wide idle thresholds, downgrade tiers, AI-consumption caps per department, reclaim-before-buy as standing policy.
- The SMP buy-vs-build decision, run properly: triggers, criteria, and a weighted shortlist (section 4b), with the homegrown reports as the bake-off acceptance test.
- An AI tier-zero support layer over internal knowledge, instrumented honestly from day one.
- Exception-driven access reviews (enriched context, auto-certify the role-aligned and recently-used, humans on anomalies only).
- Showback of SaaS + AI spend to business units: the only durable lever on the 70-81% of spend IT does not control.

**Emerging (the frontier this seat should claim early):**
- **A non-human-identity and AI-agent registry**: every service account, API key, OAuth grant, and agent gets a named human owner, scoped permissions, and an expiry: the same JML discipline humans get. Whoever governs human JML should claim agent JML before it fragments across departments.
- **MCP governance**: a curated allowlist of approved servers with security-review intake, a gateway as the single enforcement point, and read-only vs destructive tool annotation. Block proved the model at 12,000 employees; the incident record says this arrives as a postmortem if not built proactively.
- **Agentic assistants for the lane's own grind**: first-pass ticket triage, license reconciliation, renewal-prep briefs, evidence collection, always with human sign-off, in line with how Anthropic and Figma actually run theirs: supervised, scoped, measured.
- **Shadow-AI absorption**: expense-line and OAuth mining for AI tools, migration of personal-account usage into enterprise tenants, an approved catalog, and spend caps. An account-governance and FinOps problem, not a blocking problem.

---

## 4b · Buy vs build: the license and vendor management platform question

The automations in this repo are the BUILD side: seat reports, renewal radar,
evidence packs, running keyless against fixtures, and their real-mode versions
cover a small-to-mid estate for the cost of maintenance. The honest trigger
list for when to BUY a SaaS management platform (SMP) instead:

- Renewals arriving faster than a calendar-and-radar motion can hold (the
  enterprise average is roughly one per business day).
- Discovery needs exceed what SSO logs + expense mining reveal (the 30-40% of
  apps living outside the IdP).
- Finance wants chargeback/showback at a fidelity homegrown reporting can't sustain.
- Audit evidence is still manual at scale (the strongest trigger of the four:
  manual evidence collection is where audit risk and staff burnout actually live).

**The shortlist, weighted for a fast-growing, audit-serious, IT-lean company
(criteria: discovery depth, license/renewal workflows incl. budgets, automation,
fit with an existing stack):**

| Rank | Platform | Why it makes the top 3 | The honest caveat |
|---|---|---|---|
| 1 | **Zylo** | The enterprise benchmark SMP: deepest spend and utilization data in the industry, a real renewal calendar with workflows, and the license-management motion (discovery → utilization → reclaim → renewal prep) as a first-class product. Best when finance-grade spend truth is the driver | Enterprise pricing; its published waste statistics are also its marketing |
| 2 | **Torii** | Automation-first: broadest discovery layering, offboarding and license workflows a lean IT team can run without a dedicated admin. Best when the team is small and the estate is sprawling | Its "apps discovered" numbers flatter its own method; workflow depth beats reporting depth |
| 3 | **1Password (Trelica)** | The situational pick: SMP capability from the Trelica acquisition, now a Gartner MQ leader, and if 1Password already runs in the estate, one vendor covers credentials AND SaaS management, one less procurement cycle, one less integration to govern | Younger as an SMP than Zylo/Torii; evaluate the SaaS-ops depth, not the brand familiarity |

Worth a look but off the podium: **Tropic/Vendr** if the pain is the BUYING
motion (negotiation, approvals, budget workflows) more than discovery;
**BetterCloud** if the need is SaaS operations automation more than spend;
**Vertice** as negotiation-as-a-service on top of whatever manages the estate.

**The stance this repo takes:** run the build layer first, for a quarter or two.
It costs nearly nothing, it forces the team to learn where the data actually
lives, and it produces the usage truth that makes any later SMP purchase
negotiable from evidence instead of from a vendor's demo. Then buy when the
triggers above are real, and bring the homegrown reports to the bake-off as
the acceptance test: any platform worth paying for should beat them on day one.

---

## 5 · Where the sources disagree (kept on purpose)

- **App counts differ by 8x** (Okta 101 vs Torii 831): each vendor's number flatters its own discovery method. State your denominator.
- **License-waste figures conflate "unused," "underutilized," and "oversized."** Quote the range, define the term.
- **Vendor time-savings claims vs adoption reality**: platforms claim 78-88% reductions, yet only ~25-37% of orgs automate lifecycle work after a decade of these tools. The constraint is program design and ownership, which no platform ships. That gap is precisely what this seat exists to close.
- **Autonomy marketing vs frontier practice**: one lab markets 75% autonomous support resolution while Anthropic's own internal study shows engineers fully delegating only a minority of their work under active supervision. Plan for the supervised model; treat full autonomy claims as the vendor-optimistic tail.
- **Point-in-time vs continuous access reviews**: IGA vendors say quarterly campaigns produce rubber-stamped evidence; auditors still test the cadence you declared. Run the declared cadence while building toward exception-driven, and change the declaration only between audit windows.
- **Multi-year discounts inverted in 2025**: short-term contracts out-discounted 12-24-month deals (31.9% vs 26.3% **[vendor: Vendr/Tropic]**). In an AI-repricing market, uplift caps beat long commitments.

---

*Method note: compiled via a multi-agent research sweep (six parallel researchers,
one synthesis pass) over public sources, then hand-curated. Vendor-published
statistics are marked; contradictions are preserved rather than resolved by
averaging. Built the way I build everything: AI-assisted, human-judged.*
