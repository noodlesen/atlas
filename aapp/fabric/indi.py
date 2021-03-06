
"""TA INDICATORS LIBRARY."""


def typical_price(bar):
    """Return Typical price."""
    return (bar['high'] + bar['low'] + bar['close']) / 3


def cci(data, n=0):
    """CCI indicator."""
    if n == 0:
        n = len(data)
    tp_price_list = [typical_price(d) for d in data]
    tp_avg = sum(tp_price_list) / n
    md = sum(
        [
            abs(tp_avg - tp) for tp in tp_price_list
        ]
    ) / 3
    md = 0.0000001 if md == 0 else md
    return round((typical_price(data[-1]) - tp_avg) / (0.015 * md), 2)


def sma(data, n=0, par='close'):
    """SMA indicator."""
    if n == 0:
        n = len(data)

    if len(data) < n:
        raise ValueError("data is too short")
        return None

    return sum([d[par] for d in data[-n:]]) / float(n)


def ema(data, n, par='close'):
    """EMA indicator."""
    if len(data) < 2 * n:
        raise ValueError("data is too short")
    c = 2.0 / (n + 1)
    current_ema = sma(data[-n * 2:-n], n, par)
    for value in data[-n:]:
        current_ema = (c * value[par]) + ((1 - c) * current_ema)
    return current_ema
