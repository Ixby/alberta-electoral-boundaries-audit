#!/usr/bin/env python
"""
Investigation 3: For the 4 Tier-C non-converged EDs, crop out native and
600-DPI-rendered versions side-by-side so we can assess whether higher
resolution reveals any new boundary features.

The 4 Tier-C EDs (Issue #3):
  - Fort McMurray-Lac La Biche (north — majority p82, minority p93 region)
  - Chestermere-Strathmore (near-Calgary — majority p78)
  - Edmonton-Beaumont (near-Edmonton — majority p80, or Edmonton p74)
  - Lethbridge-Taber-Warner (south — majority p84 or other_cities p76)

For each, we save a rectangular crop showing a small region of the
commission map at (a) native-raster resolution and (b) 600-DPI render
(interpolated). Both crops are exported as PNG at 1:1 pixel scale so
the reader can zoom in and compare detail.

Outputs:
  maps/hires_v2/tier_c_crops/<ed>_<kind>.png
  analysis/reports/v0_1_tier_c_crop_manifest.json
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "maps" / "hires_v2" / "tier_c_crops"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Each crop: (ed_label, native_png, native_box, render_png, render_box)
# The boxes are approximate relative regions (left_frac, top_frac, right_frac, bottom_frac).
# We lift the same fractional box and crop in both images to show the same area.
# The rendered image is ~1.82-2.35x the pixel resolution of the native, so at
# the same fractional crop the render has proportionally more pixels — but that
# extra pixel count is interpolation, not new detail.
TARGETS = [
    # Fort McMurray-Lac La Biche is in the north-east of AB — top-right of p82
    dict(
        ed="fort_mcmurray_lac_la_biche",
        native=ROOT / "maps" / "hires_v2" / "v0_2_native_majority_north_MAP_p82.png",
        render=ROOT / "maps" / "hires" / "v0_1_majority_p81_north.png",
        box_frac=(0.55, 0.05, 0.95, 0.45),
    ),
    # Chestermere-Strathmore — near-Calgary
    dict(
        ed="chestermere_strathmore",
        native=ROOT / "maps" / "hires_v2" / "v0_2_native_majority_near_calgary_MAP_p78.png",
        render=ROOT / "maps" / "hires" / "v0_1_majority_p77_near_calgary.png",
        box_frac=(0.5, 0.35, 0.95, 0.7),
    ),
    # Edmonton-Beaumont — south of Edmonton, visible on near-edmonton p80 and
    # edmonton p74
    dict(
        ed="edmonton_beaumont",
        native=ROOT / "maps" / "hires_v2" / "v0_2_native_majority_edmonton_MAP_p74.jpeg"
        if (ROOT / "maps" / "hires_v2" / "v0_2_native_majority_edmonton_MAP_p74.jpeg").exists()
        else ROOT / "maps" / "hires_v2" / "v0_2_native_majority_edmonton_MAP_p74.png",
        render=ROOT / "maps" / "hires" / "v0_1_majority_p74_MAP_r600.png",
        box_frac=(0.3, 0.65, 0.85, 0.98),
    ),
    # Lethbridge-Taber-Warner — south
    dict(
        ed="lethbridge_taber_warner",
        native=ROOT / "maps" / "hires_v2" / "v0_2_native_majority_central_MAP_p84.png",
        render=ROOT / "maps" / "hires" / "v0_1_majority_p85_south.png",
        box_frac=(0.05, 0.55, 0.65, 0.98),
    ),
]


def crop_from(path: Path, box_frac: tuple[float, float, float, float]) -> Image.Image:
    img = Image.open(path)
    w, h = img.size
    x1 = int(box_frac[0] * w)
    y1 = int(box_frac[1] * h)
    x2 = int(box_frac[2] * w)
    y2 = int(box_frac[3] * h)
    return img.crop((x1, y1, x2, y2))


def main():
    manifest = {"crops": []}
    for t in TARGETS:
        native_p = t["native"]
        render_p = t["render"]
        try:
            native_crop = crop_from(native_p, t["box_frac"])
            render_crop = crop_from(render_p, t["box_frac"])
        except FileNotFoundError as e:
            manifest["crops"].append(
                dict(ed=t["ed"], error=f"missing source: {e}")
            )
            continue
        out_native = OUT_DIR / f"{t['ed']}_native_raw.png"
        out_render = OUT_DIR / f"{t['ed']}_600dpi_render.png"
        native_crop.save(out_native)
        render_crop.save(out_render)
        manifest["crops"].append(
            dict(
                ed=t["ed"],
                native_source=str(native_p.relative_to(ROOT)),
                render_source=str(render_p.relative_to(ROOT)),
                native_crop_px=native_crop.size,
                render_crop_px=render_crop.size,
                pixel_ratio=round(render_crop.size[0] / native_crop.size[0], 2),
                out_native=str(out_native.relative_to(ROOT)),
                out_render=str(out_render.relative_to(ROOT)),
            )
        )
        print(f"{t['ed']}: native={native_crop.size}  render={render_crop.size}  "
              f"render/native={render_crop.size[0]/native_crop.size[0]:.2f}x")
    out_json = ROOT / "analysis" / "reports" / "v0_1_tier_c_crop_manifest.json"
    out_json.write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {out_json}")


if __name__ == "__main__":
    main()
