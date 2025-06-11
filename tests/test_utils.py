from crypto_signals.utils import compute_rsi, moving_average


def test_moving_average():
    data = [1, 2, 3, 4, 5]
    assert moving_average(data, 3) == 4


def test_compute_rsi():
    prices = list(range(1, 20))
    rsi = compute_rsi(prices, period=14)
    assert 0 < rsi <= 100
