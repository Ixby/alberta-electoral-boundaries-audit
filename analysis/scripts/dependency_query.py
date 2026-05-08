"""Dependency-graph invalidation query CLI.

Loads ``analysis/methodology/audit_dependency_graph.json`` and answers
questions of the form:

    "If reviewer invalidates node X, what fraction of findings in §5.2-§5.9
    are orphaned (lose all supporting paths to L0) vs robust (have ≥1
    independent path to L0)?"

Usage:

    python analysis/scripts/v0_1_dependency_query.py --invalidate <node_id>
    python analysis/scripts/v0_1_dependency_query.py --invalidate L1:constructed.dpg_v0_2_topoclean
    python analysis/scripts/v0_1_dependency_query.py --list-findings
    python analysis/scripts/v0_1_dependency_query.py --describe <node_id>
    python analysis/scripts/v0_1_dependency_query.py --run-worked-examples

Exit codes:
    0 = success; 1 = invalid node id; 2 = graph file missing.

Forward: (stdout analysis report)
Backward: analysis/methodology/audit_dependency_graph.json
"""
from __future__ import annotations

# Version: 0.1 series  (last updated 2026-04-26)


import argparse
import io
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

# Force UTF-8 stdout/stderr so the report's section-marker (§) and other
# non-ASCII glyphs survive on Windows console (cp1252 by default).
if hasattr(sys.stdout, "reconfigure"):
    try:  # pragma: no cover — Python 3.7+ always has reconfigure on TextIOBase
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

ROOT = Path(__file__).resolve().parent.parent.parent
GRAPH_JSON = ROOT / "analysis" / "methodology" / "audit_dependency_graph.json"


def load_graph() -> Dict[str, Any]:
    if not GRAPH_JSON.exists():
        print(
            f"error: graph file not found at {GRAPH_JSON}. "
            "Run analysis/scripts/v0_1_dependency_graph_build.py first.",
            file=sys.stderr,
        )
        sys.exit(2)
    return json.loads(GRAPH_JSON.read_text(encoding="utf-8"))


def build_indices(
    graph: Dict[str, Any],
) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, List[Tuple[str, str]]]]:
    """Return (nodes_by_id, back_adj[target] = [(source, edge_type), ...])."""
    nodes_by_id = {n["id"]: n for n in graph["nodes"]}
    back_adj: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for e in graph["edges"]:
        back_adj[e["target"]].append((e["source"], e["type"]))
    return nodes_by_id, back_adj


def reaches_l0(
    start: str,
    nodes_by_id: Dict[str, Dict[str, Any]],
    back_adj: Dict[str, List[Tuple[str, str]]],
    invalidated: Set[str],
) -> bool:
    """Return True iff ``start`` has a path back to an L0 node that does
    not pass through any invalidated node."""
    if start in invalidated:
        return False
    if nodes_by_id[start]["layer"] == "L0":
        return True
    seen: Set[str] = {start}
    stack: List[str] = [start]
    while stack:
        cur = stack.pop()
        for src, _etype in back_adj.get(cur, []):
            if src in invalidated or src in seen:
                continue
            if nodes_by_id[src]["layer"] == "L0":
                return True
            seen.add(src)
            stack.append(src)
    return False


