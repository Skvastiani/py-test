from statistics import mean


def moving_average(values, period):
    if len(values) < period:
        return None
    return mean(values[-period:])


def compute_rsi(values, period=14):
    if len(values) <= period:
        return None
    gains = []
    losses = []
    for i in range(1, period + 1):
        diff = values[-i] - values[-i - 1]
        if diff >= 0:
            gains.append(diff)
        else:
            losses.append(-diff)
    average_gain = mean(gains) if gains else 0
    average_loss = mean(losses) if losses else 0
    if average_loss == 0:
        return 100.0
    rs = average_gain / average_loss
    return 100 - (100 / (1 + rs))
