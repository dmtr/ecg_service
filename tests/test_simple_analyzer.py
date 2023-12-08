import pytest
from ecg_service.ecg.analyzers.simple import ZeroCrossingsAnalyzer


@pytest.mark.parametrize(
    "data,expected",
    [
        ([-1, 0, 1, 0, -1], 2),
        ([1, -1, 1, -1], 3),
        ([0, 0, 0, 0, 0], 0),
        ([], 0),
        ([1, 1, 1, 1], 0),
    ],
)
def test_count_zero_crossings_numpy(data, expected):
    analyzer = ZeroCrossingsAnalyzer()
    crossings = analyzer.count_zero_crossings(data)
    assert crossings == expected
