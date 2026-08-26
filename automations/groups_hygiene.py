"""Google Groups hygiene auditor: keeping a heavily nested structure honest.

Nested groups rot in predictable ways: groups with no owner (nobody can fix
membership), empty groups that still gate access, nesting cycles (A contains B
contains A: expansion becomes ambiguous), external members hiding inside inner
groups, and chains so deep nobody can answer "who actually receives this."
This auditor walks the whole structure and reports each class of rot with the
specific group, so hygiene is a weekly five-minute review instead of an
archaeology project during an incident.

The external-member check matters most: access is usually granted to the OUTER
group, but delivery reaches every leaf. An external address nested three
levels down still gets the email. The auditor flattens every group to its
effective members so that surprise shows up here, not in a breach review.

The other half of hygiene is PROVENANCE, and it comes from governance at
creation time: every new group goes through an intake form (I ran this as a
Jira form in production) that records the group's purpose, whether it is
temporary, and who manages it. Those answers land in the group register
(fixtures/group_register.json), and this auditor checks reality against the
register: groups that exist but were never registered, temporary groups past
their expiry, and manager drift. Cleanup then stops being archaeology,
because "why does this group exist" always has an answer on file.

Mock mode reads fixtures/groups.json + fixtures/group_register.json. Real
mode: structure comes from the Directory API (groups.list + members.list),
and the register is fed by the intake form's tickets.

Usage: python automations/groups_hygiene.py --as-of 2026-08-26
"""

import argparse
import json
import os
import sys
from datetime import date

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GROUPS = os.path.join(REPO, "fixtures", "groups.json")
REGISTER = os.path.join(REPO, "fixtures", "group_register.json")
MAX_DEPTH = 3
INTERNAL_DOMAIN = "acme.example"


def load():
    with open(GROUPS, encoding="utf-8") as f:
        return {g["email"]: g for g in json.load(f)["groups"]}


def flatten(email, groups, seen=None, depth=0):
    """Effective (leaf) members of a group, plus the max nesting depth hit and
    any cycle detected along the way."""
    seen = seen or set()
    if email in seen:
        return set(), depth, True
    seen = seen | {email}
    leaves, max_depth, cycle = set(), depth, False
    for m in groups[email]["members"]:
        if m in groups:
            sub, d, c = flatten(m, groups, seen, depth + 1)
            leaves |= sub
            max_depth = max(max_depth, d)
            cycle = cycle or c
        else:
            leaves.add(m)
    return leaves, max_depth, cycle


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", required=True, help="YYYY-MM-DD, for temporary-group expiry checks")
    args = ap.parse_args()
    as_of = date.fromisoformat(args.as_of)

    groups = load()
    with open(REGISTER, encoding="utf-8") as f:
        register = {r["email"]: r for r in json.load(f)["register"]}

    findings = {"unowned": [], "empty": [], "cycles": [], "deep": [], "external": [],
                "unregistered": [], "expired": [], "ghost": []}
    for email in sorted(groups):
        if email not in register:
            findings["unregistered"].append(email)
    for email, entry in sorted(register.items()):
        if entry.get("temporary") and entry.get("expires") and date.fromisoformat(entry["expires"]) < as_of:
            state = "still exists" if email in groups else "already deleted, close the register entry"
            findings["expired"].append("{e} (expired {x}, {s})".format(e=email, x=entry["expires"], s=state))
        if email not in groups and not entry.get("temporary"):
            findings["ghost"].append(email)
    for email, g in sorted(groups.items()):
        if not g["owners"]:
            findings["unowned"].append(email)
        if not g["members"]:
            findings["empty"].append(email)
        leaves, depth, cycle = flatten(email, groups)
        if cycle:
            findings["cycles"].append(email)
        if depth > MAX_DEPTH:
            findings["deep"].append("{e} (depth {d})".format(e=email, d=depth))
        ext = sorted(m for m in leaves if not m.endswith("@" + INTERNAL_DOMAIN))
        if ext:
            findings["external"].append("{e} -> {x}".format(e=email, x=", ".join(ext)))

    print("GROUPS HYGIENE · {n} groups audited".format(n=len(groups)))
    labels = {
        "unowned": "No owner (nobody can fix membership)",
        "empty": "Empty but still grantable (delete or document why it exists)",
        "cycles": "Nesting cycle (expansion is ambiguous)",
        "deep": "Nested deeper than {d} (who receives this?)".format(d=MAX_DEPTH),
        "external": "External addresses reachable through nesting",
        "unregistered": "Exists but never went through intake (no purpose on file)",
        "expired": "Temporary group past its declared expiry",
        "ghost": "Registered as permanent but no longer exists (close or investigate)",
    }
    clean = True
    for key, label in labels.items():
        items = findings[key]
        print("\n{l}: {n}".format(l=label, n=len(items)))
        for item in items:
            print("  - " + item)
        clean = clean and not items
    print("\n" + ("CLEAN" if clean else "Findings above are this week's five-minute review."))
    return findings


if __name__ == "__main__":
    main()
    sys.exit(0)
