import pytest

def compute_neighbour_drain(ed_data, adjacency_matrix, surplus_threshold=0.15, margin_threshold=0.05):
    """
    Simulates finding adjacent EDs where one is packed (surplus > threshold)
    and the other is cracked (margin < threshold).
    """
    signals = []
    for ed_x, data_x in ed_data.items():
        total_x = data_x["ndp"] + data_x["ucp"]
        if total_x == 0: continue
        ndp_share_x = data_x["ndp"] / total_x
        # Surplus logic: if they win by more than 50% + surplus_threshold
        if ndp_share_x > (0.5 + surplus_threshold):
            for ed_y in adjacency_matrix.get(ed_x, []):
                data_y = ed_data.get(ed_y)
                if not data_y: continue
                total_y = data_y["ndp"] + data_y["ucp"]
                if total_y == 0: continue
                ndp_share_y = data_y["ndp"] / total_y
                # Cracked logic: if they lose by less than margin_threshold
                if (0.5 - margin_threshold) <= ndp_share_y < 0.5:
                    signals.append((ed_x, ed_y))
    return signals

def test_neighbour_drain_adjacency():
    # Setup mock data for packing and cracking adjacent districts
    ed_data = {
        "ED_PACKED": {"ndp": 80, "ucp": 20}, # 80% NDP
        "ED_CRACKED": {"ndp": 48, "ucp": 52}, # 48% NDP
        "ED_SAFE": {"ndp": 20, "ucp": 80}
    }
    adjacency = {
        "ED_PACKED": ["ED_CRACKED", "ED_SAFE"],
        "ED_CRACKED": ["ED_PACKED", "ED_SAFE"],
        "ED_SAFE": ["ED_PACKED", "ED_CRACKED"]
    }
    
    signals = compute_neighbour_drain(ed_data, adjacency)
    
    assert len(signals) == 1
    assert signals[0] == ("ED_PACKED", "ED_CRACKED")
