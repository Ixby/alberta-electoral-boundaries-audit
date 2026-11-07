# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
run_stepc.py
------------

Runs the registered Step C scoring of a 91-district map (Amendment 7, Part 3; Amendment 9, Part 5;
Amendment 10, Part 5) as one command, in the order of preregistration/a10_stepc_run_sheet_2026-11-04.md.
Written after the provisional run of 2026-11-04, whose hand-run steps hit a wrong script name, a
majority-map defect and a check that came too late; the runner exists so the official map's run is the
same command with a new --src.

Every step runs as a subprocess from the repository root, logs to OUT/<step>.log, and the runner stops
at the first step that exits non-zero. Nothing is scored before the pre-checks pass. OUT/manifest.json
records each command, its exit code, its seconds, and the SHA-256 of every script and input it names.

Steps
  0  ingest                 ingest_committee_map.py to data/shapefiles/<--ingest-dir>/<label>.gpkg
  0b check_changed          check_changed_reproduced.py (geometry agrees with Step A's changed list)
  0c assignment             VA -> district by representative point (node = OBJECTID - 1); every later
                            step that takes an assignment uses this one, so all steps share one path
  1  partisan               phase4c_canonical_attribution.py + joint_outlier_score_canonical.py
  2  structural             run_structural_battery.py
  3  verdict                verdict_synthesis.py
  4  x1                     score_x1.py
  5  size_matched           close_seats_ensemble.py real --extra + size_matched_results.py
  6  qsgy8                  phase_b_scorecard.py --skip-mcmc --map-s50 <step 1's seats at 50/50>
  8  cut_va                 cut_va_sensitivity_stepc.py --map fixed (only with --snap-dir: a
                            reconstruction's snapping output; an official map has none)
  9  va_cuts                va_bisection.py; with --snap-dir also mark_uncertain_cuts.py
  10 rules                  rules_check.py on the 0c assignment (supplementary)
  Step 7 (R1/R2) runs detached for hours; the runner prints its launch and scoring commands.

Usage
  python -W ignore analysis/scripts/run_stepc.py --src GPKG --name-col COL --label NAME --out DIR
         [--snap-dir DIR] [--ack DISTRICT ...] [--from STEP] [--only STEP ...]
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PY = sys.executable
VA = "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
STATED = "data/iap/iap_app7_populations.csv"
TABLE = "data/outputs/s15_2_va_criteria.csv"
TABLE_SHA = "48c928b8716f6ed218065e01a912ecabd11518917ac9e312376e4d603ee2fafc"
ORDER = ["ingest", "check_changed", "assignment", "partisan", "structural", "verdict", "x1",
         "size_matched", "qsgy8", "cut_va", "va_cuts", "rules"]


def sha(p):
    p = ROOT / p
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


class Run:
    def __init__(self, out):
        self.out = out
        self.manifest = {"started": time.strftime("%Y-%m-%dT%H:%M:%S"), "python": PY, "steps": []}
        mp = out / "manifest.json"
        if mp.exists():
            self.manifest["steps"] = json.loads(mp.read_text(encoding="utf-8"))["steps"]

    def save(self):
        (self.out / "manifest.json").write_text(json.dumps(self.manifest, indent=1), encoding="utf-8", newline="\n")

    def cmd(self, step, args, env=None):
        log = self.out / f"{step}.log"
        t0 = time.time()
        e = dict(os.environ, **(env or {}))
        with open(log, "a", encoding="utf-8") as f:
            f.write(f"$ {' '.join(args)}\n")
            f.flush()
            rc = subprocess.call([PY, "-W", "ignore", *args], cwd=ROOT, stdout=f, stderr=subprocess.STDOUT, env=e)
        files = {a: sha(a) for a in args if (ROOT / a).is_file()}
        self.manifest["steps"].append({"step": step, "args": args, "env": env or {}, "rc": rc,
                                       "seconds": round(time.time() - t0, 1), "sha256": files})
        self.save()
        if rc != 0:
            print(f"[{step}] FAILED (exit {rc}); see {log}")
            print(log.read_text(encoding="utf-8")[-2000:])
            sys.exit(rc)
        print(f"[{step}] ok ({time.time() - t0:.0f}s)")


def assignment(scored, out):
    import geopandas as gpd

    va = gpd.read_file(ROOT / VA)
    pts = va[["OBJECTID", "geometry"]].copy()
    pts["geometry"] = pts.geometry.representative_point()
    g = gpd.read_file(ROOT / scored).to_crs(va.crs)
    j = gpd.sjoin(pts, g[["EDName2025", "geometry"]], how="left", predicate="within")
    j = j[~j.index.duplicated(keep="first")].reindex(pts.index)
    if j.EDName2025.isna().any():
        sys.exit(f"[assignment] {int(j.EDName2025.isna().sum())} voting areas outside every district")
    a = j[["OBJECTID", "EDName2025"]].assign(node=lambda d: d.OBJECTID - 1).rename(columns={"EDName2025": "district"})
    a[["node", "district"]].to_csv(out, index=False)
    print(f"[assignment] ok: {len(a)} voting areas in {a.district.nunique()} districts -> {out.relative_to(ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="the map's district polygons")
    ap.add_argument("--name-col", required=True, help="district-name column in --src")
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True, help="output directory, relative to the repository root")
    ap.add_argument("--ingest-dir", default=None, help="data/shapefiles/<dir>/ (default: the label)")
    ap.add_argument("--snap-dir", default=None)
    ap.add_argument("--ack", nargs="+", metavar="DISTRICT",
                    help="districts whose check_changed FAIL a person has acknowledged (named, recorded, still reported)")
    ap.add_argument("--from", dest="start", choices=ORDER, default="ingest")
    ap.add_argument("--only", nargs="+", choices=ORDER)
    a = ap.parse_args()

    out = ROOT / a.out
    out.mkdir(parents=True, exist_ok=True)
    o = a.out.rstrip("/")
    scored = f"data/shapefiles/{a.ingest_dir or a.label}/{a.label}.gpkg"
    phase4c = f"{o}/{a.label}_phase4c.json"
    real = f"{o}/{a.label}_real_maps.json"
    run = Run(out)
    steps = a.only or ORDER[ORDER.index(a.start):]
    if sha(TABLE) != TABLE_SHA:
        sys.exit(f"criteria table SHA-256 is {sha(TABLE)}, not the Amendment 5, Part 15 table")

    for s in steps:
        if s == "ingest":
            (ROOT / scored).parent.mkdir(parents=True, exist_ok=True)
            run.cmd(s, ["analysis/scripts/ingest_committee_map.py", "--src", a.src, "--name-col", a.name_col, "--out", scored])
        elif s == "check_changed":
            run.cmd(s, ["analysis/scripts/check_changed_reproduced.py", "--map", scored, "--out", f"{o}/check_changed_reproduced.json",
                        *(["--ack", *a.ack] if a.ack else [])])
        elif s == "assignment":
            assignment(scored, out / "assignment_nodes.csv")
        elif s == "partisan":
            run.cmd(s, ["analysis/scripts/phase4c_canonical_attribution.py", "--majority", scored, "--output", phase4c, "--map-key", a.label])
            run.cmd(s, ["analysis/scripts/joint_outlier_score_canonical.py", "--map-key", a.label, "--real-scores", phase4c,
                        "--output", f"{o}/joint_outlier.json"])
        elif s == "structural":
            run.cmd(s, ["analysis/scripts/run_structural_battery.py", "--shapefile", scored, "--output", f"{o}/structural.json", "--label", a.label])
        elif s == "verdict":
            run.cmd(s, ["analysis/scripts/verdict_synthesis.py", "--structural", f"{o}/structural.json", "--joint", f"{o}/joint_outlier.json",
                        "--output", f"{o}/verdict.json"])
        elif s == "x1":
            run.cmd(s, ["analysis/scripts/score_x1.py", "--map", scored, "--out", f"{o}/x1.json"])
        elif s == "size_matched":
            run.cmd(s, ["analysis/scripts/close_seats_ensemble.py", "real", "--out", real, "--extra", scored])
            run.cmd(s, ["analysis/scripts/size_matched_results.py", "--root", "../alberta_audit", "--real", real, "--candidate", a.label,
                        "--out-json", f"{o}/size_matched.json", "--out-md", f"{o}/size_matched.md"])
        elif s == "qsgy8":
            s50 = json.loads((ROOT / phase4c).read_text(encoding="utf-8"))[a.label]["seats_at_50_50"]
            run.cmd(s, ["analysis/scripts/phase_b_scorecard.py", "--shapefile", scored, "--map-name", a.label, "--name-col", "EDName2025",
                        "--skip-mcmc", "--map-s50", f"{s50:.4f}", "--out-dir", o])
        elif s == "cut_va":
            if not a.snap_dir:
                print(f"[{s}] skipped: no --snap-dir (not a reconstruction)")
                continue
            run.cmd(s, ["findings/a10_stepc/cut_va_sensitivity_stepc.py", "--map", "fixed", "--snap-dir", a.snap_dir,
                        "--out-prefix", f"{o}/cut_va_sensitivity"], env={"A10_STEPC": "1"})
        elif s == "va_cuts":
            run.cmd(s, ["analysis/scripts/va_bisection.py", "--map", scored, "--label", a.label, "--vas", "2023", "2026",
                        "--out-csv", f"{o}/va_cuts.csv"])
            if a.snap_dir:
                run.cmd(s, ["findings/a10_stepc/mark_uncertain_cuts.py", "--map", scored, "--cuts", f"{o}/va_cuts.csv",
                            "--out", f"{o}/va_cuts_marked.csv"])
        elif s == "rules":
            run.cmd(s, ["analysis/scripts/rules_check.py", "--assignment", f"{o}/assignment_nodes.csv", "--table", TABLE,
                        "--stated", STATED, "--label", a.label, "--out", f"{o}/rules_check.json"])

    wt_osf = str(ROOT).replace("\\", "/")
    print("\nStep 7 (R1/R2), from the wt-a8 worktree at 42b5fda8, each chain detached (WMI + pythonw runner):")
    print(f"  analysis/scripts/territory_null.py --idx N --enacted {wt_osf}/{scored} --stated-low <map's count below -25%> --out <DIR>")
    print("  then findings/a10_stepc/territory/score_plans_enacted.py, territory_score.py rank, calibrate_enacted.py")


if __name__ == "__main__":
    main()
