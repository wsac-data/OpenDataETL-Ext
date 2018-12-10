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
import utils


def retrieve_data(workbook, pattern):

    wb = load_workbook(workbook, read_only=True)
    sheets = [n for n in wb.sheetnames if re.search(pattern, n, flags=re.I)]

    out_headers = []
    out_data = OrderedDict()
    for sheet_i, sheet_name in enumerate(sheets):

        print('Working on sheet "{0}"...'.format(sheet_name))

        sheet = wb[sheet_name]
        assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))

        headers = utils.get_headers(sheet)
        headers_list = list(headers.keys())

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

            year = utils.get_year(sheet, row, default=year)

            if utils.is_number(row[check_col].value or ''):
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


def transform(workbook, pattern, output):
    """
    Transform data within a messy Excel workbook file

    :param workbook: Workbook file path
    :param pattern: Pattern of sheet names to extract
    :param output: File path to CSV output file
    :return: Returns transformed workbook
    """

    print('Saving to {0}'.format(output))
    start = time()
    mkfdirp(output)
    with open(output, 'w', newline='\n') as f:
        headers, data = retrieve_data(workbook, pattern)
        cw = csv.DictWriter(f, fieldnames=headers)
        cw.writeheader()
        for row in data.values():
            cw.writerow(row)

    print('Finished in {0:.1f} seconds'.format(time() - start))


def transform_all(workbook, pattern, output):

    if '{source}' in workbook or '{dollar}' in workbook:
        for source, dollar in utils.TYPES:
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
