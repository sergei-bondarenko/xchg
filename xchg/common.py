'''Common functions used by several sub-modules. It's for internal use only.'''

import csv
from os import path
from os import listdir


def _read_candles(data_path: str) -> list:
    '''Read all csv files with candles inside the directory.

    Args:
        data_path: Where csv files with data are stored.

    Returns:
        A dictionary containing a list of currencies and a list candles.
    '''
    candles = []
    csv_files = {}
    filenames = sorted(listdir(data_path))
    currencies = []

    for filename in filenames:
        currency = path.splitext(filename)[0]
        currencies.append(currency)
        csv_files[currency] = _read_csv(path.join(data_path, filename))

    candles_number = len(csv_files[currency])

    for i in range(candles_number):
        candles.append({})
        for currency in currencies:
            candles[i][currency] = dict(csv_files[currency][i])
    return {'currencies': sorted(currencies), 'candles': candles}


def _read_csv(filepath: str) -> list:
    '''Read csv file into list of rows.

    Args:
      filepath: Path to a csv file with data is stored.

    Returns:
        A list of rows.
    '''
    with open(filepath, newline='') as csvfile:
        result = list(csv.DictReader(csvfile))
    return result
