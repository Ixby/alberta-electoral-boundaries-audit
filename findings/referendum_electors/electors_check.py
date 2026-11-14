# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
electors_check.py

Runs preregistration/referendum_electors_check_2026-11-07.md: do 2026 referendum elector counts track
the stated July 2024 population estimates or the 2021 census overlay? Electors are a check on the
figures, not the Act's test. Unregistered. Applies no legal test.

Reads   evidence/elections_alberta/referendum_2026/ed01-ed87.xlsx, index.xlsx (no openpyxl: plain XML)
        evidence/elections_alberta/EA_Voting_Area_Boundaries_2026.zip
        data/iap/iap_app7_populations.csv, data/va_pop_from_das.csv
        data/shapefiles/canonical/ea_{majority,minority}_2026_eds.gpkg
        data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg, findings/iap_para167/para167_map.gpkg
        data/shapefiles/derived/va_polygons_with_2023_votes.gpkg (2023 VAs, for the overlay)
Writes  data/referendum/electors_by_va_2026.csv, findings/referendum_electors/electors_check.json,
        division_table.csv

Usage: python -W ignore findings/referendum_electors/electors_check.py
"""
import json
import re
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / "evidence/elections_alberta/referendum_2026"
VA_ZIP = ROOT / "evidence/elections_alberta/EA_Voting_Area_Boundaries_2026.zip"
OVERLAY_VAS = ROOT / "data/shapefiles/derived/va_polygons_with_2023_votes.gpkg"
MAPS = {"majority": (ROOT / "data/shapefiles/canonical/ea_majority_2026_eds.gpkg", "EDName2025"),
        "minority": (ROOT / "data/shapefiles/canonical/ea_minority_2026_eds.gpkg", "EDName2025"),
        "panel": (ROOT / "data/shapefiles/iap_assembled/iap_2026_assembled_v3.gpkg", "district"),
        "para167": (ROOT / "findings/iap_para167/para167_map.gpkg", "district")}
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NAMED = ["Calgary-North East", "Calgary-South East", "Edmonton-Windermere"]
MIN_MATCH = 0.99


def read_xlsx(path):
    # Official downloads, read as data. ElementTree does not fetch external entities, and expat >= 2.4 limits entity expansion.
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(f"{NS}si"):
            shared.append("".join(t.text or "" for t in si.iter(f"{NS}t")))
    sheet = sorted(n for n in z.namelist() if n.startswith("xl/worksheets/sheet"))[0]
    rows = []
    for r in ET.fromstring(z.read(sheet)).iter(f"{NS}row"):
        row = {}
        for c in r.findall(f"{NS}c"):
            col = re.match(r"[A-Z]+", c.get("r")).group(0)
            v = c.find(f"{NS}v")
            if c.get("t") == "s" and v is not None:
                row[col] = shared[int(v.text)]
            elif c.get("t") == "inlineStr":
                row[col] = "".join(x.text or "" for x in c.iter(f"{NS}t"))
            else:
                row[col] = v.text if v is not None else ""
        rows.append(row)
    return rows


def load_polls():
    polls, totals = [], {}
    for i in range(1, 88):
        rows = read_xlsx(SRC / f"ed{i:02d}.xlsx")
        m = re.match(r"(\d+) - (.+)", rows[2]["A"])
        num, name = int(m.group(1)), m.group(2).strip()
        assert num == i
        for r in rows:
            if r.get("C") == "Election Day":
                polls.append({"ed_num": num, "ed_name": name, "va": str(r["A"]).strip().zfill(3), "electors": int(float(r["D"]))})
            if str(r.get("A", "")).startswith("Total Valid Vote"):
                totals[num] = int(float(r["D"]))
    return pd.DataFrame(polls), totals


def division_rows(lab, electors):
    return pd.Series(electors).groupby(np.asarray(lab)).sum()


def spread(s):
    avg = s.mean()
    dev = 100 * (s / avg - 1)
    urban = s.index.str.startswith(("Calgary-", "Edmonton-"))
    return {"n": int(len(s)), "average": round(float(avg), 1), "beyond_25": {n: round(float(d), 1) for n, d in dev[dev.abs() > 25].items()},
            "within_10": int((dev.abs() <= 10).sum()), "mad": round(float((s - avg).abs().mean())),
            "mean_calgary_edmonton": round(float(s[urban].mean())), "mean_rest": round(float(s[~urban].mean())),
            "city_gap_pct": round(100 * float(s[urban].mean() / s[~urban].mean() - 1), 1)}


def corr(a, b):
    return round(float(np.corrcoef(a, b)[0, 1]), 4)


def main():
    polls, ed_total = load_polls()
    index = read_xlsx(SRC / "index.xlsx")
    prov = next(int(float(r["D"])) for r in index if str(r.get("A", "")).startswith("Total Valid Vote"))
    polls.to_csv(ROOT / "data/referendum/electors_by_va_2026.csv", index=False)

    z = "zip://" + str(VA_ZIP)
    va = gpd.read_file(z).to_crs(3400)
    va["key"] = va.ED_NUM.astype(int).astype(str) + ":" + va.VA_NUMBER.astype(str).str.strip().str.zfill(3)
    polls["key"] = polls.ed_num.astype(str) + ":" + polls.va
    name_ok = polls.merge(va[["key", "ED_NAME"]], on="key", how="left")
    same_name = (name_ok.ED_NAME.fillna("").str.upper().str.strip() == name_ok.ed_name.str.upper()).mean()
    merged = va.merge(polls[["key", "electors"]], on="key", how="left")
    unmatched_polls = polls[~polls.key.isin(va.key)]
    match = {"polls": int(len(polls)), "va_polygons": int(len(va)), "duplicate_va_keys": int(va.key.duplicated().sum()),
             "polls_matched": int(polls.key.isin(va.key).sum()),
             "electors_total": int(polls.electors.sum()), "province_total_stated": prov,
             "share_electors_matched": round(float(polls[polls.key.isin(va.key)].electors.sum() / polls.electors.sum()), 5),
             "share_names_agree": round(float(same_name), 5),
             "divisions_where_polls_differ_from_stated_total": [k for k, v in ed_total.items() if polls[polls.ed_num == k].electors.sum() != v],
             "unmatched_polls_sample": unmatched_polls.head(25)[["ed_name", "va", "electors"]].to_dict("records"),
             "polygons_without_a_poll": int(merged.electors.isna().sum())}
    print(json.dumps(match, indent=0)[:1400])
    out = {"plan": "preregistration/referendum_electors_check_2026-11-07.md", "match": match}
    if match["share_electors_matched"] < MIN_MATCH:
        out["stopped"] = "under 99% of electors matched: comparison unreliable"
        (HERE / "electors_check.json").write_text(json.dumps(out, indent=1), encoding="utf8")
        print(out["stopped"])
        return

    merged["electors"] = merged.electors.fillna(0.0)
    pts26 = merged[["geometry"]].copy()
    pts26["geometry"] = merged.geometry.representative_point()

    v23 = gpd.read_file(OVERLAY_VAS).to_crs(3400)
    pop = pd.read_csv(ROOT / "data/va_pop_from_das.csv").set_index("va_row_idx")["pop_2021"]
    v23["pop_2021"] = pd.Series(v23.index.map(pop).values).fillna(0.0).clip(lower=1.0).values
    pts23 = v23[["geometry"]].copy()
    pts23["geometry"] = v23.geometry.representative_point()

    stated = {"panel": pd.read_csv(ROOT / "data/iap/iap_app7_populations.csv").set_index("district").population}
    for k in ("majority", "minority"):
        m = gpd.read_file(MAPS[k][0], ignore_geometry=True)
        stated[k] = m.set_index("EDName2025").PopCensus

    table, out["maps"] = [], {}
    prov_ratio = merged.electors.sum() / 4888723.0
    for k, (f, col) in MAPS.items():
        eds = gpd.read_file(f).to_crs(3400)[[col, "geometry"]]
        j = gpd.sjoin(pts26, eds, how="left", predicate="within")
        j = j[~j.index.duplicated(keep="first")].reindex(pts26.index)
        unplaced = float(merged.electors[j[col].isna()].sum())
        e = merged.electors.groupby(j[col].fillna("__none__").values).sum().drop("__none__", errors="ignore")
        j23 = gpd.sjoin(pts23, eds, how="left", predicate="within")
        j23 = j23[~j23.index.duplicated(keep="first")].reindex(pts23.index)
        o = v23.pop_2021.groupby(j23[col].values).sum()
        block = {"electors_unplaced": unplaced, "electors": spread(e), "overlay_2021": spread(o)}
        if k in stated:
            s = stated[k].reindex(e.index)
            assert s.notna().all(), k
            urban = e.index.str.startswith(("Calgary-", "Edmonton-"))
            o2 = o.reindex(e.index)
            block["stated"] = spread(s)
            block["corr_electors_vs_stated"] = {"all": corr(e, s), "calgary_edmonton": corr(e[urban], s[urban]), "rest": corr(e[~urban], s[~urban])}
            block["corr_electors_vs_overlay_2021"] = {"all": corr(e, o2), "calgary_edmonton": corr(e[urban], o2[urban]), "rest": corr(e[~urban], o2[~urban])}
            # The maps were drawn to equalise the stated figures, so their spread inside each map is squeezed and
            # any correlation with them is depressed. These two checks do not lean on that spread.
            def miss(fig, mask):
                return round(100 * float((e[mask] / ((e.sum() / fig.sum()) * fig[mask]) - 1).abs().mean()), 1)
            block["range_check"] = {"sd_stated_cities": round(float(s[urban].std())), "sd_overlay_cities": round(float(o2[urban].std())),
                                    "sd_electors_cities": round(float(e[urban].std())),
                                    "mean_abs_pct_miss_stated": {"cities": miss(s, urban), "rest": miss(s, ~urban)},
                                    "mean_abs_pct_miss_overlay": {"cities": miss(o2, urban), "rest": miss(o2, ~urban)}}
            calgary = e.index.str.startswith("Calgary-")
            edmonton = e.index.str.startswith("Edmonton-")
            block["region_shares_pct"] = {lab: {"electors": round(100 * float(e[m].sum() / e.sum()), 1), "stated": round(100 * float(s[m].sum() / s.sum()), 1),
                                                "overlay_2021": round(100 * float(o2[m].sum() / o2.sum()), 1)}
                                          for lab, m in (("calgary", calgary), ("edmonton", edmonton), ("rest", ~urban))}
            ratio = e / s
            block["electors_per_stated_person"] = {"province": round(float(prov_ratio), 4), "min": round(float(ratio.min()), 4), "max": round(float(ratio.max()), 4)}
            block["lowest_ratio"] = {n: round(float(v), 3) for n, v in ratio.sort_values().head(8).items()}
            block["highest_ratio"] = {n: round(float(v), 3) for n, v in ratio.sort_values().tail(8).items()}
            block["named"] = {n: {"electors": round(float(e[n])), "stated": int(s[n]), "overlay_2021": round(float(o2[n])),
                                  "electors_per_stated": round(float(e[n] / s[n]), 3), "electors_per_overlay": round(float(e[n] / o2[n]), 3)}
                              for n in NAMED if n in e.index}
            for n in e.index:
                table.append({"map": k, "division": n, "electors_2026": round(float(e[n])), "stated_pop": int(s[n]), "overlay_2021": round(float(o2[n])),
                              "electors_per_stated": round(float(e[n] / s[n]), 3)})
        out["maps"][k] = block
    pd.DataFrame(table).to_csv(HERE / "division_table.csv", index=False)
    (HERE / "electors_check.json").write_text(json.dumps(out, indent=1, default=float), encoding="utf8")
    print(json.dumps(out["maps"], indent=0, default=float)[:7000])


if __name__ == "__main__":
    main()
