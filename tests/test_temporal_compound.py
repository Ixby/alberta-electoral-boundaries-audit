import pytest

def simulate_heterogeneous_swing(base_votes, provincial_swing, regional_multipliers):
    """
    Applies non-uniform swing across regions and calculates seat counts.
    """
    projected_seats = {"ndp": 0, "ucp": 0}
    for ed in base_votes:
        multiplier = regional_multipliers.get(ed["region"], 1.0)
        local_swing = provincial_swing * multiplier
        
        ndp_pct = ed["ndp"] / (ed["ndp"] + ed["ucp"])
        projected_ndp_pct = ndp_pct + local_swing
        
        if projected_ndp_pct > 0.5:
            projected_seats["ndp"] += 1
        else:
            projected_seats["ucp"] += 1
            
    return projected_seats

def test_temporal_durability(sample_ed_results):
    regional_multipliers = {
        "Urban": 2.0, # Urban swings twice as hard
        "Rural": 0.2  # Rural swings very little
    }
    
    # 5 point swing to NDP
    seats_plus_5 = simulate_heterogeneous_swing(sample_ed_results, 0.05, regional_multipliers)
    
    # In base data: 1 safe NDP (70%), 1 marginal NDP (52%), 1 marginal UCP (48% NDP), 1 safe UCP (20% NDP)
    # Urban multiplier 2.0 -> swing is 0.10. Rural multiplier 0.2 -> swing is 0.01.
    # Safe NDP (Urban): 70% + 10% = 80% (NDP win)
    # Marginal NDP (Urban): 52% + 10% = 62% (NDP win)
    # Marginal UCP (Rural): 48% + 1% = 49% (UCP win) -> Fails to flip despite 5pt provincial swing!
    # Safe UCP (Rural): 20% + 1% = 21% (UCP win)
    
    assert seats_plus_5["ndp"] == 2
    assert seats_plus_5["ucp"] == 2
