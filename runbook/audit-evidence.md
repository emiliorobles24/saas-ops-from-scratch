# Audit evidence: the calendar's other half

Evidence requests arrive on the audit calendar (SOC 2 cycles, access
reviews, customer security questionnaires). The motion, honed across
multiple annual cycles on the evidence side:

1. **The request list is data.** Each control request gets an id, a source,
   and a file list (`fixtures/evidence_requests.json` models the auditor's
   PBC list).
2. **Collection is a script, not a scramble.** `evidence_pack.py` packages
   every artifact into a dated pack with a manifest: what, when, from where,
   SHA-256 per file. Re-runs are identical; "is this the same file from Q2"
   has a one-line answer.
3. **Gaps surface at collection time.** A missing artifact found by the
   packager is a conversation this week; found by the auditor, it's a
   finding.
4. **Access reviews are supported, not owned.** The lane produces the rosters
   and reports that reviewers attest against (admin rosters per app, seat
   lists, leaver deprovisioning logs); scope and policy stay with Security
   and Compliance.

Scope discipline, repeated on purpose: evidence side, not control ownership.
The person who runs this lane should be able to say exactly that sentence.
