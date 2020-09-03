'''Unit tests for common.py.'''

from ..common import _read_candles


def test_read_candles(files: dict, tmp_path: str, candles: list):
    '''Test read CSV candles data from a disk.

    Args:
        files: A dictionary with csv files content.
        tmp_path: A path which authomatically created by pytest for testing.
        candles: An expected result.
    '''
    # Prepare files.
    for filename, content in files.items():
        filepath = tmp_path / filename
        with open(filepath, 'w') as f:
            f.write(content)

    currencies = sorted([f.split('.')[0] for f in files])

    # Compare results.
    assert _read_candles(tmp_path)['currencies'] == currencies
    assert _read_candles(tmp_path)['candles'] == candles
