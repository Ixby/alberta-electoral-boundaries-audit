import pytest

def detect_boundary_chain_bias(chains, vote_data):
    """
    Detects if a chain of boundaries systematically disadvantages a party.
    """
    biased_chains = []
    for chain in chains:
        ndp_losses = 0
        for ed in chain:
            results = vote_data.get(ed, {"ndp": 0, "ucp": 0})
            if results["ucp"] > results["ndp"]:
                ndp_losses += 1
        if ndp_losses >= 3:
            biased_chains.append(chain)
    return biased_chains

def test_boundary_chain_systematic_bias():
    chains = [
        ["ED_RURAL_1", "ED_RURAL_2", "ED_RURAL_3"], # chain splitting a city
        ["ED_URBAN_1", "ED_URBAN_2"]
    ]
    vote_data = {
        "ED_RURAL_1": {"ndp": 45, "ucp": 55},
        "ED_RURAL_2": {"ndp": 48, "ucp": 52},
        "ED_RURAL_3": {"ndp": 49, "ucp": 51},
        "ED_URBAN_1": {"ndp": 60, "ucp": 40},
        "ED_URBAN_2": {"ndp": 65, "ucp": 35}
    }
    biased = detect_boundary_chain_bias(chains, vote_data)
    assert len(biased) == 1
    assert biased[0] == ["ED_RURAL_1", "ED_RURAL_2", "ED_RURAL_3"]
