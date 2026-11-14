"""Tests that pin the headline numbers the reports quote to committed data.

Each test recomputes a published figure from a committed input (the raw
Elections Alberta workbook, the committed chains, the official boundary files)
or reads it from the committed output that the reports cite, and compares it
with the value as printed in reports/public/report_public.md and
reports/academic/report_academic.md. If a committed file or the code that reads
it changes so that a published number no longer follows, a test here fails.

Data availability. Some inputs are Git LFS objects (*.gpkg). In a clone that
has not run `git lfs pull` they are ~130-byte pointer files; the tests that
need them skip with a message naming the file. Nothing here needs the network
or random numbers. The whole file runs in about a minute and a half (most of
it reading the chains and the boundary files).

Run from the repo root:
    python -m pytest tests/test_published_numbers.py -v

Forward dependencies: none
Backward dependencies:
    data/raw/2023_results.xlsx, data/reference/alberta_2023_results.csv
    data/simulation_checkpoints_canonical/chain{0..3}_samples.csv
    data/outputs/simulated_ensemble_percentiles_canonical.csv
    data/outputs/simulation_real_map_scores_canonical.json
    findings/joint_outlier_score.json
    findings/audit_2026-11-10/{seat_counts_table,pct_rank_ties,ess_uncapped}.json
    data/reference/{majority,minority}_2026_populations.csv
    data/outputs/airdrie_split_shares_2026-10-31.json
    findings/a10_stepc/{verdict,structural}.json, findings/a10_stepc_replay/verdict.json
    data/shapefiles/** (LFS)
"""
from __future__ import annotations

import json
import math
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from lfs_guard import first_unavailable  # noqa: E402
from mcmc_ensemble import autocorrelation_ess, pct_rank, seat_results  # noqa: E402

# ── Committed inputs ─────────────────────────────────────────────────────────
WORKBOOK = ROOT / "data" / "raw" / "2023_results.xlsx"
RESULTS_CSV = ROOT / "data" / "reference" / "alberta_2023_results.csv"
CHAINS = [ROOT / "data" / "simulation_checkpoints_canonical" / f"chain{i}_samples.csv" for i in range(4)]
PCT_CSV = ROOT / "data" / "outputs" / "simulated_ensemble_percentiles_canonical.csv"
REAL_SCORES = ROOT / "data" / "outputs" / "simulation_real_map_scores_canonical.json"
JOINT_JSON = ROOT / "findings" / "joint_outlier_score.json"
AUDIT = ROOT / "findings" / "audit_2026-11-10"
SEAT_TABLE = AUDIT / "seat_counts_table.json"
TIES_JSON = AUDIT / "pct_rank_ties.json"
ESS_JSON = AUDIT / "ess_uncapped.json"
VA_EDAY = ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
VA_ALL = ROOT / "data" / "shapefiles" / "derived" / "va_polygons_all_2023_ballots_primary.gpkg"
MAJ_GPKG = ROOT / "data" / "shapefiles" / "canonical" / "ea_majority_2026_eds.gpkg"
MIN_GPKG = ROOT / "data" / "shapefiles" / "canonical" / "ea_minority_2026_eds.gpkg"
PANEL_CSV = ROOT / "findings" / "a10_stepb_run" / "va_assignment_real_map.csv"
PARA167_CSV = ROOT / "findings" / "iap_para167" / "va_assignment.csv"
AIRDRIE_JSON = ROOT / "data" / "outputs" / "airdrie_split_shares_2026-10-31.json"

PARTISAN = ["efficiency_gap", "mean_median", "declination", "seats_at_50_50"]

