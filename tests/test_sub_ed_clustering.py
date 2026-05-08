import pytest

def calculate_clustering_score(hybrid_districts, distance_matrix, threshold_km=50):
    """
    Calculates whether hybrid (fractured) districts are geographically clustered.
    """
    clustered_pairs = 0
    total_pairs = 0
    for i in range(len(hybrid_districts)):
        for j in range(i + 1, len(hybrid_districts)):
            total_pairs += 1
            dist = distance_matrix.get((hybrid_districts[i], hybrid_districts[j]), 999)
            if dist < threshold_km:
                clustered_pairs += 1
                
    return clustered_pairs / total_pairs if total_pairs > 0 else 0

def test_hybrid_clustering():
    hybrids = ["Airdrie1", "Airdrie2", "Calgary1", "Calgary2"]
    # Mock distances: Airdrie and Calgary are close
    dist_matrix = {
        ("Airdrie1", "Airdrie2"): 5,
        ("Calgary1", "Calgary2"): 10,
        ("Airdrie1", "Calgary1"): 30,
        ("Airdrie1", "Calgary2"): 35,
        ("Airdrie2", "Calgary1"): 25,
        ("Airdrie2", "Calgary2"): 30,
    }
    
    score = calculate_clustering_score(hybrids, dist_matrix)
    # 6 pairs total. All distances are < 50km. Score should be 1.0 (Highly clustered)
    assert score == 1.0
