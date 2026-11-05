# Amendment 10: the third Step B calibration run — result

> Registered run under Amendment 10 (OSF 9wp5y, update `6aeb59edd63871f1daf383ab`, filed 2026-11-04 2:51 PM MST). Run 2026-11-04, 2:54 PM to 7:22 PM MST, from the frozen code at commit `070c31cd` (every script's SHA-256 matches Amendment 10). Python 3.12.13 with PyMuPDF 2.1.

## Result: the calibration passes

| Gate | Result | Limit |
|---|---|---|
| T1: sample voting areas in the wrong district | 0 of 1,909 (0.0%) | at most 10% |
| T4: province-wide efficiency-gap delta | 0.00 points | under 0.5 points |
| Sanity check, calibration map | every item passes | every item |
| Drift after snapping, calibration map | 0.005% | under 0.05% |

Before snapping, the assembly alone gave T1 63 of 1,909 (3.3%) and T4 −0.03 points.

As Amendment 10, Part 2 states, the sample is development data and this result was stated in advance; the run is a reproducibility check of the frozen pipeline, not out-of-sample evidence of its accuracy. It reproduced exactly: the voting-area assignment of both the calibration map and the panel's assembled map is identical, file for file, to the last development dry run.

## The panel's map (Amendment 10, Part 5)

With the 56 unchanged districts and Calgary-Acadia at the commission's published geometry and the 35 changed pages from this run assembled under Parts 3 and 3b, every sanity item passes (91 districts; every voting area assigned; each district connected; no overlap with a known district over 0.1%; areas within tolerance; printed neighbours; inside the page frame; locator map, with Barrhead-Westlock-Athabasca's inset a recorded source error; coverage complete), with drift 0.003%. Step C may therefore proceed, provisionally, under Amendment 10, Part 5.

## The pages

69 pages were run: 65 placed and 4 failed, the same four as in development:

- ED 57 Chestermere-Strathmore and ED 66 Grande Prairie-Wapiti: no local match within the prior's error;
- ED 63 Fort McMurray-Wood Buffalo: below the acceptance rule (363 matched points);
- ED 82 Peace River: below the acceptance rule (median 100.7 m, 36% within 60 m).

On the panel's map three of the four (57, 66, 82) are among the unchanged districts and are taken at the commission's geometry; Fort McMurray-Wood Buffalo is filled from the hole its neighbours leave. On the calibration map they are handled as registered (hole fill and the merged-hole split).

## Disclosed stop

At 4:29 PM MST both page workers crashed (python.exe, access violation 0xc0000005) when the machine left Modern Standby as a remote-desktop session connected; Phone Link crashed in the same minute. 23 pages were complete. The workers were restarted at 4:30 PM and skipped the completed pages, as Amendment 10, Part 4 allows; the stop is recorded in `findings/a10_stepb_run/run_log.txt`. The restarted pages and the uninterrupted pages are deterministic and identical to development.

## Files

- `findings/a10_stepb_calibration.json`: the scorer's full output.
- `findings/a10_stepb_run/`: the run log; the final voting-area assignments of the calibration map and the panel's map; both sanity reports; the panel's assembled districts (`districts_real_map.gpkg`, drawn by the frozen pipeline; a gap-free copy for display is made separately and does not feed any score).
