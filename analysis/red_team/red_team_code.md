# Code red team — findings

Hostile review of the Python code under `alberta_audit/analysis/`. Severity labels:
CRITICAL (would flip a reported number), HIGH (less robust than claimed),
MEDIUM (reproducibility risk), LOW (defensive coding), INFO (observation only).

All line numbers refer to the file at the time of review. All findings are
"static-analysis only — dynamic check recommended" unless otherwise stated.

## Executive summary

- CRITICAL: 5 findings
- HIGH: 12 findings
- MEDIUM: 13 findings
- LOW: 7 findings
- INFO: 6 findings
- Total scripts reviewed: 21 (of 39 `.py` files in `analysis/`)
- Scripts skimmed / not exhaustively reviewed: `338canada_historical.py` (partial, 44 KB), `shape_refinement_v2.py`, `shape_refinement_v3.py` (partial), `v0_1_submission_ocr*.py`, `submission_search.py`, `justification_tests.py`, `poll_attribution_skeleton.py`, `marginal_seats_analysis.py`, `plan_b_rerun.py`, `rural_gap_dissection.py`, `url_archival.py`, `csd_community_splits.py`, `2015_cross_election.py`, `build_academic_html.py`, `assignment_prep.py` (partial).

---

## Critical findings

### CRIT-01. Monte Carlo CI uses wrong numpy percentile convention (empirical fractional index without interpolation) and has a silent `continue` that can drop samples, leaving a non-2,000 sample set feeding the "95% CI" claim.

**File/line:** `analysis/scripts/monte_carlo_ci.py:86-89, 109-118, 162-163`
**Evidence:**
```python
for i in range(n_samples):
    ...
    if len(maj) != 89 or len(minr) != 89:
        continue  # skip invalid sample
    ...
# later, in summarize():
p025 = values_sorted[int(n * 0.025)]
p50  = values_sorted[int(n * 0.500)]
p975 = values_sorted[int(n * 0.975)]
...
ci_lo = sorted(asym)[int(len(asym) * 0.025)]
ci_hi = sorted(asym)[int(len(asym) * 0.975)]
```
**Behaviour:** `int(n * 0.975)` for `n=2000` returns `1950`, i.e. the 1,951st value (zero-indexed 1950). That is the 97.55th percentile, not 97.5th. More importantly, `int()` floor-truncates — which on the lower tail gives `int(2000*0.025)=50`, i.e. the 51st value (2.55th percentile, not 2.5th). With no interpolation, the reported 95% CI is a slightly wider / different interval than advertised. The same bug applies to `p50` (uses `values_sorted[1000]`, the 1001st value, not the median). And the `continue` can silently reduce `n` to ≤ 2000 if any jittered sample fails the 89-ED gate — yet the summarize function still uses `int(len(asym) * 0.025)` rather than an exact quantile.
**Expected:** Use `numpy.percentile(values, 2.5)` / `97.5` with linear interpolation, or (bare-metal) `(n - 1) * p` and linearly interpolate between floor and ceil. Also verify `len(asym) == n_samples` and surface the number of skipped runs.
**Impact:** For the audit's headline 95% CI on minority-vs-majority EG asymmetry (-1.34 pp to +0.27 pp per docstring), the bounds will be slightly off and the number of samples underlying the CI is not explicitly asserted. Most consequential: the "95% CI crosses zero → NOT defensible" verdict in `main()` turns on the exact ci_lo, ci_hi. If the sign of either bound is near zero, the convention matters.
**Fix recommendation:** Replace with `np.percentile(sorted_vals, [2.5, 50, 97.5])`. Also assert `len(results['asymmetry']) == n_samples` or document a skipped count.

---

### CRIT-02. 338Canada scraper regex is non-anchored, uses non-greedy `[^}]*?` with a character class `[^}]` that matches newlines — producing false-match blocks when 338's HTML contains multiple stacked JS objects with `values:` keys that do not correspond to the intended party-share/MoE/win-prob structure.

**File/line:** `analysis/scripts/338canada_scraper.py:48-55, 62-101`
**Evidence:**
```python
PARTY_BLOCK_RE = re.compile(
    r"key:\s*'([^']+)',[^}]*?values:\s*\[\s*([\-\d\.\s,]+)\]",
    re.DOTALL,
)
PARTY_WITH_MOE_RE = re.compile(
    r"key:\s*'([^']+)',[^}]*?values:\s*\[\s*([\-\d\.\s,]+)\],\s*moe:\s*\[\s*([\-\d\.\s,]+)\]",
    re.DOTALL,
)
...
share_signature = {(k, v.strip()) for k, v, _ in share_blocks}
for key, vals in all_value_blocks:
    if (key, vals.strip()) in share_signature:
        continue
    ...
    if key in parties:
        parties[key]['win_prob'] = v[-1] if v else float('nan')
```
**Behaviour:** `[^}]*?` with `DOTALL` is lazy-greedy; it will consume anything (including `{` and line breaks) up to the first subsequent `values:`. If 338's inner objects contain nested braces or keys whose values include `values:` strings (e.g. in CSS or labels), the regex can attach the wrong `values:` array to a key. More importantly, the "win probability blocks are those that do NOT appear in share_signature" rule will mis-classify if any win-prob series coincidentally equals a share series (unlikely but not impossible), or if 338 adds a fourth stacked block (e.g., moe2 for alternate scenarios). There is no integrity check that exactly 87 ridings × expected schema → expected counts were parsed.
**Expected:** Count that 87 ridings produce 87 per-riding output rows. Check that each row has valid ucp/ndp and lead_party ∈ {UCP, NDP, ...}. Fail loudly if counts mismatch.
**Impact:** A silent parse degradation at 338's end would feed wrong shares into `338canada_reallocate.py`, which rebuilds the 89-seat projected-winner table and is cited in Track J. The audit's 87-row integrity is not asserted anywhere in the script — only the end `print(f"Wrote {len(rows_out)} rows...")` shows the count. A reader of the CSV would not know if 86 rows reflect one silent fetch failure.
**Fix recommendation:** Add `assert len(rows_out) == 87` or equivalent. Validate ucp_share + ndp_share + other_share ≈ 100% per row. Sanity-check that `leading_party` ∈ known set.

---

### CRIT-03. The packing/cracking `estimate_2026` integer-truncates blended NDP / UCP votes, producing systematic downward bias in both seat counts and EG.

