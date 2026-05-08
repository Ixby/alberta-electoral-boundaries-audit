import pytest

def analyze_commissioner_attribution(hybrid_districts, authorship_map):
    """
    Determines if specific gerrymandered fractures are authored by a single commissioner.
    """
    attribution_counts = {}
    for ed in hybrid_districts:
        author = authorship_map.get(ed, "Unknown")
        attribution_counts[author] = attribution_counts.get(author, 0) + 1
    return attribution_counts

def test_authorship_concentration():
    hybrids = ["Airdrie_NE", "Airdrie_NW", "Airdrie_SE", "Airdrie_SW"]
    authorship = {
        "Airdrie_NE": "Commissioner_A",
        "Airdrie_NW": "Commissioner_A",
        "Airdrie_SE": "Commissioner_A",
        "Airdrie_SW": "Commissioner_A"
    }
    
    counts = analyze_commissioner_attribution(hybrids, authorship)
    # Flag if one commissioner authored all the controversial splits in a zone
    assert counts["Commissioner_A"] == 4
