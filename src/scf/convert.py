import definitions
import re
import utils

DOLLAR = ' ($)'
PERCENT = ' (%)'


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
        elif v == '†':
            return '0.0'
        else:
            try:
                return str(self._convert(v))
            except ValueError:
                return str(v)

    def convert_header(self, header):
        return header + self.units

    def convert_headers(self, headers):
        return [self.convert_header(h) for h in headers]


class IdentityConverter(Converter):

    @property
    def units(self):
        return ''

    def _convert(self, v):
        return v


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

    def __new__(cls, data_type_str, default=IdentityConverter):
        data_type_str = data_type_str.strip().lower()
        if re.search(r'thousands of (\d{4}\s+)?dollars', data_type_str):
            return ThousandDollarConverter()
        elif re.search(r'percentage', data_type_str):
            return PercentConverter()
        else:
            return default()


def get_default_converter(cvt_type=None):
    cvt = {
        None: IdentityConverter,
        'identity': IdentityConverter,
        'percent': PercentConverter,
        'dollar': ThousandDollarConverter,
    }
    return cvt[cvt_type]


def get_suffix(cvt_type=None):
    suffices = {
        None: '',
        'identity': '',
        'percent': PERCENT,
        'dollar': DOLLAR,
    }
    return suffices[cvt_type]


def get_default_converter_by_sheet(sheet):
    num = utils.get_table_num_from_sheet(sheet)
    return get_default_converter(definitions.CONVERT_INFO[num]['default_converter'])


def get_headers(sheet):
    num = utils.get_table_num_from_sheet(sheet)
    headers = utils.get_input_headers(sheet)
    headers_list = list(headers.keys())
    types = definitions.CONVERT_INFO[num]['types']
    beg_headers = definitions.BEG_HEADERS[num]
    assert isinstance(types, list)

    return beg_headers + [h + get_suffix(t) for t in types for h in headers_list[1:]]