**File/line:** `analysis/scripts/packing_cracking_analysis.py:445-455, 469-484`
**Evidence:**
```python
def blend(base: Dict, urban_w: float) -> Dict:
    utot = base['ndp'] + base['ucp']
    ushare = base['ndp'] / utot
    rural_w = 1 - urban_w
    blended_share = urban_w * ushare + rural_w * rural_ndp_share
    # Rural absorptions have slightly lower turnout → scale total.
    new_total = utot * (urban_w + rural_w * 0.7)
    return {
        'ndp': int(new_total * blended_share),
        'ucp': int(new_total * (1 - blended_share)),
    }
...
elif kind == 'merge':
    parts = [by_name.get(name) for name in spec[1]]
    weights = spec[2]
    if all(parts):
        ndp = sum(int(p['ndp']*w) for p, w in zip(parts, weights))
        ucp = sum(int(p['ucp']*w) for p, w in zip(parts, weights))
```
**Behaviour:** `int()` in Python floors positive floats (truncates toward zero). Every blend row loses up to 1 vote per party; every merge row loses up to 1 vote per 2019-parent per party. Over 89 EDs with ~30 hybrids × 2 parties, this is ~60 lost votes. Normally immaterial for EG — but when computing `eg = (ndp_wasted - ucp_wasted) / total` on totals near 1.7 M, the difference between int-truncated and non-truncated blending can shift the EG in the fourth decimal place and can flip a single close ED from NDP-win to UCP-win or vice versa.
**Expected:** Round-half-even or round-half-up, not truncate. Ideally keep floats and only round at the final seat-count cutoff.
**Impact:** The audit's 1-seat asymmetry (minority 52 vs majority 51 NDP wins) is the central headline and depends on individual ED marginal flips. Any row with margin within a vote or two of 50/50 can be flipped by this rounding choice, invalidating the "1-seat difference is robust" claim. Dynamic check recommended to quantify.
**Fix recommendation:** Use `round()` or keep floats throughout `compute_metrics`. Assert no ED has a two-party margin inside `±2 votes` (would be a flipped-by-rounding seat).

---

### CRIT-04. 338 reallocate v1 function has a `raise RuntimeError("blend path requires rural_ndp_share; see main()")` that will fire in-production if anyone calls the v1 rather than v2 function — yet v1 is still exported and looks like the primary entry point from the top of the file.

**File/line:** `analysis/scripts/338canada_reallocate.py:129-215` (especially line 173)
**Evidence:**
```python
def reallocate_338(t338: Dict, mapping: Dict, pop: Dict[str, int],
                   rural_ucp_share: float) -> List[Dict]:
    ...
    for new_ed, spec in mapping.items():
        kind = spec[0]
        if kind == 'direct':
            ...
        elif kind == 'blend':
            src, urban_w = spec[1], spec[2]
            ...
            raise RuntimeError("blend path requires rural_ndp_share; see main()")
```
**Behaviour:** The file defines `reallocate_338` (v1, broken for blend) and `reallocate_338_v2` (working). `main()` only calls v2. But an external caller or future session that imports `reallocate_338` will crash on the first blend row, and there is no docstring deprecation marker. Dead code that looks live is a known trap.
**Expected:** Delete v1 or rename to `_deprecated_reallocate_338_v1`. If kept for historical reference, put it in a `# DEPRECATED` block and raise `NotImplementedError` at entry.
**Impact:** Reproducibility — a reviewer who imports the module and calls the v1 function will get misleading/crashing results and conclude the audit's reallocation pipeline is broken.
**Fix recommendation:** Remove the dead v1 function.

---

### CRIT-05. `packing_cracking_analysis.py`'s `MAJORITY_2026_MAPPING` silently drops rows when `'merge'` has a missing 2019 parent; `estimate_2026` then returns fewer than 89 EDs, and `validate_2026_estimate` catches it — but the unused `out` still contains the partial list that gets returned if validation is skipped.

**File/line:** `analysis/scripts/packing_cracking_analysis.py:469-484, 491-512`
**Evidence:**
```python
elif kind == 'merge':
    parts = [by_name.get(name) for name in spec[1]]
    weights = spec[2]
    if all(parts):
        ndp = sum(int(p['ndp']*w) for p, w in zip(parts, weights))
        ucp = sum(int(p['ucp']*w) for p, w in zip(parts, weights))
        out.append({'ed': new_ed, 'ndp': ndp, 'ucp': ucp})
...
def validate_2026_estimate(estimates: List[Dict], label: str,
                           expected_n: int = 89) -> Tuple[bool, str]:
    n = len(estimates)
    ...
    if n != expected_n:
        msgs.append(f"FAIL: {label} has {n} EDs, expected {expected_n}")
        ok = False
```
**Behaviour:** If `by_name.get(name)` returns `None` for any parent in a merge, the row is silently dropped. `main()` does call `validate_2026_estimate` and aborts metrics computation — but `estimate_2026` is also called from `monte_carlo_ci.py` and `338canada_reallocate.py`, neither of which calls `validate_2026_estimate`. If a future 2019-ED name change (or a typo) breaks a merge key, the Monte Carlo will silently run on 88-ED estimates, altering efficiency gap denominators.
**Expected:** Raise explicitly if any mapping row cannot be resolved. Log the skipped name.
**Impact:** Breaks reproducibility of the Monte Carlo CI if the data gets touched. Currently passes because the 2019 names are frozen.
**Fix recommendation:** Change silent `continue`/drop patterns to explicit `raise KeyError(new_ed)` and catch at top level with a clear log.

---

## High findings

### HIGH-01. The shape-refinement v6 pipeline uses `hash(ed_name) % (2**32)` as a per-ED RNG seed, meaning Python hash randomization (on by default for strings in Python 3.3+) makes runs non-reproducible unless `PYTHONHASHSEED` is pinned — and it is not set anywhere in the pipeline.

