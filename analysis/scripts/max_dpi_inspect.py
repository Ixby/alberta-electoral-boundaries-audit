#!/usr/bin/env python
"""
Investigation 1: Inspect the commission PDF to determine whether map pages
contain raster images or vector graphics, and if raster, the native DPI.

Forward deps: writes to analysis/reports/max_dpi_inspect.json
Backward deps: reads .temp/commission_report.pdf
"""

# Version: 0.1 series  (last updated 2026-04-26)

from __future__ import annotations

import json
from pathlib import Path

import pymupdf  # fitz

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / ".temp" / "commission_report.pdf"
OUT = ROOT / "analysis" / "reports" / "max_dpi_inspect.json"

# Pages of interest (1-indexed as named in our filenames; PyMuPDF is 0-indexed)
# Majority Appendix A: p71 overview, p72 Calgary MAP, p73 Calgary, p74 Edmonton MAP,
# p75 Edmonton, p76 Other cities MAP, p77 near-Calgary, p79 near-Edmonton,
# p81 north, p83 central, p85 south.
# Minority Appendix E per-ED thumbnails: p294, p296, p322, p351
# Minority Appendix E full map set: p352-355
# Minority map pages from earlier extraction: p359-p362 (v0_1_minority_p359_map73 etc.)
MAJORITY_PAGES = [71, 72, 73, 74, 75, 76, 77, 79, 81, 83, 85]
MINORITY_PAGES = [294, 296, 322, 351, 352, 353, 354, 355, 359, 360, 361, 362]


def inspect_page(doc, page_num_1: int) -> dict:
    """Inspect a single page; return native-DPI stats."""
    page = doc[page_num_1 - 1]
    rect = page.rect  # in points (1 pt = 1/72 inch)
    width_in = rect.width / 72.0
    height_in = rect.height / 72.0

    # Images on the page
    images = []
    for img in page.get_images(full=True):
        xref = img[0]
        info = doc.extract_image(xref)
        w = info.get("width", 0)
        h = info.get("height", 0)
        # Compute native DPI by finding how this image is placed on the page.
        # Use get_image_rects — returns rectangles in point-space where this
        # image is drawn.
        try:
            rects = page.get_image_rects(xref)
        except Exception:
            rects = []
        placements = []
        for r in rects:
            placed_w_in = r.width / 72.0
            placed_h_in = r.height / 72.0
            dpi_x = w / placed_w_in if placed_w_in > 0 else 0
            dpi_y = h / placed_h_in if placed_h_in > 0 else 0
            placements.append(
                dict(
                    placed_w_in=round(placed_w_in, 3),
                    placed_h_in=round(placed_h_in, 3),
                    dpi_x=round(dpi_x, 1),
                    dpi_y=round(dpi_y, 1),
                )
            )
        images.append(
            dict(
                xref=xref,
                pixel_w=w,
                pixel_h=h,
                ext=info.get("ext"),
                colorspace=info.get("colorspace"),
                bpc=info.get("bpc"),
                placements=placements,
            )
        )

    # Count vector drawings (paths) on the page.
    try:
        drawings = page.get_drawings()
    except Exception:
        drawings = []

    vector_path_count = len(drawings)
    # Rough sense of vector complexity — total number of items across all paths.
    vector_item_count = sum(len(d.get("items", [])) for d in drawings)

    # Text bytes
    text_len = len(page.get_text("text"))

    # Decide content type: if there's a big image that dominates the page, it's raster.
    # If vector_item_count is large (many paths) and no big dominant image, it's vector.
    dominant_image_frac = 0.0
    page_area_in2 = width_in * height_in
    for im in images:
        for p in im["placements"]:
            frac = (
                (p["placed_w_in"] * p["placed_h_in"]) / page_area_in2
                if page_area_in2 > 0
                else 0
            )
            dominant_image_frac = max(dominant_image_frac, frac)

    if dominant_image_frac > 0.3:
        content_type = "raster"
    elif vector_item_count > 500:
        content_type = "vector"
    elif dominant_image_frac > 0.05 and vector_item_count < 200:
        content_type = "mostly-raster"
    elif vector_item_count > 50:
        content_type = "mostly-vector"
    else:
        content_type = "text-or-minimal"

    # Max native DPI across the biggest image.
    max_dpi = 0.0
    for im in images:
        for p in im["placements"]:
            max_dpi = max(max_dpi, p["dpi_x"], p["dpi_y"])

    return dict(
        page=page_num_1,
        width_in=round(width_in, 3),
        height_in=round(height_in, 3),
        n_images=len(images),
        n_vector_paths=vector_path_count,
        n_vector_items=vector_item_count,
        text_chars=text_len,
        dominant_image_frac=round(dominant_image_frac, 3),
        max_native_dpi=round(max_dpi, 1),
        content_type=content_type,
        images=images,
    )


def main():
    doc = pymupdf.open(str(PDF))
    print(f"PDF has {doc.page_count} pages; inspecting target pages.")
    results = {
        "pdf": str(PDF),
        "pdf_n_pages": doc.page_count,
        "majority": [],
        "minority": [],
    }
    for p in MAJORITY_PAGES:
        if p - 1 < doc.page_count:
            r = inspect_page(doc, p)
            results["majority"].append(r)
            print(
                f"MAJ p{p}: type={r['content_type']}, n_img={r['n_images']}, "
                f"max_native_dpi={r['max_native_dpi']}, vec_items={r['n_vector_items']}"
            )
    for p in MINORITY_PAGES:
        if p - 1 < doc.page_count:
            r = inspect_page(doc, p)
            results["minority"].append(r)
            print(
                f"MIN p{p}: type={r['content_type']}, n_img={r['n_images']}, "
                f"max_native_dpi={r['max_native_dpi']}, vec_items={r['n_vector_items']}"
            )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
