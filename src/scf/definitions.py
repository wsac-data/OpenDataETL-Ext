
class ConvertInfo:
    def __init__(self, default, types=None, add_suffix=False, add_horizontally=False):
        self.default = default
        if types is None:
            types = [None]
        assert isinstance(types, list)
        self.types = types
        self.add_suffix = add_suffix
        self.add_horizontally = add_horizontally


TYPES = [
    ('public', 'nominal'),
    ('internal', 'nominal'),
    ('public', 'real'),
    ('internal', 'real'),
]

URL = r'https://www.federalreserve.gov/econres/files/scf2016_tables_{source}_{dollar}_historical.xlsx'

HEADER_ROWS = {
    '1': [3, 4, 5],
    '2': [4, 5],
    '3': [3],
    '4': [3, 4],
    '13': [3, 4],
    '15': [3, 4],
    '16': [3],
    '17': [3, 4],
}

YEAR_INFO = {
    '1': {},
    '2': {'column': 0, 'regex': r'^\s*(\d{4})'},
    '3': {},
    '4': {},
    '13': {'cell': 'A2', 'regex': r'^\s*(\d{4})'},
    '15': {},
    '16': {},
    '17': {},
}

CONVERT_INFO = {
    '1': ConvertInfo('dollar_default', add_suffix=True, add_horizontally=True),
    '2': ConvertInfo('percent', add_suffix=True),
    '3': ConvertInfo('percent'),
    '4': ConvertInfo('dollar'),
    '13': ConvertInfo('identity', types=['percent', 'dollar'], add_suffix=True),
    '15': ConvertInfo('percent', add_horizontally=True),
    '16': ConvertInfo('percent'),
    '17': ConvertInfo('percent', add_suffix=True),
}

BEG_HEADERS = {
    '1': ['Characteristic', 'Sub-Characteristic'],
    '2': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '3': ['Sub-Characteristic'],
    '4': ['Characteristic', 'Sub-Characteristic'],
    '13': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '15': ['Characteristic', 'Sub-Characteristic'],
    '16': ['Sub-Characteristic'],
    '17': ['Characteristic', 'Sub-Characteristic'],
}