**File/line:** `analysis/scripts/refine_boundaries.py:247`
**Evidence:**
```python
# T5: reverse sampling
minx, miny, maxx, maxy = poly_geo.bounds
rng = np.random.default_rng(hash(ed_name) % (2**32))
hits = 0
tries = 0
while hits < 20 and tries < 2000:
    px = rng.uniform(minx, maxx); py = rng.uniform(miny, maxy)
```
**Behaviour:** Python's `hash(str)` is randomized per process by default. Two separate invocations of the script produce different hashes for `"Calgary-De Winton"`, giving different RNG seeds, giving different sample points for the T5 reverse-sampling test. Since T5 has a pass threshold of exactly 20 hits, a polygon on the edge (20.00 expected hits) could pass one run and fail the next.
**Expected:** Use a fixed, explicit seed per ED — e.g. `zlib.crc32(ed_name.encode())` or a pre-tabulated mapping. Or pin `PYTHONHASHSEED=0` in the script via `os.environ` at startup.
**Impact:** The v6 log claims pass/fail for each of 7 active-disproof tests. Reproducibility of those pass/fail flags requires deterministic seeds. Currently not satisfied.
**Fix recommendation:** Replace with `rng = np.random.default_rng(int.from_bytes(hashlib.md5(ed_name.encode()).digest()[:4], 'big'))` or similar.

---

### HIGH-02. The `optimise_affine_dt` brute-force pre-search in v6 processors uses `np.arange` over three nested floating-point ranges with small step sizes — the number of combinations is 100k+, each of which calls `cost()`. Performance is one issue; more importantly, `np.arange` on floats is known to produce off-by-one boundary points (e.g. `np.arange(0, 0.3, 0.1)` may return 4 elements instead of 3). This can cause the grid search to silently miss the documented boundary tx/ty.

**File/line:** `analysis/scripts/shape_refinement_v6_processors.py:72-80`
**Evidence:**
```python
# Brute-force pre-search for good initial tx/ty
best = (c0, x0)
for tx_try in np.arange(initial_tx - 50000, initial_tx + 50000, 10000):
    for ty_try in np.arange(initial_ty - 50000, initial_ty + 50000, 10000):
        for s_try in np.arange(initial_scale - 3, initial_scale + 3, 0.5):
            x_try = [1 / s_try, 0, -tx_try / s_try, 0, -1 / s_try, ty_try / s_try]
            c_try = cost(x_try)
            if c_try < best[0]:
                best = (c_try, x_try)
```
**Behaviour:** `np.arange(initial_scale - 3, initial_scale + 3, 0.5)` with `initial_scale=13.5` returns `[10.5, 11.0, ..., 16.0]` — but depending on floating-point accumulation, the last element may or may not be included. This is a known gotcha in the NumPy docs. The outer tx/ty loops also have this risk.
**Expected:** Use `np.linspace` with an explicit number of steps, or a hand-coded integer range.
**Impact:** Deterministic — the search misses specific grid cells. If the true optimum sits at one of the missing cells, the Nelder-Mead downstream could get stuck in a local minimum. Affects the quality (RMS residual) of the affine fit for the v6 vectorisation of Calgary-De Winton, Calgary-South, Edmonton-Windermere.
**Fix recommendation:** `np.linspace(initial_scale-3, initial_scale+3, 13)` etc.

---

### HIGH-03. Shape-refinement v4-v5 builds Calgary-De Winton and Edmonton-Windermere from hand-coded bounding boxes with magic-number pixel coordinates that are **not validated against the 2019 shapefile** — `hays_miny + 0.85 * (hays_maxy - hays_miny)` depends on Calgary-Hays's 2019 extents. If the 2019 shapefile were ever re-issued with minor corrections, the hardcoded percentages silently produce wrong polygons without error.

**File/line:** `analysis/scripts/shape_refinement_v4.py:555-647`, `analysis/scripts/shape_refinement_v5.py:930-971`
**Evidence:**
```python
west_x = 72000
east_x = 76500
south_y = hays_miny - 200
north_y = hays_miny + 0.85 * (hays_maxy - hays_miny)
base_rect = box(west_x, south_y, east_x, north_y)
cs_base = base_rect.intersection(hays)
# Apply notch on NE corner...
notch_w = 1500
notch_h = 1200
```
**Behaviour:** `west_x = 72000` is an absolute coordinate in EPSG:3401; if the 2019 shapefile's Calgary-Hays polygon centroid shifted by even a few hundred metres (due to re-projection or clean-up), the rectangle's overlap with the true Hays polygon would differ. The script has no cross-check that `west_x` falls inside Hays.
**Expected:** Express all bounding boxes as fractions of the source polygon's bounds, or precompute `hays_centroid` and place the rectangle relative to it with a documented offset.
**Impact:** Breaks if 2019 data is re-issued; otherwise fine. Reproducibility depends on the 2019 shapefile staying identical.
**Fix recommendation:** Wrap each magic number with a `# VERIFIED 2026-04-22 against alberta_2019_eds/EDS_ENACTED_BILL33_15DEC2017.shp` comment, and add a startup `assert hays.contains(Point(west_x, north_y))`.

---

### HIGH-04. `shape_refinement.py` phase 2 OSM-snap pathological-snap guard rejects new polygons outside [0.6, 1.5] × original area — silently falling back to the original polygon. This is reported as a non-failure in the output gpkg (the row's `refined_note` still says "snapped:…" unless we look at `mean_shift_m = 0.0`). The guard's log line is `[phase2/{label}] {name} FAILED: {e}` — but pathological guards fail without exception, and there's no dedicated log message.

**File/line:** `analysis/scripts/shape_refinement.py:288-298`
**Evidence:**
```python
# Guard: reject pathological snaps
try:
    orig_area = poly.area
    new_area = new_poly.area if new_poly and not new_poly.is_empty else 0.0
    if orig_area > 0 and (new_area / orig_area < 0.6 or new_area / orig_area > 1.5):
        return poly, 0.0, 0.0
except Exception:  # noqa: BLE001
    return poly, 0.0, 0.0

return new_poly, mean_shift, max_shift
```
**Behaviour:** Rejected-snap rows are returned with `mean_shift=0, max_shift=0, new_poly=poly`. The caller writes `refined_note = f"snapped:mean={mean_s:.1f}m,max={max_s:.1f}m"` regardless, so the gpkg shows `"snapped:mean=0.0m,max=0.0m"` — indistinguishable from "snap ran but nothing moved". Downstream (`phase4_compactness`) treats a zero-shift row as "snapped" and therefore uses the tight CI rule rather than the ±0.03 widened CI.
**Expected:** On guard rejection, log explicitly and set `refined_note = f"SNAP_REJECTED_PATHOLOGICAL_area_ratio={ratio:.2f}"`.
**Impact:** The Polsby-Popper CIs reported in §5 of the academic report may be too narrow for rows where the snap was silently rejected.
**Fix recommendation:** Distinguish the guard-rejection case in the log, and treat it as equivalent to the "not snapped" case for CI computation.

---

