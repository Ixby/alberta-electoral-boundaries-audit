# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
a10_assemble.py
---------------

Amendment 10: assemble the per-page reconstructions (a10_reconstruct_pages.py) and the districts
whose official geometry is known into one VA -> district map. A library (assemble, load_pages) and
a CLI. Five mechanical rules, applied in this order; none is tuned after a run:

  1. Known-overlap   a reconstruction that overlaps the union of the known districts by more than
                     KNOWN_OVERLAP_MAX of its own area is rejected.
  2. Mutual-overlap  of two surviving reconstructions whose intersection exceeds MUTUAL_OVERLAP_MAX
                     of the smaller one's area, one is rejected: the one that (i) conflicts with
                     MORE other reconstructions (partners over the pairs above the threshold, on
                     the current survivors); tie, (ii) the higher share of its own area inside
                     the known union; tie, (iii) the lower in60; tie, (iv) the lower n_layer_pts;
                     tie, the higher ED. The worst pair goes first; conflicts are recomputed
                     after every rejection until none exceed. Each reason names the stage used.
  3. Assignment      each VA goes to the district (known or surviving reconstruction) holding the
                     largest share of its AREA (actual intersections, not centroids). Ties go to
                     a known district, then the lower ED. A VA whose best share is under
                     MIN_AREA_SHARE is left unassigned for now.
  4. Hole fill       connected components of unassigned VAs (on the VA rook-adjacency graph from
                     mcmc_ensemble.build_va_graph) are claimed by unplaced districts (rejected or
                     failed pages). Title anchors are the CSDs (names of 4+ letters) in
                     V1._csd() whose normalised name is a whole-word substring of the normalised
                     page title ("-" read as a space); the json's own "anchors" are not used.
                     A district CLAIMS a component (a) when a CSD centroid of one of its title
                     anchors lies in the component; or, only if it has no title anchor at all,
                     (b) when the page's "all_hits_window" bounds contain the component's
                     representative point. A claim is dropped (and recorded) unless the
                     district's App. 7 area_km2 is within AREA_TOL of the component's area; (b)
                     uses a window built from CSD names (all_hits + title CSDs), buffered by
                     max(6 km, 0.5*sqrt(area_km2) km). A district fills only one component. A
                     component goes to its claimant only when exactly one valid claim remains;
                     with none or several it stays unassigned. Every claim is recorded in
                     summary["hole_fill_components"] with its type and the area numbers.
  5. Population      for every reconstructed or filled district (known ones too, for reference),
                     the VA population (pop_2021) scaled by (App. 7 provincial total / VA
                     provincial total) is compared with the App. 7 population and reported as
                     pop_diff_pct. Informational only: no flag from it gates anything and it does
                     not change va_district (the VA population proxy runs -39% to +13% from the
                     stated figure even on districts whose geometry is known exactly).

District names are normalised with a7_stepb_calibrate.norm throughout. Everything is in EPSG:3400.
Deterministic: no random numbers.

Usage:
  python analysis/scripts/a10_assemble.py --pages OUT_DIR --known tuning|fixed --out result.json [--csv va_assignment.csv]
    tuning = the 22 tuning districts' official geometry (calibration); fixed = the 56 unchanged
    districts plus Calgary-Acadia (Step C).
