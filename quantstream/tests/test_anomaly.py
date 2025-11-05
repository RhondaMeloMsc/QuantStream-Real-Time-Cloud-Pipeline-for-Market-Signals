
from statistics import mean, pstdev

def z(series):
    if len(series) < 5:
        return 0.0
    m = mean(series)
    s = pstdev(series) if len(series) > 1 else 0.0
    return 0.0 if s == 0 else (series[-1] - m) / s

def test_basic_zscore():
    s = [100,101,102,103,104,105,106,107,108,300]
    val = z(s)
    assert abs(val) > 3.0  # last point is a big outlier
