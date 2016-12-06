"""
"""

import filecmp


def test_csv2table():
    assert filecmp.cmp(
        'tests/grid.md',
        'tests/grid_reference.md'
    )
    return
