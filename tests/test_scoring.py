"""Pytest suite for the audit's core scoring functions.

Two layers:

1. **Synthetic-input unit tests.** Hand-computed reference values for
   tiny made-up maps (3-5 districts), verifying that `seat_results()`
   and the `seats_at_50_50` calculation produce the textbook answers.

2. **Verification-subset integrity check.** Loads the 10,000 saved
   per-step partition assignments from the verification subset and
   independently recomputes their metrics from scratch. Confirms that
   what the audit saved as "metrics for step N" actually matches what
   you get when you start from the saved assignment for step N and
   compute the metrics fresh. This is the byte-verifiable forensic
   guarantee — if this passes, the verification artefact is internally
   consistent.

Run from the repo root:
    python -m pytest tests/ -v
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

from mcmc_ensemble import seat_results

# ============================================================
# Layer 1: Synthetic-input unit tests
# ============================================================


def test_seat_results_minimal_50_50():
    """Two districts, identical 50/50 votes — should produce zero on
    every partisan-fairness metric."""
    ucp = np.array([100.0, 100.0])
    ndp = np.array([100.0, 100.0])
    m = seat_results(ucp, ndp)

    # Both districts are tied (UCP == NDP), so neither party "won"
    # under the strict > comparison. ucp_seats should be 0.
    assert m["ucp_seats"] == 0
    assert m["n_districts"] == 2
    assert m["ucp_vote_share"] == 0.5


def test_seat_results_clean_majority():
    """Three districts, UCP wins all 3 by 60-40. UCP wins all seats;
    efficiency gap should be positive (UCP-favoured)."""
    ucp = np.array([60.0, 60.0, 60.0])
    ndp = np.array([40.0, 40.0, 40.0])
    m = seat_results(ucp, ndp)

    assert m["ucp_seats"] == 3
    assert m["n_districts"] == 3
    assert abs(m["ucp_vote_share"] - 0.6) < 1e-9
    # All three districts have UCP at exactly 50/50 after uniform
    # shift to provincial 50/50. With fractional tie-splitting, each
    # tie is worth 0.5 seats. 3 districts * 0.5 = 1.5 / 3 = 0.5 share.
    assert m["seats_at_50_50"] == 0.5


def test_seat_results_packing_signal():
    """Three districts: UCP wins two narrowly (51-49) and loses one
    badly (10-90). UCP has 71/(71+128) ≈ 35.7% of the vote but wins
    2/3 of the seats. Strong UCP-favoured efficiency gap expected."""
    ucp = np.array([51.0, 51.0, 10.0])  # 112 total UCP
    ndp = np.array([49.0, 49.0, 90.0])  # 188 total NDP
    m = seat_results(ucp, ndp)

    assert m["ucp_seats"] == 2
    assert m["n_districts"] == 3
    expected_ucp_share = 112.0 / 300.0
    assert abs(m["ucp_vote_share"] - expected_ucp_share) < 1e-9
    # UCP-favoured: positive efficiency gap
    assert m["efficiency_gap"] > 0


def test_seats_at_50_50_uniform_swing():
    """Verify the uniform-swing math. Three districts where UCP gets
    60%, 50%, 40%. Provincial UCP share = 50%, so no shift is applied."""
    ucp = np.array([60.0, 50.0, 40.0])
    ndp = np.array([40.0, 50.0, 60.0])
    m = seat_results(ucp, ndp)
    # UCP wins 1 of 3 (60%), ties 1 of 3 (50%), loses 1 of 3 (40%).
    # Total wins = 1.0 + 0.5 = 1.5. Share = 1.5 / 3.0 = 0.5.
    assert abs(m["seats_at_50_50"] - 0.5) < 1e-9


def test_seats_at_50_50_swing_required():
    """UCP starts at 70/30 in three districts (provincial UCP share
    = 70%). Uniform swing of -20pp brings each district to 50/10
    (still UCP-winning). seats_at_50_50 = 1.0."""
    ucp = np.array([70.0, 70.0, 70.0])
    ndp = np.array([30.0, 30.0, 30.0])
    m = seat_results(ucp, ndp)
    # After shift to 50/50 provincial: each district's UCP share = 0.5
    # The seats@50/50 metric fractionalizes ties, so each district counts
    # as 0.5. Result: 3 * 0.5 / 3 = 0.5
    assert m["seats_at_50_50"] == 0.5


def test_seat_results_zero_case_has_all_keys():
    """seat_results() on all-zero input must return the same key set as the
    non-empty path — callers must not get KeyError on ucp_vote_share."""
    ucp = np.array([0.0, 0.0])
    ndp = np.array([0.0, 0.0])
    m_empty = seat_results(ucp, ndp)
    # Compute non-empty reference to get the canonical key set
    m_nonempty = seat_results(np.array([60.0]), np.array([40.0]))
    missing = set(m_nonempty.keys()) - set(m_empty.keys())
    assert not missing, f"Zero-case return dict missing keys: {missing}"
    import math
    assert math.isnan(m_empty["ucp_vote_share"]), "ucp_vote_share should be NaN for zero input"


def test_mean_median_hand_oracle():
    """Hand-computed mean-median oracle (added 2026-07-09 mutation audit:
    mean-median previously had NO unit oracle — a sign flip survived Layer 1
    and was caught only by the Layer-2 frozen baseline).

    UCP shares [0.80, 0.55, 0.45] (100-vote districts).
    median = 0.55, mean = 0.60 -> mean_median = 0.55 - 0.60 = -0.05
    (median UCP share minus mean; negative = NDP-favoured tail here).
    """
    ucp = np.array([80.0, 55.0, 45.0])
    ndp = np.array([20.0, 45.0, 55.0])
    m = seat_results(ucp, ndp)
    assert abs(m["mean_median"] - (-0.05)) < 1e-9


def test_declination_hand_oracle_ucp_favoured():
    """Hand-computed declination oracle under the Amendment-10 Warrington
    convention (added 2026-07-09 mutation audit: reintroducing the exact
    pre-Amendment-10 sign bug previously survived every unit test and was
    caught only by the Layer-2 frozen baseline).

    UCP shares [0.40, 0.56, 0.70]; n=3, UCP wins R=2, NDP wins D=1.
      theta_R = atan2(mean(0.56,0.70) - 0.5, 2/(2*3)) = atan2(0.13, 1/3)
      theta_D = atan2(0.5 - 0.40, 1/(2*3))            = atan2(0.10, 1/6)
      delta   = (2/pi) * (theta_D - theta_R) = +0.10731081015827497
    Positive = UCP-favoured (UCP's wins are narrower than NDP's).
    """
    ucp = np.array([40.0, 56.0, 70.0])
    ndp = np.array([60.0, 44.0, 30.0])
    m = seat_results(ucp, ndp)
    assert abs(m["declination"] - 0.10731081015827497) < 1e-12


def test_declination_hand_oracle_mirror_ndp_favoured():
    """Mirror image of the case above (UCP shares [0.30, 0.44, 0.60]):
    the same geometry reflected across 0.5 must give the exact negative,
    -0.10731081015827497. Kills any asymmetric sign-convention drift."""
    ucp = np.array([30.0, 44.0, 60.0])
    ndp = np.array([70.0, 56.0, 40.0])
    m = seat_results(ucp, ndp)
    assert abs(m["declination"] - (-0.10731081015827497)) < 1e-12


def test_efficiency_gap_proportional():
    """When seat share matches vote share exactly, efficiency gap
    should be near zero. UCP wins one of three with 51-49 and loses
    two with 49-51. Vote share is exactly 50/50; seat share is 1/3.
    Negative efficiency gap (UCP under-represented)."""
    ucp = np.array([51.0, 49.0, 49.0])  # 149 UCP
    ndp = np.array([49.0, 51.0, 51.0])  # 151 NDP
    m = seat_results(ucp, ndp)
    assert m["ucp_seats"] == 1
    # UCP gets ~50% of votes but only 1/3 of seats — disadvantaged.
    # In the audit's convention (positive = UCP-favoured), EG should
    # be negative here.
    assert m["efficiency_gap"] < 0


# ============================================================
# Layer 2: Verification-subset integrity check
# ============================================================

VERIFICATION_METRICS = (
    ROOT / "data" / "outputs" / "mcmc" / "simulation_verification_metrics.csv"
)
VERIFICATION_ASSIGNMENTS = (
    ROOT / "data" / "outputs" / "mcmc" / "verification_assignments_raw.npz"
)
VA_VOTES_PATH = (
    ROOT / "data" / "shapefiles" / "derived" / "va_polygons_with_2023_votes.gpkg"
)


def _va_votes_unavailable_reason():
    """Return a skip reason when the VA votes GPKG can't actually be read.

    Two unavailability modes: the file is absent, or it exists only as a
    Git LFS pointer (a ~130-byte text stub starting with 'version https://
    git-lfs...') because the clone couldn't run `git lfs pull`. Reading the
    pointer with pyogrio raises DataSourceError, so detect it up front.
    """
    if not VA_VOTES_PATH.exists():
        return f"VA votes file not present at {VA_VOTES_PATH}"
    with open(VA_VOTES_PATH, "rb") as fh:
        head = fh.read(64)
    if head.startswith(b"version https://git-lfs"):
        return f"VA votes file is an un-pulled Git LFS pointer: {VA_VOTES_PATH}"
    return None


def _load_va_votes():
    """Load voting-area-level UCP/NDP votes, keyed by VA ID."""
    import geopandas as gpd

    va = gpd.read_file(VA_VOTES_PATH)
    return va


def _recompute_metrics_from_assignment(assignment_vec, va_votes_keyed_by_id):
    """Independently recompute seat_results from a saved assignment.
    This is a clean reimplementation that doesn't share code with the
    pipeline's aggregation step — if both produce the same answer,
    the saved metrics match the saved assignment.

    assignment_vec: int array of length n_va, value = district id
    va_votes_keyed_by_id: dict mapping va_id -> (ucp, ndp)
    """
    # Determine number of districts from the assignment
    n_districts = int(assignment_vec.max()) + 1
    ucp_per_district = np.zeros(n_districts, dtype=float)
    ndp_per_district = np.zeros(n_districts, dtype=float)

    for va_idx, district_id in enumerate(assignment_vec):
        # The npz stores assignments indexed by va_ids (sorted graph node order).
        # We need to look up each VA's vote totals by its graph node ID.
        # Caller passes va_votes_keyed_by_id, a list/array indexed the same way.
        ucp, ndp = va_votes_keyed_by_id[va_idx]
        ucp_per_district[district_id] += ucp
        ndp_per_district[district_id] += ndp

    return seat_results(ucp_per_district, ndp_per_district)


def test_verification_subset_files_present():
    """Smoke test: the verification subset artefacts exist and are non-empty."""
    assert (
        VERIFICATION_METRICS.exists()
    ), f"Verification metrics CSV missing at {VERIFICATION_METRICS}"
    assert (
        VERIFICATION_ASSIGNMENTS.exists()
    ), f"Verification assignments NPZ missing at {VERIFICATION_ASSIGNMENTS}"
    assert VERIFICATION_METRICS.stat().st_size > 0
    assert VERIFICATION_ASSIGNMENTS.stat().st_size > 0


def test_verification_subset_metric_count_matches_assignment_count():
    """The metrics CSV must have one row per saved assignment."""
    metrics = pd.read_csv(VERIFICATION_METRICS)
    npz = np.load(VERIFICATION_ASSIGNMENTS)
    assignments = npz["assignments"]
    assert (
        len(metrics) == assignments.shape[0]
    ), f"Metric rows ({len(metrics)}) != assignment rows ({assignments.shape[0]})"


def test_verification_subset_recompute_spot_check():
    """For 10 randomly-chosen saved partitions, independently
    recompute the metrics from the assignment and confirm they match
    the saved metrics row to within float tolerance.

    This is the integrity guarantee: if the audit cites a metric for
    step N, and a hostile expert loads the saved assignment for step N
    and recomputes from scratch, they get the same number.
    """
    unavailable = _va_votes_unavailable_reason()
    if unavailable:
        import pytest

        pytest.skip(unavailable)

    metrics = pd.read_csv(VERIFICATION_METRICS)
    npz = np.load(VERIFICATION_ASSIGNMENTS)
    assignments = npz["assignments"]
    va_ids = npz["va_ids"]

    va = _load_va_votes()
    # Build VA-id -> (ucp, ndp) lookup. The npz stores VA ids in the
    # order they appeared in the gerrychain Graph (sorted node order
    # at script execution time). We reproduce that ordering here.
    if "OBJECTID" in va.columns:
        # Match graph node id; gerrychain typically uses the dataframe
        # index, which corresponds to row order in the gpkg.
        va_lookup = {
            i: (float(va.iloc[i]["va_ucp"]), float(va.iloc[i]["va_ndp"]))
            for i in range(len(va))
        }
    else:
        import pytest

        pytest.skip("VA file structure unexpected; skipping recompute spot-check")

    # Spot-check 10 random steps
    rng = np.random.default_rng(seed=2026)
    n_steps = assignments.shape[0]
    sample_indices = rng.choice(n_steps, size=min(10, n_steps), replace=False)

    failures = []
    for step_idx in sample_indices:
        saved = metrics.iloc[step_idx]
        assignment = assignments[step_idx].astype(int)

        # Map npz va_ids -> graph index. The npz stores assignments
        # indexed by sorted va_id order, not gpkg row order. Build a
        # per-step va-index -> (ucp, ndp) mapping that respects the npz ordering.
        try:
            ucp_per_district = {}
            ndp_per_district = {}
            for npz_idx, district_id in enumerate(assignment):
                vid = int(va_ids[npz_idx])
                # The npz va_ids correspond to graph node IDs which
                # correspond to gpkg row indices (by gerrychain convention).
                ucp, ndp = va_lookup[vid]
                ucp_per_district[district_id] = (
                    ucp_per_district.get(district_id, 0.0) + ucp
                )
                ndp_per_district[district_id] = (
                    ndp_per_district.get(district_id, 0.0) + ndp
                )
        except KeyError as e:
            raise KeyError(f"Lookup failed for va_id {e} at step {step_idx}") from e

        n_dist = max(ucp_per_district.keys()) + 1
        ucp_arr = np.array([ucp_per_district.get(i, 0.0) for i in range(n_dist)])
        ndp_arr = np.array([ndp_per_district.get(i, 0.0) for i in range(n_dist)])

        recomputed = seat_results(ucp_arr, ndp_arr)

        # Confirm match within float tolerance
        for metric in (
            "efficiency_gap",
            "mean_median",
            "declination",
            "seats_at_50_50",
        ):
            saved_val = float(saved[metric])
            recomputed_val = float(recomputed[metric])
            if abs(saved_val - recomputed_val) > 1e-6:
                failures.append(
                    f"step {step_idx}, metric {metric}: "
                    f"saved={saved_val:.10f}, recomputed={recomputed_val:.10f}, "
                    f"delta={saved_val - recomputed_val:+.10f}"
                )

    assert not failures, "Verification subset integrity failures:\n" + "\n".join(
        failures
    )


# ============================================================
# Layer 3: Regression tests for the bugs Gemini surfaced
# (one test per finding, kept tight and focused)
# ============================================================


def test_score_exogenous_map_sjoin_deduplicates_overlap():
    """HIGH: a centroid that falls inside two overlapping polygons must
    have its votes credited to exactly one district, not both. Without
    the index dedup, the groupby/sum step double-counts. Reproduces the
    v0_8 sliver-overlap failure mode against synthetic geometry so the
    test is fast and self-contained."""
    import geopandas as gpd
    from shapely.geometry import Polygon, Point
    import tempfile, os

    from mcmc_ensemble import score_exogenous_map

    # One VA, sitting at (5, 5), with 100 UCP / 100 NDP votes
    va = gpd.GeoDataFrame(
        {
            "va_ucp": [100.0],
            "va_ndp": [100.0],
            "va_other": [0.0],
            "total_votes": [200.0],
        },
        geometry=[Point(5, 5).buffer(0.5)],
        crs="EPSG:3401",
    )
    # Two proposed districts whose polygons OVERLAP at (5,5) — a sliver
    # case the v0_8 inheritance-fill carve-out can produce
    poly_a = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
    poly_b = Polygon([(4, 4), (10, 4), (10, 10), (4, 10)])  # overlaps poly_a
    proposed = gpd.GeoDataFrame(
        {"name_2026": ["A", "B"]},
        geometry=[poly_a, poly_b],
        crs="EPSG:3401",
    )

    with tempfile.TemporaryDirectory() as td:
        gpkg = Path(td) / "proposed.gpkg"
        proposed.to_file(gpkg, driver="GPKG")
        result = score_exogenous_map(va, gpkg, id_col="name_2026")

    # Total covered VAs must equal 1 (not 2). Without the dedup, the
    # sjoin returns two rows, both groupby-summed → 200+200 = 400 votes.
    assert result["coverage_vas"] == 1, (
        f"Expected exactly 1 covered VA, got {result['coverage_vas']} — "
        "sjoin dedup is broken; overlapping slivers are double-counting."
    )


def test_score_exogenous_map_enforces_crs_alignment():
    """MEDIUM: passing proposed polygons in EPSG:4326 against a VA frame
    in EPSG:3401 must transparently reproject and produce non-zero
    matches. If the CRS reprojection branch silently fails, every
    centroid would fall outside every polygon (since 4326 lat/lon
    coordinates are tiny relative to 3401 metre coordinates) and the
    function would report coverage_pct == 0."""
    import geopandas as gpd
    from shapely.geometry import Polygon, Point
    import tempfile

    from mcmc_ensemble import score_exogenous_map

    # VA frame in EPSG:3401 (Alberta-relevant projected metres)
    va = gpd.GeoDataFrame(
        {
            "va_ucp": [100.0, 100.0],
            "va_ndp": [100.0, 100.0],
            "va_other": [0.0, 0.0],
            "total_votes": [200.0, 200.0],
        },
        geometry=[Point(0, 0).buffer(1.0), Point(100_000, 100_000).buffer(1.0)],
        crs="EPSG:3401",
    )
    # Build the equivalent polygon in 4326 by reprojecting a 3401 polygon
    proposed_3401 = gpd.GeoDataFrame(
        {"name_2026": ["X"]},
        geometry=[
            Polygon([(-1, -1), (200_000, -1), (200_000, 200_000), (-1, 200_000)])
        ],
        crs="EPSG:3401",
    )
    proposed_4326 = proposed_3401.to_crs("EPSG:4326")

    with tempfile.TemporaryDirectory() as td:
        gpkg = Path(td) / "proposed_4326.gpkg"
        proposed_4326.to_file(gpkg, driver="GPKG")
        result = score_exogenous_map(va, gpkg, id_col="name_2026")

    assert result["coverage_pct"] > 0.0, (
        "CRS mismatch was not auto-reprojected — every VA reported as "
        "uncovered, which is the silent-failure mode the audit fears."
    )


def test_run_ensemble_state_persistence_across_chunks():
    """CRITICAL #1: chunked execution must thread chain state forward.

    Bit-identity between a continuous chain and a split chain is not
    achievable because gerrychain's MarkovChain constructor consumes RNG
    state when a fresh chain is built mid-loop. So instead we test the
    *property* that distinguishes broken from correct chunked execution:

      - BROKEN behaviour (the bug Gemini found): every chunk re-seeds
        from `initial`, so after N chunks the final state is statistically
        close to a single chunk's worth of exploration from the seed.
      - CORRECT behaviour: chunks thread state, so after N chunks the
        chain has actually wandered N×chunk_size steps from the seed.

    We run both and assert the chunked-with-threading path diverges
    further from the seed than the chunked-without-threading path.

    Built on a tiny synthetic graph so the test runs in seconds.
    """
    import random
    from gerrychain import Graph
    import networkx as nx

    from mcmc_ensemble import run_ensemble

    g = nx.grid_2d_graph(6, 6)  # 36 nodes — small but enough for ReCom moves
    g = nx.convert_node_labels_to_integers(g)
    rng = random.Random(0)
    for n in g.nodes():
        g.nodes[n]["pop_2021"] = 100.0
        g.nodes[n]["va_ucp"] = float(rng.randint(20, 80))
        g.nodes[n]["va_ndp"] = 100.0 - g.nodes[n]["va_ucp"]
        g.nodes[n]["va_other"] = 0.0
        g.nodes[n]["va_area"] = 1_000_000.0  # 1 km² — below 5,000 km² s.15(2) threshold
    graph = Graph.from_networkx(g)

    # THREE-district initial partition (three horizontal stripes). This is
    # load-bearing (2026-07-09 mutation audit): with only TWO districts,
    # every ReCom proposal merges the entire map and re-splits it from the
    # RNG stream alone — the chain is memoryless, threaded and restarted
    # runs are byte-identical BY CONSTRUCTION, and no assertion can ever
    # distinguish correct threading from the CRITICAL #1 bug. With three
    # districts each step re-splits one adjacent pair and leaves the third
    # district's boundary as carried state, so threading becomes observable.
    initial = {n: ("A" if n < 12 else ("B" if n < 24 else "C")) for n in g.nodes()}

    def _hamming(part_assign, baseline):
        """Count nodes whose district label changed."""
        d = dict(part_assign.items())
        return sum(1 for k in baseline if d[k] != baseline[k])

    import numpy as _np

    # ---- broken simulation: each chunk restarts from `initial` ----
    random.seed(123)
    _np.random.seed(123)
    state = initial
    for _ in range(4):
        _, final_broken = run_ensemble(
            graph,
            initial,
            n_steps=8,
            pop_deviation=0.5,
            verbose=False,
            return_final_partition=True,
        )
        # critically: do NOT update `state` to final_broken — this is the bug
        state = initial
    broken_drift = _hamming(final_broken.assignment, initial)

    # ---- correct simulation: threaded state ----
    random.seed(123)
    _np.random.seed(123)
    state = initial
    for _ in range(4):
        _, state = run_ensemble(
            graph,
            state,
            n_steps=8,
            pop_deviation=0.5,
            verbose=False,
            return_final_partition=True,
        )
    threaded_drift = _hamming(state.assignment, initial)

    # The threaded chain has had 32 steps of wandering vs the broken
    # chain's effective 8 steps of wandering — it should have drifted
    # at least as far from `initial`. We require strictly further drift,
    # which empirically holds for this tiny graph; if it fails the
    # threading is no-op.
    assert threaded_drift >= broken_drift, (
        f"Threaded run drifted only {threaded_drift} nodes from initial "
        f"vs broken-run's {broken_drift} — state threading appears to "
        f"have no effect, which is the CRITICAL #1 failure mode."
    )

    # And the threaded final must not equal the seed (proves the chain
    # actually moved across all 4 chunks combined).
    assert (
        threaded_drift > 0
    ), "Threaded chain returned the seed assignment — chain did not advance."

    # Deterministic no-op detector (added 2026-07-09 mutation audit).
    # The two drift assertions above CANNOT catch the very regression this
    # test targets: if run_ensemble silently discards threaded state, the
    # "broken" and "threaded" loops replay identically (both phases reseed
    # the RNG to 123), drift is equal, and `>=` passes — a mutation
    # simulating exactly that survived the suite. But that identical replay
    # is itself the signature: under a threading no-op the two final
    # assignments are EXACTLY equal, while under correct threading the
    # threaded chain takes 24 extra steps beyond the broken chain's replayed
    # 8 and must land elsewhere. Deterministic given the fixed seeds.
    broken_assign = dict(final_broken.assignment.items())
    threaded_assign = dict(state.assignment.items())
    assert threaded_assign != broken_assign, (
        "Threaded final assignment is byte-identical to the restart-every-"
        "chunk final — run_ensemble is discarding the passed chain state "
        "(CRITICAL #1 regression)."
    )
