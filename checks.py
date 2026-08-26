"""CI gate: every automation must run clean on the fixture estate.

Same rule as my other repos: if it does not run in CI with zero keys, it is a
diagram, not an automation. Each check runs the real script the way an
operator would, on a pinned --as-of date so results are reproducible, and
asserts the findings the fixture estate is designed to contain. A fixture
edit that silently changes what the tools detect fails the build.
"""

import io
import subprocess
import sys
import tempfile
import os

AS_OF = "2026-08-26"
PY = sys.executable
HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, *extra):
    cmd = [PY, os.path.join(HERE, "automations", script), *extra]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.join(HERE, "automations"))
    if out.returncode != 0:
        print(out.stdout)
        print(out.stderr)
        raise SystemExit("FAIL: {s} exited {c}".format(s=script, c=out.returncode))
    return out.stdout


def main():
    failures = []

    seat = run("seat_report.py", "--as-of", AS_OF)
    for expect in ("SEAT UTILIZATION REVIEW", "casey@acme.example", "Total annualized reclaim opportunity"):
        if expect not in seat:
            failures.append("seat_report missing: " + expect)

    radar = run("renewal_radar.py", "--as-of", AS_OF)
    for expect in ("RENEWAL RADAR", "Notion", "TRUE-UP PREP"):
        if expect not in radar:
            failures.append("renewal_radar missing: " + expect)

    with tempfile.TemporaryDirectory() as tmp:
        pack = run("evidence_pack.py", "--as-of", AS_OF, "--out", tmp)
        if "manifest.json written" not in pack:
            failures.append("evidence_pack: no manifest")
        if "GAP" in pack:
            failures.append("evidence_pack: fixture pack should be complete")
        if not os.path.exists(os.path.join(tmp, "manifest.json")):
            failures.append("evidence_pack: manifest file absent")

    groups = run("groups_hygiene.py", "--as-of", AS_OF)
    for expect in ("frontend@acme.example", "legacy-2019@acme.example", "partners-external@vendor.example", "launch-q3@acme.example"):
        if expect not in groups:
            failures.append("groups_hygiene should flag: " + expect)

    slack = run("slack_app_audit.py", "--as-of", AS_OF)
    for expect in ("LegacyStandupBot", "DataExporter", "riley@acme.example"):
        if expect not in slack:
            failures.append("slack_app_audit should flag: " + expect)

    if failures:
        for f in failures:
            print("FAIL:", f)
        return 1
    print("PASS: all five automations ran clean on the fixture estate ({d})".format(d=AS_OF))
    return 0


if __name__ == "__main__":
    sys.exit(main())
