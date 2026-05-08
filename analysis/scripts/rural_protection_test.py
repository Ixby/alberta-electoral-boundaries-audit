"""Test the UCP-side argument: do the 2026 maps actually protect rural
representation, and which one does it better?

The argument under test: hybrid urban-rural EDs are needed because
otherwise Alberta's cities would dominate the legislature, drowning
out rural voters.

Truth check: the *Electoral Boundaries Commission Act* already provides
a rural-protection mechanism — section 15(2) permits up to four EDs
with -50% population deviation (where the standard limit is +/-25%).
A map that genuinely prioritises rural representation would (a) use
the 15(2) provision, and (b) keep rural EDs systematically under-
populated relative to urban ones.

This script compares the three maps (2019 enacted, 2026 majority,
2026 minority) on five tests:

1. How many s15(2) special-rural EDs each map declares
2. Average population in rural EDs vs urban EDs vs hybrid EDs
3. Per-voter representation weight (1/population) in rural vs urban
4. Where the hybrid EDs sit on the rural-urban population spectrum
5. Population variance across each map (the EBCA's actual proxy for
   "voter equality")
"""

# Version: 0.1 series  (last updated 2026-04-26)


import sys
from pathlib import Path
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

import sys
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parent.parent.parent
DATA = data_loader._resolve_path("data")

en19 = pd.read_csv(DATA / "alberta_2019_populations.csv")
maj = pd.read_csv(DATA / "majority_2026_populations.csv")
mino = pd.read_csv(DATA / "minority_2026_populations.csv")

print("Files loaded:")
print(f"  2019 enacted: {len(en19)} EDs, columns: {list(en19.columns)}")
print(f"  Majority 2026: {len(maj)} EDs, columns: {list(maj.columns)}")
print(f"  Minority 2026: {len(mino)} EDs, columns: {list(mino.columns)}")
print()


def classify(name, region_type=None):
    """Classify an ED as urban / rural / hybrid based on name and explicit type."""
    if region_type and isinstance(region_type, str):
        rt = region_type.lower()
        if "hybrid" in rt:
            return "hybrid"
        if "calgary" in rt or "edmonton" in rt:
            return "urban"
        if "rural" in rt:
            return "rural"
    name_l = name.lower() if isinstance(name, str) else ""
    # Hybrid markers
    # NOTE: any ED name that doesn't trigger one of these markers will hit the
    # ValueError at the bottom — there is no silent rural fallback. When
    # auditing a new map, add the ED name explicitly and document why.
    hybrid_markers = [
        "airdrie",
        "chestermere",
        "cochrane",
        "okotoks",
        "peigan",
        "bearspaw",
        "sturgeon",
        "sherwood park",
        "fort saskatchewan",
        # Small-city + rural pairings (city anchors a rural ring)
        "medicine hat",  # Brooks/Cypress + Medicine Hat
        "lac ste. anne",
        "lac ste anne",  # Lac Ste. Anne-Parkland
        "parkland",
    ]  # Parkland County wraps west Edmonton
    rural_only = [
        "banff",
        "kananaskis",
        "athabasca",
        "barrhead",
        "westlock",
        "battle river",
        "bonnyville",
        "cold lake",
        "innisfail",
        "lacombe",
        "drumheller",
        "drayton",
        "stony plain",
        "rocky",
        "wainwright",
        "vermilion",
        "lloydminster",
        "cardston",
        "siksika",
        "taber",
        "warner",
        "lethbridge-west",
        "wetaskiwin",
        "ponoka",
        "maskwacis",
        "yellowhead",
        "peace river",
        "central peace",
        "notley",
        "lesser slave",
        "fort mcmurray",
        "wood buffalo",
        "morinville",
        "olds",
        "didsbury",
        "three hills",
        "vulcan",
        "high river",
        "livingstone",
        "macleod",
        "spruce grove",
        "leduc",
        "nisku",
        "sundre",
        "clearwater",
        "rimbey",
        "grande prairie",
        "smoky",
        "wabasca",
        "lac la biche",
        "two hills",
        "vegreville",
        "redwater",
        "camrose",
        # Pure-rural EDs the bare county name didn't catch above
        "highwood",  # Highwood (south-central rural)
        "mountain view",  # Mountain View-Kneehill
        "kneehill",
    ]
    if any(h in name_l for h in hybrid_markers):
        # Calgary-Airdrie, Calgary-Peigan-Chestermere, Calgary-Foothills-Airdrie West, etc.
        if "calgary" in name_l or "edmonton" in name_l:
            return "hybrid"
        if "airdrie" in name_l and not any(
            c in name_l for c in ["calgary", "edmonton"]
        ):
            # Pure-Airdrie EDs (e.g. "Airdrie-East" 2019) are urban-suburban
            return "hybrid"
        return "hybrid"
    # Pure-Calgary / pure-Edmonton (no hybrid markers above)
    if "calgary-" in name_l or "edmonton-" in name_l:
        return "urban"
    if any(r in name_l for r in rural_only):
        return "rural"
    if "lethbridge" in name_l:
        # Lethbridge-East/West are urban; Lethbridge-Taber-Warner is hybrid
        if "taber" in name_l or "warner" in name_l:
            return "hybrid"
        return "urban"
    if "red deer" in name_l:
        if (
            "sylvan" in name_l
            or "blackfalds" in name_l
            or "lacombe" in name_l
            or "innisfail" in name_l
        ):
            return "hybrid"
        return "urban"
    if "st. albert" in name_l or "st albert" in name_l:
        if "sturgeon" in name_l:
            return "hybrid"
        return "urban"
    # No silent rural fallback. If a 2026 proposal introduces a new naming
    # convention (e.g. a brand-new suburban district), we must categorise it
    # explicitly rather than letting it drift into the rural bucket and
    # contaminate the rural-vs-urban population averages this test relies on.
    raise ValueError(
        f"Unclassified ED name: {name!r} (region_type={region_type!r}). "
        "Add it to hybrid_markers, rural_only, or an explicit branch above."
    )