# ── The numbers as the reports print them ────────────────────────────────────
OFFICIAL_2023 = {"ucp": 928_900, "ndp": 777_404, "valid": 1_764_915, "ucp_seats": 49, "ndp_seats": 38}
N_PLANS = 1_010_000
# (value as printed, percentile as printed) for the two commission maps.
PUBLISHED = {
    "minority 2026 canonical": {
        "efficiency_gap": (0.0402, 94.54),
        "mean_median": (0.0104, 99.97),
        "declination": (0.0770, 98.79),
        "seats_at_50_50": (46 / 89, 99.99),
    },
    "majority 2026 canonical": {
        "efficiency_gap": (0.0010, 16.52),
        "mean_median": (-0.0362, 0.99),
        "declination": (-0.0267, 21.85),
        "seats_at_50_50": (41 / 89, 78.54),
    },
}
PLANS_AT_MINORITY_SEATS = 69          # "only 69 of 1,010,000"
D2_MINORITY = 33.64
D2_MAJORITY = 7.74
D2_2019 = 13.16
# UCP-NDP seats; (election day, all ballots, tied vote election day, tied vote all ballots)
SEAT_TABLE_PUBLISHED = {
    "map_2019": ((57, 30), (49, 38), 40, 41),
    "majority_2026": ((55, 34), (48, 41), 41, 42),
    "minority_2026": ((60, 29), (55, 34), 46, 46),
    "panel": ((58, 33), (51, 40), 44, 45),
    "para167": ((56, 35), (50, 41), 43, 44),
}


def _skip_unless(*paths):
    reason = first_unavailable(*paths)
    if reason:
        pytest.skip(reason)


# ── Loaders (cached: several tests share them) ───────────────────────────────

@lru_cache(maxsize=1)
def _workbook_totals() -> dict:
    """Province totals from the 'Total (All Voting Options)' row of each of the 87 sheets."""
    xl = pd.ExcelFile(WORKBOOK)
    party: dict[str, float] = {}
    valid = 0.0
    seats = {"UCP": 0, "NDP": 0}
    per_ed_candidates = {}
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, header=None)
        headers = df.iloc[0].tolist()
        row = next(r for _, r in df.iterrows() if "Total (All Voting Options)" in str(r.iloc[1]))
        valid += float(row.iloc[headers.index("Valid Ballots Cast")])
        ed = {}
        for i, h in enumerate(headers):
            if isinstance(h, str) and "\n" in h:
                p = h.split("\n")[-1].strip()
                party[p] = party.get(p, 0.0) + float(row.iloc[i])
                ed[p] = ed.get(p, 0.0) + float(row.iloc[i])
        seats[max(("UCP", "NDP"), key=lambda p: ed.get(p, 0.0))] += 1
        per_ed_candidates[sheet] = ed
    return {"n_sheets": len(xl.sheet_names), "party": party, "valid": valid, "seats": seats,
            "per_ed": per_ed_candidates}


@lru_cache(maxsize=1)
def _chains() -> pd.DataFrame:
    """The 1,010,000 committed plans, four chains in order. Read with the exact
    parser so k/n seat shares come back as written."""
    cols = PARTISAN + ["population_mad", "chain"]
    return pd.concat(
        [pd.read_csv(p, usecols=cols, float_precision="round_trip") for p in CHAINS],
        ignore_index=True,
    )


@lru_cache(maxsize=1)
def _pct_table() -> pd.DataFrame:
    return pd.read_csv(PCT_CSV).set_index(["metric", "map"])


@lru_cache(maxsize=1)
def _d2():
    """Mahalanobis D² of every plan and of the three real maps, built as
    joint_outlier_score_canonical.py builds it (sample mean and covariance of
    the four partisan metrics)."""
    X = _chains()[PARTISAN].to_numpy(float)
    mu = X.mean(axis=0)
    cinv = np.linalg.pinv(np.cov(X, rowvar=False))
    diffs = X - mu
    d2_all = np.einsum("ij,jk,ik->i", diffs, cinv, diffs)
    real = json.loads(REAL_SCORES.read_text(encoding="utf-8"))
    out = {}
    for key in ("minority_2026", "majority_2026", "2019_enacted"):
        obs = np.array([real[key][c] for c in PARTISAN]) - mu
        out[key] = float(obs @ cinv @ obs)
    return d2_all, out


# ── 1. Official 2023 totals, from the raw workbook ───────────────────────────

