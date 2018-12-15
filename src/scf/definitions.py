
class ConvertInfo:
    def __init__(self, default, types=None, add_suffix=False, header_rows=None, header=None, year_row=0):

        if types is None:
            types = [None]
        assert isinstance(types, list)

        self.header_rows = []
        if header_rows is not None:
            self.header_rows = header_rows

        self.header = ''
        if header is not None:
            self.header = header

        self.default = default
        self.types = types
        self.add_suffix = add_suffix
        self.year_row = year_row


TYPES = [
    ('public', 'nominal'),
    ('internal', 'nominal'),
    ('public', 'real'),
    ('internal', 'real'),
]

URL = r'https://www.federalreserve.gov/econres/files/scf2016_tables_{source}_{dollar}_historical.xlsx'

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
    '1': ConvertInfo('dollar_default', add_suffix=True, header_rows=[4, 5], year_row=3),
    '2': ConvertInfo('percent', add_suffix=True, header_rows=[4, 5]),
    '3': ConvertInfo('percent', year_row=3, header='Percent of Respondents'),
    '4': ConvertInfo('dollar', header_rows=[4], year_row=3),
    '13': ConvertInfo('identity', types=['percent', 'dollar'], add_suffix=True, header_rows=[3, 4]),
    '15': ConvertInfo('percent', header_rows=[4], year_row=3),
    '16': ConvertInfo('percent', year_row=3, header='Percent of Respondents'),
    '17': ConvertInfo('percent', add_suffix=True, header_rows=[4], year_row=4),
}

BEG_HEADERS = {
    '1': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '2': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '3': ['Year', 'Sub-Characteristic'],
    '4': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '13': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '15': ['Year', 'Characteristic', 'Sub-Characteristic'],
    '16': ['Year', 'Sub-Characteristic'],
    '17': ['Year', 'Characteristic', 'Sub-Characteristic'],
}
