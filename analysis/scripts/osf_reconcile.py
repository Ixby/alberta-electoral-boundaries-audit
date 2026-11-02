# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""Reconcile the OSF record with the repo, both ways. A check, not a report.

The ledger preregistration/osf_ledger.json is the repo's statement of what is
on the OSF: every registration and project, every registration update, every
archived file (SHA-256), a SHA-256 of each registration's current response
text, and where each amendment in findings/pre_registration_amendment_log.md
was filed, and any repo item a human has acknowledged (file, a substring of
the line, who, when, why). This script never writes the ledger. A human (or a session acting
for one) edits it deliberately, in the same commit as the OSF write it
records.

OSF -> repo: every registration, update, file and response text on the OSF
must match the ledger. Anything on the OSF the ledger does not hold is red.
Repo -> OSF:
  - every ledger entry must exist on the OSF as recorded;
  - every amendment heading in the log must be recorded as filed;
  - every OSF id cited in tracked source text must be in the ledger and public;
  - every "pending"/"to be filed" OSF claim in preregistration/ and the
    amendment log stays red until resolved.

Exit codes: 0 reconciled (every check consumed live OSF state); 1 drift, each
item named; 2 NOT A GATE (no token, so private projects and drafts unchecked).

Run it before and after any OSF write, and before any commit that touches
preregistration/ or the amendment log.

Auth: OSF_TOKEN from the environment or private_workspace/key.env, as in
osf_register_lane3.py. Read-only: only GET requests are made. The token is
never printed.

Usage:
  python analysis/scripts/osf_reconcile.py
  python analysis/scripts/osf_reconcile.py --observed   # print live OSF state as JSON (stdout only)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
LEDGER = ROOT / "preregistration" / "osf_ledger.json"
LOG = ROOT / "findings" / "pre_registration_amendment_log.md"
KEY_ENV = ROOT / "private_workspace" / "key.env"
API = "https://api.osf.io/v2"

# osf.io paths that are not object ids
NON_IDS = {"regis", "setti", "login", "prepr", "inves", "insti", "colle", "meeti", "suppo", "dashb", "searc"}
# built site, bundles and binaries are generated from sources that are scanned
SKIP = re.compile(r"^(docs/|viewer/static/|viewer/build/|node_modules/)|\.(js|pdf|png|jpg|jpeg|svg|gpkg|zip|csv|parquet|json|pkl|ipynb)$")
PENDING = re.compile(r"(OSF[^.\n]{0,60}(pending|to be filed|not yet filed))|((pending|to be filed)[^.\n]{0,60}OSF)|is to be filed", re.I)


def token() -> str:
    t = os.environ.get("OSF_TOKEN", "").strip()
    if not t and KEY_ENV.exists():
        for line in KEY_ENV.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("OSF_TOKEN="):
                t = line.split("=", 1)[1].strip().strip('"')
    return t


class OSF:
    def __init__(self, tok):
        self.tok = tok

    def get(self, url):
        """GET one object, or every page of a list."""
        out = []
        while url:
            req = urllib.request.Request(url)
            if self.tok:
                req.add_header("Authorization", f"Bearer {self.tok}")
            d = json.load(urllib.request.urlopen(req, timeout=60))
            if not isinstance(d.get("data"), list):
                return d["data"]
            out += d["data"]
            url = d.get("links", {}).get("next")
        return out

    def files(self, kind, nid):
        out = {}

        def walk(url, pre):
            for f in self.get(url):
                a = f["attributes"]
                if a["kind"] == "folder":
                    walk(f["relationships"]["files"]["links"]["related"]["href"], pre + a["name"] + "/")
                else:
                    out[pre + a["name"]] = (a.get("extra") or {}).get("hashes", {}).get("sha256")
        for p in self.get(f"{API}/{kind}/{nid}/files/"):
            walk(p["relationships"]["files"]["links"]["related"]["href"], p["attributes"]["name"] + ":")
        return out