def test_official_2023_totals_from_workbook():
    """UCP 928,900, NDP 777,404, 1,764,915 valid votes, 49-38 seats."""
    _skip_unless(WORKBOOK)
    t = _workbook_totals()
    assert t["n_sheets"] == 87
    assert t["party"]["UCP"] == OFFICIAL_2023["ucp"]
    assert t["party"]["NDP"] == OFFICIAL_2023["ndp"]
    assert t["valid"] == OFFICIAL_2023["valid"]
    assert sum(t["party"].values()) == OFFICIAL_2023["valid"], "candidate columns must sum to valid ballots"
    assert t["seats"] == {"UCP": OFFICIAL_2023["ucp_seats"], "NDP": OFFICIAL_2023["ndp_seats"]}
    # two-party total and third-party total quoted in the academic report
    assert t["party"]["UCP"] + t["party"]["NDP"] == 1_706_304
    assert t["valid"] - t["party"]["UCP"] - t["party"]["NDP"] == 58_611


def test_results_csv_matches_workbook_except_three_communist_candidates():
    """The results CSV agrees with the workbook on every division's UCP, NDP and
    valid-vote totals. Its six candidate slots omit three Communist Party
    candidates (379 votes), so the candidate columns sum to 1,764,536; that
    omission is documented in data/reference/README.md and must not grow."""
    _skip_unless(WORKBOOK, RESULTS_CSV)
    t = _workbook_totals()
    csv = pd.read_csv(RESULTS_CSV, dtype={"sheet_num": str})
    assert len(csv) == 87
    assert int(csv["total_valid_votes"].sum()) == OFFICIAL_2023["valid"]
    vote_cols = [f"votes_{i}" for i in range(1, 7)]
    assert int(csv[vote_cols].sum().sum()) == OFFICIAL_2023["valid"] - 379
    assert t["party"]["CP-A"] == 379

    short = {}
    for _, r in csv.iterrows():
        ed = t["per_ed"][r["sheet_num"]]
        ucp = ndp = 0
        for i in range(1, 7):
            cand, v = r[f"cand_{i}"], r[f"votes_{i}"]
            if pd.isna(cand) or pd.isna(v):
                continue
            if str(cand).endswith("(UCP)"):
                ucp += int(v)
            elif str(cand).endswith("(NDP)"):
                ndp += int(v)
        assert ucp == ed["UCP"], r["ed_name"]
        assert ndp == ed["NDP"], r["ed_name"]
        gap = int(r["total_valid_votes"]) - int(sum(v for v in r[vote_cols] if pd.notna(v)))
        if gap:
            short[r["ed_name"]] = gap
    assert short == {"Calgary-East": 64, "Edmonton-Highlands-Norwood": 102, "Edmonton-Meadows": 213}


# ── 2. Partisan metrics and percentiles, from the committed chains ───────────

def test_ensemble_size():
    _skip_unless(*CHAINS)
    df = _chains()
    assert len(df) == N_PLANS
    assert df.groupby("chain").size().tolist() == [252_500] * 4
    assert not df[PARTISAN].isna().any().any()


@pytest.mark.parametrize("map_name", sorted(PUBLISHED))
@pytest.mark.parametrize("metric", PARTISAN)
def test_partisan_metric_and_percentile(map_name, metric):
    """Each commission map's four metrics and percentiles: the committed table
    matches a recomputation from the chains, and both match the reports."""
    _skip_unless(*CHAINS, PCT_CSV)
    row = _pct_table().loc[(metric, map_name)]
    printed_value, printed_pct = PUBLISHED[map_name][metric]

    # the value the reports print
    assert row["value"] == pytest.approx(printed_value, abs=5e-5)
    # the percentile, recomputed from the chains, against the committed table ...
    recomputed = pct_rank(_chains()[metric].to_numpy(), float(row["value"]))
    assert recomputed == pytest.approx(row["percentile"], abs=1e-6)
    # ... and against the report, at the two decimals it prints
    assert round(recomputed, 2) == pytest.approx(printed_pct, abs=1e-9)


