# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""File a registration update on the OSF: append text to one response field.

An OSF registration update (a "schema response" revision) cannot add files;
it can only change response text. This appends a block of text to one field,
keeping the field's existing text unchanged, with a required justification.

Steps, each run separately so that the person who owns the registration
approves every write:
  --plan     (default) print what would be written; no OSF writes
  --draft    create the in-progress update and fill it; re-read it from the
             OSF and check the field equals the intended text, in the
             OSF's storage form (it saves & < > as HTML entities). Not public;
             deletable with --delete. Prints the update id.
  --submit ID   submit that update. All admins are emailed; it is approved
             by an admin or automatically after 48 hours. Once approved it
             is PERMANENT and PUBLIC.
  --approve ID  approve a submitted update as an admin.
  --delete ID   delete an update that is still in progress (irreversible).

After an approved update, record it in preregistration/osf_ledger.json in the
same commit, then run analysis/scripts/osf_reconcile.py.

Auth: OSF_TOKEN (scope osf.full_write) from the environment or
private_workspace/key.env. The token is never printed.

Usage
  python analysis/scripts/osf_file_update.py --registration 9wp5y --field 344-86 \
      --text-file BLOCK.md --justification-file WHY.txt [--plan|--draft]
  python analysis/scripts/osf_file_update.py --submit ID | --approve ID | --delete ID
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
KEY_ENV = ROOT / "private_workspace" / "key.env"
API = "https://api.osf.io/v2"
SEP = "\n\n---\n\n"


def token() -> str:
    t = os.environ.get("OSF_TOKEN", "").strip()
    if not t and KEY_ENV.exists():
        for line in KEY_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("OSF_TOKEN="):
                t = line.split("=", 1)[1].strip().strip('"')
    if not t:
        sys.exit("No OSF token (OSF_TOKEN or private_workspace/key.env).")
    return t


def call(method, path, body=None):
    req = urllib.request.Request(path if path.startswith("http") else API + path, method=method,
                                 data=None if body is None else json.dumps(body).encode())
    req.add_header("Authorization", f"Bearer {token()}")
    req.add_header("Content-Type", "application/vnd.api+json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read()
            return json.loads(raw)["data"] if raw else None
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {path}: HTTP {e.code}: {e.read().decode(errors='replace')[:800]}")


def intended(reg, field, block):
    cur = call("GET", f"/registrations/{reg}/")["attributes"]
    if cur.get("revision_state") != "approved":
        sys.exit(f"{reg} has an update in progress or pending ({cur.get('revision_state')}); resolve it first")
    old = (cur.get("registration_responses") or {}).get(field)
    if not isinstance(old, str):
        sys.exit(f"{reg} field {field} is not a text field")
    if block.strip() in old:
        sys.exit(f"{reg} field {field} already contains this text")
    return old, old.rstrip() + SEP + block.strip() + "\n"


def sha(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registration")
    ap.add_argument("--field")
    ap.add_argument("--text-file")
    ap.add_argument("--justification-file")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--plan", action="store_true")
    g.add_argument("--draft", action="store_true")
    g.add_argument("--submit", metavar="ID")
    g.add_argument("--approve", metavar="ID")
    g.add_argument("--delete", metavar="ID")
    a = ap.parse_args()

    for flag, trigger in (("submit", "submit"), ("approve", "approve")):
        sid = getattr(a, flag)
        if sid:
            call("POST", f"/schema_responses/{sid}/actions/",
                 {"data": {"type": "schema-response-actions", "attributes": {"trigger": trigger},
                           "relationships": {"target": {"data": {"type": "schema-responses", "id": sid}}}}})
            s = call("GET", f"/schema_responses/{sid}/")["attributes"]
            print(f"{sid}: {trigger} sent; state now {s.get('reviews_state')}, submitted {s.get('date_submitted')}")
            return
    if a.delete:
        call("DELETE", f"/schema_responses/{a.delete}/")
        print(f"{a.delete}: deleted")
        return

    block = Path(a.text_file).read_text(encoding="utf-8")
    why = Path(a.justification_file).read_text(encoding="utf-8").strip()
    old, new = intended(a.registration, a.field, block)
    print(f"registration {a.registration}, field {a.field}")
    print(f"  existing text: {len(old):,} chars, sha256 {sha(old)}")
    print(f"  appended block: {len(block.strip()):,} chars, sha256 {sha(block.strip())}")
    print(f"  field after: {len(new):,} chars, sha256 {sha(new)}")
    print(f"  justification ({len(why)} chars): {why[:300]}")
    if not a.draft:
        print("PLAN ONLY: nothing written to the OSF")
        return
    sr = call("POST", "/schema_responses/",
              {"data": {"type": "schema-responses",
                        "relationships": {"registration": {"data": {"type": "registrations", "id": a.registration}}}}})
    sid = sr["id"]
    call("PATCH", f"/schema_responses/{sid}/",
         {"data": {"type": "schema-responses", "id": sid,
                   "attributes": {"revision_justification": why, "revision_responses": {a.field: new}}}})
    back = call("GET", f"/schema_responses/{sid}/")["attributes"]
    got = (back.get("revision_responses") or {}).get(a.field)
    # the OSF stores response text HTML-escaped (& < > as entities), registered text included
    ok = got == html.escape(html.unescape(new), quote=False) and (back.get("revision_justification") or "").strip() == why
    print(f"DRAFT {sid}: state {back.get('reviews_state')}; field read back {'MATCHES' if ok else 'DIFFERS'} "
          f"({len(got or ''):,} chars, sha256 {sha(got or '')})")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