def findings(nodes_by_id: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [n for n in nodes_by_id.values() if n["layer"] == "L3"]


def invalidate(graph: Dict[str, Any], targets: Iterable[str]) -> Dict[str, Any]:
    nodes_by_id, back_adj = build_indices(graph)
    targets_set = set(targets)
    missing = [t for t in targets_set if t not in nodes_by_id]
    if missing:
        return {"error": f"unknown node ids: {missing}"}

    # A node survives invalidation iff:
    #   * it is not in the invalidated set;
    #   * AND (it is L0, OR it has at least one inbound edge from a surviving
    #     source, AND every "required" inbound edge comes from a surviving
    #     source).
    # "corroborating" edges offer alternative paths — breaking one does not
    # invalidate the target as long as another surviving inbound edge exists.
    # "validating" edges are soft: they assert a gate has been applied, but
    # their invalidation does not by itself break the target.
    valid: Dict[str, bool] = {}

    def is_valid(nid: str, stack: List[str]) -> bool:
        if nid in valid:
            return valid[nid]
        if nid in stack:  # cycle — shouldn't happen on a DAG
            return False
        if nid in targets_set:
            valid[nid] = False
            return False
        node = nodes_by_id[nid]
        stack.append(nid)
        try:
            inbound = back_adj.get(nid, [])
            required_sources = [s for s, t in inbound if t == "required"]
            non_validating = [s for s, t in inbound if t != "validating"]
            # L0 nodes are axiomatic: valid if not directly invalidated AND
            # all of their required ancestors (if any) are valid. An L0 node
            # with no inbound edges is trivially valid.
            if node["layer"] == "L0":
                required_ok = all(is_valid(s, stack) for s in required_sources)
                if required_ok:
                    valid[nid] = True
                    return True
                valid[nid] = False
                return False
            # Non-L0: all required sources must be valid AND at least one
            # non-validating source must be valid.
            required_ok = all(is_valid(s, stack) for s in required_sources)
            any_supporting = any(is_valid(s, stack) for s in non_validating)
            if required_ok and any_supporting:
                valid[nid] = True
                return True
            valid[nid] = False
            return False
        finally:
            stack.pop()

    for nid in nodes_by_id:
        is_valid(nid, [])

    all_findings = findings(nodes_by_id)
    orphaned: List[str] = []
    robust: List[str] = []
    for f in all_findings:
        if valid[f["id"]]:
            robust.append(f["id"])
        else:
            orphaned.append(f["id"])

    return {
        "invalidated": sorted(targets_set),
        "total_findings": len(all_findings),
        "orphaned": sorted(orphaned),
        "robust": sorted(robust),
        "orphaned_count": len(orphaned),
        "robust_count": len(robust),
        "robustness_rate": (len(robust) / len(all_findings)) if all_findings else 0.0,
    }


def print_result(graph: Dict[str, Any], result: Dict[str, Any], verbose: bool) -> None:
    if "error" in result:
        print(result["error"], file=sys.stderr)
        sys.exit(1)

    nodes_by_id = {n["id"]: n for n in graph["nodes"]}
    total = result["total_findings"]
    invalidated = result["invalidated"]
    orphaned = result["orphaned"]
    robust = result["robust"]

    print("INVALIDATION QUERY")
    print("=" * 70)
    print(f"Invalidated node(s) ({len(invalidated)}):")
    for nid in invalidated:
        node = nodes_by_id.get(nid, {})
        print(f"  - {nid}  [{node.get('layer', '?')}]  {node.get('name', '')}")
    print()
    print(
        f"Of {total} L3 findings: "
        f"{len(robust)} robust ({result['robustness_rate']*100:.1f}%), "
        f"{len(orphaned)} orphaned ({(1 - result['robustness_rate'])*100:.1f}%)."
    )
    print()
    if orphaned:
        print(f"Orphaned findings ({len(orphaned)}):")
        for fid in orphaned:
            node = nodes_by_id.get(fid, {})
            section = node.get("report_section", "")
            print(f"  - §{section}  {node.get('name', fid)}")
        print()
    if verbose and robust:
        print(f"Robust findings ({len(robust)}):")
        for fid in robust:
            node = nodes_by_id.get(fid, {})
            section = node.get("report_section", "")
            print(f"  + §{section}  {node.get('name', fid)}")


WORKED_EXAMPLES: List[Tuple[str, List[str]]] = [
    (
        "Invalidate v0_2 topology-clean DPG",
        ["L1:constructed.dpg_v0_2_topoclean"],
    ),
    (
        "Invalidate 2023 Statement of Vote",
        ["L0:data.2023_statement_of_vote"],
    ),
    (
        "Invalidate commission map PNGs",
        ["L0:data.commission_map_pngs"],
    ),
    (
        "Invalidate 2021 census DAs (DA-anchoring + DA-pop paths)",
        ["L0:data.2021_das_gpkg", "L0:data.2021_da_populations"],
    ),
    (
        "Invalidate the 100k MCMC ensemble",
        ["L1:constructed.mcmc_ensemble_100k"],
    ),
]


def run_worked_examples(graph: Dict[str, Any]) -> None:
    for title, nids in WORKED_EXAMPLES:
        print("#" * 70)
        print(f"# {title}")
        print("#" * 70)
        result = invalidate(graph, nids)
        print_result(graph, result, verbose=False)
        print()


def describe(graph: Dict[str, Any], node_id: str) -> None:
    nodes_by_id, back_adj = build_indices(graph)
    if node_id not in nodes_by_id:
        print(f"error: unknown node id {node_id}", file=sys.stderr)
        sys.exit(1)
    node = nodes_by_id[node_id]
    out_adj: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
    for e in graph["edges"]:
        out_adj[e["source"]].append((e["target"], e["type"]))
    print(f"Node: {node_id}")
    for key, value in node.items():
        print(f"  {key}: {value}")
    print(f"Incoming ({len(back_adj[node_id])}):")
    for src, etype in back_adj[node_id]:
        print(f"  <- [{etype}] {src}")
    print(f"Outgoing ({len(out_adj[node_id])}):")
    for dst, etype in out_adj[node_id]:
        print(f"  -> [{etype}] {dst}")


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--invalidate",
        action="append",
        default=[],
        help="Node id to invalidate (may be given multiple times).",
    )
    parser.add_argument(
        "--list-findings",
        action="store_true",
        help="List all L3 findings.",
    )
    parser.add_argument(
        "--list-nodes",
        metavar="LAYER",
        help="List nodes in given layer (L0/L1/L2/L3).",
    )
    parser.add_argument(
        "--describe",
        metavar="NODE_ID",
        help="Describe a node: its attributes + incoming + outgoing edges.",
    )
    parser.add_argument(
        "--run-worked-examples",
        action="store_true",
        help="Run the 5 canonical worked-example queries.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="List robust findings in addition to orphaned.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the raw invalidation result as JSON.",
    )
    args = parser.parse_args(argv)

    graph = load_graph()

    if args.list_nodes:
        layer = args.list_nodes.upper()
        for n in graph["nodes"]:
            if n["layer"] == layer:
                print(f"  {n['id']}  {n.get('name', '')}")
        return 0
    if args.list_findings:
        for n in graph["nodes"]:
            if n["layer"] == "L3":
                print(
                    f"  §{n.get('report_section', '')}  {n['id']}  {n.get('name', '')}"
                )
        return 0
    if args.describe:
        describe(graph, args.describe)
        return 0
    if args.run_worked_examples:
        run_worked_examples(graph)
        return 0
    if args.invalidate:
        result = invalidate(graph, args.invalidate)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_result(graph, result, args.verbose)
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
