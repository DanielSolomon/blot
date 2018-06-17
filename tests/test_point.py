import blot.graph
import random
import pytest

@pytest.fixture
def number() -> int:
    return random.randint(-100, 100)

@pytest.fixture
def neg_number() -> int:
    return random.randint(-100, 0)

@pytest.fixture
def pos_number() -> int:
    return random.randint(0, 100)

# Simple hack to use multiple fixtures of the same type in one function.
number1 = number
number2 = number
negnum1 = neg_number
negnum2 = neg_number
posnum1 = pos_number
posnum2 = pos_number


@pytest.fixture
def point() -> blot.graph.Point:
    return blot.graph.Point(
        x = random.randint(-100, 100),
        y = random.randint(-100, 100),
    )

point1 = point
point2 = point

def test_dummy_point(number1: int, number2: int) -> None:
    p = blot.graph.Point(number1, number2)
    assert p.x == number1
    assert p.y == number2

def test_scale_point(point: blot.graph.Point, pos_number: int, neg_number: int) -> None:
    x = point.x
    y = point.y

    p1 = pos_number * point
    p2 = p1 * neg_number

    assert p1.x == pos_number * x
    assert p1.y == y * pos_number
    assert p2.x == p1.x * neg_number
    assert p2.y == neg_number * p1.y

def test_general_scale_point(point: blot.graph.Point, number1: int, number2: int) -> None:
    x = point.x
    y = point.y

    p1 = point.scale(
        x = number1, 
        y = number2,
    )

    assert p1.x == number1 * x
    assert p1.y == y * number2

def test_quarter(posnum1: int, posnum2: int, negnum1: int, negnum2: int) -> None:
    q1 = blot.graph.Point(posnum1, posnum2)
    q2 = blot.graph.Point(negnum1, posnum2)
    q3 = blot.graph.Point(negnum1, negnum2)
    q4 = blot.graph.Point(posnum1, negnum2)

    assert q1.quarter == blot.graph.Point.QUARTER1
    assert q2.quarter == blot.graph.Point.QUARTER2
    assert q3.quarter == blot.graph.Point.QUARTER3
    assert q4.quarter == blot.graph.Point.QUARTER4