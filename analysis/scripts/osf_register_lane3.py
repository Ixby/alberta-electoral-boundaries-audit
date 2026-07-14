# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Register the Lane 3 process scorecard on the OSF.

Files preregistration/lane3_process_scorecard_draft.md as an OSF
Open-Ended Registration (schema 5df83f7dd28338001ac0ab0d, v3), embedding the
document verbatim in the registration summary together with its git commit
hash and SHA-256 so the OSF copy is the frozen record. Registration on the
OSF is PERMANENT once approved — withdrawn registrations leave a public
tombstone. Do not run --submit casually.

Auth: personal access token (scope: osf.full_write) from either the
OSF_TOKEN environment variable or a line `OSF_TOKEN=...` in
private_workspace/key.env (gitignored). The token is never printed.

Usage:
    python analysis/scripts/osf_register_lane3.py            # create+populate DRAFT only, print its URL
    python analysis/scripts/osf_register_lane3.py --submit   # ...and submit it for registration (permanent)

Backward:
  preregistration/lane3_process_scorecard_draft.md — the document being registered
  private_workspace/key.env — OSF_TOKEN (gitignored)
Forward:
  (OSF registration record; the draft doc's status banner is updated manually
   with the resulting OSF ID after a successful --submit run)
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
DOC = ROOT / "preregistration" / "lane3_process_scorecard_draft.md"
KEY_ENV = ROOT / "private_workspace" / "key.env"

API = "https://api.osf.io/v2"
SCHEMA_ID = "5df83f7dd28338001ac0ab0d"  # Open-Ended Registration v3 (verified 2026-07-14)
TITLE = ("Alberta Electoral Boundary Audit — Lane 3 Process Scorecard "
         "(prospective evaluation of the 2026 Lunty committee process)")


def token() -> str:
    t = os.environ.get("OSF_TOKEN", "").strip()
    if not t and KEY_ENV.exists():
        for line in KEY_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("OSF_TOKEN="):
                t = line.split("=", 1)[1].strip()
    if not t:
        sys.exit("No OSF token found. Set OSF_TOKEN in the environment or add a "
                 "line 'OSF_TOKEN=...' to private_workspace/key.env "
                 "(mint one at https://osf.io/settings/tokens with scope osf.full_write).")
    return t


def call(method: str, url: str, payload: dict | None, tok: str) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/vnd.api+json",
    })
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        sys.exit(f"OSF API {method} {url} -> HTTP {e.code}\n{body}")


def main() -> None:
    submit = "--submit" in sys.argv
    tok = token()

    text = DOC.read_text(encoding="utf-8")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                            capture_output=True, text=True).stdout.strip()

    summary = (
        "This registration freezes the criteria, predicted directions, and "
        "pass/fail conditions for Lane 3 of the Alberta Electoral Boundary "
        "Audit: a nine-feature scorecard of the redistricting PROCESS, to be "
        "applied prospectively to the Alberta Select Special Committee on "
        "Electoral Boundaries (the Lunty committee) on the day its report is "
        "released (due 2026-11-02).\n\n"
        f"Repository: https://github.com/Ixby/alberta-electoral-boundaries-audit\n"
        f"Document: preregistration/lane3_process_scorecard_draft.md\n"
        f"Git commit at registration: {commit}\n"
        f"SHA-256 of the document: {sha}\n\n"
        "The document follows verbatim.\n\n"
        "----------------------------------------------------------------\n\n"
        + text
    )

    # 1. Create a (project-less) draft registration on the Open-Ended schema
    draft = call("POST", f"{API}/draft_registrations/", {
        "data": {
            "type": "draft_registrations",
            "relationships": {
                "registration_schema": {
                    "data": {"type": "registration-schemas", "id": SCHEMA_ID}
                }
            },
        }
    }, tok)
    draft_id = draft["data"]["id"]
    print(f"draft created: {draft_id}")

    # 2. Populate title + summary
    call("PATCH", f"{API}/draft_registrations/{draft_id}/", {
        "data": {
            "id": draft_id,
            "type": "draft_registrations",
            "attributes": {
                "title": TITLE,
                "description": ("Lane 3 (process) criteria for the November 2026 "
                                "committee evaluation — frozen before the committee reports."),
                "category": "methods and measures",
                "registration_responses": {"summary": summary},
                "tags": ["redistricting", "Alberta", "electoral boundaries",
                         "process scorecard", "pre-registration"],
            },
        }
    }, tok)
    print("draft populated (title, summary, tags)")
    print(f"review it at: https://osf.io/registries/drafts/{draft_id}/")

    if not submit:
        print("\nDRAFT ONLY — nothing has been registered. "
              "Re-run with --submit to file it (permanent).")
        return

    # 3. Submit the draft for registration, public immediately.
    #    The API has used two attribute spellings across versions; try both.
    payload = {
        "data": {
            "type": "registrations",
            "attributes": {"draft_registration": draft_id},
        }
    }
    try:
        reg = call("POST", f"{API}/registrations/", payload, tok)
    except SystemExit:
        print("first submit shape rejected; retrying with draft_registration_id …")
        payload["data"]["attributes"] = {"draft_registration_id": draft_id}
        reg = call("POST", f"{API}/registrations/", payload, tok)

    reg_id = reg["data"]["id"]
    print(f"\nSUBMITTED. Registration id: {reg_id}")
    print(f"URL: https://osf.io/{reg_id}/")
    print("OSF holds new registrations in a short admin-approval window; "
          "approve it from the email OSF sends, or it auto-finalizes.")
    print("\nNext manual step: update the status banner in "
          "preregistration/lane3_process_scorecard_draft.md with this OSF id.")


if __name__ == "__main__":
    main()
