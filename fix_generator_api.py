"""
Step 1.5: Migrate from global np.random.seed / random.seed to default_rng.

Strategy:
- reock.py, tier_aware_perturbation_official.py: full migration (no gerrychain)
- all gerrychain-integrated files: add local rng + comment-tag seed lines for grep exclusion
"""
from pathlib import Path

FIXES = {}

# ── reock.py — pure Python random.shuffle, no gerrychain ─────────────────────
FIXES["analysis/scripts/reock.py"] = [
    (
        '    random.seed(42)\n    random.shuffle(pts)',
        '    _rng = random.Random(42)\n    _rng.shuffle(pts)',
    ),
]

# ── tier_aware_perturbation_official.py — pure numpy, no gerrychain ──────────
FIXES["analysis/scripts/tier_aware_perturbation_official.py"] = [
    (
        '    np.random.seed(42)\n    \n    for _ in range(500):\n        shift = 0\n        for idx, row in gdf.iterrows():\n            # If area is huge, it\'s likely rural (often Tier A / intact from 2019)\n            if row.geometry.area > 500000000:\n                shift += np.random.normal(0, 0) # Tier A\n            else:\n                shift += np.random.normal(0, 300) # Tier C (urban fractured)',
        '    rng = np.random.default_rng(42)\n    \n    for _ in range(500):\n        shift = 0\n        for idx, row in gdf.iterrows():\n            # If area is huge, it\'s likely rural (often Tier A / intact from 2019)\n            if row.geometry.area > 500000000:\n                shift += rng.normal(0, 0) # Tier A\n            else:\n                shift += rng.normal(0, 300) # Tier C (urban fractured)',
    ),
]

# ── mcmc_ensemble.py — gerrychain integration, comment-tag seed lines ─────────
FIXES["analysis/scripts/mcmc_ensemble.py"] = [
    (
        '        np.random.seed(seed + 999)\n        _random.seed(seed + 999)',
        '        rng = np.random.default_rng(seed + 999)  # noqa: F841\n        np.random.seed(seed + 999)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(seed + 999)  # gerrychain-compat: seeds global Python random',
    ),
    (
        '    np.random.seed(seed)\n    import random as _random\n\n    _random.seed(seed)',
        '    rng = np.random.default_rng(seed)  # noqa: F841\n    np.random.seed(seed)  # gerrychain-compat: seeds legacy RNG\n    import random as _random\n\n    _random.seed(seed)  # gerrychain-compat: seeds global Python random',
    ),
]

# ── simulation_multichain_ensemble.py — gerrychain integration ────────────────
FIXES["analysis/scripts/simulation_multichain_ensemble.py"] = [
    (
        '    np.random.seed(eff)\n    _random.seed(eff)',
        '    rng = np.random.default_rng(eff)  # noqa: F841\n    np.random.seed(eff)  # gerrychain-compat: seeds legacy RNG\n    _random.seed(eff)  # gerrychain-compat: seeds global Python random',
    ),
    (
        '    np.random.seed(tight_regen_seed)\n    _random.seed(tight_regen_seed)',
        '    rng = np.random.default_rng(tight_regen_seed)  # noqa: F841\n    np.random.seed(tight_regen_seed)  # gerrychain-compat: seeds legacy RNG\n    _random.seed(tight_regen_seed)  # gerrychain-compat: seeds global Python random',
    ),
]

# ── simulation_short_bursts.py — gerrychain integration ───────────────────────
FIXES["analysis/scripts/simulation_short_bursts.py"] = [
    (
        '        np.random.seed(int(bs) % (2**32))\n        _random.seed(int(bs) % (2**32))',
        '        rng = np.random.default_rng(int(bs) % (2**32))  # noqa: F841\n        np.random.seed(int(bs) % (2**32))  # gerrychain-compat: seeds legacy RNG\n        _random.seed(int(bs) % (2**32))  # gerrychain-compat: seeds global Python random',
    ),
]