"""
import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.strtree import STRtree

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))
sys.path.insert(0, str(REPO / "analysis" / "utils"))

import a7_stepb_calibrate as C  # noqa: E402  (MAJ, APP7, norm)
import a7_stepb_reconstruct as V1  # noqa: E402  (_csd, _norm: CSD table for the hole fill)

norm = C.norm

KNOWN_OVERLAP_MAX = 0.05   # rule 1: max share of a reconstruction's own area inside known districts
MUTUAL_OVERLAP_MAX = 0.10  # rule 2: max overlap, as a share of the smaller reconstruction's area
MIN_AREA_SHARE = 0.5       # rule 3: a VA needs at least this share of its area in one district
TIE_DECIMALS = 9           # rule 3: area shares equal to this many decimals are a tie
AREA_TOL = 0.25            # rule 4: a hole claim needs |component area - App. 7 area_km2| <= this share of the latter
POP_TOL = 0.05             # rule 5, reporting only (pop_within_5pct): the 2021 VA population proxy is NOT a gate,
                           # it misses the stated figure by -39% to +13% even on exactly known districts
FIXED_EXTRA = ("Calgary-Acadia",)  # ED 1: changed by 2 people, treated as fixed (Amendment 8)
CITIES = {"calgary", "edmonton", "st. albert", "red deer", "lethbridge", "medicine hat", "grande prairie",
          "airdrie", "sherwood park"}   # a bare city label on a neighbour page stands for all of that city districts
UNCHANGED_56 = REPO / "analysis/a8/unchanged_56.json"
_BIG = 10 ** 6             # sort key for a known district with no ED number


@dataclass
class AssemblyResult:
    va_district: pd.Series        # aligned to va.index; district name (normalised) or None
    rejected: dict                # ed -> reason (rules 1 and 2)
    filled: dict                  # ed -> n_vas assigned by the hole fill
    unassigned_components: list   # VA counts of the components left unassigned, largest first
    districts: pd.DataFrame       # ed, district, source, n_vas, pop_va_scaled, pop_stated, pop_diff_pct, pop_within_5pct
    summary: dict


# ---- inputs ------------------------------------------------------------------------------------

def _valid(g):
    """A valid polygonal geometry (buffer(0) as in V3.reconstruct); GeometryCollections are cleaned."""
    if g is None or g.is_empty:
        return g
    if not g.is_valid:
        g = g.buffer(0)
    if g.geom_type not in ("Polygon", "MultiPolygon"):
        parts = [p for p in getattr(g, "geoms", []) if p.geom_type in ("Polygon", "MultiPolygon")]
        g = unary_union(parts) if parts else Polygon()
    return g


def load_pages(out_dir, with_rejected=True):
    """Read an a10_reconstruct_pages.py output directory.

    The ED number comes from the json "ed" field, not the file name; an ED polygon is the gpkg
    with the same stem as its json. A page is PLACED only if it has a gpkg and its json says
    polygon_status "accepted" (or, when the key is absent, has no error). A gpkg on any other page
    is a rejected fit: returned separately and never used by assemble.
    Returns (polys, pages, rejected_polys): polys = {ed: polygon in EPSG:3400} for placed pages;
    pages = {ed: json dict} for every json (plus neighbour_eds / city_labels / neighbour_labels from
    edNN_neighbours.json when present); rejected_polys = {ed: polygon}. with_rejected=False returns
    the old two values (polys, pages). A gpkg with no json is treated as placed (ED from its "ed" column)."""
    out_dir = Path(out_dir)
    polys, pages, rejected_polys, stems = {}, {}, {}, set()

    def read_gpkg(f):
        g = gpd.read_file(f)
        if g.crs is not None and g.crs.to_epsg() != 3400:
            g = g.to_crs(3400)
        geom = _valid(g.geometry.union_all())
        return g, (None if geom is None or geom.is_empty else geom)

    for f in sorted(out_dir.glob("ed*.json")):
        if f.stem.endswith("_neighbours"):
            continue
        d = json.loads(f.read_text(encoding="utf-8"))
        nf = f.with_name(f.stem + "_neighbours.json")
        if nf.exists():
            nd = json.loads(nf.read_text(encoding="utf-8"))
            d["neighbour_eds"] = [int(x) for x in nd["neighbour_eds"]]
            d["city_labels"] = nd.get("city_labels")
            d["neighbour_labels"] = nd.get("labels")
        if "ed" not in d:
            raise ValueError(f"{f.name} has no 'ed' field")
        ed = int(d["ed"])
        if ed in pages:
            raise ValueError(f"two page jsons for ED {ed} (second: {f.name})")
        pages[ed] = d
        stems.add(f.stem)
        gp = f.with_suffix(".gpkg")
        if gp.exists():
            geom = read_gpkg(gp)[1]
            if geom is not None:
                st = d.get("polygon_status")
                accepted = (st == "accepted") if st is not None else not d.get("error")
                (polys if accepted else rejected_polys)[ed] = geom
    for f in sorted(out_dir.glob("ed*.gpkg")):
        if f.stem in stems:
            continue
        g, geom = read_gpkg(f)
        if geom is not None and "ed" in g.columns and len(g):
            polys.setdefault(int(g["ed"].iloc[0]), geom)
    return (polys, pages, rejected_polys) if with_rejected else (polys, pages)


def load_app7():
    return pd.read_csv(C.APP7).set_index("ed_number")


def load_majority():
    """The commission majority map in EPSG:3400 with a normalised-name key column."""
    maj = gpd.read_file(C.MAJ).to_crs(3400)
    maj["key"] = maj.EDName2025.map(norm)
    return maj


def known_districts(which, app7, maj=None):
    """{normalised name: geometry} of the districts whose official geometry is used as-is.
    'tuning' = the 22 tuning districts (a9_stepb_reconstruct_v3.TUNING; names from App. 7);
    'fixed'  = the 56 unchanged districts (analysis/a8/unchanged_56.json) plus Calgary-Acadia."""
    maj = load_majority() if maj is None else maj
    if which == "tuning":
        import a9_stepb_reconstruct_v3 as V3
        names = [norm(app7.loc[n, "district"]) for n in V3.TUNING]
    elif which == "fixed":
        names = [norm(x) for x in json.loads(UNCHANGED_56.read_text(encoding="utf-8"))["districts"]]
        names += [norm(x) for x in FIXED_EXTRA]
    else:
        raise ValueError(f"--known must be tuning or fixed, not {which!r}")
    have = set(maj.key)
    missing = [n for n in names if n not in have]
    if missing:
        raise ValueError(f"known districts missing from the majority map: {missing}")
    if len(set(names)) != len(names):
        raise ValueError("duplicate names in the known list")
    return {n: _valid(maj.loc[maj.key == n, "geometry"].union_all()) for n in names}


# ---- geometry helpers --------------------------------------------------------------------------

def _inter_area(a, b):
    try:
        return a.intersection(b).area
    except shapely.errors.GEOSException:
        return a.buffer(0).intersection(b.buffer(0)).area


def _area_shares(va_geoms, va_area, dist_geoms):
    """Share of each VA's area inside each district: arrays (va_pos, dist_pos, share), share > 0."""
    tree = STRtree(va_geoms)
    di_all, vi_all = tree.query(dist_geoms, predicate="intersects")
    out_v, out_d, out_s = [], [], []
    for di, g in enumerate(dist_geoms):
        cand = vi_all[di_all == di]
        if not len(cand):
            continue
        shapely.prepare(g)
        inside = shapely.contains(g, va_geoms[cand])
        share = np.ones(len(cand))
        rest = np.flatnonzero(~inside)
        if len(rest):
            sub = va_geoms[cand[rest]]
            try:
                ia = shapely.area(shapely.intersection(sub, g))
            except shapely.errors.GEOSException:
                ia = np.array([_inter_area(s, g) for s in sub])
            share[rest] = ia / va_area[cand[rest]]
        keep = share > 0
        out_v.append(cand[keep])
        out_d.append(np.full(int(keep.sum()), di))
        out_s.append(np.minimum(share[keep], 1.0))
    if not out_v:
        return np.array([], int), np.array([], int), np.array([])
    return np.concatenate(out_v), np.concatenate(out_d), np.concatenate(out_s)


