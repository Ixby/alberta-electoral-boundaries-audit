import pytest

def find_fracture_networks(segments):
    """
    Finds connected components of boundary segments within a municipality.
    A set of segments that touch at endpoints forms a fracture network.
    
    segments: list of dicts, each with:
        - "endpoints": tuple of node IDs (e.g., (1, 2))
        - "eds": tuple of EDs separated by this segment
    """
    # Build adjacency list of segments (segments are adjacent if they share an endpoint)
    adj = {i: set() for i in range(len(segments))}
    for i, seg1 in enumerate(segments):
        for j, seg2 in enumerate(segments):
            if i != j:
                # If they share an endpoint (intersection is not empty)
                if set(seg1["endpoints"]) & set(seg2["endpoints"]):
                    adj[i].add(j)
                    adj[j].add(i)
                    
    # Find connected components (DFS)
    visited = set()
    components = []
    
    for i in range(len(segments)):
        if i not in visited:
            stack = [i]
            comp = set()
            while stack:
                curr = stack.pop()
                if curr not in visited:
                    visited.add(curr)
                    comp.add(curr)
                    stack.extend(adj[curr] - visited)
            
            # Extract unique EDs involved in this fracture network
            involved_eds = set()
            for idx in comp:
                involved_eds.update(segments[idx]["eds"])
                
            components.append({
                "segment_indices": comp,
                "eds": list(involved_eds)
            })
            
    return components

def detect_hub_and_spoke_bias(fracture_networks, vote_data, min_eds_in_hub=3):
    """
    Detects if a connected fracture network systematically disadvantages a party.
    Instead of just a linear chain, this detects radial (pizza-slice) or staggered hubs.
    """
    biased_hubs = []
    
    for net in fracture_networks:
        eds = net["eds"]
        if len(eds) >= min_eds_in_hub:
            ndp_losses = 0
            for ed in eds:
                results = vote_data.get(ed, {"ndp": 0, "ucp": 0})
                if results["ucp"] > results["ndp"]:
                    ndp_losses += 1
            
            # If the hub splits the city into 3+ pieces, and ALL (or almost all) pieces
            # land in districts that the urban party loses, it's a systemic drain.
            if ndp_losses >= 3:
                biased_hubs.append(net)
                
    return biased_hubs


def test_radial_pizza_slice_fracture():
    """
    Tests a classic 'pizza slice' or 'hub and spoke' fracture where 3 boundary lines
    meet at a central point (a Y-shape intersection).
    """
    # 3 boundary segments meeting at central vertex 0. 
    # They separate ED_A, ED_B, and ED_C.
    segments = [
        {"endpoints": (0, 1), "eds": ("ED_A", "ED_B")},
        {"endpoints": (0, 2), "eds": ("ED_B", "ED_C")},
        {"endpoints": (0, 3), "eds": ("ED_C", "ED_A")}
    ]
    
    # The vote data shows that despite being split from an urban center,
    # all three resulting districts are UCP-won (drained into rural surroundings).
    vote_data = {
        "ED_A": {"ndp": 45, "ucp": 55},
        "ED_B": {"ndp": 48, "ucp": 52},
        "ED_C": {"ndp": 49, "ucp": 51}
    }
    
    networks = find_fracture_networks(segments)
    assert len(networks) == 1  # All 3 segments form a single connected component
    assert len(networks[0]["eds"]) == 3
    
    biased = detect_hub_and_spoke_bias(networks, vote_data)
    assert len(biased) == 1
    # Successfully flagged the pizza-slice hub as biased!


def test_staggered_offset_fracture():
    """
    Tests a fracture that evades traditional 'hub' detectors because the segments 
    don't meet at a single central vertex, but are staggered (e.g. an H-shape).
    """
    # H-shape fracture inside a city, separating 4 EDs: ED_North, ED_South, ED_East, ED_West
    segments = [
        {"endpoints": (1, 2), "eds": ("ED_North", "ED_West")},  # Left arm top
        {"endpoints": (2, 3), "eds": ("ED_South", "ED_West")},  # Left arm bottom
        {"endpoints": (2, 4), "eds": ("ED_North", "ED_South")}, # The crossbar
        {"endpoints": (4, 5), "eds": ("ED_North", "ED_East")},  # Right arm top
        {"endpoints": (4, 6), "eds": ("ED_South", "ED_East")},  # Right arm bottom
    ]
    
    vote_data = {
        "ED_North": {"ndp": 40, "ucp": 60},
        "ED_South": {"ndp": 42, "ucp": 58},
        "ED_East":  {"ndp": 49, "ucp": 51},
        "ED_West":  {"ndp": 47, "ucp": 53}
    }
    
    networks = find_fracture_networks(segments)
    assert len(networks) == 1 # The H-shape is a single connected boundary network
    assert len(networks[0]["eds"]) == 4 # Involves 4 districts
    
    biased = detect_hub_and_spoke_bias(networks, vote_data)
    assert len(biased) == 1
    # Successfully flagged the staggered hub!
