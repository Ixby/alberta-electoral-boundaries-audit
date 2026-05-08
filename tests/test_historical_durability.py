import pytest

def evaluate_durability_over_time(map_biases_over_time, threshold=0.07):
    """
    Checks if a map's partisan bias holds up over historic polling cycles.
    """
    for month, bias in map_biases_over_time.items():
        if abs(bias) >= threshold:
            return False, month # Map broke the threshold, durability failed
    return True, None

def test_full_historical_backtest():
    # 338Canada backtest data
    biases = {
        "2020_01": -0.04,
        "2021_06": -0.05,
        "2023_05": -0.06,
        "2024_02": -0.08  # Fails durability at UCP low point
    }
    
    passed, failed_month = evaluate_durability_over_time(biases)
    assert passed is False
    assert failed_month == "2024_02"
