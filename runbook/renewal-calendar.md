# The renewal calendar: never surprised, never unprepared

Renewals are calendar work living alongside a live queue, and both fail if
either is left to memory. The calendar is data (`fixtures/renewals.json`
stands in for the contract-system export), and `automations/renewal_radar.py`
turns it into a weekly radar.

## The cadence

- **T-90**: renewal enters the radar. Pull the seat-utilization report for the
  app. Open the renewal ticket; it holds every artifact from here on.
- **T-60**: true-up prep sheet done (contracted vs provisioned vs actually
  used, with the dollar delta). Reclaim obviously dead seats NOW, before the
  negotiation, not after. Ping the vendor CSM for the renewal quote.
- **T-30**: package for Procurement/Finance: quote, utilization facts, delta,
  recommendation (right-size down / hold / expand). Their decision, made easy.
- **Notice deadlines are tracked separately** from renewal dates; an
  auto-renew clause with a missed notice window is a year-long decision made
  by silence. The radar flags notice-due 30 days ahead of the notice date.

## Roles, stated plainly

This lane owns the calendar, the utilization evidence, the true-up math, and
the vendor CSM relationship day to day. Contract negotiation and spend
approval stay with Procurement and Finance. The lane's job is that nobody
walks into a renewal conversation without the usage facts.

## The monthly utilization review

Once a month, `seat_report.py` runs across the whole estate, not just apps in
renewal windows. Reclaim candidates each become a manager conversation, and
the confirmed releases become reclaimed licenses. Ran this motion in
production: a license audit run this way funded itself many times over.
