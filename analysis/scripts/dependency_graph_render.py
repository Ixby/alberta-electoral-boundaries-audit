"""Render the audit dependency graph.

Primary path: shells out to Graphviz ``dot -Tsvg`` if available.

Fallback: emits a pure-Python SVG that layers L0/L1/L2/L3 vertically and
draws each node as a coloured box with its label. The fallback is legible
enough for PO review and does not depend on Graphviz being installed.

Usage:
    python analysis/scripts/v0_1_dependency_graph_render.py          # primary
    python analysis/scripts/v0_1_dependency_graph_render.py --pure   # force pure-Python

Outputs:
    maps/audit_dependency_graph.svg

Forward: maps/audit_dependency_graph.svg
Backward:
  analysis/methodology/audit_dependency_graph.json
  analysis/methodology/audit_dependency_graph.dot
"""

# Version: 0.1 series  (last updated 2026-04-26)


import sys
try:
    import data_loader
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "utils"))
    import data_loader

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH_JSON = ROOT / "analysis" / "methodology" / "audit_dependency_graph.json"
GRAPH_DOT = ROOT / "analysis" / "methodology" / "audit_dependency_graph.dot"
OUT_SVG = data_loader._resolve_path("data") / "maps" / "audit_dependency_graph.svg"


LAYER_FILL = {
    "L0": "#d0e8f2",
    "L1": "#ddebbd",
    "L2": "#fce4a7",
    "L3": "#f2c6c6",
}
LAYER_STROKE = {
    "L0": "#2a7aa8",
    "L1": "#6a8e33",
    "L2": "#b57c1b",
    "L3": "#b3403a",
}
LAYER_BAND_Y = {"L0": 0, "L1": 1, "L2": 2, "L3": 3}
LAYER_TITLE = {
    "L0": "L0 — Raw data",
    "L1": "L1 — Constructed data",
    "L2": "L2 — Measurement scripts",
    "L3": "L3 — Findings",
}
EDGE_COLOR = {
    "required": "#444444",
    "corroborating": "#2a7f2a",
    "validating": "#8a6200",
}
EDGE_DASH = {
    "required": "",
    "corroborating": "6,4",
    "validating": "2,3",
}


def try_dot(dot_path: Path, out_svg: Path) -> bool:
    """Attempt to render via Graphviz. Returns True on success."""
    dot = shutil.which("dot")
    if not dot:
        return False
    try:
        out_svg.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            [dot, "-Tsvg", str(dot_path), "-o", str(out_svg)],
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, OSError):
        return False


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _wrap(text: str, width: int) -> List[str]:
    words = text.split()
    lines: List[str] = []
    current = ""
    for w in words:
        if len(current) + len(w) + 1 > width:
            if current:
                lines.append(current)
            current = w
        else:
            current = (current + " " + w).strip() if current else w
    if current:
        lines.append(current)
    return lines[:5]  # cap at 5 lines to keep layout tight