def test_real_map_metrics_recompute_from_official_boundaries():
    """The four metrics of both commission maps, recomputed from the official
    boundary files and the election-day vote file, equal the committed table."""
    _skip_unless(VA_EDAY, MAJ_GPKG, MIN_GPKG, PCT_CSV)
    import geopandas as gpd

    va = gpd.read_file(VA_EDAY)
    pts = gpd.GeoDataFrame(
        {"ucp": va["va_ucp"].fillna(0.0), "ndp": va["va_ndp"].fillna(0.0)},
        geometry=va.geometry.representative_point(), crs=va.crs,
    )
    for gpkg, map_name in ((MAJ_GPKG, "majority 2026 canonical"), (MIN_GPKG, "minority 2026 canonical")):
        ed = gpd.read_file(gpkg)[["EDName2025", "geometry"]].to_crs(va.crs)
        j = gpd.sjoin(pts, ed, predicate="within", how="left")
        assert j["EDName2025"].notna().all() and not j.index.duplicated().any()
        agg = j.groupby("EDName2025")[["ucp", "ndp"]].sum()
        assert len(agg) == 89
        m = seat_results(agg["ucp"].to_numpy(), agg["ndp"].to_numpy())
        for metric in PARTISAN:
            assert m[metric] == pytest.approx(_pct_table().loc[(metric, map_name), "value"], abs=1e-12), (
                map_name, metric)


def test_69_plans_reach_the_minority_seat_share():
    """'Only 69 of 1,010,000' neutral plans reach the minority's seats at a tied
    vote: 69 plans sit at 45/87, the ensemble maximum, and none above. The
    minority's 46/89 lies just below 45/87, so those 69 are the plans at or
    beyond it."""
    _skip_unless(*CHAINS)
    s = _chains()["seats_at_50_50"].to_numpy()
    assert int(np.isclose(s, 45 / 87, atol=1e-9).sum()) == PLANS_AT_MINORITY_SEATS
    assert s.max() == pytest.approx(45 / 87, abs=1e-12)
    assert int((s >= 46 / 89 - 1e-9).sum()) == PLANS_AT_MINORITY_SEATS
    assert 100.0 * (N_PLANS - PLANS_AT_MINORITY_SEATS) / N_PLANS == pytest.approx(99.99317, abs=1e-5)
    # neutral envelope high quoted in the public report: 51.72%
    assert round(100 * s.max(), 2) == 51.72


def test_2019_seats_percentile_is_a_midrank():
    """The 2019 map's 40/87 is shared by 266,278 plans. Its midrank percentile
    is 65.36 (findings/audit_2026-11-10/pct_rank_ties.json). The committed
    percentile table still carries 78.54, the share at or below, written before
    pct_rank counted near-equal values as ties; that cell needs a rerun of
    mcmc_ensemble_canonical.py. This test pins the midrank and accepts either
    value in the table, so it passes before and after that rerun and fails on
    anything else."""
    _skip_unless(*CHAINS, PCT_CSV, TIES_JSON)
    ties = json.loads(TIES_JSON.read_text(encoding="utf-8"))["summary"]
    s = _chains()["seats_at_50_50"].to_numpy()
    assert int(np.isclose(s, 40 / 87, atol=1e-9).sum()) == ties["seats_2019_plans_tied"] == 266_278
    mid = pct_rank(s, 40 / 87)
    assert mid == pytest.approx(ties["seats_2019_tie_aware_midrank"], abs=1e-4)
    assert round(mid, 2) == 65.36
    table = float(_pct_table().loc[("seats_at_50_50", "2019 enacted"), "percentile"])
    assert table == pytest.approx(78.5384, abs=1e-3) or table == pytest.approx(mid, abs=1e-3)
    assert ties["only_2019_seats_changes"] is True


def test_every_other_percentile_in_the_table_recomputes():
    """All committed partisan and population-MAD percentiles recompute from the
    chains with the tie-tolerant pct_rank, except the 2019 seats cell above."""
    _skip_unless(*CHAINS, PCT_CSV)
    df = _chains()
    checked = 0
    for (metric, map_name), row in _pct_table().iterrows():
        if metric not in PARTISAN + ["population_mad"] or pd.isna(row["value"]):
            continue
        if (metric, map_name) == ("seats_at_50_50", "2019 enacted"):
            continue
        assert pct_rank(df[metric].to_numpy(), float(row["value"])) == pytest.approx(
            row["percentile"], abs=1e-6), (metric, map_name)
        checked += 1
    assert checked == 13


# ── 3. The joint distance ────────────────────────────────────────────────────

