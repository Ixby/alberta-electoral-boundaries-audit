"""
simulate_338.py -- 338Canada's Oct 19, 2026 Alberta riding projections, re-run on each candidate map.

What it does (plain terms)
  1. Rebuild 2023 votes by voting area (VA) on ALL ballots, the audit's Amendment 12 substrate, in
     memory (same rule as the audit's analysis/scripts/vote_anywhere_splat.py), and check it equals
     the official 2023 result in all 87 districts.
  2. Re-score 2023 on every map and check the audit's published all-ballots numbers come back.
  3. Move each VA from its 2023 shares toward 338's projection for its 2019 district
     (proportional swing, the main method; additive swing as a check).
  4. Check that re-adding VAs into the 2019 districts gives 338's own riding leaders.
  5. Add the VAs up into each map's districts: seats, close seats, seats at 50/50, and the
     provincial lead each party needs for a majority.
  6. Monte Carlo: one province-wide swing per draw plus riding noise, the SAME draws on every map.

Inputs are read in place from the audit repo (paths in INP below; the SHA-256 of each, as first
run at commit 557d11fe, is in input_sha256.txt), plus the 338 snapshot in
evidence/projections/338canada_2026-10-19/ridings_2026-10-19.csv.
Writes only to ./out/.

Run from anywhere: python3 -I -W ignore findings/p338_projection/simulate_338.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyogrio

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
INP = {  # name in input_sha256.txt -> repo path
    "polls_2023_unified.csv": "data/outputs/polls_2023_unified.csv",
    "alberta_2023_results.csv": "data/reference/alberta_2023_results.csv",
    "assignment_va_to_2026_canonical.csv": "data/outputs/assignment_va_to_2026_canonical.csv",
    "panel_assignment_nodes_a10_stepc_replay.csv": "findings/a10_stepc_replay/assignment_nodes.csv",
    "para167_va_assignment.csv": "findings/iap_para167/va_assignment.csv",
    "real_maps_all_ballots.json": "findings/allballots_ranking/real_maps_all_ballots.json",
    "para167_real_maps_all_ballots.json": "findings/iap_para167/real_maps_all_ballots.json",
    "va_polygons_with_full_2023_votes.gpkg": "data/shapefiles/derived/va_polygons_with_full_2023_votes.gpkg",
}
INP = {k: REPO / v for k, v in INP.items()}
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
P338 = REPO / "evidence/projections/338canada_2026-10-19/ridings_2026-10-19.csv"

SEED = 20261019
N_DRAWS = 5000
CHUNK = 500
Z90 = 1.6449            # a 90% interval is +/- 1.645 standard deviations
PROV_HALF = 5.0         # 338 provincial range: UCP 48 +/- 5, NDP 43 +/- 5
FLOOR = 0.005           # no party's riding target goes below 0.5% in a draw
CAL_ITERS = 20          # passes of scale-and-renormalise (converges to ~1e-13 in about 10)
PARTIES = ["ucp", "ndp", "other"]

MAPS = {  # key: (label, seats)
    "map2019": ("2019 enacted map", 87),
    "majority": ("Commission majority 2026", 89),
    "minority": ("Commission minority 2026", 89),
    "panel": ("Advisory panel (reconstruction)", 91),
    "para167": ("Panel minority ¶167 (reconstruction)", 91),
}


def need(n):
    return n // 2 + 1


# ---------------------------------------------------------------------------------------------
# 1. 2023 all-ballots votes by VA (in memory; same rule as vote_anywhere_splat.py)
# ---------------------------------------------------------------------------------------------
def load_votes():
    va = pyogrio.read_dataframe(INP["va_polygons_with_full_2023_votes.gpkg"], read_geometry=False)
    assert (va.OBJECTID.values == np.arange(1, len(va) + 1)).all()
    polls = pd.read_csv(INP["polls_2023_unified.csv"], dtype={"sheet_num": str, "voting_areas": str},
                        encoding="cp1252")
    cols = {"ucp": "ucp_votes", "ndp": "ndp_votes", "other": "other_votes"}
    for c in cols.values():
        polls[c] = pd.to_numeric(polls[c], errors="coerce").fillna(0)
    anywhere = polls[polls.poll_name.str.contains("Vote Anywhere", na=False, case=False)]
    add = anywhere.groupby("ed_2019")[list(cols.values())].sum()
    w = va.va_ucp + va.va_ndp
    tot = w.groupby(va.parent_ed_2019).transform("sum")
    n = va.groupby("parent_ed_2019").va_ucp.transform("size")
    share = (w / tot).where(tot > 0, 1.0 / n)
    for p, c in cols.items():
        va[p] = va[f"va_{p}_full"] + share * va.parent_ed_2019.map(add[c]).fillna(0.0)

    off = pd.read_csv(INP["alberta_2023_results.csv"]).set_index("ed_name")

    def party(r, p):
        for i in range(1, 7):
            c = r.get(f"cand_{i}")
            if isinstance(c, str) and c.endswith(f"({p})"):
                return r[f"votes_{i}"]
        return 0

    o = pd.DataFrame(index=off.index)
    o["ucp"] = off.apply(lambda r: party(r, "UCP"), axis=1)
    o["ndp"] = off.apply(lambda r: party(r, "NDP"), axis=1)
    o["other"] = off.total_valid_votes - o.ucp - o.ndp
    got = va.groupby("parent_ed_2019")[PARTIES].sum()
    maxdiff = float((got - o.reindex(got.index)).abs().max().max())
    assert len(got) == 87 and maxdiff < 0.5, maxdiff
    return va, off, {"districts": 87, "max_abs_diff_votes": maxdiff,
                     "province": {p: float(got[p].sum()) for p in PARTIES}}


# ---------------------------------------------------------------------------------------------
# 2. Map assignments (VA row -> district) and the 2023 reproduction
# ---------------------------------------------------------------------------------------------
def load_maps(va):
    cn = pd.read_csv(INP["assignment_va_to_2026_canonical.csv"])
    assert (cn.OBJECTID.values == va.OBJECTID.values).all()
    pan = pd.read_csv(INP["panel_assignment_nodes_a10_stepc_replay.csv"])   # representative-point
    assert (pan.node.values == np.arange(len(va))).all()                    # assignment, as scored
    par = pd.read_csv(INP["para167_va_assignment.csv"])
    assert (par.va_index.values == np.arange(len(va))).all()
    lab = {"map2019": va.parent_ed_2019.values, "majority": cn.ed_2026_maj.values,
           "minority": cn.ed_2026_min.values, "panel": pan.district.values, "para167": par.district.values}
    out = {}
    for k, a in lab.items():
        names = np.array(sorted(set(a)))
        idx = pd.Index(names).get_indexer(a)
        assert (idx >= 0).all() and len(names) == MAPS[k][1], (k, len(names))
        H = np.zeros((len(va), len(names)))
        H[np.arange(len(va)), idx] = 1.0
        out[k] = {"names": names, "idx": idx, "H": H}
    return out


def tally(U, N, O):
    """Seat results from district totals (arrays). Ties are ties. Margins as the audit defines them:
    |UCP - NDP| / (UCP + NDP), two-party, close if <= 2 or 4 points."""
    U, N, O = (np.asarray(x, float) for x in (U, N, O))
    tol = 1e-9 * (U + N)
    ucp = U > N + tol
    ndp = N > U + tol
    tie = ~ucp & ~ndp
    assert (O < np.maximum(U, N)).all(), "an 'other' total beat both main parties"
    gap = np.abs(U - N) / (U + N)
    sh = U / (U + N)
    sw = 0.5 - U.sum() / (U + N).sum()
    s = sh + sw
    s50 = float((s > 0.5 + 1e-9).sum() + 0.5 * (np.abs(s - 0.5) <= 1e-9).sum())
    n = len(U)
    return {"n": n, "need": need(n), "ucp": int(ucp.sum()), "ndp": int(ndp.sum()), "tie": int(tie.sum()),
            "close2": int((gap <= 0.02).sum()), "close4": int((gap <= 0.04).sum()),
            "seats_at_50_50_ucp": s50, "seats_at_50_50_share": s50 / n}


def check_2023(va, maps):
    ref = json.loads((INP["real_maps_all_ballots.json"]).read_text())
    ref_p = json.loads((INP["para167_real_maps_all_ballots.json"]).read_text())
    refkey = {"map2019": (ref, "2019_enacted"), "majority": (ref, "majority_2026"),
              "minority": (ref, "minority_2026"), "panel": (ref, "iap_2026_assembled"),
              "para167": (ref_p, "para167_map")}
    V = va[PARTIES].to_numpy()
    res = {}
    for k, m in maps.items():
        D = V.T @ m["H"]
        t = tally(*D)
        r = refkey[k][0][refkey[k][1]]
        ok = (t["ucp"] == r["ucp_seats"] and t["close2"] == r["close2"] and t["close4"] == r["close4"]
              and abs(t["seats_at_50_50_share"] - r["seats_at_50_50"]) < 1e-12)
        res[k] = {"ours": t, "audit": {x: r[x] for x in ("ucp_seats", "close2", "close4", "seats_at_50_50")},
                  "match": bool(ok)}
    return res


# ---------------------------------------------------------------------------------------------
# 3. 338 projections, matched to Elections Alberta names
# ---------------------------------------------------------------------------------------------
def load_338(names2019, off):
    p = pd.read_csv(P338)
    fix = {"Livingston-Macleod": "Livingstone-Macleod",
           "Vermillion-Lloydminster-Wainwright": "Vermilion-Lloydminster-Wainwright"}
    norm = lambda s: re.sub(r"[^a-z]", "", s.lower())
    en = {norm(x): x for x in names2019}
    p["ea"] = [en[norm(fix.get(x, x))] for x in p.name]
    assert p.ea.is_unique and len(p) == 87
    p = p.set_index("ea").loc[names2019]
    # name-match check: 338's 2023 winner and winner % against the official result
    w = off.loc[names2019]
    bad = [(n, a, b) for n, a, b in zip(names2019, p.winner2023, w.winner_party) if a != b]
    pct = float(np.abs(p.winner2023_pct.values - w.winner_pct.values).max())
    return p, {"winner_mismatch": bad, "max_winner_pct_diff": pct}


# ---------------------------------------------------------------------------------------------
# 4. Swing models
# ---------------------------------------------------------------------------------------------
class Swing:
    """VA shares moved from 2023 toward riding targets on the 2019 map. Weights = 2023 VA totals."""

    def __init__(self, va, m2019):
        V = va[PARTIES].to_numpy()
        self.T = V.sum(1)
        self.di = m2019["idx"]
        self.H = m2019["H"]
        S = V.T @ self.H                       # (3, 87) district totals
        self.Dtot = S.sum(0)
        self.S23 = (S / self.Dtot).T           # (87, 3) 2023 district shares
        sh = np.where(self.T[:, None] > 0, V / np.maximum(self.T, 1e-12)[:, None], self.S23[self.di])
        # A party with no 2023 vote in a district starts at the same tiny share in every VA,
        # so scaling spreads its projected vote evenly across the district.
        Z = self.S23 == 0
        self.zero_party = [(i, PARTIES[j]) for i, j in zip(*np.where(Z))]
        sh = np.where(Z[self.di], 1e-4, sh)
        self.sh = sh / sh.sum(1, keepdims=True)
        self.Sb = self._agg(self.sh[None])[0]  # baseline district shares (= S23 up to the 1e-4 start)

    def _agg(self, x):
        """x (B, V, 3) VA shares -> (B, 87, 3) district shares on the 2019 map."""
        B = x.shape[0]
        Y = (x * self.T[None, :, None]).transpose(0, 2, 1).reshape(B * 3, -1) @ self.H
        Y = Y.reshape(B, 3, -1).transpose(0, 2, 1)
        return Y / Y.sum(2, keepdims=True)

    def proportional(self, P, iters=CAL_ITERS):
        """P (B, 87, 3) targets. Scale each party's VA share by target/2023, renormalise; repeat the
        scaling (iters passes) until the district totals equal the targets. iters=1 is one pass."""
        m = P / self.Sb[None]
        for i in range(iters):
            x = self.sh[None] * m[:, self.di, :]
            x /= x.sum(2, keepdims=True)
            if i < iters - 1:
                m *= P / self._agg(x)
        return x

    def additive(self, P):
        """Add the district's change in points to each VA, clip at 0, renormalise (one pass)."""
        x = np.clip(self.sh[None] + (P - self.Sb[None])[:, self.di, :], 0, None)
        clipped = float((self.sh[None] + (P - self.Sb[None])[:, self.di, :] < 0).any(2).mean())
        return x / x.sum(2, keepdims=True), clipped


