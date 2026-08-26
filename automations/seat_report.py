"""Seat utilization report: the automation behind the monthly utilization review.

Reads per-app seat exports and produces the three numbers that drive license
operations: what we pay for, what is actually used, and what to reclaim.
Reclaim candidates are conservative on purpose: a seat is only flagged when the
user is suspended, is a known leaver, or has not signed in for RECLAIM_DAYS.
The output is a decision sheet for humans, not an auto-revoker; reclamation is
a conversation with the seat's manager before it is a deprovisioning action.

Mock mode (default): reads fixtures/seats/*.json so the whole report runs with
zero API keys, including in CI. Real mode: point each loader at the vendor's
seat/usage API (most expose last-login per user); the report logic does not
change, which is the point of keeping ingestion behind one function.

Usage: python automations/seat_report.py --as-of 2026-08-26 [--csv out.csv]
"""

import argparse
import csv
import json
import os
import sys
from datetime import date, timedelta

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEATS_DIR = os.path.join(REPO, "fixtures", "seats")
RECLAIM_DAYS = 45


def load_apps(seats_dir=SEATS_DIR):
    apps = []
    for name in sorted(os.listdir(seats_dir)):
        if name.endswith(".json"):
            with open(os.path.join(seats_dir, name), encoding="utf-8") as f:
                apps.append(json.load(f))
    return apps


def analyze(app, as_of):
    cutoff = as_of - timedelta(days=RECLAIM_DAYS)
    seats, reclaim = [], []
    for seat in app["seats"]:
        last = date.fromisoformat(seat["last_login"])
        reason = None
        if seat["status"] != "active":
            reason = "status: " + seat["status"]
        elif last < cutoff:
            reason = "no sign-in for {d} days".format(d=(as_of - last).days)
        seats.append(seat)
        if reason:
            reclaim.append({"email": seat["email"], "reason": reason})
    monthly = app["unit_cost_monthly"]
    return {
        "app": app["app"],
        "seats_total": len(seats),
        "seats_reclaimable": len(reclaim),
        "monthly_cost": round(len(seats) * monthly, 2),
        "monthly_reclaimable": round(len(reclaim) * monthly, 2),
        "annual_reclaimable": round(len(reclaim) * monthly * 12, 2),
        "reclaim": reclaim,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", required=True, help="Report date, YYYY-MM-DD (explicit for reproducible runs)")
    ap.add_argument("--csv", help="Optional path for a reclaim-candidates CSV")
    args = ap.parse_args()
    as_of = date.fromisoformat(args.as_of)

    rows = [analyze(app, as_of) for app in load_apps()]
    total_annual = round(sum(r["annual_reclaimable"] for r in rows), 2)

    print("SEAT UTILIZATION REVIEW · as of {d} · reclaim threshold {t} days".format(d=as_of, t=RECLAIM_DAYS))
    print("{:<10} {:>6} {:>10} {:>12} {:>14}".format("app", "seats", "reclaim", "monthly $", "annual reclaim $"))
    for r in rows:
        print("{:<10} {:>6} {:>10} {:>12} {:>14}".format(
            r["app"], r["seats_total"], r["seats_reclaimable"], r["monthly_cost"], r["annual_reclaimable"]))
    print("\nReclaim candidates (each one is a manager conversation, not an auto-revoke):")
    for r in rows:
        for c in r["reclaim"]:
            print("  {a:<10} {e:<28} {why}".format(a=r["app"], e=c["email"], why=c["reason"]))
    print("\nTotal annualized reclaim opportunity: ${v}".format(v=total_annual))

    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["app", "email", "reason"])
            for r in rows:
                for c in r["reclaim"]:
                    w.writerow([r["app"], c["email"], c["reason"]])
    return rows


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