def test_joint_distance_d2():
    """D² = 33.64 for the minority map, 7.74 for the majority, 13.16 for 2019;
    no sampled plan reaches the minority's (largest sampled D² 28.43)."""
    _skip_unless(*CHAINS, REAL_SCORES, JOINT_JSON)
    d2_all, d2 = _d2()
    assert round(d2["minority_2026"], 2) == D2_MINORITY
    assert round(d2["majority_2026"], 2) == D2_MAJORITY
    assert round(d2["2019_enacted"], 2) == D2_2019
    assert round(float(d2_all.max()), 2) == 28.43
    assert int((d2_all >= d2["minority_2026"]).sum()) == 0
    assert int((d2_all >= d2["majority_2026"]).sum()) == 102_111
    assert int((d2_all >= d2["2019_enacted"]).sum()) == 12_370

    committed = json.loads(JOINT_JSON.read_text(encoding="utf-8"))["maps"]
    assert committed["minority"]["mahalanobis_distance"] == pytest.approx(math.sqrt(d2["minority_2026"]), abs=5e-5)
    assert committed["majority"]["mahalanobis_distance"] == pytest.approx(math.sqrt(d2["majority_2026"]), abs=5e-5)


def test_joint_model_probability():
    """The chi-square(4) tail at D² = 33.64 is about 8.84e-07; doubled, about
    1.77e-06, which is 1 in about 566,000 (the reports' '1 in 568,000' comes
    from rounding the doubled p to 1.76e-06 first)."""
    _skip_unless(*CHAINS, REAL_SCORES, JOINT_JSON)
    _, d2 = _d2()
    x = d2["minority_2026"]
    p = math.exp(-x / 2.0) * (1.0 + x / 2.0)  # chi-square survival function, 4 degrees of freedom
    assert p == pytest.approx(8.84e-7, rel=2e-3)
    assert 2 * p == pytest.approx(1.77e-6, rel=3e-3)
    assert round(1 / (2 * p), -3) == 566_000
    committed = json.loads(JOINT_JSON.read_text(encoding="utf-8"))
    assert committed["maps"]["minority"]["joint_partisan_p"] == pytest.approx(p, rel=5e-3)
    # The headline doubles the unrounded p: 1 in 565,691 (joint_sensitivity.json: one_in_doubled).
    assert committed["joint_headline"]["one_in"] == 565_691
    assert committed["joint_headline"]["p_doubled_model_estimate"] == pytest.approx(2 * p, rel=1e-3)


def test_effective_sample_size_published_and_uncapped():
    """The published pooled ESS (1,413 to 1,522) is the lag-capped estimate and
    the cap binds; with no cap it is about 1,000 (894 to 1,250)."""
    _skip_unless(*CHAINS, ESS_JSON)
    committed = json.loads(ESS_JSON.read_text(encoding="utf-8"))["metrics"]
    published = {"efficiency_gap": 1522, "mean_median": 1448, "declination": 1513, "seats_at_50_50": 1413}
    uncapped = {"efficiency_gap": 1037, "mean_median": 1250, "declination": 1039, "seats_at_50_50": 894}
    df = _chains()
    for metric in PARTISAN:
        x = df[metric].to_numpy()
        capped = autocorrelation_ess(x)
        assert capped["cap_bound"] is True, metric
        assert round(capped["n_eff"]) == published[metric]
        free = autocorrelation_ess(x, uncapped=True)
        assert free["cap_bound"] is False
        assert round(free["n_eff"]) == uncapped[metric]
        assert free["n_eff"] == pytest.approx(committed[metric]["pooled_chains_joined"]["uncapped"]["ess"], abs=0.06)
        assert free["n_eff"] < capped["n_eff"]


# ── 4. The seat-count table ──────────────────────────────────────────────────

def _seats(ucp, ndp):
    ucp, ndp = np.asarray(ucp, float), np.asarray(ndp, float)
    return int((ucp > ndp).sum()), int((ndp > ucp).sum()), seat_results(ucp, ndp)["seats_at_50_50"] * len(ucp)


def test_seat_counts_table_committed_matches_reports():
    """findings/audit_2026-11-10/seat_counts_table.json holds the counts the reports print."""
    _skip_unless(SEAT_TABLE)
    table = json.loads(SEAT_TABLE.read_text(encoding="utf-8"))["table"]
    for key, (eday, allb, tied_eday, tied_all) in SEAT_TABLE_PUBLISHED.items():
        e, a = table["election_day"][key], table["all_ballots"][key]
        assert (e["ucp_seats"], e["ndp_seats"]) == eday, key
        assert (a["ucp_seats"], a["ndp_seats"]) == allb, key
        assert e["ucp_seats_at_tied_vote"] == tied_eday, key
        assert a["ucp_seats_at_tied_vote"] == tied_all, key
    # the 2019 map on all ballots is the official 2023 result
    assert SEAT_TABLE_PUBLISHED["map_2019"][1] == (OFFICIAL_2023["ucp_seats"], OFFICIAL_2023["ndp_seats"])