### HIGH-05. Chen-Rodden ensemble (`chen_rodden_alberta.py` Test 2) uses `random.Random(42)` as the walk RNG but also calls `np.random.default_rng(seed)` in Test 1 and `dev.shuffle(v)` in Test 1's permutation — different RNG objects. Different numpy versions change the default RNG implementation silently in minor releases.

**File/line:** `analysis/scripts/chen_rodden_alberta.py:133-156, 403-404`
**Evidence:**
```python
def morans_i_permutation_test(values: np.ndarray, W: np.ndarray,
                              n_perm: int = 999, seed: int = 42) -> Dict:
    rng = np.random.default_rng(seed)
    ...
# Test 2
rng = random.Random(42)
```
**Behaviour:** `numpy.random.default_rng(42)` uses a Philox-based bit generator since numpy 1.17; the stream is stable but differs from Python's `random.Random(42)` stream. The two tests are independent but the script claims reproducibility — that claim requires pinning numpy version, which is not done.
**Expected:** State numpy version (and Python version) in the docstring; or use `np.random.SeedSequence(42).generate_state(n)` and wrap explicit generators.
**Impact:** MEDIUM — if someone rebuilds with numpy 2.x+, they get identical streams (good); but if someone does it with numpy 1.16, the Moran's I permutation p-value will differ. Boundary case: p_value near 0.05 could flip.
**Fix recommendation:** Document numpy version; use `np.random.Generator(np.random.PCG64(seed))` explicitly.

---

### HIGH-06. `cross_election_rural_baseline.py` uses ED-name-prefix heuristic ("Calgary-*", "Edmonton-*", else "Rest of Alberta") for 2015 regional classification. The 2015 boundaries differ from 2019, so a 2015 ED named "Calgary-Buffalo" may include territory that 2019 assigned to a non-Calgary ED (and vice versa). The docstring acknowledges this as "closely matches … but is not boundary-accurate", but the script itself does not quantify or flag the drift. The output is fed into the v0.3 Monte Carlo as the rural range.

**File/line:** `analysis/scripts/cross_election_rural_baseline.py:27-33, 86-96`
**Evidence:**
```python
def region_from_name(ed_name: str) -> str:
    n = ed_name.strip()
    if n.lower().startswith("calgary"):
        return "Calgary"
    if n.lower().startswith("edmonton"):
        return "Edmonton"
    return "Rest of Alberta"

def load_2015() -> list:
    ...
    out.append({"region": region_from_name(r["ed_2015"]),
                "ndp": ndp, "ucp_equiv": ucp_equiv})
```
**Behaviour:** 2015 Edmonton-Calder, 2015 Calgary-Currie, etc. are classified purely by name-prefix. A 2015 ED named "Spruce Grove-St. Albert" (outside Edmonton city limits but near it) would be classified "Rest of Alberta" — correct. A 2015 ED named "Edmonton-Rutherford" that is actually a Leduc-adjacent ED including rural territory would be fully counted as Edmonton even though ~20% of its voters are rural. The audit's 2015 rural NDP share of 35.05% is therefore an approximation that is not error-bounded.
**Expected:** Cross-check against 2019 and 2023 using the same name-prefix heuristic (which would also be wrong but in the same direction), then state the error band. Or use the 2019 shapefile + 2015 poll-level data to reaggregate.
**Impact:** The v0.3 Monte Carlo range `Uniform(0.28, 0.38)` is calibrated on these three numbers. If the 2015 observed rural share is biased +2 pp by the heuristic, the Monte Carlo is subtly mis-calibrated.
**Fix recommendation:** State the name-prefix-heuristic error band explicitly; add a robustness variant using 2019-ED-mapped 2015 polls.

---

### HIGH-07. `build_cover.py` regenerates `report_public.pdf` by running `build_pdf.py` as a subprocess and then `replace()`-ing it to `report_public_article.pdf` — but this design has a race condition if `report_public.pdf` is open in a viewer, and the call `env={**os.environ, "PYTHONIOENCODING": "utf-8"}` overrides the entire environment without preserving `PATH`, `PROGRAMFILES`, and other Windows-critical vars (on Windows, missing PROGRAMFILES breaks geopandas's GDAL loader).

**File/line:** `analysis/scripts/build_cover.py:488-502`
**Evidence:**
```python
build_pdf_py = REPO_ROOT / "analysis" / "build_pdf.py"
subprocess.run(
    [sys.executable, str(build_pdf_py)],
    check=True,
    env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"},
)
# build_pdf.py wrote to OUT_PDF (report_public.pdf). Move it aside.
if OUT_PDF.exists():
    OUT_PDF.replace(ARTICLE_PDF)
```
**Behaviour:** `{**os.environ, ...}` actually copies the entire env and adds/overrides `PYTHONIOENCODING` — so `PATH` et al. are preserved. Not a bug. But `OUT_PDF.replace(ARTICLE_PDF)` on Windows silently fails if `OUT_PDF` has an open handle (e.g. PDF viewer), leaving `report_public.pdf` in the previous state and `ARTICLE_PDF` not created → merge step then reads the old article. No check that `ARTICLE_PDF.exists()` after the replace.
**Expected:** Add `assert ARTICLE_PDF.exists(), "build_pdf.py did not produce output"` after the rename.
**Impact:** Reproducibility hazard on a rebuild when the previous run's PDF is open.
**Fix recommendation:** Assert file existence; or close-on-retry loop.

---

### HIGH-08. Chrome headless PDF invocation uses `--no-sandbox` (security flag) which on CI or locked-down systems could fail silently; `--virtual-time-budget=15000` is arbitrary (15s) and has no dynamic check that fonts/images loaded. Print-to-PDF always writes a file — but if Chrome silently renders without the Google Fonts (network outage), the PDF degrades to system-serif and the report looks wrong without any error.

**File/line:** `analysis/scripts/build_pdf.py:513-534`, `analysis/scripts/build_cover.py:420-437`
**Evidence:**
```python
cmd = [
    browser_path,
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    f"--print-to-pdf={out_pdf.resolve()}",
    ...
]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
if result.returncode != 0:
    sys.stderr.write(result.stderr or result.stdout or "")
    raise RuntimeError(...)
```
**Behaviour:** `--no-sandbox` is used even on Windows where it's unnecessary for end-users (it's a Linux container concern). On a fresh machine with no Chrome profile, `--virtual-time-budget` of 15s may be insufficient if Playfair Display / Lora / Source Sans 3 are fetched cold. A font-fallback degrade is silent — returncode stays 0.
**Expected:** Post-hoc PDF validation: parse the generated PDF with `pypdf` or `pdfplumber` and assert at least one page; optionally embed the Google Fonts as base64 in the HTML (true "self-contained") rather than `@import`.
**Impact:** A build on a network-isolated machine could produce a visually broken report that looks fine to the script. Low probability for the audit's primary authors but a reproducibility hazard for reviewers.
**Fix recommendation:** Inline Google Fonts, or assert fonts loaded post-render.

