#!/usr/bin/env python
"""
Investigation 2: Extract the commission map pages at max useful resolution.

Strategy: every map page is a single dominant embedded raster image at ~300 or
~380-388 DPI native. We extract the raw embedded image (bit-exact native pixels)
and also render the full page at 600 DPI for direct comparison with the prior
hires/ set. Then we note that rendering above ~400 DPI gives no real new detail,
only interpolation.

Forward deps: maps/hires_v2/*.png, analysis/reports/v0_1_max_dpi_extract.json
Backward deps: .temp/commission_report.pdf
"""
from __future__ import annotations

import json
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / ".temp" / "commission_report.pdf"
OUT_DIR = ROOT / "maps" / "hires_v2"
OUT_JSON = ROOT / "analysis" / "reports" / "v0_1_max_dpi_extract.json"

# Tier-C non-converged EDs from Issue #3 — need extra attention
# (identified commission map coverage)
PAGE_MANIFEST = {
    # Majority Appendix A
    ("majority", 72): "calgary_MAP",
    ("majority", 74): "edmonton_MAP",
    ("majority", 76): "other_cities_MAP",
    ("majority", 78): "near_calgary_MAP",
    ("majority", 80): "near_edmonton_MAP",
    ("majority", 82): "north_MAP",
    ("majority", 84): "central_MAP",
    # Minority Appendix E — per-ED full maps start ~p91 and extend
    # to end. The ones we already cached at p359-362 are also in that range.
    ("minority", 91): "min_map1",
    ("minority", 93): "min_map2",
    ("minority", 95): "min_map3",
    ("minority", 101): "min_map_calgary",
    ("minority", 107): "min_map_edmonton",
}


def extract_native_and_render(doc, page_1: int, label: str) -> dict:
    page = doc[page_1 - 1]
    page_area_in2 = (page.rect.width / 72.0) * (page.rect.height / 72.0)

    result = {"page": page_1, "label": label, "outputs": []}

    # Extract the largest embedded image (the map itself).
    imgs = page.get_images(full=True)
    best = None
    for img in imgs:
        xref = img[0]
        info = doc.extract_image(xref)
        rects = page.get_image_rects(xref)
        if not rects:
            continue
        r = rects[0]
        w_in = r.width / 72.0
        h_in = r.height / 72.0
        frac = (w_in * h_in) / page_area_in2 if page_area_in2 else 0
        dpi = info["width"] / w_in if w_in else 0
        if frac > 0.3 and (best is None or frac > best["frac"]):
            best = dict(
                xref=xref,
                info=info,
                frac=frac,
                placed_w_in=w_in,
                placed_h_in=h_in,
                dpi=dpi,
            )

    if best is not None:
        ext = best["info"].get("ext", "png")
        native_path = OUT_DIR / f"v0_2_native_{label}_p{page_1}.{ext}"
        native_path.write_bytes(best["info"]["image"])
        result["outputs"].append(
            dict(
                kind="native_extract",
                path=str(native_path.relative_to(ROOT)),
                pixel_w=best["info"]["width"],
                pixel_h=best["info"]["height"],
                native_dpi=round(best["dpi"], 1),
                placed_w_in=round(best["placed_w_in"], 3),
                placed_h_in=round(best["placed_h_in"], 3),
            )
        )

    # Also render the whole page at 600 DPI (matches existing hires baseline).
    # And at 1200 DPI to confirm whether rendering above native yields anything.
    for render_dpi in (600, 1200):
        pix = page.get_pixmap(dpi=render_dpi, alpha=False)
        render_path = OUT_DIR / f"v0_2_render_{label}_p{page_1}_r{render_dpi}.png"
        pix.save(str(render_path))
        result["outputs"].append(
            dict(
                kind="page_render",
                path=str(render_path.relative_to(ROOT)),
                render_dpi=render_dpi,
                pixel_w=pix.width,
                pixel_h=pix.height,
                file_bytes=render_path.stat().st_size,
            )
        )

    return result


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(PDF))
    out = {"pdf": str(PDF), "pages": []}
    for (which, page_1), label in PAGE_MANIFEST.items():
        tag = f"{which}_{label}"
        print(f"Processing {which} p{page_1} ({label}) ...")
        try:
            r = extract_native_and_render(doc, page_1, tag)
            out["pages"].append(r)
        except Exception as e:
            print(f"  FAILED: {e}")
            out["pages"].append({"page": page_1, "label": tag, "error": str(e)})
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(out, indent=2))
    print(f"\nWrote {OUT_JSON}")
    print(f"Outputs in {OUT_DIR}")


if __name__ == "__main__":
    main()
