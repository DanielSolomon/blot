import colorama
import itertools
import pytest
import pyshart.color
import random
import string

from pyshart.tests.test_point import pos_number

FORES   = colorama.Fore.__dict__.keys()
BACKS   = colorama.Back.__dict__.keys()
STYLES  = colorama.Style.__dict__.keys()

@pytest.fixture
def rstr():
    return ''.join(random.choices(string.ascii_letters, k=20))

rstr1 = rstr
rstr2 = rstr


def get_from_colorama(module: str, attr: str) -> str:
    m = colorama.__getattribute__(module)
    return m.__getattribute__(attr)

@pytest.mark.parametrize('fore,back,style', itertools.product(FORES, BACKS, STYLES))
def test_colored_string_basic_functionality(rstr: str, fore: str, back: str, style: str) -> None:
    fore    = get_from_colorama('Fore', fore)
    back    = get_from_colorama('Back', back)
    style   = get_from_colorama('Style', style)
    cs = pyshart.color.ColoredString(rstr, fore, back, style)
    assert cs._value == fore + back + style + rstr + colorama.Style.RESET_ALL

def test_addition(rstr1: str, rstr2: str) -> None:
    cs1 = pyshart.color.ColoredString(rstr1, colorama.Fore.RED, colorama.Back.GREEN, colorama.Style.BRIGHT)
    cs2 = pyshart.color.ColoredString(rstr1, colorama.Fore.GREEN, colorama.Back.BLACK, colorama.Style.DIM)

    assert cs1 + cs2 == cs1._value + cs2._value
    assert cs1 + rstr2 == cs1._value + rstr2
    assert rstr1 + cs2 == rstr1 + cs2._value

def test_multiplication(rstr: str, pos_number: int) -> None:
    cs = pyshart.color.ColoredString(rstr, colorama.Fore.RED, colorama.Back.GREEN, colorama.Style.BRIGHT)
    assert cs * pos_number == pyshart.color.ColoredString(rstr * pos_number, colorama.Fore.RED, colorama.Back.GREEN, colorama.Style.BRIGHT)._value
    assert pos_number * cs == pyshart.color.ColoredString(pos_number * rstr, colorama.Fore.RED, colorama.Back.GREEN, colorama.Style.BRIGHT)._value
    