---

### HIGH-09. `check_voice_and_readability.py` "not X — Y" rule is too narrow — it only matches `\bnot\s+(a|an|the|just)\s+[a-zA-Z ]{3,30}\s+[—–-]\s+`, so phrases like "not partisan — structural", "not gerrymandering — redistribution", "not surprising — expected" (no leading `a/an/the/just`) slip through. The docstring claims to catch "mirrored 'not X — Y' reversals" generally.

**File/line:** `analysis/scripts/check_voice_and_readability.py:33-42`
**Evidence:**
```python
WUFF_VIOLATIONS = [
    (r"\bnot\s+(a|an|the|just)\s+[a-zA-Z ]{3,30}\s+[—–-]\s+",
     "'not X — Y' mirror reversal"),
    ...
]
```
**Behaviour:** Only matches constructions with `not a/an/the/just ...`. "Not partisan — structural" (the most common audit-voice violation) is missed.
**Expected:** `\bnot\s+[a-zA-Z]+\s+[—–-]\s+[a-zA-Z]` to catch the bare-adjective form.
**Impact:** The voice checker approves drafts that contain the very pattern it is designed to reject. Given the audit has extensive prose, many violations likely slip past.
**Fix recommendation:** Broaden the regex; add a test fixture of known positive/negative examples.

---

### HIGH-10. `check_voice_and_readability.py` Flesch-Kincaid fallback approximation uses `re.findall(r"[aeiouy]+", w)` to count syllables — this is a crude vowel-group heuristic that systematically undercounts syllables for words ending in 'e' (handled) but **silently overcounts** compound words like "re-examine" (the hyphen is stripped on the strip step, producing "reexamine" with vowel-group count 4 when the real syllable count is 4 — OK in this case, but "queue" returns 2 via `[aeiouy]+` match = `queue` → `ueue` = 1 group, giving 1 syllable when the real count is 1-2 depending on dialect).

**File/line:** `analysis/scripts/check_voice_and_readability.py:70-81`
**Evidence:**
```python
words = re.findall(r"\b[A-Za-z][A-Za-z']*\b", stripped)
if not words:
    return None, "approx"
total_syl = 0
for w in words:
    w = w.lower()
    groups = re.findall(r"[aeiouy]+", w)
    syl = max(1, len(groups))
    if w.endswith("e") and syl > 1 and not w.endswith("le"):
        syl -= 1
    total_syl += syl
return 0.39 * (len(words) / len(sents)) + 11.8 * (total_syl / len(words)) - 15.59, "approx"
```
**Behaviour:** The approximation differs from `textstat.flesch_kincaid_grade` by up to ±2 grade levels for typical prose. The script explicitly labels the output as `"approx"` — good — but then proceeds to compare it to the threshold `target_grade + 0.5` **and fails the file if the approximation exceeds the threshold**. On a run where `textstat` is not installed, the approximation can push a compliant public report above 12.0 and the exit code flips to 1.
**Expected:** Either require `textstat` (hard dependency), or do not fail the gate on the approximation output — report it as informational.
**Impact:** A reviewer running the voice checker without `textstat` installed could get false FAIL outcomes and conclude the report fails the reading-level bar when it does not.
**Fix recommendation:** Only fail the reading-level gate when `method=="textstat"`.

---

### HIGH-11. `a1_legal_baseline_2021_census.py` reprojects CSD / DA polygons to EPSG:3401 and computes `.area` — this is correct. But the DA-population file handling `df["population_2021"].fillna(0).astype(int)` silently **zeroes out suppressed DAs** without documenting how many. The docstring acknowledges CSD-level suppression but is silent about DA-level.

**File/line:** `analysis/scripts/a1_legal_baseline_2021_census.py:110-123`
**Evidence:**
```python
def load_da_populations() -> pd.DataFrame:
    df = pd.read_csv(DA_POP_CSV)
    df = df.rename(columns={"DAUID": "DAUID_int"})
    df["DAUID_int"] = df["DAUID_int"].astype(int)
    n_null = int(df["population_2021"].isna().sum())
    if n_null:
        print(f"  Note: {n_null} DAs with null 2021 pop (suppressed);"
              " treated as zero.")
    df["population_2021"] = df["population_2021"].fillna(0).astype(int)
```
**Behaviour:** Logs the count but does not accumulate the implied uncertainty into the MAD output. Suppressed DAs are concentrated in Indian reserves and small towns — systematic bias affects specifically the s.15(2)-protected districts that the audit claims may not qualify.
**Expected:** Track the allocated population that depends on suppressed DAs per ED. Flag any ED where >5% of population is "from suppressed DAs" so the reader can discount its MAD contribution.
**Impact:** The 2021-census MAD cited in Appendix C may be silently different from the true MAD for s.15(2) districts.
**Fix recommendation:** Compute and report a "suppressed-DA pop share" per ED.

---

### HIGH-12. `majority_symmetry_counter_test.py` has a hand-coded Edmonton zone classifier that lists hybrid naming variants (both `Edmonton-Castle Downs` and `Edmonton-Castledowns`, both `Edmonton-Enoch` and `Edmonton-Enoch-Devon`) — but the majority/minority 2026 population CSVs use their respective canonical names, and a future data refresh that adds a new Edmonton ED would silently fall into `"Edmonton-unclassified"` and be skipped from the test. The script logs `unclassified_count` but does not fail on nonzero.

**File/line:** `analysis/scripts/majority_symmetry_counter_test.py:108-153, 170-220`
**Evidence:**
```python
def edmonton_zone_classifier(ed_name: str) -> str:
    zone_c = {
        "Edmonton-Beverly-Clareview",
        "Edmonton-Castle Downs",
        "Edmonton-Castledowns",
        ...
    }
    zone_d = {
        "Edmonton-Beaumont",
        ...
    }
    if ed_name in zone_c:
        return "Zone C"
    if ed_name in zone_d:
        return "Zone D"
    return "Edmonton-unclassified"

def test_1_edmonton_packing(...) -> list[dict]:
    ...
    uncl = edmonton[edmonton["zone"] == "Edmonton-unclassified"]
    ...
    if len(uncl):
        unclassified_names: list
    ...
```
**Behaviour:** Report does not fail the test on nonzero unclassified count. Zone means are computed only from `zc` and `zd`. If the data changes, the test becomes silently incomplete.
**Expected:** Raise an assertion if `len(uncl) > 0` or output a `SETUP_ERROR` flag.
**Impact:** Reproducibility; the test is as strong as the hand-curated dict.
**Fix recommendation:** Fail-loud on unclassified EDs.

