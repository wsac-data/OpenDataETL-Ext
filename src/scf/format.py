"""
Prepared for Chadd in response to Upwork posting

Developed by Andre Dozier 2018

Converts
"""

import argparse
from collections import OrderedDict
import convert
import csv
from openpyxl import load_workbook
from openpyxl.worksheet.read_only import ReadOnlyWorksheet
import os
import re
from time import time

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

YEAR_CELLS = {
    '2': 'Column 0',
    '13': 'A2',
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


def get_year_cell(sheet):
    num = get_table_num_from_sheet(sheet)
    return YEAR_CELLS[num]


def get_year(sheet, rows, default=None):
    year_cell = get_year_cell(sheet)
    m = re.search('column (\d+)', year_cell, flags=re.I)

    if m is not None:
        col = int(m.group(1))
        return int(rows[col].value or default or 0)

    else:
        return int(sheet[year_cell].value or default or 0)


def get_year_by_cell(cell, regex, default='err'):
    m = re.search(regex, str(cell.value or ''))
    if m is None:
        if default.startswith('err'):
            raise ValueError('No matching value for year in cell: {0}'.format(cell))
        return default
    return m.group(1)


def get_year_by_sheet(sheet, cell_name, regex):
    assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))
    return get_year_by_cell(sheet[cell_name], regex)


def is_number(v):
    try:
        float(v)
        return True
    except (ValueError, TypeError):
        return False


def retrieve_data(workbook, pattern):

    wb = load_workbook(workbook, read_only=True)
    sheets = [n for n in wb.sheetnames if re.search(pattern, n, flags=re.I)]

    out_headers = []
    out_data = OrderedDict()
    for sheet_i, sheet_name in enumerate(sheets):

        sheet = wb[sheet_name]
        assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))

        headers = get_headers(sheet)
        headers_list = list(headers.keys())

        print('Working on sheet "{0}" (year {1})...'.format(sheet_name, year))

        # headers
        curr_headers = ['Year', 'Characteristic', 'Sub-Characteristic'] + \
                       [h + convert.PERCENT for h in headers_list[1:]] + \
                       [h + convert.DOLLAR for h in headers_list[1:]]
        if sheet_i == 0:
            out_headers = curr_headers
        else:
            if curr_headers != out_headers:
                print('Differences:\n  {0}'.format('\n  '.join(set(out_headers) - set(curr_headers))))

        char_col = headers.pop(headers_list[0])
        check_col = headers[headers_list[1]]

        cvt = convert.IdentityConverter()
        characteristic = ''
        year = 0
        for row in sheet.rows:

            year = get_year(sheet, row, default=year)
            if is_number(row[check_col].value or ''):
                key = '__'.join([str(year), characteristic, row[char_col].value or ''])

                if key not in out_data:
                    out_data[key] = {
                        'Year': year,
                        'Characteristic': characteristic,
                        'Sub-Characteristic': row[char_col].value or '',
                    }

                # add data to row
                out_data[key].update({
                    cvt.convert_header(h): cvt.convert(row[c].value or '')
                    for h, c in headers.items()
                })

            else:
                characteristic = str(row[char_col].value or '').strip()
                if not characteristic and row[check_col].value:
                    cvt = convert.DataTypeConverter(str(row[check_col].value or '').strip())

    return out_headers, out_data


def mkdirp(file_dir):
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    return file_dir


def mkfdirp(file_path):
    mkdirp(os.path.dirname(file_path))
    return file_path


def transform(workbook, pattern, output, defn=None):
    """
    Transform data within a messy Excel workbook file

    :param workbook: Workbook file path
    :param pattern: Pattern of sheet names to extract
    :param output: File path to CSV output file
    :param defn: A subclass of WorkbookDataDefinition that reads information about the worksheet
    :return: Returns transformed workbook
    """

    print('Saving to {0}'.format(output))
    start = time()
    mkfdirp(output)
    with open(output, 'w', newline='\n') as f:
        headers, data = retrieve_data(workbook, pattern, defn=defn)
        cw = csv.DictWriter(f, fieldnames=headers)
        cw.writeheader()
        for row in data.values():
            cw.writerow(row)

    print('Finished in {0:.1f} seconds'.format(time() - start))


def transform_all(workbook, pattern, output):

    if '{source}' in workbook or '{dollar}' in workbook:
        for source, dollar in TYPES:
            wb_file = workbook.format(source=source, dollar=dollar)
            out_file = output.format(source=source, dollar=dollar)
            transform(wb_file, pattern, out_file)

    else:
        transform(workbook, pattern, output)


def main():
    parser = argparse.ArgumentParser(description='Transform data')

    parser.add_argument('workbook', type=str, help='Path to the workbook')
    parser.add_argument('pattern', type=str, help='REGEX pattern of the sheet names to extract')
    parser.add_argument('output', type=str, help='Location of CSV output file')

    args = parser.parse_args()

    transform_all(args.workbook, args.pattern, args.output)


if __name__ == '__main__':
    main()