def text_hash(responses):
    return hashlib.sha256(json.dumps(responses, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def observe(osf, account):
    """Live OSF state for the account, in the ledger's shape."""
    authed = bool(osf.tok)
    regs = osf.get(f"{API}/users/me/registrations/?page[size]=100" if authed
                   else f"{API}/users/{account}/registrations/?page[size]=100")
    state = {"registrations": {}, "projects": {}, "draft_registrations": []}
    for r in regs:
        a, rel = r["attributes"], r["relationships"]
        src = rel.get("registered_from", {}).get("links", {}).get("related", {}).get("href", "")
        sch = rel.get("registration_schema", {}).get("links", {}).get("related", {}).get("href", "")
        updates = []
        for s in osf.get(f"{API}/registrations/{r['id']}/schema_responses/"):
            sa = s["attributes"]
            if sa.get("is_original_response"):
                continue
            updates.append({"id": s["id"], "state": sa.get("reviews_state"),
                            "submitted_utc": sa.get("date_submitted"),
                            "justification_head": (sa.get("revision_justification") or "")[:80]})
        state["registrations"][r["id"]] = {
            "title": a["title"], "registered_utc": a["date_registered"],
            "registered_from": src.rstrip("/").rsplit("/", 1)[-1] if src else None,
            "schema": sch.rstrip("/").rsplit("/", 1)[-1] if sch else None,
            "public": a.get("public"), "withdrawn": a.get("withdrawn"),
            "pending_update": a.get("revision_state") != "approved",
            "responses_sha256": text_hash(a.get("registration_responses") or {}),
            "updates": sorted(updates, key=lambda u: u["submitted_utc"] or ""),
            "files": osf.files("registrations", r["id"]),
        }
    if authed:
        for n in osf.get(f"{API}/users/me/nodes/?page[size]=100"):
            a = n["attributes"]
            state["projects"][n["id"]] = {"title": a["title"], "created_utc": a["date_created"],
                                          "public": a.get("public"), "files": osf.files("nodes", n["id"])}
        state["draft_registrations"] = [d["id"] for d in osf.get(f"{API}/draft_registrations/?page[size]=100")]
    return state


def diff(path, want, got, red):
    """Name every difference between the ledger (want) and the OSF (got)."""
    if isinstance(want, dict) and isinstance(got, dict):
        for k in sorted(set(want) | set(got)):
            if k not in got:
                red.append(f"{path}.{k}: in the ledger, not on the OSF")
            elif k not in want:
                red.append(f"{path}.{k}: on the OSF, not in the ledger ({json.dumps(got[k])[:120]})")
            else:
                diff(f"{path}.{k}", want[k], got[k], red)
    elif want != got:
        red.append(f"{path}: ledger {json.dumps(want)[:120]} != OSF {json.dumps(got)[:120]}")


def acked(ledger, f, line, used):
    """A repo red item a human has acknowledged in the ledger (file + a substring of the line)."""
    for i, a in enumerate(ledger.get("acknowledged", [])):
        if a["file"] == f and a["contains"] in line:
            used.add(i)
            return True
    return False


def repo_checks(ledger, red):
    used = set()
    known = {**ledger["registrations"], **ledger["projects"]}
    public = {k for k, v in known.items() if v.get("public")}
    files = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    bare = re.compile(r"\b(" + "|".join(map(re.escape, known)) + r")\b")
    url = re.compile(r"osf\.io/(?:project/)?([a-z0-9]{5})\b")
    cites = 0
    for f in files:
        if not f or SKIP.search(f):
            continue
        p = ROOT / f
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if acked(ledger, f, line, used):
                continue
            for m in url.finditer(line):
                cites += 1
                if m.group(1) not in known and m.group(1) not in NON_IDS:
                    red.append(f"{f}:{i}: cites osf.io/{m.group(1)}, which is not in the ledger")
            for m in bare.finditer(line):
                cites += 1
                if m.group(1) not in public:
                    red.append(f"{f}:{i}: cites {m.group(1)}, which is private on the OSF (readers cannot open it)")
            if (f.startswith("preregistration/") or f == LOG.relative_to(ROOT).as_posix()) and PENDING.search(line):
                red.append(f"{f}:{i}: OSF claim still pending: {line.strip()[:140]}")
    for i, a in enumerate(ledger.get("acknowledged", [])):
        if i not in used:
            red.append(f"acknowledgement no longer matches anything: {a['file']} '{a['contains']}' (remove it from the ledger)")
        else:
            print(f"ACKNOWLEDGED  {a['file']}: '{a['contains']}' ({a['by']}, {a['date']}: {a['reason']})")
    # every amendment heading must be recorded as filed
    heads = [int(n) for n in re.findall(r"^## Amendment (\d+)\b", LOG.read_text(encoding="utf-8"), re.M)]
    amd = ledger.get("amendments", {})
    for n in heads:
        rec = amd.get(str(n))
        if not rec or rec.get("status") != "filed":
            red.append(f"Amendment {n}: in the log, not filed on the OSF ({(rec or {}).get('note', 'no ledger entry')})")
        elif rec.get("registration") not in ledger["registrations"]:
            red.append(f"Amendment {n}: ledger says filed in {rec.get('registration')}, which is not a ledger registration")
    for n in amd:
        if int(n) not in heads:
            red.append(f"Amendment {n}: in the ledger, no '## Amendment {n}' heading in the log")
    return cites, len(heads)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--observed", action="store_true", help="print live OSF state as JSON and exit")
    a = ap.parse_args()
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    osf = OSF(token())
    got = observe(osf, ledger["account"])
    if a.observed:
        print(json.dumps(got, indent=1, ensure_ascii=False))
        return 0
    red = []
    diff("registrations", ledger["registrations"], got["registrations"], red)
    if osf.tok:
        diff("projects", ledger["projects"], got["projects"], red)
        for d in got["draft_registrations"]:
            red.append(f"draft registration {d} exists on the OSF (file it or delete it, then record that)")
    cites, n_amd = repo_checks(ledger, red)
    n_upd = sum(len(r["updates"]) for r in got["registrations"].values())
    n_files = sum(len(r["files"]) for r in got["registrations"].values())
    for r in red:
        print("RED  " + r)
    print(f"checked: {len(got['registrations'])} registrations, {n_upd} updates, {n_files} archived files, "
          f"{len(got['projects'])} projects, {cites} OSF citations in the repo, {n_amd} amendment headings")
    if red:
        print(f"NOT RECONCILED: {len(red)} item(s) above")
        return 1
    if not osf.tok:
        print("NOT A GATE: no OSF token, so private projects and draft registrations were not checked")
        return 2
    print("RECONCILED: the ledger, the repo and the OSF agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
