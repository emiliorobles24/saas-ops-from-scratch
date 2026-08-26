"""Renewal radar: the renewal calendar as code.

Renewals fail in two boring ways: the notice deadline passes unnoticed (auto-
renew locks you in), or the renewal call happens without utilization data
(you re-buy shelfware). This script kills both: it reads the contract
calendar, computes which renewals are inside the T-90/T-60/T-30 windows AND
which notice deadlines are approaching, then joins the seat data to produce a
true-up prep sheet: contracted seats vs provisioned seats vs actively used
seats, per app, with the dollar delta.

Negotiation and spend approval belong to Procurement and Finance; this
report's job is making sure they walk into that conversation with the
utilization facts, prepared before the window, not after.

Mock mode reads fixtures/renewals.json + fixtures/seats/. Real mode: the
renewals file is the source of truth you maintain from contracts (a contract
system export or a reviewed YAML/JSON in this repo's spirit), and seats come
from the same loaders as seat_report.py.

Usage: python automations/renewal_radar.py --as-of 2026-08-26
"""

import argparse
import json
import os
import sys
from datetime import date, timedelta

from seat_report import load_apps, analyze

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENEWALS = os.path.join(REPO, "fixtures", "renewals.json")
WINDOWS = (90, 60, 30)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()
    as_of = date.fromisoformat(args.as_of)

    with open(RENEWALS, encoding="utf-8") as f:
        renewals = json.load(f)["renewals"]
    usage = {r["app"]: r for r in (analyze(a, as_of) for a in load_apps())}

    print("RENEWAL RADAR · as of {d}".format(d=as_of))
    upcoming = []
    for r in sorted(renewals, key=lambda x: x["renewal_date"]):
        renew = date.fromisoformat(r["renewal_date"])
        days_out = (renew - as_of).days
        notice_by = renew - timedelta(days=r["notice_days"])
        window = next((w for w in reversed(WINDOWS) if days_out <= w), None)
        flag = "T-{w}".format(w=window) if window else ""
        notice_flag = "NOTICE DUE {d}".format(d=notice_by) if as_of >= notice_by - timedelta(days=30) and days_out > 0 else ""
        overdue = "PAST" if days_out < 0 else ""
        print("  {a:<10} renews {rd}  ({dd:>4}d)  {f:<5} {n} {o}".format(
            a=r["app"], rd=renew, dd=days_out, f=flag, n=notice_flag, o=overdue))
        if window and days_out >= 0:
            upcoming.append((r, days_out))

    print("\nTRUE-UP PREP (inside the 90-day window):")
    print("{:<10} {:>11} {:>12} {:>8} {:>14}".format("app", "contracted", "provisioned", "in use", "annual delta $"))
    for r, days_out in upcoming:
        u = usage.get(r["app"])
        provisioned = u["seats_total"] if u else "?"
        in_use = (u["seats_total"] - u["seats_reclaimable"]) if u else "?"
        delta = ""
        if u:
            delta = round((r["seats_contracted"] - in_use) * r["unit_cost_monthly"] * 12, 2)
        print("{:<10} {:>11} {:>12} {:>8} {:>14}".format(r["app"], r["seats_contracted"], provisioned, in_use, delta))
    print("\nReading the delta: positive = paying for seats nobody uses (negotiate down or")
    print("reclaim before the call); negative = using more than contracted (budget the")
    print("true-up now instead of discovering it in the invoice).")
    return True


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
