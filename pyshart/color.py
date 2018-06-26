import colorama
colorama.init()


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