def _graph_edges(va, graph):
    """Edge array in va row positions. graph=None builds it with mcmc_ensemble.build_va_graph (the
    one authority for adjacency) and requires the same VA table; nodes are labelled by va.index."""
    if graph is None:
        va2, graph = C.me.build_va_graph(verbose=False)
        if len(va2) != len(va) or not va2.index.equals(va.index):
            raise ValueError("graph=None: build_va_graph's VA table differs from the one passed in")
    if graph.number_of_nodes() != len(va):
        raise ValueError(f"graph has {graph.number_of_nodes()} nodes for {len(va)} VAs")
    e = np.array(list(graph.edges()), dtype=object)
    if not len(e):
        return np.zeros((0, 2), int)
    pos = va.index.get_indexer(e.ravel().tolist()).reshape(-1, 2)
    if (pos < 0).any():
        raise ValueError("graph nodes are not labelled by va.index")
    return pos


# ---- the five rules ----------------------------------------------------------------------------

def _rule1_known_overlap(live, known_geoms, known_max, rejected):
    """Reject reconstructions overlapping the known union by more than known_max of their own area.
    Returns {ed: that share} for every reconstruction examined (rule 2's second tie-break)."""
    tree = STRtree(known_geoms) if known_geoms else None
    shares = {}
    for ed in sorted(live):
        g = live[ed]
        ov = 0.0
        if tree is not None and g.area:
            cand = tree.query(g, predicate="intersects")
            if len(cand):
                ov = unary_union([g.intersection(known_geoms[i]) for i in cand]).area / g.area
        shares[ed] = ov
        if ov > known_max:
            rejected[ed] = f"overlaps known districts: {100 * ov:.1f}%"
    for ed in rejected:
        live.pop(ed, None)
    return shares


RULE2_STAGES = ("partner count", "known-overlap share", "in60", "n_layer_pts", "ED")