---

## Medium findings

### MED-01. `shape_refinement.py` silently accepts the zip-extracted path for the 2019 ED shapefile. If two `.shp` files exist in `.temp/2019_eds.zip` (for example, if the zip contains both a state-level and ED-level file), the code picks the first one returned by `rglob` — non-deterministic on some filesystems.

**File/line:** `analysis/scripts/shape_refinement.py:154-162`
**Evidence:**
```python
def _load_2019_eds():
    import zipfile, tempfile
    z = ROOT / ".temp" / "2019_eds.zip"
    tmp = Path(tempfile.mkdtemp(prefix="eds2019_"))
    with zipfile.ZipFile(z) as zf:
        zf.extractall(tmp)
    shp = list(tmp.rglob("*.shp")) + list(tmp.rglob("*.gpkg"))
    if not shp:
        raise FileNotFoundError("No 2019 ED shapefile found in 2019_eds.zip")
    return gpd.read_file(shp[0])
```
**Behaviour:** `rglob` order is unspecified. Deterministic only if exactly one file matches.
**Expected:** Assert `len(shp) == 1` or filter by expected filename.
**Fix recommendation:** Add an assertion.

---

### MED-02. `shape_refinement.py` phase 2's OSM fetch is wrapped in a retry loop with exponential backoff `time.sleep(2 ** i)` for `retries=2`. That's one retry after 1 second. If Overpass is experiencing a rate-limit spike, one-second retry is insufficient. Subsequent failures surface as `OSM_UNAVAILABLE` and the row carries the 2019 geometry unchanged — silent fallback.

**File/line:** `analysis/scripts/shape_refinement.py:165-189, 346-356`

---

### MED-03. `assignment_prep.py` imports and runs top-level code at module load (not inside `main()`), meaning any `import` of this module by a different script triggers full pipeline execution. Tagged `from __future__ import annotations` and has no `if __name__ == "__main__":` guard.

**File/line:** `analysis/scripts/assignment_prep.py:36-end`
**Evidence:**
```python
print("[1/5] Loading inputs...")
vas = gpd.read_file(DATA / "alberta_2023_vas")
eds19 = gpd.read_file(DATA / "alberta_2019_eds" / "EDS_ENACTED_BILL33_15DEC2017.shp")
...
```
**Fix recommendation:** Wrap in `def main():` and `if __name__ == "__main__": main()`.

---

### MED-04. `assignment_prep.py` uses `encoding="latin-1"` for the `polls_2023_unified.csv` loader but every other file in the audit uses `utf-8`. A mix-up could silently corrupt candidate names containing UTF-8 characters (e.g., diacritics in French names, `'` apostrophes).

**File/line:** `analysis/scripts/assignment_prep.py:41`
**Evidence:**
```python
polls = pd.read_csv(ANALYSIS / "polls_2023_unified.csv", encoding="latin-1")
```
**Fix recommendation:** Confirm that the CSV is actually Latin-1 encoded. If UTF-8, change to `utf-8` and add a chardet check.

---

### MED-05. `electoral_forensics_population.py` s.15(2) criteria are hand-typed with magic numbers (area, distance to major centre) for 6 ridings. The docstring says these are from "publicly available sources (Natural Resources Canada atlas, StatsCan 2021 census, Treaty maps)" but no URLs or retrieval dates. If any number is wrong, the "FAIL 3/5" verdict for Canmore-Banff and Rocky Mountain House-Banff Park is wrong.

**File/line:** `analysis/scripts/electoral_forensics_population.py:293-371`
**Evidence:**
```python
S15_2_CRITERIA = {
    "Canmore-Banff (majority)": {
        "dev_pct": -27.2,
        "area_km2": 8500,
        "dist_major_centre_km": 85,
        "town_4000_plus": True,
        ...
    },
    ...
}
```
**Fix recommendation:** Add URL + retrieval-date comments for each claimed fact, or compute `area_km2` from the 2019 shapefile directly.

---

### MED-06. `chen_rodden_alberta.py` population proxy uses 2023 two-party vote total as a proxy for population — acknowledged in docstring, but the ±25% constraint `lo = target_pop * 0.75; hi = target_pop * 1.25` is then enforced in *vote-total* space, not *population* space. Vote-to-population ratio varies across EDs (rural turnout lower, urban higher), so the random-walk ensemble is sampling from a slightly different population-constrained plan space than the one claimed. Docstring acknowledges this but does not quantify the bias.

**File/line:** `analysis/scripts/chen_rodden_alberta.py:331-337`

---

### MED-07. `packing_cracking_analysis.py` sensitivity test re-computes `maj_w`, `min_w` twice in the same loop iteration (once from the unchanged mapping, once from an overridden mapping). The first computation is dead code — but it burns compute and suggests the original intent was different. A maintainer could accidentally swap the semantics later.

**File/line:** `analysis/scripts/packing_cracking_analysis.py:572-586`
**Evidence:**
```python
for w in [0.60, 0.70, 0.80]:
    maj_w = estimate_2026(dists_2019, MAJORITY_2026_MAPPING, rural_ndp, urban_weight=w)
    min_w = estimate_2026(dists_2019, MINORITY_2026_MAPPING, rural_ndp, urban_weight=w)
    # Re-blend with alternative weight requires overriding URBAN_WEIGHT_DEFAULT
    # For this sensitivity check we rebuild mappings with override weight:
    override_maj = {k: (v[0], v[1], w) if v[0] == 'blend' else v
                    for k, v in MAJORITY_2026_MAPPING.items()}
    ...
    maj_w = estimate_2026(dists_2019, override_maj, rural_ndp)
    min_w = estimate_2026(dists_2019, override_min, rural_ndp)
```
**Behaviour:** Both `maj_w`/`min_w` lines execute. The second assignment wins. The first is wasted. Also note: the `urban_weight=w` parameter on the first call does nothing — the mapping tuples have the weight baked in. This is actually the correct behaviour but the dead code is confusing.
**Fix recommendation:** Remove the first two `estimate_2026` calls.

