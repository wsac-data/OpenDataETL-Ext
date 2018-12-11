

TYPES = [
    ('public', 'nominal'),
    ('internal', 'nominal'),
    ('public', 'real'),
    ('internal', 'real'),
]

URL = r'https://www.federalreserve.gov/econres/files/scf2016_tables_{source}_{dollar}_historical.xlsx'

HEADER_ROWS = {
    '2': [4, 5],
    '3': [3],
    '4': [3, 4],
    '13': [3, 4],
    '16': [3],
    '17': [3, 4],
}

YEAR_INFO = {
    '2': {'column': 0, 'regex': r'^\s*(\d{4})'},
    '3': {},
    '4': {},
    '13': {'cell': 'A2', 'regex': r'^\s*(\d{4})'},
    '16': {},
    '17': {},
}

CONVERT_INFO = {
    '2': {'default_converter': 'percent', 'types': ['percent'], 'add_suffix': True},
    '3': {'default_converter': 'percent', 'types': ['percent'], 'add_suffix': False},
    '4': {'default_converter': 'dollar', 'types': ['dollar'], 'add_suffix': False},
    '13': {'default_converter': 'identity', 'types': ['percent', 'dollar'], 'add_suffix': True},
    '16': {'default_converter': 'percent', 'types': ['percent'], 'add_suffix': False},
    '17': {'default_converter': 'percent', 'types': ['percent'], 'add_suffix': True},
}

BEG_HEADERS = {
    '2': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '3': ['Sub-Characteristic'],
    '4': ['Characteristic', 'Sub-Characteristic'],
    '13': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '16': ['Sub-Characteristic'],
    '17': ['Characteristic', 'Sub-Characteristic'],
}