def _rule2_mutual_overlap(live, pages, known_share, mutual_max, rejected):
    def diag(ed, k):
        v = ((pages.get(ed) or {}).get("diagnostics") or {}).get(k)
        return float("-inf") if v is None else float(v)

    def key(ed, partners):  # the larger key loses, stage by stage
        return (partners.get(ed, 0), round(known_share.get(ed, 0.0), TIE_DECIMALS),
                -round(diag(ed, "in60"), TIE_DECIMALS), -diag(ed, "n_layer_pts"), ed)

    def shown(ed, partners, stage):
        return (partners.get(ed, 0), f"{100 * known_share.get(ed, 0.0):.1f}%", f"{diag(ed, 'in60'):.4f}",
                f"{diag(ed, 'n_layer_pts'):.0f}", ed)[stage]

    eds = sorted(live)
    geoms = [live[e] for e in eds]
    tree = STRtree(geoms)
    qi, ti = tree.query(geoms, predicate="intersects")
    pair = {}  # (ed_a, ed_b) -> fraction of the smaller one's area
    for a, b in zip(qi, ti):
        if a < b:
            ia = _inter_area(geoms[a], geoms[b])
            small = min(geoms[a].area, geoms[b].area)
            pair[(eds[a], eds[b])] = ia / small if small else 0.0
    while True:
        bad = {k: f for k, f in pair.items() if f > mutual_max}
        if not bad:
            break
        partners = {}
        for a, b in bad:
            partners[a] = partners.get(a, 0) + 1
            partners[b] = partners.get(b, 0) + 1
        (a, b), frac = max(bad.items(), key=lambda kv: (kv[1], -kv[0][0], -kv[0][1]))  # worst pair, then lower EDs
        ka, kb = key(a, partners), key(b, partners)
        loser, winner = (a, b) if ka > kb else (b, a)
        stage = next(i for i, (x, y) in enumerate(zip(ka, kb)) if x != y)
        rejected[loser] = (f"mutual overlap {100 * frac:.1f}% with ED {winner}; conflict partners "
                           f"{partners[loser]} vs {partners[winner]}; decided at stage {stage + 1} "
                           f"({RULE2_STAGES[stage]}): {shown(loser, partners, stage)} vs {shown(winner, partners, stage)}")
        live.pop(loser)
        for k in [k for k in pair if loser in k]:
            del pair[k]


def _rule3_assign(va, dist_geoms, dist_ed, dist_known, dist_names):
    """Returns label (district position per VA, -1 = unassigned) and the best share per VA."""
    va_geoms = np.asarray(va.geometry.values, dtype=object)
    va_area = shapely.area(va_geoms)
    vi, di, sh = _area_shares(va_geoms, va_area, np.asarray(dist_geoms, dtype=object))
    label = np.full(len(va), -1, int)
    best = np.zeros(len(va))
    if not len(vi):
        return label, best
    t = pd.DataFrame({"vi": vi, "di": di, "sh": sh})
    t["tie"] = np.round(-t.sh, TIE_DECIMALS)
    t["kn"] = np.where(np.asarray(dist_known)[di], 0, 1)
    t["ed"] = [(_BIG if dist_ed[d] is None else dist_ed[d]) for d in di]
    t["nm"] = [dist_names[d] for d in di]
    top = t.sort_values(["vi", "tie", "kn", "ed", "nm"], kind="mergesort").drop_duplicates("vi")
    best[top.vi.to_numpy()] = top.sh.to_numpy()
    ok = top.sh.to_numpy() >= MIN_AREA_SHARE
    label[top.vi.to_numpy()[ok]] = top.di.to_numpy()[ok]
    return label, best


def _title_csd_mask(csd, page):
    """CSDs (names of 4+ letters) whose normalised name is a whole word of the normalised title."""
    tblob = " " + V1._norm(str(page.get("title") or "").replace("-", " ")) + " "
    return csd.nm.map(lambda nm: len(nm) >= 4 and (" " + nm + " ") in tblob).to_numpy(bool)


