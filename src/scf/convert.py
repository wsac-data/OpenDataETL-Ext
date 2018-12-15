import definitions
import re
import utils

DOLLAR = ' ($)'
PERCENT = ' (%)'


class Converter:

    def __init__(self, add_suffix=True):
        self.add_suffix = add_suffix

    @property
    def units(self):
        raise NotImplementedError()

    def _convert(self, v):
        raise NotImplementedError()

    def set_header(self, h):
        pass

    def convert(self, v):
        v = utils.prepare_str(v)

        if not v or v == '*':
            return ''
        elif v in {'†', 'n.a.'}:
            return '0.0'
        else:
            try:
                return str(self._convert(v))
            except ValueError:
                return str(v)

    def convert_header(self, header, col_type=None):
        suffix = ''
        if self.add_suffix:
            suffix = get_suffix(col_type) if col_type else self.units
        return header + suffix

    def convert_headers(self, headers):
        return [self.convert_header(h) for h in headers]

    def iter_headers(self, headers, cvt_info=None):
        types = [None] if cvt_info is None else cvt_info.types
        for t in types:
            for h in headers:
                self.set_header(h)
                cvt = self.convert
                new_h = self.convert_header(h, col_type=t)
                yield h, new_h, cvt


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


class ThousandDollarDefaultConverter(Converter):

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        Converter.__init__(self, **kwargs)
        self._curr = None

    @property
    def units(self):
        return self._curr.units

    def set_header(self, h):
        Converter.set_header(self, h)
        self._curr = DataTypeConverter(h, ThousandDollarConverter(**self.kwargs), **self.kwargs)

    def _convert(self, v):
        return self._curr._convert(v)


class DataTypeConverter:
    thousand_dollars = 0
    percent = 1

    cvt = {
        None: IdentityConverter,
        'identity': IdentityConverter,
        'percent': PercentConverter,
        'dollar': ThousandDollarConverter,
        'dollar_default': ThousandDollarDefaultConverter,
        'column': Converter,
    }

    def __new__(cls, data_type_str, default=None, **kwargs):
        data_type_str = data_type_str.strip().lower()
        if re.search(r'thousands of (\d{4}\s+)?dollars', data_type_str, flags=re.I):
            return ThousandDollarConverter(**kwargs)
        elif re.search(r'percentage', data_type_str, flags=re.I):
            return PercentConverter(**kwargs)
        elif data_type_str in cls.cvt:
            return cls.cvt[data_type_str](**kwargs)
        else:
            if default is not None:
                if isinstance(default, Converter):
                    return default
                else:
                    return DataTypeConverter(default, **kwargs)
            else:
                return IdentityConverter(**kwargs)


def get_convert_info(sheet):
    num = utils.get_table_num_from_sheet(sheet)
    ci = definitions.CONVERT_INFO[num]
    return ci


def get_suffix(cvt_type=None):
    suffices = {
        None: '',
        'identity': '',
        'percent': PERCENT,
        'dollar': DOLLAR,
    }
    return suffices[cvt_type]


def get_default_converter_by_sheet(sheet):
    ci = get_convert_info(sheet)
    return DataTypeConverter(ci.default, add_suffix=ci.add_suffix)


def get_headers(sheet):
    num = utils.get_table_num_from_sheet(sheet)
    _, headers, _ = utils.get_input_headers(sheet)
    ci = get_convert_info(sheet)
    beg_headers = definitions.BEG_HEADERS[num]

    default = get_default_converter_by_sheet(sheet)
    return beg_headers + [new_h for _, new_h, _ in default.iter_headers(headers[1:], cvt_info=ci)]


def get_converters_by_header(sheet, headers):
    default = get_default_converter_by_sheet(sheet)
    return [DataTypeConverter(h, default=default) for h in headers]
