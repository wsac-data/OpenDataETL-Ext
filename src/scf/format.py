"""
Prepared for Chadd in response to Upwork posting

Developed by Andre Dozier 2018

Converts
"""

import argparse
import csv
from collections import OrderedDict
from openpyxl import load_workbook
from openpyxl.worksheet.read_only import ReadOnlyWorksheet
import os
import re
from time import time

DOLLAR = ' ($)'
PERCENT = ' (%)'

DATA = [
    dict(url=r'https://www.federalreserve.gov/econres/files/scf2016_tables_internal_nominal_historical.xlsx'),
    dict(url=r'https://www.federalreserve.gov/econres/files/scf2016_tables_internal_real_historical.xlsx'),
    dict(url=r'https://www.federalreserve.gov/econres/files/scf2016_tables_public_nominal_historical.xlsx'),
    dict(url=r'https://www.federalreserve.gov/econres/files/scf2016_tables_public_real_historical.xlsx'),
]


class WorkbookDataDefinition:

    year_cell = 'A2'
    header_rows = [3, 4]

    def year(self, sheet):
        assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))
        return re.search(r'^\s*(\d{4})\b', str(sheet[self.year_cell].value or '')).group(1)

    def headers(self, sheet):
        assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))

        headers = OrderedDict()
        curr_data = [''] * len(self.header_rows)  # assume blank unless filled
        for c in range(1, sheet.max_column + 1):
            updated = False

            for i, r in enumerate(self.header_rows):
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


def is_number(v):
    try:
        float(v)
        return True
    except (ValueError, TypeError):
        return False


class Converter:

    @property
    def units(self):
        raise NotImplementedError()

    def _convert(self, v):
        raise NotImplementedError()

    def convert(self, v):
        if v is None:
            v = ''
        elif isinstance(v, str):
            v = v.strip()

        if not v or v == '*':
            return ''
        else:
            try:
                return str(self._convert(v))
            except ValueError:
                return str(v)

    def convert_header(self, header):
        return header + self.units

    def convert_headers(self, headers):
        return [self.convert_header(h) for  h in headers]


class ThousandDollarConverter(Converter):

    @property
    def units(self):
        return DOLLAR

    def _convert(self, v):
        return float(v) * 1000.0


class PercentConverter(Converter):

    @property
    def units(self):
        return PERCENT

    def _convert(self, v):
        return float(v) / 100.0


class DataTypeConverter:
    thousand_dollars = 0
    percent = 1

    def __new__(cls, data_type_str):
        data_type_str = data_type_str.strip().lower()
        if re.search(r'thousands of (\d{4}\s+)?dollars', data_type_str):
            return ThousandDollarConverter()
        elif re.search(r'percentage', data_type_str):
            return PercentConverter()
        else:
            return Converter()


def retrieve_data(workbook, pattern, defn=None):

    wb = load_workbook(workbook, read_only=True)
    sheets = [n for n in wb.sheetnames if re.search(pattern, n, flags=re.I)]

    if defn is None:
        defn = WorkbookDataDefinition
    reader = defn()

    out_headers = []
    out_data = OrderedDict()
    for sheet_i, sheet_name in enumerate(sheets):

        sheet = wb[sheet_name]
        assert isinstance(sheet, ReadOnlyWorksheet), 'Found type {0}'.format(type(sheet))

        year = reader.year(sheet)
        headers = reader.headers(sheet)
        headers_list = list(headers.keys())

        print('Working on sheet "{0}" (year {1})...'.format(sheet_name, year))

        # headers
        curr_headers = ['Year', 'Characteristic', 'Sub-Characteristic'] + \
                       [h + PERCENT for h in headers_list[1:]] + \
                       [h + DOLLAR for h in headers_list[1:]]
        if sheet_i == 0:
            out_headers = curr_headers
        else:
            if curr_headers != out_headers:
                print('Differences:\n  {0}'.format('\n  '.join(set(out_headers) - set(curr_headers))))

        char_col = headers.pop(headers_list[0])
        check_col = headers[headers_list[1]]

        cvt = Converter()
        characteristic = ''
        for row in sheet.rows:
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
                    cvt = DataTypeConverter(str(row[check_col].value or '').strip())

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


def main():
    parser = argparse.ArgumentParser(description='Transform data')

    parser.add_argument('workbook', type=str, help='Path to the workbook')
    parser.add_argument('pattern', type=str, help='REGEX pattern of the sheet names to extract')
    parser.add_argument('output', type=str, help='Location of CSV output file')

    args = parser.parse_args()

    transform(args.workbook, args.pattern, args.output)


if __name__ == '__main__':
    main()