def _rule4_hole_fill(va, edges, unassigned, unplaced, stated_area, va_ed, area_tol=AREA_TOL):
    """unassigned: bool array over va rows; unplaced: {ed: page json}; stated_area: {ed: App. 7 km2}.
    Returns (comp, ncomp, claims, sizes, areas): component id per VA (-1 outside), the component
    count, claims[c] = list of every claim on component c (ed, type, areas, status "valid" or
    "dropped: area X vs stated Y"), the VA count and the area (km2) of each component."""
    pos = np.flatnonzero(unassigned)
    comp = np.full(len(va), -1, int)
    if not len(pos):
        return comp, 0, {}, {}, {}
    e = edges
    keep = unassigned[e[:, 0]] & unassigned[e[:, 1]]
    e = e[keep]
    remap = np.full(len(va), -1, int)
    remap[pos] = np.arange(len(pos))
    m = coo_matrix((np.ones(len(e)), (remap[e[:, 0]], remap[e[:, 1]])), shape=(len(pos), len(pos)))
    ncomp, lab = connected_components(m, directed=False)
    comp[pos] = lab
    adj = {c: set() for c in range(ncomp)}   # EDs of assigned districts sharing a VA-graph edge with component c
    for a, b in edges:
        for x, y in ((a, b), (b, a)):
            if comp[x] >= 0 and va_ed[y] >= 0:
                adj[comp[x]].add(int(va_ed[y]))
    sizes = {c: int((lab == c).sum()) for c in range(ncomp)}
    geoms = np.asarray(va.geometry.values[pos], dtype=object)
    unions = [unary_union(list(geoms[lab == c])) for c in range(ncomp)]
    areas = {c: unions[c].area / 1e6 for c in range(ncomp)}
    rep = [u.representative_point() for u in unions]
    claims = {c: [] for c in range(ncomp)}
    csd = V1._csd()
    cent = csd.geometry.centroid
    tree = STRtree(geoms)

    def claim(c, ed, kind, pg, area_used, pooled):
        st = stated_area.get(ed, float("nan"))
        ratio = area_used / st if st > 0 else float("nan")
        ok = st > 0 and abs(area_used - st) <= area_tol * st
        printed = pg.get("_printed_neighbours")
        adjc = adj[c]
        n_in = len(adjc & printed) if printed is not None else None
        nb_ok = printed is None or not adjc or n_in > len(adjc) / 2
        why = [] if ok else [f"area {area_used:.1f} vs stated {st:.1f}" + (" (pooled)" if pooled else "")]
        if not nb_ok:
            why.append(f"neighbour check: {n_in} of {len(adjc)} adjacent EDs printed")
        claims[c].append({"ed": int(ed), "type": kind, "pooled": pooled, "component_area_km2": areas[c],
                          "area_used_km2": area_used, "stated_area_km2": st, "area_ratio": ratio,
                          "adjacent_eds": sorted(adjc),
                          "neighbour_check": "not run" if printed is None else
                          (f"ok ({n_in}/{len(adjc)})" if nb_ok else f"fail ({n_in}/{len(adjc)})"),
                          "status": "valid" if not why else "dropped: " + "; ".join(why)})

    for ed, pg in unplaced.items():
        mask = _title_csd_mask(csd, pg)
        hit = []
        if mask.any():  # (a) title-anchor CSD centroids; claims on several components are pooled for the area test
            pts = np.asarray(cent[mask].values, dtype=object)
            _, vpos = tree.query(pts, predicate="intersects")
            hit = sorted(set(lab[vpos].tolist()))
            tot = sum(areas[c] for c in hit)
            for c in hit:
                claim(c, ed, "title anchor", pg, tot if len(hit) > 1 else areas[c], len(hit) > 1)
        if not hit:  # (b) no title-anchor centroid in any component: window from the page CSD names
            names = {V1._norm(x) for x in (pg.get("all_hits") or [])}
            sel = mask | csd.nm.isin(names).to_numpy()
            if sel.any():
                st = stated_area.get(ed, float("nan"))
                buf = max(6000.0, 500.0 * float(np.sqrt(st)) if st > 0 else 0.0)
                win = unary_union(list(csd.geometry[sel])).envelope.buffer(buf)
                for c, p in enumerate(rep):
                    if win.contains(p):
                        claim(c, ed, "names window", pg, areas[c], False)
    return comp, ncomp, claims, sizes, areas