---

### MED-08. `canadian_base_rate_compute.py` deflates seat-share asymmetry to EG asymmetry using a hardcoded `0.455` factor derived from one cycle's ratio (Alberta 2026: 0.51 EG / 1.12 seat-share). Applied to 6 other cycles with different seat counts, party compositions, and election contexts. Docstring acknowledges this but the benchmark distribution (mean, median, percentile) is computed on those deflated values and cited as a "Canadian base rate."

**File/line:** `analysis/scripts/canadian_base_rate_compute.py:76-98, 412-453`
**Evidence:**
```python
@property
def eg_asymmetry_proxy_pp(self) -> float | None:
    # ... Apply 0.45× deflator — the audit's actual Alberta figure was 0.51 pp
    # against a 1.12 pp seat-share asymmetry, ratio 0.455.
    sa = self.seat_share_asymmetry_pp
    if sa is None:
        return None
    return sa * 0.455
```
**Behaviour:** Deflator is constant across cycles. There is no dimensional analysis — the deflator depends on the ratio of wasted-vote effects to seat-flip effects, which varies with each jurisdiction's EG structure. The "71st percentile" placement of Alberta relative to the distribution becomes dependent on an assumption the audit itself flags as unvalidated.
**Fix recommendation:** Widen the proxy with `eg_low` and `eg_high` using the full [0.40, 1.20] ratio bounds cited in the docstring.

---

### MED-09. Shape refinement v5's `process_calgary_south` fallback path is entered when cleaning removes the polygon, but the fallback itself uses `hays.centroid` and a bbox — this produces a centered rectangle that is guaranteed to be inside Hays but may bear no resemblance to the actual Calgary-South. The `v5_method` column is not updated to reflect the fallback.

**File/line:** `analysis/scripts/shape_refinement_v4.py:620-630`

---

### MED-10. `track_l_drift.py` uses hand-coded growth factors per CSD. The docstring cites "Alberta TBF and StatsCan-published annual growth rates" but no explicit URL/retrieval date per CSD. Default growth by CSDTYPE is `1.075` — a single flat number regardless of whether the CSD is, e.g., Wood Buffalo (explicitly override to 0.990). Any new CSD not in the hand-coded dict gets the flat default.

**File/line:** `analysis/scripts/track_l_drift.py:51-177`

---

### MED-11. `build_overlay_figures.py` hardcodes the v5 → v4 fallback order. If v5 is broken / not yet regenerated and v4 is stale, the publication figures silently use v4 and the caption says "v4" — but the report text may still reference "v5 shapes." There's no cross-check that the text and figures match.

**File/line:** `analysis/scripts/build_overlay_figures.py:289-292`

---

### MED-12. `chen_rodden_alberta.py` Moran's I permutation test shuffles `values` in-place (`rng.shuffle(v)`) where `v = values.copy()`. The copy is shuffled but the original `values` is untouched — correct. However, the calculation compares `abs(perm_I - expected) >= abs(I_obs - expected)` — using `expected` from the formula `-1/(n-1)`, not the permutation mean. Under standard Moran's I theory, the null distribution mean equals `expected` only asymptotically; using it for a two-sided p-value is conservative but not standard.

**File/line:** `analysis/scripts/chen_rodden_alberta.py:133-156`
**Fix recommendation:** Compare to `perm_I.mean()` (empirical null) rather than theoretical `expected`.

---

### MED-13. Chen-Rodden Test 2 `compute_plan_metrics` function has a degenerate case when a plan has only one district (NDP-swept or UCP-swept) — `n_ndp_wins = 87, n_ucp_wins = 0`. The declination formula returns `float('nan')` but the efficiency gap still computes as `(ndp_wasted - ucp_wasted) / total`. If `ucp_wasted = 0` (all UCP voters in losing districts), the EG still equals `(NDP_surplus - 0) / total` and is reported, but interpreting this EG as "gerrymandering signal" vs "natural-sweep" requires a separate sweep check.

**File/line:** `analysis/scripts/chen_rodden_alberta.py:228-242`

---

## Low findings / observations

### LOW-01. `build_pdf.py` regex `r"(<hr\s*/?>\s*)<p>"` matches the FIRST `<hr>` in the rendered HTML — but the markdown author may include the first `<hr>` for a different purpose (e.g., a horizontal rule between sections rather than after the masthead block). If the masthead markdown changes, the lede class may attach to the wrong paragraph.

**File/line:** `analysis/scripts/build_pdf.py:494-500`

---

### LOW-02. `packing_cracking_analysis.py`'s `compute_metrics` uses `tt // 2 + 1` as the majority threshold, which assumes all EDs have even vote counts and that "majority" means >50%. For an odd-count ED, `(tt // 2) + 1` gives the actual vote threshold. For an even-count ED where the vote is tied, the EG treats the NDP-won outcome as requiring strict inequality. This is consistent with standard EG (Stephanopoulos-McGhee) but is worth noting.

**File/line:** `analysis/scripts/packing_cracking_analysis.py:131-142`

---

### LOW-03. Multiple scripts use `float("nan")` in the rounding chain (e.g., `round(v, 2) if v == v else ''`) — the `v == v` test is Python-idiomatic NaN detection, but `math.isnan(v)` is clearer and handles infinities. Minor style.

**File/line:** `analysis/scripts/338canada_scraper.py:146-157, 173-174`, `analysis/scripts/338canada_reallocate.py:47-60` and scattered.

---

### LOW-04. Chen-Rodden `_votes` helper in Test 3 uses `for i in range(1, 7)` — the 2019 results file has up to 8 candidates (the `cross_election_rural_baseline.py` loader uses `range(1, 9)`). So Test 3 silently stops at candidate 6, missing candidates 7 and 8 for some EDs. In practice Alberta's major parties are NDP and UCP and the 2-party vote is captured, but this is a silent schema mismatch.

**File/line:** `analysis/scripts/chen_rodden_alberta.py:533-548`, compare `analysis/scripts/cross_election_rural_baseline.py:66` (`range(1, 9)`).

---

### LOW-05. `shape_refinement.py`'s `_snap_polygon_to_roads` sample-spacing is `max(int(line.length / 200.0) + 1, 8)` — that's at least 8 samples per ring even for rings shorter than 1.6 km. Reasonable for small urban EDs but may produce 200+ samples on long rural rings, which is fine.

