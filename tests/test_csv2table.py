"""
"""

import filecmp


def test_csv2table():
    assert filecmp.cmp(
        'tests/reference_grid-caption.md',
        'tests/test_grid-caption.md'
    )
    assert filecmp.cmp(
        'tests/reference_grid-IO.md',
        'tests/test_grid-IO.md'
    )
    assert filecmp.cmp(
        'tests/reference_grid-noheader.md',
        'tests/test_grid-noheader.md'
    )
    assert filecmp.cmp(
        'tests/reference_grid-standardIO.md',
        'tests/test_grid-standardIO.md'
    )
    return
