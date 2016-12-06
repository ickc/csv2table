"""
"""

import filecmp


def test_csv2table():
    assert filecmp.cmp(
        'tests/test_grid.md',
        'tests/reference_grid.md'
    )
    return
