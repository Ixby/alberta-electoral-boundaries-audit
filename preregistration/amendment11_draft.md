# Amendment 11 (draft): fixes found by the provisional Step C run, before the official map is scored

> **Status: DRAFT, not filed.** Written 2026-11-04 (Alberta time), after the provisional Step C run on the panel's assembled map (`findings/a10_stepc/README.md`, commits `8fcf4318` and `083c0d1f`). Every Step C result has been seen. Nothing here changes a test, a threshold, a statistic or a reading of a result. It changes two pieces of code that failed when the panel's map was scored, and it writes down one procedure that was applied by precedent during the run. All three would recur on the official map. Not filed until the author approves the text.

**Why.** Step C ran each registered step by hand. Three registered pieces did not do what the amendments say they do on a scored map:

- the cut-voting-area sensitivity (Amendment 10, Part 5) scored the commission majority's map, not the map given;
- the redraw-test scorer (Amendment 8) cannot score a rerun's plans from its command line;
- one redraw-test chain did not seed, and no amendment says what to do.

Step C worked around each and disclosed it (`preregistration/a10_stepc_run_sheet_2026-11-04.md`, "Changes to this sheet"). This amendment makes the workarounds the registered procedure, so the official map's run needs no decision at run time.

**Part 1: the cut-voting-area sensitivity on a scored map.** `findings/a10_dev/cut_va_sensitivity.py` (SHA-256 `c264a49e…a0dc`) builds, in its step 2, the calibration composite (the majority map with only the sample districts replaced) for every map. On `--map fixed` it therefore never scored the changed districts; its Step C output gave the majority's efficiency gap (+0.098%) instead of the panel's (+1.45%). That output is kept as `findings/a10_stepc/cut_va_sensitivity_fixed_REGISTERED_CODE_DEFECT.json`. For any scored map, the registered script is `findings/a10_stepc/cut_va_sensitivity_stepc.py` (SHA-256 `5f45ec65e7266b29146567190fa906084da958f9dca2bf490b394ec0f4defe8b`). It differs from the original in that step only: on `--map fixed` each district is the union of the voting areas the assignment gives it. On `--map tuning` it is unchanged. Its baseline efficiency gap equals the partisan lane's and R1's on the same map (+1.45%).

**Part 2: the redraw-test scorer takes the scored map.** At `42b5fda8`, `territory_score.py` (SHA-256 `0485e788…2b55`) builds its territory from the scored map only in `rank`. `plans` and `calibrate` build it from Step A's list, so on a rerun (Amendment 8, Part 5) they fail with a shape mismatch. The registered scorer becomes `territory_score.py` at the commit that adds `--enacted` and `--stated-low` to `plans` and `calibrate`, passed to the same `Substrate` that `rank` uses (SHA-256 `47ead0966445b4f2a3aefbc33102b155666b7bf7fd7f1b0c263c17367fd9a142`). Without `--enacted` both subcommands behave exactly as before. Check: on Step C's plans, `plans --enacted` reproduces Step C's `scores.csv` byte for byte (made with the wrapper `score_plans_enacted.py`, SHA-256 `9ed54016…c79a`), and `calibrate --ref 1 2 4 6 --holdout 5 --enacted` reproduces its `calibration.json` byte for byte (made with `calibrate_enacted.py`, SHA-256 `db227364…5da`). The fix is commit `569250cd` on branch `a8-territory-null`. The two wrappers are then no longer needed; they stay in `findings/a10_stepc/territory/` as the record of what Step C ran.

**Part 3: a redraw-test chain that does not seed.** Amendment 8 runs chains 1 to 5 from the registered drand round (salts `a8-territory-null-chain<idx>`). Chains 1 to 4 are the reference and chain 5 is the holdout. A chain *does not seed* when `territory_null.py` exits before its first step because `recursive_tree_part` finds no starting plan. Then:

1. That chain is retired and recorded as retired with its log. It is not rerun with another seed or setting.
2. Its place is taken by the next index not yet used: 6, then 7, and so on, with the same code, salt pattern, run length and thinning. A replacement for a reference chain joins the reference set. A replacement for chain 5 becomes the holdout.
3. Whether every chain seeds is settled when the chains are launched, before any plan is scored. The reference and holdout chains are written into the run record at that point.

This is the rule Step C applied, citing Amendment 5, Part 14 (set D's index 250, retired because it does not seed; the next free index is used). Step C retired chain 3 and used chain 6.

**What this amendment does not change.** No test, threshold, null, ensemble, statistic, flag rule or outcome rule. The 2×2 outcome, X1, the size-matched sets, the qsgy8 tripwires, R1 and R2 are scored exactly as Amendments 5 to 10 say. The Step C results stand as recorded, labelled provisional. This amendment gives no conclusion on whether any map is a gerrymander.

**Outside this amendment (on GitHub, not registered).** These changes were also made after Step C. They are tooling and data checks, not registered rules.
- `analysis/scripts/run_stepc.py` runs Step C as one command and stops at the first failure.
- `analysis/scripts/check_changed_reproduced.py` checks before scoring that the map's geometry agrees with Step A's list of changed districts. On the provisional map it flags Edmonton-Meadows.
- `analysis/scripts/vote_anywhere_splat.py` builds the all-ballots substrate with the Vote Anywhere ballots included; it is used by the seat-claim test, not by Step C.