def render_pure_python(graph: Dict[str, Any], out_svg: Path) -> None:
    nodes = graph["nodes"]
    edges = graph["edges"]
    by_layer: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for n in nodes:
        by_layer[n["layer"]].append(n)

    # Sort nodes in each layer by in-degree descending so the most-connected
    # nodes cluster near the centre — improves visual flow.
    indeg: Dict[str, int] = defaultdict(int)
    for e in edges:
        indeg[e["target"]] += 1
    for layer in by_layer:
        by_layer[layer].sort(key=lambda n: (-indeg[n["id"]], n.get("name", n["id"])))

    # Layout parameters — tuned for ~200 nodes to fit in a viewable SVG.
    box_w = 128
    box_h = 42
    h_gap = 8
    v_gap = 44  # between layer bands
    row_gap = 8  # between rows within a layer

    # Wrap each layer into rows. Target a consistent max columns so the whole
    # image stays within ~2500 px wide.
    nodes_per_row = 14

    layer_y: Dict[str, int] = {}
    layer_rows: Dict[str, List[List[Dict[str, Any]]]] = {}
    y_cursor = 40

    for layer in ("L0", "L1", "L2", "L3"):
        nodes_here = by_layer.get(layer, [])
        rows: List[List[Dict[str, Any]]] = []
        for i in range(0, len(nodes_here), nodes_per_row):
            rows.append(nodes_here[i : i + nodes_per_row])
        layer_rows[layer] = rows
        layer_y[layer] = y_cursor
        y_cursor += max(1, len(rows)) * (box_h + row_gap) + v_gap

    total_w = nodes_per_row * (box_w + h_gap) + 80
    total_h = y_cursor + 40

    # Build node position lookup.
    pos: Dict[str, Tuple[float, float]] = {}
    for layer in ("L0", "L1", "L2", "L3"):
        rows = layer_rows[layer]
        base_y = layer_y[layer]
        for ri, row in enumerate(rows):
            row_width = len(row) * (box_w + h_gap) - h_gap
            x_start = (total_w - row_width) / 2
            for ci, node in enumerate(row):
                x = x_start + ci * (box_w + h_gap)
                y = base_y + ri * (box_h + row_gap)
                pos[node["id"]] = (x, y)

    svg: List[str] = []
    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" '
        f'viewBox="0 0 {total_w} {total_h}" font-family="Helvetica, Arial, sans-serif">'
    )
    svg.append("<defs>")
    # Arrowhead markers per edge type.
    for etype, color in EDGE_COLOR.items():
        svg.append(
            f'<marker id="arrow_{etype}" viewBox="0 0 10 10" refX="10" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{color}" />'
            f"</marker>"
        )
    svg.append("</defs>")

    # Layer band backgrounds.
    for layer in ("L0", "L1", "L2", "L3"):
        rows = layer_rows[layer]
        if not rows:
            continue
        y = layer_y[layer] - 20
        h = max(1, len(rows)) * (box_h + row_gap) + 22
        svg.append(
            f'<rect x="10" y="{y}" width="{total_w - 20}" height="{h}" '
            f'fill="{LAYER_FILL[layer]}22" stroke="{LAYER_STROKE[layer]}" '
            f'stroke-width="0.5" rx="8" />'
        )
        svg.append(
            f'<text x="20" y="{y + 14}" font-size="12" font-weight="bold" '
            f'fill="{LAYER_STROKE[layer]}">{LAYER_TITLE[layer]}</text>'
        )

    # Edges — draw before nodes so nodes sit on top.
    # Reduce clutter by only drawing edges whose endpoints exist in the
    # position map (always true here).
    for e in edges:
        src = pos.get(e["source"])
        dst = pos.get(e["target"])
        if not src or not dst:
            continue
        x1, y1 = src[0] + box_w / 2, src[1] + box_h
        x2, y2 = dst[0] + box_w / 2, dst[1]
        etype = e.get("type", "required")
        color = EDGE_COLOR.get(etype, "#555555")
        dash = EDGE_DASH.get(etype, "")
        dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
        # Use a simple bezier for smoother lines.
        mid_y = (y1 + y2) / 2
        path = f"M {x1},{y1} C {x1},{mid_y} {x2},{mid_y} {x2},{y2}"
        svg.append(
            f'<path d="{path}" stroke="{color}" stroke-width="0.6" '
            f'fill="none" opacity="0.55" {dash_attr} '
            f'marker-end="url(#arrow_{etype})" />'
        )

    # Nodes.
    for n in nodes:
        if n["id"] not in pos:
            continue
        x, y = pos[n["id"]]
        layer = n["layer"]
        name = n.get("name", n["id"])
        section = n.get("report_section")
        title = f"§{section} — {name}" if section else name
        svg.append(
            f'<g><title>{_escape(title)} [{n["id"]}]</title>'
            f'<rect x="{x}" y="{y}" width="{box_w}" height="{box_h}" rx="5" '
            f'fill="{LAYER_FILL[layer]}" stroke="{LAYER_STROKE[layer]}" '
            f'stroke-width="1" />'
        )
        lines = _wrap(title, 26)
        for i, line in enumerate(lines):
            ly = y + 13 + i * 9
            svg.append(
                f'<text x="{x + 5}" y="{ly}" font-size="8" '
                f'fill="#222">{_escape(line)}</text>'
            )
        svg.append("</g>")

    # Legend.
    legend_y = total_h - 30
    svg.append(
        f'<g font-size="10" transform="translate(20 {legend_y})">'
        f'<rect x="-4" y="-14" width="460" height="20" fill="white" opacity="0.7"/>'
    )
    xoff = 0
    for label, color, dash in (
        ("required", EDGE_COLOR["required"], EDGE_DASH["required"]),
        ("corroborating", EDGE_COLOR["corroborating"], EDGE_DASH["corroborating"]),
        ("validating", EDGE_COLOR["validating"], EDGE_DASH["validating"]),
    ):
        dash_attr = f'stroke-dasharray="{dash}"' if dash else ""
        svg.append(
            f'<line x1="{xoff}" y1="0" x2="{xoff + 28}" y2="0" '
            f'stroke="{color}" stroke-width="2" {dash_attr}/>'
            f'<text x="{xoff + 32}" y="3" fill="#222">{label}</text>'
        )
        xoff += 140
    svg.append("</g>")

    svg.append("</svg>")

    out_svg.parent.mkdir(parents=True, exist_ok=True)
    out_svg.write_text("\n".join(svg), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pure",
        action="store_true",
        help="Force pure-Python SVG render, bypassing Graphviz.",
    )
    args = parser.parse_args()

    if not GRAPH_JSON.exists():
        print(
            f"error: graph file not found at {GRAPH_JSON}. "
            "Run v0_1_dependency_graph_build.py first.",
            file=sys.stderr,
        )
        return 2
    graph = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

    used_dot = False
    if not args.pure:
        used_dot = try_dot(GRAPH_DOT, OUT_SVG)

    if not used_dot:
        render_pure_python(graph, OUT_SVG)
        print(
            f"Graphviz not used (dot not available or --pure requested). "
            f"Emitted pure-Python SVG: {OUT_SVG.relative_to(ROOT)}"
        )
    else:
        print(f"Rendered via Graphviz dot: {OUT_SVG.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
