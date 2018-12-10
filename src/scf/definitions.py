

TYPES = [
    ('public', 'nominal'),
    ('internal', 'nominal'),
    ('public', 'real'),
    ('internal', 'real'),
]

URL = r'https://www.federalreserve.gov/econres/files/scf2016_tables_{source}_{dollar}_historical.xlsx'

HEADER_ROWS = {
    '2': [4, 5],
    '13': [3, 4],
}

YEAR_INFO = {
    '2': {'column': 0, 'regex': r'^\s*(\d{4})'},
    '13': {'cell': 'A2', 'regex': r'^\s*(\d{4})'},
}

CONVERT_INFO = {
    '2': {'default_converter': 'percent', 'types': ['percent']},
    '13': {'default_converter': 'identity', 'types': ['percent', 'dollar']},
}

BEG_HEADERS = {
    '2': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '13': ['Year', 'Characteristic', 'Sub-Characteristic'],
}