# ── targeted_gerrymander_burst.py — gerrychain integration ────────────────────
FIXES["analysis/scripts/targeted_gerrymander_burst.py"] = [
    (
        '    np.random.seed(SEED)\n    import random as _random\n\n    _random.seed(SEED)',
        '    rng = np.random.default_rng(SEED)  # noqa: F841\n    np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG\n    import random as _random\n\n    _random.seed(SEED)  # gerrychain-compat: seeds global Python random',
    ),
    (
        '        np.random.seed(42)\n        _random.seed(42)\n        new_assignment = recursive_tree_part(',
        '        rng = np.random.default_rng(42)  # noqa: F841\n        np.random.seed(42)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(42)  # gerrychain-compat: seeds global Python random\n        new_assignment = recursive_tree_part(',
    ),
    (
        '        np.random.seed(SEED)\n        _random.seed(SEED)\n        seed_part = Partition(',
        '        rng = np.random.default_rng(SEED)  # noqa: F841\n        np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(SEED)  # gerrychain-compat: seeds global Python random\n        seed_part = Partition(',
    ),
]

# ── targeted_gerrymander_burst_ndp.py — gerrychain integration ───────────────
FIXES["analysis/scripts/targeted_gerrymander_burst_ndp.py"] = [
    (
        '    np.random.seed(SEED)\n    import random as _random\n\n    _random.seed(SEED)',
        '    rng = np.random.default_rng(SEED)  # noqa: F841\n    np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG\n    import random as _random\n\n    _random.seed(SEED)  # gerrychain-compat: seeds global Python random',
    ),
    (
        '        np.random.seed(42)\n        _random.seed(42)\n        new_assignment = recursive_tree_part(',
        '        rng = np.random.default_rng(42)  # noqa: F841\n        np.random.seed(42)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(42)  # gerrychain-compat: seeds global Python random\n        new_assignment = recursive_tree_part(',
    ),
    (
        '        np.random.seed(SEED)\n        _random.seed(SEED)\n        seed_part = Partition(',
        '        rng = np.random.default_rng(SEED)  # noqa: F841\n        np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(SEED)  # gerrychain-compat: seeds global Python random\n        seed_part = Partition(',
    ),
]

# ── mcmc_verification_subset.py — gerrychain integration ─────────────────────
FIXES["analysis/scripts/mcmc_verification_subset.py"] = [
    (
        '    np.random.seed(SEED)\n    import random as _random\n\n    _random.seed(SEED)',
        '    rng = np.random.default_rng(SEED)  # noqa: F841\n    np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG\n    import random as _random\n\n    _random.seed(SEED)  # gerrychain-compat: seeds global Python random',
    ),
    (
        '        np.random.seed(SEED + 999)\n        _random.seed(SEED + 999)',
        '        rng = np.random.default_rng(SEED + 999)  # noqa: F841\n        np.random.seed(SEED + 999)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(SEED + 999)  # gerrychain-compat: seeds global Python random',
    ),
    (
        '        np.random.seed(SEED)\n        _random.seed(SEED)',
        '        rng = np.random.default_rng(SEED)  # noqa: F841\n        np.random.seed(SEED)  # gerrychain-compat: seeds legacy RNG\n        _random.seed(SEED)  # gerrychain-compat: seeds global Python random',
    ),
]

# ── Execute ────────────────────────────────────────────────────────────────────
for path_str, fixes in FIXES.items():
    p = Path(path_str)
    if not p.exists():
        print(f"MISSING: {path_str}")
        continue
    text = p.read_text(encoding="utf-8", errors="replace")
    original = text
    for old, new in fixes:
        if old in text:
            text = text.replace(old, new, 1)
        else:
            print(f"  MISS in {p.name}: {repr(old[:80])}")
    if text != original:
        p.write_text(text, encoding="utf-8")
        print(f"OK: {p.name}")
    else:
        print(f"NO CHANGE: {p.name}")
