import pytest

from bbl.visualization import log_radius


@pytest.mark.parametrize(
    ("length", "expected"),
    [
        (1, 0),
        (3, 0),
        (4, 1),
        (31, 1),
        (32, 2),
        (316, 2),
        (317, 3),
    ],
)
def test_base_ten_geometric_boundaries(
    length: int,
    expected: int,
) -> None:
    assert log_radius(length, base=10) == expected