**File/line:** `analysis/scripts/shape_refinement.py:219-220`

---

### LOW-06. `a1_legal_baseline_2021_census.py` does not pin its CRS assumption — it asserts `TARGET_CRS = "EPSG:3401"` but does not verify the input shapefile's declared CRS matches (it just reprojects). If the input has a wrong declared CRS (wrong EPSG tag but correct coords), `to_crs` would silently "reproject" nonsense.

**File/line:** `analysis/scripts/a1_legal_baseline_2021_census.py:146-154`

---

### LOW-07. `majority_symmetry_counter_test.py` `count_eds_containing_city` uses string matching which has edge cases: for `city = "Fort McMurray"`, the ED named `Fort McMurray-Wood Buffalo` matches. But `city = "Red Deer"` with ED `Red Deer County` (doesn't exist in 2026 but could in future data) would also match. More critically: for `Calgary` the script *excludes* big-city-prefix suffixes — the inverted logic at line 238-243 is confusing and bug-prone.

**File/line:** `analysis/scripts/majority_symmetry_counter_test.py:223-244`

---

## Info / observations

### INFO-01. EPSG:3401 description disagreement. `shape_refinement.py:58` and all shape-refinement files label `EPSG:3401` as "3TM 115 (Calgary/Edmonton corridor)", but `data_preparation.md:170` labels it as "NAD83 3TM 114°W for Alberta". The correct authority: EPSG:3401 is NAD83 3TM Zone 114°W (it covers all of Alberta — not a corridor). The scripts are not actually using the wrong CRS (calls to `.area` work correctly because the coordinates are stored in the shapefile), but the docstrings are misleading.

**File/line:** `analysis/scripts/shape_refinement.py:56-58` and the v2-v5 headers.

---

### INFO-02. The cover builder `build_cover.py:488-501` regenerates the whole report by re-invoking `build_pdf.py`. This is an expensive re-render (markdown → HTML → Chrome PDF). On a re-run with only cover changes, the entire report is re-rendered. A Makefile / DAG could cache the article PDF.

---

### INFO-03. Every shape-refinement version except v6 uses `WORK_CRS = "EPSG:3401"` and reprojects at various points. v6 switches to `AREA_CRS = "EPSG:3400"` for area computation and `WORK_CRS = "EPSG:3401"` for writing. The rationale (per `data_preparation.md`) is that 3400 preserves area across Alberta while 3401 is the native shapefile CRS. Both are Alberta 3TM variants; area differences between them are sub-percent. Acceptable in practice but the inconsistency across versions is a readability hazard.

---

### INFO-04. `refine_boundaries.py:389-399` carries a 40+-line block of commented-out anchor-finding logic with semi-structured debugging notes ("Let me use more reliable anchors…", "Actually, looking more carefully…"). This is working-memory comments that made it into the committed file; it should be squashed to just the final anchor list. Not a bug but a readability / review-quality concern.

---

### INFO-05. `monte_carlo_ci.py:61-62` seeds `random.Random(42)` — a specific integer, documented. Good RNG discipline. But the `jittered_mapping` function called per sample uses the same `rng` across iterations, so the sample's `(base_w, rural, urban_weight_for_ed_X)` tuple depends on all previous draws. The n=2000 trajectory is correctly reproducible given the seed. This is stated in the docstring.

---

### INFO-06. `338canada_scraper.py:162` pauses 150 ms between requests ("gentle pacing"). Reasonable. No authentication token leakage. `UA` string is clearly identifying: `"Mozilla/5.0 (research; Alberta boundaries audit, v0_1)"`. Good hygiene.

---

## Cross-cutting observations

1. **Silent fallback is pervasive.** Multiple pipelines (shape refinement v3-v5, OSM fetch, 338 scraper) fall back to a default / previous polygon / zero on any failure, logged at best via a `print()` line. Reviewers and downstream consumers have no machine-readable way to distinguish "successful refinement" from "silent fallback." Proposal: emit a status code column (`status in {"ok", "fallback", "error"}`) in every output artifact.
2. **Seed discipline is inconsistent.** `monte_carlo_ci.py` pins `seed=42`. `chen_rodden_alberta.py` pins `seed=42` for Moran's I and `random.Random(42)` for the walk. `refine_boundaries.py` uses `hash(ed_name) % (2**32)` — hash randomization-dependent. No single canonical seed convention across the repo.
3. **CRS metadata in docstrings is stale.** EPSG:3401 is consistently referred to as "3TM 115 Calgary/Edmonton corridor" in the shape refinement files — it is actually NAD83 3TM 114°W covering all of Alberta. Does not affect correctness but trips reviewers.
4. **No integrity assertions at stage boundaries.** 87 2019 EDs → 89 2026 EDs is the canonical count. Most scripts trust that inputs are correct. `packing_cracking_analysis.py:validate_2026_estimate` is the rare counter-example — extend that pattern.
5. **Build pipeline assumes Chrome/Edge on Windows paths.** `build_pdf.py:33-38` hardcodes Program Files paths. No Linux fallback (`chromium`, `google-chrome` via `which`). The directive says Chrome is the canonical renderer — but reviewers on Linux cannot reproduce without modifying the script.
6. **338Canada depends on an unstable external HTML schema.** The regex-based parser has no version check. A 338 redesign would silently change parsed numbers. Proposal: compute a hash of `html[:10000]` and flag if it changes between runs; or (better) save raw HTML to a `.cache/` directory for audit-trail purposes.

---

## Scripts not exhaustively reviewed (flagged for follow-up)

The following were read in part or skimmed; a second-pass review is recommended:

- `338canada_historical.py` (44 KB, complex Wayback integration)
- `shape_refinement_v2.py` (superseded by v3-v5-v6; historical but still referenced)
- `shape_refinement_v3.py` (superseded by v4-v5-v6; historical)
- `submission_ocr.py` and `submission_ocr_analyze.py` (OCR pipeline)
- `submission_search.py` (search tool)
- `justification_tests.py`, `plan_b_rerun.py`, `poll_attribution_skeleton.py`, `marginal_seats_analysis.py`, `rural_gap_dissection.py`, `csd_community_splits.py`, `2015_cross_election.py` (statistical / analysis scripts)
- `url_archival.py` (URL archival utility)
- `build_academic_html.py` (HTML builder for academic report)
- `assignment_prep.py` (Phase 4C preparation — top-level code rather than main, flagged MED-03)

End of findings.