def assemble(polys, pages, known, va, app7, *, known_overlap_max=KNOWN_OVERLAP_MAX,
             mutual_overlap_max=MUTUAL_OVERLAP_MAX, pop_tol=POP_TOL, area_tol=AREA_TOL, graph=None, rejected_polys=None):
    """Build the VA -> district assignment. See the module docstring for the five rules.

    polys {ed: geometry} placed reconstructions; pages {ed: page json} for every page (title,
    all_hits_window, diagnostics); known {name: geometry} official geometry used as-is; va the
    canonical VA table (EPSG:3400, pop_2021); app7 indexed by ed_number with district, population,
    area_km2. graph = the VA
    adjacency graph from build_va_graph (nodes labelled by va.index); built when None and needed."""
    t0 = time.time()
    rejected_polys = dict(rejected_polys or {})   # listed only; a rejected fit is never used here
    name_of = {int(ed): norm(str(nm)) for ed, nm in app7["district"].items()}
    ed_of = {nm: ed for ed, nm in name_of.items()}
    known = {norm(k): _valid(g) for k, g in known.items()}
    for ed in list(polys) + list(pages):
        if int(ed) not in name_of:
            raise ValueError(f"ED {ed} is not in App. 7")
    if "area_km2" not in app7.columns:
        raise ValueError("app7 needs an area_km2 column (rule 4 area condition)")

    # reconstructions of a known district are not used: its official geometry stands
    ignored_known = sorted(ed for ed in polys if name_of[ed] in known)
    live = {int(ed): _valid(g) for ed, g in polys.items() if name_of[int(ed)] not in known}
    pages = {int(k): v for k, v in pages.items()}
    rejected = {}

    known_names = sorted(known)
    known_geoms = [known[n] for n in known_names]
    known_share = _rule1_known_overlap(live, known_geoms, known_overlap_max, rejected)
    n_rule1 = len(rejected)
    if len(live) > 1:
        _rule2_mutual_overlap(live, pages, known_share, mutual_overlap_max, rejected)
    n_rule2 = len(rejected) - n_rule1

    # rule 3
    recon_eds = sorted(live)
    dist_names = known_names + [name_of[e] for e in recon_eds]
    dist_ed = [ed_of.get(n) for n in known_names] + recon_eds
    dist_known = [True] * len(known_names) + [False] * len(recon_eds)
    dist_geoms = known_geoms + [live[e] for e in recon_eds]
    label, best = _rule3_assign(va, dist_geoms, dist_ed, dist_known, dist_names)
    unassigned0 = label < 0

    # rule 4
    placed_names = set(known_names) | {name_of[e] for e in recon_eds}
    unplaced = {ed: (pg or {}) for ed, pg in sorted(pages.items()) if name_of[ed] not in placed_names}
    failed = sorted(ed for ed in unplaced if ed not in rejected)
    edges = _graph_edges(va, graph) if unassigned0.any() else np.zeros((0, 2), int)
    va_ed = np.array([(-1 if dist_ed[d] is None else dist_ed[d]) if d >= 0 else -1 for d in label], int)
    for ed, pg in list(unplaced.items()):
        if pg.get("neighbour_eds") is not None:
            printed = set(pg["neighbour_eds"])
            cands = pg.get("city_labels") or [x for x in (pg.get("neighbour_labels") or []) if norm(str(x)).lower() in CITIES]
            for city in {norm(str(x)).lower() for x in cands}:
                printed |= {e for e, n in name_of.items() if n.lower() == city or n.lower().startswith(city + "-")}
            unplaced[ed] = dict(pg, _printed_neighbours=printed)
    stated_area = {ed: float(app7.loc[ed, "area_km2"]) for ed in unplaced}
    comp, ncomp, claims, sizes, areas = _rule4_hole_fill(
        va, edges, unassigned0, unplaced, stated_area, va_ed, area_tol)
    names = np.array(dist_names + [None], dtype=object)
    va_district = names[np.where(label < 0, len(dist_names), label)].astype(object)
    filled, filled_type, left, comps = {}, {}, [], []
    ncl = {}   # valid single-component claims per district (pooled title claims are exempt)
    for cc in claims:
        for k in claims[cc]:
            if k['status'] == 'valid' and not k['pooled']:
                ncl[k['ed']] = ncl.get(k['ed'], 0) + 1
    for c in range(ncomp):
        valid = {k["ed"]: k["type"] for k in claims[c] if k["status"] == "valid"}
        rec = {"n_vas": sizes[c], "area_km2": areas[c], "claims": claims[c], "claimants": valid, "assigned_to": None}
        vc = [k for k in claims[c] if k['status'] == 'valid']
        if len(vc) == 1 and (vc[0]['pooled'] or ncl[vc[0]['ed']] == 1):
            ed = next(iter(valid))
            idx = np.flatnonzero(comp == c)
            va_district[idx] = name_of[ed]
            filled[ed] = filled.get(ed, 0) + len(idx)
            filled_type.setdefault(ed, set()).add(valid[ed])
            rec["assigned_to"] = ed
        else:
            why = ("several valid claims" if len(valid) > 1 else "claimant claims several components" if valid else
                   "all claims dropped on area" if claims[c] else "no claim")
            left.append({"c": c, "n_vas": sizes[c], "area_km2": areas[c], "claims": claims[c], "claimants": valid, "why": why})
        comps.append(rec)
    # enclosed fragments: an unassigned component whose VA-graph neighbours all belong to one district
    enclosed = []
    while True:
        un = np.array([x is None for x in va_district])
        if not un.any():
            break
        posn = np.flatnonzero(un)
        rm = np.full(len(va), -1, int); rm[posn] = np.arange(len(posn))
        ee = edges[un[edges[:, 0]] & un[edges[:, 1]]]
        _, lb = connected_components(coo_matrix((np.ones(len(ee)), (rm[ee[:, 0]], rm[ee[:, 1]])), shape=(len(posn),) * 2), directed=False)
        nbn = {}
        for a, b in edges:
            for x, y in ((a, b), (b, a)):
                if un[x] and not un[y]:
                    nbn.setdefault(lb[rm[x]], set()).add(va_district[y])
        hit = [(c, next(iter(v))) for c, v in sorted(nbn.items()) if len(v) == 1]
        if not hit:
            break
        for c, nm_ in hit:
            idx = posn[lb == c]
            va_district[idx] = nm_
            enclosed.append({"n_vas": int(len(idx)), "to": nm_, "flag": "enclosed"})
    left = [d for d in left if any(x is None for x in va_district[comp == d["c"]])]
    for d in left:
        d.pop("c")
    left.sort(key=lambda d: -d["n_vas"])
    comps.sort(key=lambda d: -d["n_vas"])
    # a page without the title / all_hits_window keys cannot claim anything: say so rather than fail quietly
    stale = sorted(ed for ed, pg in unplaced.items() if "title" not in pg or "all_hits" not in pg)
    va_district = pd.Series(va_district, index=va.index, name="district", dtype=object)


    # rule 5 (reporting only)
    scale = float(app7["population"].sum()) / float(va["pop_2021"].sum())
    pop_by = va.groupby(va_district.fillna("\0"))["pop_2021"].sum() * scale
    n_by = va_district.value_counts()
    within_col = f"pop_within_{100 * pop_tol:g}pct"
    rows = []
    for ed_, nm, src in ([(ed_of.get(n), n, "known") for n in known_names]
                         + [(e, name_of[e], "reconstructed") for e in recon_eds]
                         + [(e, name_of[e], "filled") for e in sorted(filled)]):
        stated = float(app7.loc[ed_, "population"]) if ed_ is not None else float("nan")
        pv = float(pop_by.get(nm, 0.0))
        diff = 100 * (pv - stated) / stated if stated == stated and stated else float("nan")
        rows.append({"ed": ed_, "district": nm, "source": src, "n_vas": int(n_by.get(nm, 0)),
                     "pop_va_scaled": pv, "pop_stated": stated, "pop_diff_pct": diff,
                     within_col: bool(abs(diff) <= 100 * pop_tol) if diff == diff else False})
    districts = pd.DataFrame(rows, columns=["ed", "district", "source", "n_vas", "pop_va_scaled",
                                            "pop_stated", "pop_diff_pct", within_col])
    districts["ed"] = districts["ed"].astype("Int64")
    districts[within_col] = districts[within_col].astype(bool)
    districts = districts.sort_values(["ed", "district"], na_position="last").reset_index(drop=True)

    new = districts[districts.source != "known"]
    kn = districts[districts.source == "known"]
    summary = {
        "n_vas": int(len(va)),
        "n_vas_assigned": int(va_district.notna().sum()),
        "n_vas_unassigned": int(va_district.isna().sum()),
        "n_vas_unassigned_before_fill": int(unassigned0.sum()),
        "coverage_pct": float(va_district.notna().mean()),
        "n_known": len(known_names),
        "n_reconstructions_in": len(polys),
        "ignored_known_pages": ignored_known,
        "rejected_known_overlap": n_rule1,
        "rejected_polygons_not_used": sorted(int(k) for k in rejected_polys),
        "rejected_mutual_overlap": n_rule2,
        "n_reconstructed": len(recon_eds),
        "reconstructed": recon_eds,
        "failed_pages": failed,
        "filled": {int(k): v for k, v in filled.items()},
        "filled_claim_type": {int(k): sorted(v) for k, v in filled_type.items()},
        "enclosed_fragments": enclosed,
        "n_hole_components": len(comps),
        "hole_fill_components": comps,
        "unplaced_pages_missing_title_or_all_hits_window": stale,
        "n_unassigned_components": len(left),
        "unassigned_components_detail": left[:25],
        "pop_reporting": {"column": within_col, "tol": pop_tol,
                          "reconstructed_or_filled_n": int(len(new)),
                          "reconstructed_or_filled_within_tol": int(new[within_col].sum()),
                          "reconstructed_or_filled_median_abs_diff_pct": float(new.pop_diff_pct.abs().median()) if len(new) else None,
                          "known_median_abs_diff_pct": float(kn.pop_diff_pct.abs().median()) if len(kn) else None},
        "pop_scale": scale,
        "thresholds": {"known_overlap_max": known_overlap_max, "mutual_overlap_max": mutual_overlap_max,
                       "min_area_share": MIN_AREA_SHARE, "area_tol": area_tol, "pop_tol": pop_tol},
        "seconds": round(time.time() - t0, 1),
    }
    return AssemblyResult(va_district=va_district, rejected=dict(sorted(rejected.items())),
                          filled={int(k): v for k, v in sorted(filled.items())},
                          unassigned_components=[d["n_vas"] for d in left],
                          districts=districts, summary=summary)