def test_seat_counts_table_recomputes():
    """Every cell of the seat-count table, recomputed from the vote files and
    the five maps' voting-area assignments."""
    _skip_unless(SEAT_TABLE, VA_EDAY, VA_ALL, MAJ_GPKG, MIN_GPKG, PANEL_CSV, PARA167_CSV)
    import geopandas as gpd

    table = json.loads(SEAT_TABLE.read_text(encoding="utf-8"))
    panel = pd.read_csv(PANEL_CSV, dtype={"VA_NUMBER": str})
    p167 = pd.read_csv(PARA167_CSV)
    eds = {k: gpd.read_file(p)[["EDName2025", "geometry"]] for k, p in
           (("majority_2026", MAJ_GPKG), ("minority_2026", MIN_GPKG))}

    for vkey, vpath in (("election_day", VA_EDAY), ("all_ballots", VA_ALL)):
        va = gpd.read_file(vpath)
        assert len(va) == 4765 == len(panel) == len(p167)
        assert (va["OBJECTID"].values == panel["OBJECTID"].values).all()
        assert (p167["va_index"].values == np.arange(4765)).all()
        totals = table["checks"][vkey]
        assert float(va["va_ucp"].sum()) == pytest.approx(totals["province_ucp"], abs=1e-3)
        assert float(va["va_ndp"].sum()) == pytest.approx(totals["province_ndp"], abs=1e-3)

        pts = gpd.GeoDataFrame(geometry=va.geometry.representative_point(), crs=va.crs)
        assign = {"map_2019": va["parent_ed_2019"].values,
                  "panel": panel["district"].values,
                  "para167": p167["district"].values}
        for key, ed in eds.items():
            j = gpd.sjoin(pts, ed.to_crs(va.crs), predicate="within", how="left")
            assert j["EDName2025"].notna().all() and not j.index.duplicated().any()
            assign[key] = j["EDName2025"].reindex(pts.index).values

        for key, districts in assign.items():
            d = pd.DataFrame({"d": districts, "ucp": va["va_ucp"].values, "ndp": va["va_ndp"].values}).groupby("d").sum()
            ucp_seats, ndp_seats, tied = _seats(d["ucp"].values, d["ndp"].values)
            want = table["table"][vkey][key]
            assert len(d) == want["n_districts"], (vkey, key)
            assert (ucp_seats, ndp_seats) == (want["ucp_seats"], want["ndp_seats"]), (vkey, key)
            assert tied == pytest.approx(want["ucp_seats_at_tied_vote"], abs=1e-9), (vkey, key)

    # all ballots add up to the official province totals
    assert table["checks"]["all_ballots"]["province_ucp"] == OFFICIAL_2023["ucp"]
    assert table["checks"]["all_ballots"]["province_ndp"] == OFFICIAL_2023["ndp"]
    assert table["checks"]["all_ballots"]["province_all_parties"] == OFFICIAL_2023["valid"]


# ── 5. Structural values ─────────────────────────────────────────────────────

def test_population_spread_from_commission_tables():
    """Mean absolute deviation from the provincial average of 54,929: 4,707
    (minority) against 3,180 (majority), 48% wider, from the commission's own
    population tables (findings/population_equality.md, section A1)."""
    pops = {key: pd.read_csv(ROOT / "data" / "reference" / f"{key}_2026_populations.csv")["population"]
            for key in ("majority", "minority")}
    assert all(len(p) == 89 for p in pops.values())
    assert int(pops["majority"].sum()) == 4_888_723
    assert int(pops["minority"].sum()) == 4_888_773  # the printed table's Calgary-Varsity is 50 higher
    average = round(4_888_723 / 89)
    assert average == 54_929
    mad = {key: float((p - average).abs().mean()) for key, p in pops.items()}
    assert round(mad["minority"]) == 4707
    assert round(mad["majority"]) == 3180
    assert round(100 * (mad["minority"] / mad["majority"] - 1)) == 48

    # the figure script builds its panel from the same tables
    import article_figures

    fig = article_figures.commission_table_mad()
    assert fig["provincial_average"] == average
    assert (round(fig["majority"]), round(fig["minority"]), round(fig["pct_wider"])) == (3180, 4707, 48)
    air = article_figures.airdrie_district_counts()
    assert (air["majority"], air["minority"], air["minority_smallest_piece"]) == (2, 4, 351)


