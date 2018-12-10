from collections import OrderedDict
import csv
import definitions
from openpyxl.worksheet.read_only import ReadOnlyWorksheet
import os
import re


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
    return definitions.HEADER_ROWS[num]


def get_input_headers(sheet):
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
    return definitions.YEAR_INFO[num]


def get_year_by_cell(cell, regex, default=None):
    m = re.search(regex, str(cell.value or ''))
    if m is None:
        if default is None:
            raise ValueError('No matching value for year in cell: {0}'.format(cell))
        return int(default)
    return int(m.group(1))


def get_year(sheet, rows, default=None):
    year_info = get_year_info(sheet)

    if len(year_info) == 0:
        return 0

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


def mkdirp(file_dir):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    return file_dir


def mkfdirp(file_path):
    mkdirp(os.path.dirname(file_path))
    return file_path


def write_csv(output, headers, data):
    mkfdirp(output)
    with open(output, 'w', newline='\n') as f:
        cw = csv.DictWriter(f, fieldnames=headers)
        cw.writeheader()
        for row in data:
            cw.writerow(row)
