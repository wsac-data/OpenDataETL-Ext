import definitions
import re
import utils

DOLLAR = ' ($)'
PERCENT = ' (%)'


def remove_extra_whitespace(v):
    return re.sub(r'\s+', ' ', v)


def prepare_str(v):
    if v is None:
        v = ''

    v = str(v).strip()
    return remove_extra_whitespace(v)


class Converter:

    def __init__(self, add_suffix=True):
        self.add_suffix = add_suffix

    @property
    def units(self):
        raise NotImplementedError()

    def _convert(self, v):
        raise NotImplementedError()

    def convert(self, v):
        v = prepare_str(v)

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
        return header + (self.units if self.add_suffix else '')

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

    def __new__(cls, data_type_str, default=None):
        data_type_str = data_type_str.strip().lower()
        if re.search(r'thousands of (\d{4}\s+)?dollars', data_type_str):
            return ThousandDollarConverter()
        elif re.search(r'percentage', data_type_str):
            return PercentConverter()
        else:
            return default if default is not None else IdentityConverter()


def get_default_converter(cvt_type, add_suffix):
    cvt = {
        None: IdentityConverter(add_suffix),
        'identity': IdentityConverter(add_suffix),
        'percent': PercentConverter(add_suffix),
        'dollar': ThousandDollarConverter(add_suffix),
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
    cvt_info = definitions.CONVERT_INFO[num]
    return get_default_converter(cvt_info['default_converter'], cvt_info['add_suffix'])


def get_headers(sheet):
    num = utils.get_table_num_from_sheet(sheet)
    headers = utils.get_input_headers(sheet)
    headers_list = list(headers.keys())
    types = definitions.CONVERT_INFO[num]['types']
    add_suffix = definitions.CONVERT_INFO[num]['add_suffix']
    beg_headers = definitions.BEG_HEADERS[num]
    assert isinstance(types, list)

    return beg_headers + [h + (get_suffix(t) if add_suffix else '') for t in types for h in headers_list[1:]]