def annotate(df, name_col="ed_name", pop_col="population"):
    region_col = "region_type" if "region_type" in df.columns else None
    out = df.copy()
    if region_col:
        out["category"] = [
            classify(n, r) for n, r in zip(out[name_col], out[region_col])
        ]
    else:
        out["category"] = [classify(n) for n in out[name_col]]
    out["pop"] = out[pop_col]
    return out


# 2019 enacted uses 'ed_name' and 'population_2017_report'
en19_a = annotate(en19, name_col="ed_name", pop_col="population_2017_report")
maj_a = annotate(maj, name_col="ed_name", pop_col="population")
mino_a = annotate(mino, name_col="ed_name", pop_col="population")


def summarise(df, label):
    total_pop = df["pop"].sum()
    n_eds = len(df)
    ideal = total_pop / n_eds
    print(f"\n=== {label} ===")
    print(
        f"  total pop: {total_pop:,.0f}    EDs: {n_eds}    ideal pop/ED: {ideal:,.0f}"
    )
    print()
    print(
        f"  {'category':<10} {'n_eds':>6} {'avg_pop':>10} {'min_pop':>10} {'max_pop':>10} {'avg_dev':>9}"
    )
    for cat in ["urban", "rural", "hybrid"]:
        sub = df[df["category"] == cat]
        if len(sub) == 0:
            continue
        avg = sub["pop"].mean()
        mn = sub["pop"].min()
        mx = sub["pop"].max()
        dev = (avg - ideal) / ideal * 100
        print(
            f"  {cat:<10} {len(sub):>6} {avg:>10,.0f} {mn:>10,.0f} {mx:>10,.0f} {dev:>+8.2f}%"
        )
    # Voter representation weight
    urban = df[df["category"] == "urban"]
    rural = df[df["category"] == "rural"]
    if len(urban) and len(rural):
        u_weight = 1 / urban["pop"].mean()
        r_weight = 1 / rural["pop"].mean()
        ratio = r_weight / u_weight
        print()
        print(f"  Per-voter representation weight ratio (rural / urban): {ratio:.3f}x")
        print(
            f"  Rural voters carry {(ratio - 1) * 100:+.1f}% more representation than urban voters"
        )
    return ideal


for df, label in [
    (en19_a, "2019 Enacted"),
    (maj_a, "2026 Majority"),
    (mino_a, "2026 Minority"),
]:
    summarise(df, label)

# Hybrid ED detail per map
print("\n\n=== HYBRID ED COMPARISON ===")
for df, label in [
    (en19_a, "2019 enacted"),
    (maj_a, "2026 majority"),
    (mino_a, "2026 minority"),
]:
    hybrids = df[df["category"] == "hybrid"]
    print(f"\n{label}: {len(hybrids)} hybrid EDs")
    for _, r in hybrids.sort_values("pop", ascending=False).iterrows():
        print(f"   {r['ed_name']:<55} pop {r['pop']:>7,.0f}")

# s15(2) special-rural identification
print("\n\n=== SPECIAL-RURAL (s.15(2)) USAGE ===")
for df, label, source_col in [
    (en19, "2019 enacted", None),  # 2019 doesn't have explicit s15_2 column
    (maj, "2026 majority", "is_s15_2" if "is_s15_2" in maj.columns else None),
    (mino, "2026 minority", None),
]:
    if source_col:
        s15 = df[df[source_col] == True]
        print(f"  {label}: {len(s15)} EDs declared under s.15(2)")
        for _, r in s15.iterrows():
            print(f"     {r['ed_name']}")
    else:
        print(f"  {label}: s15(2) flag not in source file")
