# Checking the assembled 91-district map against the panel's own evidence (2026-11-05)

**Post-registration check, made after Step C was run and seen. Unregistered; sensitivity only.** The registered map (`data/shapefiles/iap_assembled/iap_2026_assembled.gpkg`, SHA-256 `518a59fe…b3a2e6e7`) and the Step C reading in `findings/a10_stepc/` stand unchanged. This note gives no conclusion on whether any map is a gerrymander.

Script: `analysis/scripts/iap_reconstruction_check.py`. Output: `check.json` and `data/shapefiles/iap_assembled/iap_2026_assembled_v2.gpkg` (SHA-256 `4525c92c876795821e8c17ead2a9fd97c6c5a676e3009e497b68af22ae75e075`). Inputs outside the repo:

- the accepted page polygons of the registered run, `C:/tmp/a10reg/pages/` (run commit `070c31cd`);
- the Version 4 placements, `C:/tmp/a10test/v4/ed40.gpkg` (`0a2a16a9…3bc29`) and `ed49.gpkg` (`27f91b18…cd7ef`).

## Why

Against the commission's majority map, 36 of the 91 districts overlap less than 99.9% (`C:/tmp/cmp91.csv`). Overlap with the majority is the wrong test for a changed district, which is meant to differ. So each district was checked against what the panel published:

- its stated area (Appendix 7, whole km², so ±0.5 km²);
- its map page;
- where one exists, an outside reference.

The stated-area test was validated on the 57 copied districts: the official areas are within 0.5 km² of the stated figure in 56 of them.

## Results

| Check | Result |
|---|---|
| VAs in unchanged districts (representative point, as scored) | 0 differ from the majority map |
| VAs in placed districts against their page | 1,615 agree; 0 contradict |
| VAs with no accepted page | 167: 165 in the hole-filled Calgary-North West-Bearspaw (56), Edmonton-Windermere (44), Edmonton-Meadows (29) and Fort McMurray-Wood Buffalo (36). The other two are VA 014 (Olds-Didsbury-Three Hills, 181 votes) and VA 042 (Rocky Mountain House-Sundre, 218 votes), whose representative points sit 3 m and 10 m outside their own page's edge, inside the 40 m snap tolerance. |
| Fort McMurray-Lac La Biche, Fort McMurray-Wood Buffalo vs 2017 borders | IoU 0.99996 and 0.99999. Every 2019 VA of each is in it, and the stated areas equal the 2017 areas. |
| Edmonton-Meadows, Edmonton-Windermere vs the Version 4 placements | IoU 0.991 and 0.983 before the correction, 0.998 and 0.996 after. The same VAs in both. |
| Districts outside the stated area ±0.5 km² | 16 before the correction, 14 after |

## The correction (v2)

Two copied districts held land outside their official boundaries. In both cases the land belongs to the hole-filled neighbour, so it is a defect of the registered assembly.

| District | Excess | Goes to | Area after (stated) |
|---|---|---|---|
| Edmonton-Rutherford | 0.707 km² | Edmonton-Windermere | 26.07 (26); Windermere 55.55 (56) |
| Edmonton-Mill Woods | 0.092 km² | Edmonton-Meadows | 24.35 (24); Meadows 12.82 (13) |

The excess held no VA's representative point. **No VA changes district, so every score of the registered run is unchanged.** The script refuses any correction that would move one.

## Districts looked at and left as they are

- **Red Deer-South (overlap 0.885 with the majority) is a real change, not a placement error.**
  - The panel moves the City of Red Deer south of 19 St, including Westerner Park, into Blackfalds-Innisfail (page PDF p299; text PDF p055).
  - The reconstruction follows the page. Its area is 31.07 km², against the panel's stated 31 km² and the commission's 35.10 km².
  - The piece holds 2 VAs with about 400 election-day votes. By 2021 dissemination-area counts it holds about 1,190–1,390 people, which matches the panel minority's "approximately 1,300 people in the City of Red Deer" (PDF p129, para 37).
  - **The panel's own population figure does not reflect this.** Appendix 7 and the page both give 59,121, which is 2 fewer than the commission's 59,123. The conflict is in the panel's report; the geometry was not tuned to it.
- **Chestermere-Strathmore is a real change that Step A cannot see.**
  - Its stated population equals the commission's (56,679), so Step A counted it unchanged. But its stated area is 1,025 km² against the official 1,019.72 km².
  - Step A's rule (name and population) cannot detect a change of unpopulated land. `iap_unchanged_districts.md` is left as filed; this note records the blind spot.
  - **Placed page (added later the same evening).**
    - The registered run never placed this page, and Version 4 cannot ("no page layer matches a reference"). `analysis/scripts/iap_chestermere_page_fit.py` places the page's red outline (PDF p272) onto the official district with the inset fit from `a10_inset.py`, sampled every 100 m. Fit error: median 26.5 m, 90th percentile 48 m. Output: `chestermere_page_fit.json`.
    - The page differs from the majority district in one place only: a 3.25 km² strip of the Bow River valley at Chestermere-Strathmore's south-east corner (about 606–611 km E, 5,626–5,630 km N, mean width 375 m).
    - On that stretch the majority's line runs along the north edge of the valley. The panel's runs along the river. The strip was the majority's High River-Vulcan-Siksika, and it holds no VA representative point.
    - **The v2 map already has this strip,** taken by the assembly, and nothing else: v2 against the placed page has IoU 0.9997, with no piece over 0.1 km² in either direction. The geometry is resolved; no change is made.
    - The page traces to 1,022.95 km², against the stated 1,025. That 0.2% sits inside the spread between page traces and stated areas on placed districts (Okotoks's page is +0.22%, Macleod-Crowsnest's −0.21%). No other departure as wide as the fit's precision shows on the page. The missing 2.05 km² cannot be located from it.
    - One VA sits on the line. VA 014 (2019 Chestermere-Strathmore, 181 votes) has its representative point 1 m inside the placed page's edge. Both the official majority line (High River-Vulcan-Siksika side) and the v2 map (Olds-Didsbury-Three Hills) put that point outside Chestermere-Strathmore. A 1 m distance is far inside the 26 m fit error, so the page cannot settle it, and the VA stays where it is.
- **Calgary-North West-Bearspaw (hole fill, no accepted page).**
  - It is the majority's Calgary-North West plus 11.2 km² of Bearspaw holding 3 VAs (408 votes).
  - Its area is 37.41 km² (stated 37).
  - Its stated population is 1,873 above Calgary-North West's 52,488, in line with those 3 rural VAs.
  - Version 4 could not place this page either, so there is no independent check.
- **Rural area misses: Banff-Canmore-Diamond Valley +13.3 km², Macleod-Crowsnest −9.3, Okotoks +2.6, and ten others off by 0.56 to 1.03 km².**
  - All of them lie in gap land that neither page claims, or in page traces that are themselves off: Macleod-Crowsnest's page is 28 km² short and Okotoks's is 2.7 km² over.
  - None holds a VA representative point. Giving Banff-Canmore-Diamond Valley's gaps to Macleod-Crowsnest would leave Banff-Canmore-Diamond Valley at its stated area but push Macleod-Crowsnest to +4.7. With no votes at stake, that would only fit one number.
- **The other placed districts below 0.999** (the Lethbridge, Calgary-west, Edmonton-south and central-Alberta redraws) differ from the majority because the panel redrew them. Every VA in them agrees with its page.

## Not changed

The registered files, the Step C results, `iap_unchanged_districts.md`, OSF. Nothing here is filed.
