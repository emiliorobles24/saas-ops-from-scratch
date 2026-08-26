"""Audit evidence packager: evidence pulls as a repeatable, verifiable motion.

The evidence side of a SOC 2 cycle is a logistics problem: the auditor asks
for N artifacts by control, and the answers need to be complete, traceable,
and identical every time someone re-runs the pull. This script packages an
evidence request list into a dated pack: one folder per request id, every file
copied in, and a manifest.json recording what was collected, when, from where,
and each file's SHA-256, so "is this the same file you gave us in Q2" has a
one-line answer.

Scope discipline, stated because it matters: this automates the EVIDENCE side.
Audit scope, control ownership, and policy live with Security and Compliance;
this tool makes their requests painless, it does not answer for them.

Mock mode packages fixtures/evidence_src per fixtures/evidence_requests.json.
Real mode: the request list comes from the auditor's PBC list, and sources map
to the systems that hold each artifact (exports, admin consoles, this repo's
own seat reports).

Usage: python automations/evidence_pack.py --as-of 2026-08-26 --out /tmp/pack
"""

import argparse
import hashlib
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUESTS = os.path.join(REPO, "fixtures", "evidence_requests.json")
SRC = os.path.join(REPO, "fixtures", "evidence_src")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", required=True, help="Collection date, YYYY-MM-DD")
    ap.add_argument("--out", required=True, help="Output directory for the evidence pack")
    ap.add_argument("--collector", default="saas-ops", help="Who ran the pull (goes in the manifest)")
    args = ap.parse_args()

    with open(REQUESTS, encoding="utf-8") as f:
        spec = json.load(f)

    os.makedirs(args.out, exist_ok=True)
    manifest = {"audit": spec["audit"], "collected": args.as_of, "collector": args.collector, "requests": []}
    missing = 0
    for req in spec["requests"]:
        req_dir = os.path.join(args.out, req["id"])
        os.makedirs(req_dir, exist_ok=True)
        entry = {"id": req["id"], "description": req["description"], "source": req["source"], "files": []}
        for name in req["files"]:
            src_path = os.path.join(SRC, name)
            if not os.path.exists(src_path):
                entry["files"].append({"file": name, "status": "MISSING"})
                missing += 1
                continue
            shutil.copy2(src_path, os.path.join(req_dir, name))
            entry["files"].append({"file": name, "status": "collected", "sha256": sha256(src_path)})
        manifest["requests"].append(entry)

    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("EVIDENCE PACK · {a} · collected {d}".format(a=spec["audit"], d=args.as_of))
    for entry in manifest["requests"]:
        ok = sum(1 for x in entry["files"] if x["status"] == "collected")
        print("  [{s}] {i}: {n}/{t} artifacts  ({d})".format(
            s="ok" if ok == len(entry["files"]) else "GAP", i=entry["id"],
            n=ok, t=len(entry["files"]), d=entry["description"]))
    print("manifest.json written with SHA-256 per artifact")
    if missing:
        print("MISSING ARTIFACTS: {m}. A gap surfaced at collection time is a".format(m=missing))
        print("conversation this week; a gap surfaced by the auditor is a finding.")
    return missing == 0


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
