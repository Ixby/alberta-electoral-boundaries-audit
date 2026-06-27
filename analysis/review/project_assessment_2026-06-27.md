# Project assessment — Alberta Electoral Boundary Audit (2026-06-27)

Multi-agent assessment: 8 parallel dimension assessors → adversarial verification of every critical/high finding → lead-reviewer synthesis. 16 agents, ~1.17M tokens. All 7 critical/high findings were CONFIRMED (0 refuted).

## Overall verdict

The audit is methodologically sound and publishable in substance: its headline rests on a symmetric, pre-committed neutral-ensemble outlier test with a genuinely exemplary self-correction culture (Fisher retired, SZAT demoted, collapsed findings retained as retractions), and the primary public surface (the live viewer's `en.ts`) is accurately grounded and verified against canonical outputs. The credibility risk is not the conclusion — it is the gap between the corrected live site and everything downstream of it. Hostile-reviewer-facing artifacts are currently in a worse state than the analysis: the downloadable public PDF carries a geometrically false claim, the repo's own integrity gates are red on master (provenance manifest stale, the sole recompute test failing), the master-QA harness reports PASS while a check FAILs because `run_audit.py` never exits non-zero, and factual corrections never propagated to 13 machine locales (two of which silently fall back to English for the entire accessibility shadow-site). **Biggest risk: a sophisticated critic running the repo's documented commands, or reading the linked PDF, finds a red CI gate and a false geographic claim — undermining the project's "let the data speak" credibility even though the core analysis holds.**

## Health by dimension

- **Statistical methodology** — Adequate. Sound, well-hedged core; weaknesses are stale-code, precision-framing, and convergence-provenance, not a broken conclusion.
- **Report accuracy & grounding** — Needs work. Live `en.ts` is clean; the downloadable public report (PDF linked from the site) still carries a false ED claim and superseded figures.
- **Viewer code quality (SvelteKit/Svelte 5)** — Strong. Well-engineered deck.gl explorer, 118/118 tests pass; no critical findings.
- **Analysis pipeline (Python)** — Needs work. Strong architecture/seeding/manifest, but the two integrity mechanisms (recompute test, master-QA) are non-functional.
- **Accessibility (WCAG)** — Adequate. Conscientious hand-built foundation, but zero end-to-end validation (no axe, no Playwright, no screen-reader pass).
- **Internationalization (19 locales)** — Needs work. Solid architecture/fallback, fr fully synced; factual corrections un-propagated, two locales mis-nested, no parity test.
- **Security & privacy** — Adequate. Core privacy architecture verified server-side; medium/low hygiene items only.
- **Reproducibility, data integrity & git hygiene** — Adequate. Canonical-shapefile integrity bit-exact and well-documented; but the committed-output provenance gate is failing on master.

## Top issues (confirmed critical/high only, prioritized)

**1. [HIGH — Reproducibility] Provenance CI gate is failing on master; manifest is stale.**
`python analysis/scripts/check_provenance.py --manifest data/provenance_manifest.json` (the exact CI command) FAILs 4 of 6 files and exits 1: `phase4c_canonical_results.json` (6615844f→48e9283f), `simulated_ensemble_percentiles_canonical.csv` (c8322582→757e82cf), `simulation_real_map_scores_canonical.json` (0a9eadfd→7abe51e5), `simulation_convergence_diagnostics_canonical.json` (8b0fa771→39e7a195). Outputs were regenerated without updating the manifest. **Fix:** regenerate + update `data/provenance_manifest.json` in the same commit until the gate exits 0; make it a required status check.

**2. [HIGH — Analysis pipeline] `run_audit.py` never exits non-zero, so master-QA reports PASS while Check 8 permanently FAILs.**
No `sys.exit`/`raise`; `run_master_qa.py:40` gates on `returncode == 0`. Check 8 compares the `*_full` vote universe (1,598,982) against a stale Apr-28 election-day score (`covered_votes` 932,164) — a guaranteed permanent FAIL the documented QA command cannot surface. **Fix:** `sys.exit(1)` on any FAIL; make Check 8 like-for-like; reconcile the two vote universes in `config.yaml`.

**3. [HIGH — Analysis pipeline] The only recompute-integrity test that runs is red (declination sign-flip).**
`pytest tests/` → 1 failed: `test_scoring.py::test_verification_subset_recompute_spot_check`. Saved `declination` is the exact negation of the recompute (step 263 saved 0.0504578746 vs −0.0504578746). `amendment_10_declination_migration.py` flipped the sign for 6 files but not `simulation_verification_metrics.csv`. **Fix:** regenerate the verification subset post-flip, pin its hash, unskip/xfail the silent ensemble checks.

**4. [HIGH — Report accuracy] Public report PDF names the wrong ED for the Airdrie split.**
`reports/public/report_public.md` L107 & L113 list "Calgary-Nolan Hill-Cochrane" (0% intersection with Airdrie). Correct fourth ED is Olds-Three Hills-Didsbury (27.1%). Fixed in `en.ts`, never in the markdown → PDF (linked from the live site). **Fix:** correct L107/L113, rebuild via `build_pdf.py`.

**5. [HIGH — i18n] Truth-audit corrections never reached the 13 machine locales.**
Wrong Airdrie ED + superseded drain figures persist in ar/hi/ko/pa/pdt/pl/ru/so/tl/ur/vi/zh-Hans/zh-Hant (airdrie_p, airdrie_callout_p2, table_r8_b, table_r8_c, closing_p2). **Fix:** run the propagation pass (in progress — en/fr/es/de/uk/crk done).

**6. [HIGH — i18n / Accessibility] `ru` and `zh-Hant` mis-nest `explorer.text` under `explorer.flags`.**
`ru.ts:972` and `zh-Hant.ts:994` place `text:` inside the unclosed `flags:` object → ~26 keys land at `explorer.flags.text.*`; every `explorer.text.*` lookup renders English, degrading the screen-reader shadow-site to English for Russian and Traditional-Chinese users. **Fix:** close `flags` before `text:`; add a key-parity test.

**7. [HIGH — Accessibility] The entire a11y surface is unverified end-to-end.**
No @axe-core, no Playwright, no jest-axe; no screen-reader pass. **Fix:** add @axe-core/playwright smoke tests over the report, `/explorer`, `/explorer/text` (incl. ar/ur RTL); commit a manual NVDA/VoiceOver log; treat the screen-reader pass as a release gate.

## Refuted / downgraded

None — adversarial verification confirmed all seven critical/high findings.

## Strengths

- **Exemplary self-correction** (Fisher retired for channel dependence; SZAT demoted after a contiguity-respecting null, p 0.0024→0.1947; retractions kept in place).
- **Symmetric, pre-committed design**; all RNG seeds drand-anchored before the official shapefiles arrived.
- **Accurate, well-hedged academic headline**; confirmatory vs exploratory cleanly separated.
- **Verified canonical-data integrity** (SHA-256 + byte-size bit-exact; LFS oid == content hash).
- **Strong viewer engineering** (118/118 tests; idiomatic Svelte 5; robust i18n fallback).
- **Sound, server-verified privacy** (deny-all RLS, cookieless daily-salted analytics, layered anti-abuse).
- **Honest provenance narrative** (DPG→canonical sunset documented, DOCUMENTED CORRECTIONS boxes, dead findings archived).

## Recommended next actions (ordered)

1. **Green the integrity gates first** (#1, #2, #3) — they invalidate the project's own credibility claims. Make both gates required status checks; add data-output paths to the CI trigger.
2. **Fix the false geography on every published surface:** `report_public.md` + rebuild PDF (#4); machine-locale propagation for the five Airdrie/drain keys (#5).
3. **Repair `ru`/`zh-Hant` mis-nesting** (#6) + add a flatten-and-diff key-parity test (would have caught #5, #6, the 11-key drift, the 4 dead nav keys).
4. **Stand up a11y validation** (#7): axe/playwright smoke tests + a committed NVDA/VoiceOver log as a release gate.
5. **Medium statistical/framing items:** reframe headline p as a chi²(4)/MVN extrapolation + report the empirical floor; fix `szat.py --use-block-permutation` to use connected-component blocks; gate/remove the retired Fisher block; delete stale DPG-era Reock/anchoring lines; reconcile the public report's pre-registration overclaim with the methodology doc.
6. **Hygiene:** propagate the 11 new source keys to all locales; fix the privacy-policy "encrypted cookie" overclaim; bound the anon-insert `shares` table; reconcile competing ensemble-size/hash statements.
