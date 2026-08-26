"""Slack app auditor: installs, scopes, and credential age as a weekly review.

Slack app sprawl is an access problem wearing a convenience costume: apps
accumulate, scopes are granted once and never re-read, credentials never
rotate, and the person who installed something leaves. This auditor turns
that into four concrete lists: credentials past rotation age, apps installed
by people who have left (orphaned ownership), apps holding broad read scopes
(history/email class), and apps that look abandoned.

Scope review for NEW installs belongs with the security team; this report is
the operations side that keeps the reviewed state true over time. Rotation
itself is done WITH the app's developer or owner, never as a surprise;
the report's job is making the conversation happen on a calendar.

Mock mode reads fixtures/slack_apps.json. Real mode: the same inventory comes
from the Slack admin APIs (admin.apps.approved.list and friends on Enterprise
Grid) plus the org's leaver feed.

Usage: python automations/slack_app_audit.py --as-of 2026-08-26
"""

import argparse
import json
import os
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS = os.path.join(REPO, "fixtures", "slack_apps.json")
ROTATION_DAYS = 180
STALE_DAYS = 120
BROAD_SCOPES = {"channels:history", "groups:history", "im:history", "users:read.email", "files:read"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", required=True, help="YYYY-MM-DD")
    args = ap.parse_args()
    as_of = date.fromisoformat(args.as_of)

    with open(APPS, encoding="utf-8") as f:
        data = json.load(f)
    leavers = set(data["leavers"])

    rotate, orphaned, broad, stale = [], [], [], []
    for app in data["apps"]:
        cred_age = (as_of - date.fromisoformat(app["credential_created"])).days
        if cred_age > ROTATION_DAYS:
            rotate.append("{n} (credential {d} days old)".format(n=app["name"], d=cred_age))
        if app["installed_by"] in leavers:
            orphaned.append("{n} (installed by {p}, who has left)".format(n=app["name"], p=app["installed_by"]))
        wide = sorted(set(app["scopes"]) & BROAD_SCOPES)
        if wide:
            broad.append("{n}: {s}".format(n=app["name"], s=", ".join(wide)))
        last_used = (as_of - date.fromisoformat(app["last_used"])).days
        if last_used > STALE_DAYS:
            stale.append("{n} (unused {d} days)".format(n=app["name"], d=last_used))

    print("SLACK APP AUDIT · as of {d} · {n} apps".format(d=as_of, n=len(data["apps"])))
    for label, items in (
        ("Credentials past {d}-day rotation (rotate WITH the owner, on a schedule)".format(d=ROTATION_DAYS), rotate),
        ("Orphaned ownership (installer has left; reassign before it breaks)", orphaned),
        ("Broad read scopes (re-justify with security or narrow them)", broad),
        ("Possibly abandoned (unused {d}+ days; uninstall candidates)".format(d=STALE_DAYS), stale),
    ):
        print("\n{l}: {n}".format(l=label, n=len(items)))
        for item in items:
            print("  - " + item)
    return {"rotate": rotate, "orphaned": orphaned, "broad": broad, "stale": stale}


if __name__ == "__main__":
    main()
    sys.exit(0)
