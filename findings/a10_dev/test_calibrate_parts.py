# © Will Conner 2026 | GNU GPL v3.0 <https://www.gnu.org/licenses/gpl-3.0.html>
# Data: Elections Alberta (public domain) | https://ixby.github.io
"""
Unit test of the parts of analysis/scripts/a10_stepb_calibrate.py that do not need the assembly:
the sample-VA truth labelling (T1) and the composite-map construction (T4).

A "perfect assembly" is faked by labelling every VA with the official district its representative
point lies in. It must score T1 = 0 and a T4 delta of about 0. Two negative controls make sure the
checks can fail: wrong labels must be counted by name, and an omitted district must lose its VAs
from the composite's coverage.

Takes 2-4 minutes (mcmc_ensemble.build_va_graph and four score_exogenous_map calls).
Usage: C:/Users/email/.venvs/audit-k91/Scripts/python.exe -W ignore findings/a10_dev/test_calibrate_parts.py
"""
import sys
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "analysis" / "scripts"))

import a10_stepb_calibrate as S  # noqa: E402

t0 = time.time()
app7, maj, eds, name, truth = S.load_context()
known = S.tuning_known(app7, maj)
assert not (set(known) & set(name.values())), "tuning and sample must be disjoint"
print(f"sample {len(eds)}, known {len(known)}", flush=True)

va, _ = S.me.build_va_graph(verbose=False)
va3400 = va.to_crs(3400)
pts = gpd.GeoSeries(va3400.geometry.representative_point(), index=va.index, crs=3400)
print(f"VAs {len(va)}  crs {va.crs.to_epsg()}  ({time.time() - t0:.0f}s)", flush=True)

# fake perfect assembly: every VA carries the name of the official district holding its point
j = gpd.sjoin(gpd.GeoDataFrame(geometry=pts), maj[["key", "geometry"]], how="left", predicate="within")
j = j[~j.index.duplicated(keep="first")]
fake = j["key"].reindex(va.index)
labels = S.clean_labels(fake, va.index)
print(f"labelled {int(labels.notna().sum())} of {len(va)} VAs by official district", flush=True)

inside = S.sample_vas(pts, truth)
n_inside = sum(len(v) for v in inside.values())
assert n_inside > 0 and all(len(v) > 0 for v in inside.values()), {n: len(v) for n, v in inside.items()}
all_idx = [i for v in inside.values() for i in v]
assert len(all_idx) == len(set(all_idx)), "a VA is a sample VA of two districts"

# T1 positive: perfect labels
rows, wrong, total = S.score_t1(labels, inside, name)
assert total == n_inside and wrong == 0, (wrong, total)
print(f"T1 perfect labels: wrong {wrong}/{total}", flush=True)

# T1 negative control: 7 VAs unassigned, 5 given to another sample district
a, b = eds[0], eds[1]
bad = labels.copy()
bad.loc[inside[a][:7]] = None
bad.loc[inside[a][7:12]] = name[b]
rows_bad, wrong_bad, _ = S.score_t1(bad, inside, name)
assert wrong_bad == 12, wrong_bad
assert rows_bad[a]["va_wrong"] == 12
assert rows_bad[a]["va_wrong_assigned_to"] == {"(unassigned)": 7, name[b]: 5}, rows_bad[a]
assert all(rows_bad[n]["va_wrong"] == 0 for n in eds if n != a)
print(f"T1 negative control: wrong {wrong_bad} (7 None + 5 relabelled), destinations named", flush=True)

# T4 positive: composite from perfect labels
eg_off = S.me.score_exogenous_map(va, S.MAJ)
comp, used = S.composite_map(maj, va3400.geometry, labels, eds, name)
assert set(used) == set(name.values()), set(name.values()) - set(used)
eg_comp = S.score_composite(va, comp)
d = eg_comp["efficiency_gap"] - eg_off["efficiency_gap"]
print(f"T4 perfect labels: EG official {eg_off['efficiency_gap']:.6f}  composite {eg_comp['efficiency_gap']:.6f}  "
      f"delta {100 * d:.6f} points  coverage {eg_off['coverage_vas']} -> {eg_comp['coverage_vas']}", flush=True)
assert abs(d) < 1e-6, d
assert eg_comp["coverage_vas"] == eg_off["coverage_vas"]

# T4 negative control: leave one sample district out of the assembly
omit = eds[2]
lab_omit = labels.copy()
lab_omit[lab_omit == name[omit]] = None
comp2, used2 = S.composite_map(maj, va3400.geometry, lab_omit, eds, name)
assert name[omit] not in used2 and len(used2) == len(eds) - 1
eg2 = S.score_composite(va, comp2)
lost = eg_off["coverage_vas"] - eg2["coverage_vas"]
print(f"T4 omit {name[omit]}: coverage {eg_off['coverage_vas']} -> {eg2['coverage_vas']} (lost {lost}, "
      f"sample VAs of it {len(inside[omit])}); EG {eg2['efficiency_gap']:.6f}", flush=True)
assert lost == len(inside[omit]), (lost, len(inside[omit]))

# T4 negative control 2: move one district's VAs wholesale to another (labels swapped)
lab_swap = labels.copy()
lab_swap[labels == name[eds[3]]] = name[eds[4]]
comp3, used3 = S.composite_map(maj, va3400.geometry, lab_swap, eds, name)
assert name[eds[3]] not in used3 and used3[name[eds[4]]] == used[name[eds[3]]] + used[name[eds[4]]]
eg3 = S.score_composite(va, comp3)
print(f"T4 swap {eds[3]}->{eds[4]}: districts {len(comp3)} (was {len(comp)}), EG {eg3['efficiency_gap']:.6f}, "
      f"delta {100 * (eg3['efficiency_gap'] - eg_off['efficiency_gap']):.4f} points", flush=True)

print(f"OK ({time.time() - t0:.0f}s)")
