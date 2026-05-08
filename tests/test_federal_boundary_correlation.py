import pytest

def check_federal_boundary_splits(provincial_eds, federal_eds, overlap_threshold=0.9):
    """
    Checks if provincial districts actively break natural communities that
    federal districts kept whole. Returns ratio of disjointed overlaps.
    """
    violations = 0
    for prov in provincial_eds:
        # Check maximum overlap with any single federal district
        max_overlap = max(prov["overlap_with_fed"].values())
        if max_overlap < overlap_threshold:
            violations += 1
    return violations / len(provincial_eds)

def test_federal_correlation():
    provincial_eds = [
        {"name": "ED_1", "overlap_with_fed": {"Fed_A": 0.95, "Fed_B": 0.05}}, # Respects federal boundary
        {"name": "ED_2", "overlap_with_fed": {"Fed_C": 0.50, "Fed_D": 0.50}}  # Splits across two federal boundaries
    ]
    
    violation_rate = check_federal_boundary_splits(provincial_eds, federal_eds=None)
    assert violation_rate == 0.5 # 1 out of 2 violates
