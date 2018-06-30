import colorama
import enum
import typing
colorama.init()

COLORED_FORE_DESCRIPTION_MAP = dict(
    bla     = colorama.Fore.BLACK,
    blu     = colorama.Fore.BLUE,
    c       = colorama.Fore.CYAN,
    g       = colorama.Fore.GREEN,
    lbla    = colorama.Fore.LIGHTBLACK_EX,
    lblu    = colorama.Fore.LIGHTBLUE_EX,
    lc      = colorama.Fore.LIGHTCYAN_EX,
    lg      = colorama.Fore.LIGHTGREEN_EX,
    lm      = colorama.Fore.LIGHTMAGENTA_EX,
    lr      = colorama.Fore.LIGHTRED_EX,
    lw      = colorama.Fore.LIGHTWHITE_EX,
    ly      = colorama.Fore.LIGHTYELLOW_EX,
    m       = colorama.Fore.MAGENTA,
    r       = colorama.Fore.RED,
    w       = colorama.Fore.WHITE,
    y       = colorama.Fore.YELLOW,
)

COLORED_BACK_DESCRIPTION_MAP = dict(
    bla     = colorama.Back.BLACK,
    blu     = colorama.Back.BLUE,
    c       = colorama.Back.CYAN,
    g       = colorama.Back.GREEN,
    lbla    = colorama.Back.LIGHTBLACK_EX,
    lblu    = colorama.Back.LIGHTBLUE_EX,
    lc      = colorama.Back.LIGHTCYAN_EX,
    lg      = colorama.Back.LIGHTGREEN_EX,
    lm      = colorama.Back.LIGHTMAGENTA_EX,
    lr      = colorama.Back.LIGHTRED_EX,
    lw      = colorama.Back.LIGHTWHITE_EX,
    ly      = colorama.Back.LIGHTYELLOW_EX,
    m       = colorama.Back.MAGENTA,
    r       = colorama.Back.RED,
    w       = colorama.Back.WHITE,
    y       = colorama.Back.YELLOW,
)

COLORED_STYLE_DESCRIPTION_MAP = dict(
    b = colorama.Style.BRIGHT,
    d = colorama.Style.DIM,
    n = colorama.Style.NORMAL,
)

class ColorType(enum.Enum):
    """
    ColorType enum holds colors options (fore, back and style).
    """

    FORE    = 1
    BACK    = 2
    STYLE   = 3

def get_color(key: str, ctype: ColorType = None) -> str:
    """
    Returns color code (from colorama) by string shortcut or full string.

    :param key: color shortcut key or full string
    :type key: str
    :param ctype: color type (fore/back/style), defaults to None
    :param ctype: ColorType, optional
    :return: color code from colorama
    :rtype: str
    """

    if ctype is None:
        ctype = ColorType.FORE

    def _get_color(key: str, ctype: str, kmap: typing.Dict) -> str:
        if key in kmap:
            return kmap[key]
        m = getattr(colorama, ctype)
        try:
            return getattr(m, key.upper())
        except AttributeError:
            raise KeyError(f'unknown color {key} of type {ctype}')
    
    if ctype == ColorType.FORE:
        return _get_color(key, 'Fore', COLORED_FORE_DESCRIPTION_MAP)
    elif ctype == ColorType.BACK:
        return _get_color(key, 'Back', COLORED_BACK_DESCRIPTION_MAP)
    elif ctype == ColorType.STYLE:
        return _get_color(key, 'Style', COLORED_STYLE_DESCRIPTION_MAP)
    else:
        raise ValueError(f'unknown color type {ctype}')


class ColoredString(str):
    """
    ColoredString object that wraps string and let you change it colors easily.
    """

    def __new__(cls, value, *args, **kwargs):
        return super().__new__(cls, value)

    def __init__(self, value, fore=None, back=None, style=None):
        self.value  = value
        self.fore   = fore
        self.back   = back
        self.style  = style

    @property
    def _value(self) -> str:
        fore    = self.fore                 if self.fore    is not None else ''
        back    = self.back                 if self.back    is not None else ''
        style   = self.style                if self.style   is not None else ''
        end     = colorama.Style.RESET_ALL  if any([fore, back, style]) else ''
        return fore + back + style + self.value + end

    def __str__(self) -> str:
        return self._value

    def __repr__(self) -> str:
        return f'ColoredString({self.value}, fore={self.fore}, back={self.back}, style={self.style})'

    def __add__(self, other: str) -> str:
        if not isinstance(other, str):
            raise TypeError('must be str, not {type(other)}')
        return self._value + other
    
    def __radd__(self, other: str) -> str:
        if not isinstance(other, str):
            raise TypeError('expected str not {type(other)}')
        return other + self._value

    def __mul__(self, other: int) -> str:
        if not isinstance(other, int):
            raise TypeError('can\'t multiply sequence by non-int of type \'{type(other)}\'')
        # In order to return a string with the color prefix and not multiple prefixes we create new ColoredString and take its value.
        return ColoredString(
            value   = self.value * other,
            fore    = self.fore,
            back    = self.back,
            style   = self.style,
        )._value

    __rmul__ = __mul__