def to_map(x, T, H):
    """(B, V, 3) VA shares -> (B, 3, k) district votes on a map."""
    B = x.shape[0]
    return ((x * T[None, :, None]).transpose(0, 2, 1).reshape(B * 3, -1) @ H).reshape(B, 3, -1)


def seats_batch(Y, n):
    U, N, O = Y[:, 0], Y[:, 1], Y[:, 2]
    tol = 1e-9 * (U + N)
    u = U > N + tol
    d = N > U + tol
    other_beats = int((O >= np.maximum(U, N)).sum())
    return u, d, other_beats


# ---------------------------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------------------------
def main():
    res = {"seed": SEED, "n_draws": N_DRAWS}
    va, off, splat = load_votes()
    res["substrate_check"] = splat
    maps = load_maps(va)
    res["check_2023"] = check_2023(va, maps)
    assert all(v["match"] for v in res["check_2023"].values()), res["check_2023"]

    names19 = maps["map2019"]["names"]
    p338, namecheck = load_338(names19, off)
    res["name_check"] = namecheck
    P = np.c_[p338.UCP, p338.NDP, 100 - p338.UCP - p338.NDP] / 100.0     # (87, 3) point targets
    sw = Swing(va, maps["map2019"])
    res["zero_2023_party_districts"] = [(names19[i], p) for i, p in sw.zero_party]
    T = sw.T

    # ---- point projection --------------------------------------------------------------------
    x_prop = sw.proportional(P[None])
    x_one = sw.proportional(P[None], iters=1)
    x_add, clip0 = sw.additive(P[None])
    A = {"prop": sw._agg(x_prop)[0], "one": sw._agg(x_one)[0], "add": sw._agg(x_add)[0]}

    def leaders(S):
        d = np.round((S[:, 0] - S[:, 1]) * 1e9)
        return np.sign(d)

    L338 = leaders(P)
    chk = {"338_points": {"UCP": int((L338 > 0).sum()), "NDP": int((L338 < 0).sum()), "tie": int((L338 == 0).sum())}}
    for k, S in A.items():
        l = leaders(S)
        chk[k] = {"UCP": int((l > 0).sum()), "NDP": int((l < 0).sum()), "tie": int((l == 0).sum()),
                  "max_abs_dev_pts": float(np.abs(S - P).max() * 100),
                  "mean_abs_dev_pts": float(np.abs(S - P).mean() * 100),
                  "leader_changes": [{"district": names19[i], "338": (P[i] * 100).round(2).tolist(),
                                      "model": (S[i] * 100).round(2).tolist()} for i in np.where(l != L338)[0]]}
    chk["additive_clipped_va_share"] = clip0
    res["check_338"] = chk
    assert chk["prop"]["leader_changes"] == [] and chk["add"]["leader_changes"] == []

    # provincial totals implied by the projection with 2023 turnout
    Yp = to_map(x_prop, T, maps["map2019"]["H"])[0]
    prov = Yp.sum(1) / Yp.sum()
    res["province_projected_pct"] = dict(zip(PARTIES, (prov * 100).round(2).tolist()))
    base_lead = (prov[0] - prov[1]) * 100

    point = {}
    district_tables = {}
    for k, m in maps.items():
        Yp = to_map(x_prop, T, m["H"])[0]
        Ya = to_map(x_add, T, m["H"])[0]
        tp, ta = tally(*Yp), tally(*Ya)
        point[k] = {"proportional": tp, "additive": ta}
        Y23 = va[PARTIES].to_numpy().T @ m["H"]
        df = pd.DataFrame({"district": m["names"], "n_vas": m["H"].sum(0).astype(int),
                           "votes_2023": Y23.sum(0).round(1)})
        for j, p in enumerate(PARTIES):
            df[f"{p}_2023_pct"] = (100 * Y23[j] / Y23.sum(0)).round(2)
        df["winner_2023"] = np.where(Y23[0] > Y23[1], "UCP", "NDP")
        for j, p in enumerate(PARTIES):
            df[f"{p}_proj_pct"] = (100 * Yp[j] / Yp.sum(0)).round(2)
        g = Yp[0] - Yp[1]
        tie = np.abs(g) <= 1e-9 * (Yp[0] + Yp[1])
        df["winner_proj"] = np.where(tie, "TIE", np.where(g > 0, "UCP", "NDP"))
        df["ucp_minus_ndp_pts_allvotes"] = (100 * g / Yp.sum(0)).round(2)
        df["ucp_minus_ndp_pts_twoparty"] = (100 * g / (Yp[0] + Yp[1])).round(2)
        df["close4"] = np.abs(g) / (Yp[0] + Yp[1]) <= 0.04
        df["close2"] = np.abs(g) / (Yp[0] + Yp[1]) <= 0.02
        for j, p in enumerate(PARTIES):
            df[f"{p}_proj_additive_pct"] = (100 * Ya[j] / Ya.sum(0)).round(2)
        df["winner_proj_additive"] = np.where(np.abs(Ya[0] - Ya[1]) <= 1e-9 * (Ya[0] + Ya[1]), "TIE",
                                              np.where(Ya[0] > Ya[1], "UCP", "NDP"))
        if k == "map2019":
            df["p338_ucp"] = p338.UCP.values
            df["p338_ndp"] = p338.NDP.values
            df["p338_other"] = 100 - p338.UCP.values - p338.NDP.values
            df["p338_ucp_range"] = [f"{a}-{b}" for a, b in zip(p338.UCP_lo, p338.UCP_hi)]
            df["p338_ndp_range"] = [f"{a}-{b}" for a, b in zip(p338.NDP_lo, p338.NDP_hi)]
            df["ucp_one_pass_pct"] = (100 * A["one"][:, 0]).round(2)
            df["ndp_one_pass_pct"] = (100 * A["one"][:, 1]).round(2)
        district_tables[k] = df

    # ---- seats at 50/50 under the model, and the lead each party needs ------------------------
    def det_seats(delta):
        """Deterministic: shift every riding's UCP-minus-NDP lead by delta points (half to each)."""
        Pd = P.copy()
        Pd[:, 0] += delta / 200
        Pd[:, 1] -= delta / 200
        Pd = np.clip(Pd, FLOOR, None)
        Pd /= Pd.sum(1, keepdims=True)
        x = sw.proportional(Pd[None])
        out = {}
        for k, m in maps.items():
            Y = to_map(x, T, m["H"])[0]
            u, d, _ = seats_batch(Y[None], MAPS[k][1])
            out[k] = (int(u.sum()), int(d.sum()))
        Yp = to_map(x, T, maps["map2019"]["H"])[0].sum(1)
        return out, 100 * (Yp[0] - Yp[1]) / Yp.sum(), Yp[0] / (Yp[0] + Yp[1])

    lo, hi = -15.0, 5.0                         # bisection: delta at which UCP = NDP province-wide
    for _ in range(60):
        mid = (lo + hi) / 2
        if det_seats(mid)[2] < 0.5:
            lo = mid
        else:
            hi = mid
    s50, lead50, _ = det_seats(hi)
    grid = np.round(np.arange(-20, 20.001, 0.05), 3)
    curve = {k: [] for k in maps}
    leads = []
    for dlt in grid:
        o, ld, _ = det_seats(dlt)
        leads.append(ld)
        for k in maps:
            curve[k].append(o[k])
    leads = np.array(leads)
    needed = {}
    for k in maps:
        u = np.array([c[0] for c in curve[k]])
        d = np.array([c[1] for c in curve[k]])
        nd = need(MAPS[k][1])
        needed[k] = {"ucp_majority_from_lead_pts": float(leads[np.argmax(u >= nd)]),
                     "ndp_majority_below_lead_pts": float(leads[len(d) - 1 - np.argmax((d >= nd)[::-1])]),
                     "seats_at_50_50_model": {"ucp": s50[k][0], "ndp": s50[k][1]}}
    res["model_50_50_delta_pts"] = hi
    res["lead_needed"] = needed
    pd.DataFrame({"provincial_ucp_lead_pts": leads.round(3),
                  **{f"{k}_ucp": [c[0] for c in curve[k]] for k in maps},
                  **{f"{k}_ndp": [c[1] for c in curve[k]] for k in maps}}).to_csv(OUT / "seats_vs_lead.csv", index=False)

    res["point"] = point
    res["province_lead_pts_point"] = base_lead

    # ---- Monte Carlo -------------------------------------------------------------------------
    rng = np.random.default_rng(SEED)
    half = (((p338.UCP_hi - p338.UCP_lo) + (p338.NDP_hi - p338.NDP_lo)) / 4).to_numpy(float)
    z_prov = rng.standard_normal(N_DRAWS)
    z_rid = rng.standard_normal((N_DRAWS, 87))

    def run(method="prop", z=Z90, riding_scale=1.0):
        sd_prov = 2 * PROV_HALF / z                                    # on the UCP-minus-NDP lead
        sd_rid = riding_scale * 2 * np.sqrt(np.clip(half ** 2 - PROV_HALF ** 2, 0, None)) / z
        lead_shift = sd_prov * z_prov[:, None] + sd_rid[None] * z_rid  # (draws, 87) points
        u = {k: np.zeros((N_DRAWS, MAPS[k][1]), bool) for k in maps}
        d = {k: np.zeros((N_DRAWS, MAPS[k][1]), bool) for k in maps}
        prov_lead = np.zeros(N_DRAWS)
        clipped_t, clipped_va, other_beats = 0.0, [], 0
        for s in range(0, N_DRAWS, CHUNK):
            Pd = np.repeat(P[None], min(CHUNK, N_DRAWS - s), 0)
            Pd[:, :, 0] += lead_shift[s:s + CHUNK] / 200
            Pd[:, :, 1] -= lead_shift[s:s + CHUNK] / 200
            clipped_t += float((Pd < FLOOR).any(2).sum())
            Pd = np.clip(Pd, FLOOR, None)
            Pd /= Pd.sum(2, keepdims=True)
            if method == "prop":
                x = sw.proportional(Pd)
            else:
                x, c = sw.additive(Pd)
                clipped_va.append(c)
            for k, m in maps.items():
                Y = to_map(x, T, m["H"])
                uu, dd, ob = seats_batch(Y, MAPS[k][1])
                u[k][s:s + CHUNK], d[k][s:s + CHUNK] = uu, dd
                other_beats += ob
                if k == "map2019":
                    tot = Y.sum(2)
                    prov_lead[s:s + CHUNK] = 100 * (tot[:, 0] - tot[:, 1]) / tot.sum(1)
        diag = {"riding_targets_clipped_share": clipped_t / (N_DRAWS * 87),
                "additive_va_clipped_share": float(np.mean(clipped_va)) if clipped_va else None,
                "other_party_wins": other_beats,
                "sd_prov_lead_pts": sd_prov, "sd_riding_lead_pts_median": float(np.median(sd_rid)),
                "sd_riding_lead_pts_range": [float(sd_rid.min()), float(sd_rid.max())],
                "provincial_lead_pct": {q: float(np.percentile(prov_lead, q)) for q in (5, 50, 95)}}
        return u, d, diag

    def summarise(u, d):
        per, outcome, useats, lead = {}, {}, {}, {}
        for k in maps:
            n = MAPS[k][1]
            U, D = u[k].sum(1), d[k].sum(1)
            nd = need(n)
            oc = np.where(U >= nd, "UCP majority", np.where(D >= nd, "NDP majority", "hung"))
            outcome[k], useats[k], lead[k] = oc, U, U - D
            per[k] = {"seats": n, "need": nd,
                      "ucp_median": float(np.median(U)), "ndp_median": float(np.median(D)),
                      "ucp_mean": float(U.mean()), "ndp_mean": float(D.mean()),
                      "ucp_p05_p95": [float(np.percentile(U, 5)), float(np.percentile(U, 95))],
                      "ndp_p05_p95": [float(np.percentile(D, 5)), float(np.percentile(D, 95))],
                      "p_ucp_majority": float((oc == "UCP majority").mean()),
                      "p_ndp_majority": float((oc == "NDP majority").mean()),
                      "p_hung": float((oc == "hung").mean()),
                      "p_ucp_win_by_district": u[k].mean(0)}
        pairs = {}
        keys = list(maps)
        for i, a in enumerate(keys):
            for b in keys[i + 1:]:
                for x, y in ((a, b),):
                    du = useats[x] - useats[y]
                    dl = lead[x] - lead[y]
                    flip = outcome[x] != outcome[y]
                    pairs[f"{x}_vs_{y}"] = {
                        "ucp_seat_diff_median": float(np.median(du)),
                        "ucp_seat_diff_p05_p95": [float(np.percentile(du, 5)), float(np.percentile(du, 95))],
                        "ucp_lead_diff_median": float(np.median(dl)),
                        "ucp_lead_diff_p05_p95": [float(np.percentile(dl, 5)), float(np.percentile(dl, 95))],
                        "p_lead_better_for_ucp_on_first": float((dl > 0).mean()),
                        "p_lead_same": float((dl == 0).mean()),
                        "p_lead_better_for_ndp_on_first": float((dl < 0).mean()),
                        "p_government_differs": float(flip.mean()),
                        "p_ucp_maj_on_first_only": float(((outcome[x] == "UCP majority") & (outcome[y] != "UCP majority")).mean()),
                        "p_ucp_maj_on_second_only": float(((outcome[y] == "UCP majority") & (outcome[x] != "UCP majority")).mean())}
        return per, pairs

    variants = {"main": dict(method="prop"),
                "additive_swing": dict(method="add"),
                "no_riding_noise": dict(method="prop", riding_scale=0.0),
                "riding_noise_x1.5": dict(method="prop", riding_scale=1.5),
                "ranges_as_95pct": dict(method="prop", z=1.96),
                "riding_noise_x0.5": dict(method="prop", riding_scale=0.5)}
    mc = {}
    for name, kw in variants.items():
        u, d, diag = run(**kw)
        per, pairs = summarise(u, d)
        if name == "main":
            for k in maps:
                district_tables[k]["p_ucp_win_mc"] = per[k]["p_ucp_win_by_district"].round(3)
                district_tables[k]["p_ndp_win_mc"] = d[k].mean(0).round(3)
        for k in per:
            per[k].pop("p_ucp_win_by_district")
        mc[name] = {"settings": {**kw}, "diagnostics": diag, "maps": per, "pairs": pairs}
        print(name, {k: round(per[k]["p_ucp_majority"], 3) for k in per}, flush=True)
    res["mc"] = mc
    res["p338_headline"] = {"vote": "UCP 48 +/- 5, NDP 43 +/- 5", "seats": "UCP 44 [33-60], NDP 43 [27-54]",
                            "odds": "UCP 60% / NDP 40% (most seats and majority)"}

    for k, df in district_tables.items():
        df.to_csv(OUT / f"districts_{k}.csv", index=False)
    (OUT / "results.json").write_text(json.dumps(res, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)),
                                      encoding="utf8")
    print(json.dumps({"check_2023": {k: v["match"] for k, v in res["check_2023"].items()},
                      "check_338": {k: v for k, v in res["check_338"].items()},
                      "province": res["province_projected_pct"], "lead_needed": needed,
                      "point": {k: v["proportional"] for k, v in point.items()},
                      "point_add": {k: (v["additive"]["ucp"], v["additive"]["ndp"], v["additive"]["tie"]) for k, v in point.items()},
                      "diag": mc["main"]["diagnostics"]}, indent=1, default=str))


if __name__ == "__main__":
    sys.exit(main())