def test_population_medad_and_percentile():
    """Median absolute deviation on the official boundary files, 3,938 against
    2,827; the minority's sits at the 99th percentile of the ensemble."""
    _skip_unless(*CHAINS, PCT_CSV)
    t = _pct_table()
    mn = t.loc[("population_mad", "minority 2026 canonical")]
    mj = t.loc[("population_mad", "majority 2026 canonical")]
    assert round(mn["value"]) == 3938 and round(mj["value"]) == 2827
    mad = _chains()["population_mad"].to_numpy()
    assert round(pct_rank(mad, float(mn["value"])), 1) == 99.1
    assert round(pct_rank(mad, float(mj["value"])), 1) == 15.9


def test_airdrie_shares():
    """Airdrie: four districts on the minority map, three holding 2% or more of
    its people; Airdrie East holds 54.7% of the city and is nine-tenths
    Airdrie; the north piece holds about 350 people. Two districts on the
    majority map."""
    d = json.loads(AIRDRIE_JSON.read_text(encoding="utf-8"))["maps"]
    mn, mj = d["minority"], d["majority"]
    assert mn["districts_with_any_airdrie_residents"] == 4
    assert mn["districts_holding_2pct_or_more"] == 3
    assert mn["districts_where_airdrie_is_a_majority"] == ["Airdrie-East"]
    by = {r["district"]: r for r in mn["districts"]}
    assert round(100 * by["Airdrie-East"]["share_of_airdrie_held"], 1) == 54.7
    assert round(100 * by["Airdrie-East"]["share_of_district_airdrie"]) == 90
    assert round(by["Olds-Three Hills-Didsbury"]["airdrie_residents"], -1) == 350
    assert sum(r["share_of_airdrie_held"] for r in mn["districts"]) == pytest.approx(1.0, abs=2e-4)
    assert mj["districts_with_any_airdrie_residents"] == 2
    assert mj["districts_holding_2pct_or_more"] == 2
    assert sorted(mj["districts_where_airdrie_is_a_majority"]) == ["Airdrie-East", "Airdrie-West"]


# ── 6. The Step C scorecard (the panel's map) ────────────────────────────────

@pytest.mark.parametrize("folder", ["a10_stepc", "a10_stepc_replay"])
def test_stepc_scorecard_counts(folder):
    """Structural half 2 of 5 flags, partisan half 1 of 4; seats at a tied vote
    at the 98.8th percentile. Same counts in the replay."""
    v = json.loads((ROOT / "findings" / folder / "verdict.json").read_text(encoding="utf-8"))
    assert v["structural_lane_flags"] == 2
    assert v["structural_verdict"] == "not_replicated"
    assert v["partisan_detail"]["n_flags"] == 1
    assert v["partisan_verdict"] == "absent"
    flags = v["partisan_detail"]["flags"]
    assert sum(bool(f) for f in flags.values()) == 1 and flags["P4_S50"] is True
    assert round(100 * v["partisan_detail"]["ucp_direction_percentiles"]["seats_at_50_50"], 1) == 98.8


def test_stepc_structural_flags_add_up():
    """The 2-of-5 count is the number of flagged structural metrics, with S4
    measured but excluded from the count."""
    s = json.loads((ROOT / "findings" / "a10_stepc" / "structural.json").read_text(encoding="utf-8"))
    m = s["metrics"]
    counted = [k for k, v in m.items() if not v.get("non_discriminating")]
    assert len(counted) == 5
    assert sum(bool(m[k]["flag"]) for k in counted) == s["structural_lane_flags"] == 2
    assert [k for k in counted if m[k]["flag"]] == ["S1_population_mad", "S3_anchoring_score"]