# ---- CLI ---------------------------------------------------------------------------------------

def _round(x, nd=4):
    if isinstance(x, (float, np.floating)):
        return round(float(x), nd)
    if isinstance(x, dict):
        return {k: _round(v, nd) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_round(v, nd) for v in x]
    return x


def _plain(x):
    """JSON-ready: numpy scalars to Python, NA/NaN to None."""
    if x is pd.NA or (isinstance(x, (float, np.floating)) and np.isnan(x)):
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    if isinstance(x, dict):
        return {str(k): _plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_plain(v) for v in x]
    return x


def result_to_json(res):
    return _plain({
        "summary": res.summary,
        "rejected": res.rejected,
        "filled": res.filled,
        "unassigned_components": res.unassigned_components,
        "districts": res.districts.astype(object).where(res.districts.notna(), None).to_dict("records"),
    })


def main():
    ap = argparse.ArgumentParser(description="Assemble page reconstructions + known districts into a VA map")
    ap.add_argument("--pages", required=True, help="a10_reconstruct_pages.py output directory")
    ap.add_argument("--known", required=True, choices=["tuning", "fixed"])
    ap.add_argument("--out", required=True, help="result json")
    ap.add_argument("--csv", help="optional per-VA assignment csv")
    ap.add_argument("--area-tol", type=float, default=AREA_TOL, help="rule 4 area condition")
    a = ap.parse_args()

    app7 = load_app7()
    known = known_districts(a.known, app7)
    va, graph = C.me.build_va_graph(verbose=False)
    polys, pages, rej_polys = load_pages(a.pages)
    print(f"pages {len(pages)} (placed {len(polys)}, rejected fits {len(rej_polys)}), known {len(known)} ({a.known})", flush=True)
    res = assemble(polys, pages, known, va, app7, area_tol=a.area_tol, graph=graph, rejected_polys=rej_polys)

    out = result_to_json(res)
    out["inputs"] = {"pages": str(a.pages), "known": a.known}
    Path(a.out).write_text(json.dumps(out, indent=1), encoding="utf-8")
    if a.csv:
        cols = [c for c in ("OBJECTID", "VA_NUMBER") if c in va.columns]
        df = pd.DataFrame({"va_row": va.index}, index=va.index)
        for c in cols:
            df[c] = va[c].to_numpy()
        df["district"] = res.va_district
        df.to_csv(a.csv, index=False, lineterminator="\n")
    d = res.districts.copy()
    for c in ("pop_va_scaled", "pop_stated", "pop_diff_pct"):
        d[c] = d[c].round(4)
    print(d.to_string(index=False))
    skip = ("unassigned_components_detail", "hole_fill_components", "reconstructed")
    print(json.dumps(_round({k: v for k, v in res.summary.items() if k not in skip}), indent=1))
    print("rejected:", json.dumps(res.rejected, indent=1))
    for c in res.summary["hole_fill_components"]:
        print(f"hole component {c['n_vas']:>4} VAs {c['area_km2']:>9.1f} km2  -> {c['assigned_to']}")
        for k in c["claims"]:
            print(f"    ED {k['ed']:>2} {k['type']:<15} {k['status']}")


if __name__ == "__main__":
    main()
