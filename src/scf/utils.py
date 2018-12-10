from collections import OrderedDict
from openpyxl.worksheet.read_only import ReadOnlyWorksheet
import re


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


def get_table_num(sheet_name, regex=r'^Table (\d+)'):
    m = re.search(regex, sheet_name)
    if m is None:
        raise ValueError('"{0}" has no number!'.format(sheet_name))
    num = m.group(1)
    return num


def get_table_num_from_sheet(sheet):
    assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))
    return get_table_num(sheet.title)


def get_header_rows(sheet):
    num = get_table_num_from_sheet(sheet)
    return HEADER_ROWS[num]


def get_headers(sheet):
    assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))

    header_rows = get_header_rows(sheet)

    headers = OrderedDict()
    curr_data = [''] * len(header_rows)  # assume blank unless filled
    for c in range(1, sheet.max_column + 1):
        updated = False

        for i, r in enumerate(header_rows):
            v = str(sheet.cell(row=r, column=c).value or '')
            if v.strip():
                curr_data[i] = re.sub(r'[\r\n]', ' ', v, flags=re.I)
                updated = True
            elif i > 0:
                curr_data[i] = ''

        if not updated:
            break

        header_parts = [d.strip() for d in curr_data if d.strip()]
        if header_parts:
            header = ' - '.join(header_parts)
            headers[header] = c - 1  # maps to zero-based column number

    return headers


def get_year_info(sheet):
    num = get_table_num_from_sheet(sheet)
    return YEAR_INFO[num]


def get_year_by_cell(cell, regex, default=None):
    m = re.search(regex, str(cell.value or ''))
    if m is None:
        if default is None:
            raise ValueError('No matching value for year in cell: {0}'.format(cell))
        return int(default)
    return int(m.group(1))


def get_year(sheet, rows, default=None):
    year_info = get_year_info(sheet)

    if 'cell' in year_info:
        cell = sheet[year_info['cell']]
    elif 'column' in year_info:
        cell = rows[year_info['column']]
    else:
        raise ValueError('Must have either "cell" or "column" in YEAR_INFO!')

    regex = year_info['regex']

    return int(get_year_by_cell(cell, regex, default=default))


def is_number(v):
    try:
        float(v)
        return True
    except (ValueError, TypeError):
        return False


