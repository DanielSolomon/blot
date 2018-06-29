import functools
import inspect
import pytest
import pyshart.graph

from .test_point import pos_number, neg_number

class PosInt:
    pass

class NegInt:
    pass

def default(func):
    """useful decorator for replacing default None values with some other values.
    
    :param func: function with annotations! to wrap its default values.
    :type func: function
    :return: function with other default values (PosInt -> random positive number, NegInt -> random negative number).
    :rtype: function
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_kwargs = kwargs.copy()
        for key, vtype in list(func.__annotations__.items())[len(args):]:
            if key not in new_kwargs:
                if vtype is PosInt:
                    new_kwargs[key] = pos_number()
                elif vtype is NegInt:
                    new_kwargs[key] = -pos_number()
        return func(*args, **new_kwargs)
    return wrapper

@pytest.fixture
@default
def empty_graph(
    pos_width   : PosInt = None,
    neg_width   : NegInt = None,
    pos_height  : PosInt = None,
    neg_height  : NegInt = None,
    step        : PosInt = None,
):
    pyshart.graph.Graph(
        points      = [],
        pos_width   = pos_width,
        neg_width   = neg_width,
        pos_height  = pos_height,
        neg_height  = neg_height,
        step        = step,
    )

edge_points = [
    (0, 0),             # zero point.
    (pos_number(), 0),  # positive x axis.
    (neg_number(), 0),  # negative x axis.
    (0, pos_number()),  # positive y axis.
    (0, neg_number()),  # negative y axis.
]

quarter_points = [
    (pos_number(), pos_number()),
    (pos_number(), neg_number()),
    (neg_number(), pos_number()),
    (neg_number(), neg_number()),
]

def _perpare_axis(point):
    pos_width   = abs(point.x) + 1 if point.x > 0 else 0,
    neg_width   = abs(point.x) + 1 if point.x < 0 else 0,
    pos_height  = abs(point.y) + 1 if point.y > 0 else 0,
    neg_height  = abs(point.y) + 1 if point.y < 0 else 0,
    if pos_width == 0 and neg_width == 0:
        pos_width = neg_width = 10
    if pos_height == 0 and neg_height == 0:
        pos_height = neg_height = 10
    return pos_width, neg_width, pos_height, neg_height
    
@pytest.mark.parametrize('x,y', edge_points + quarter_points)
def test_one_dot_insertion_graph(x, y):
    point = pyshart.graph.Point(x, y)
    pos_width, neg_width, pos_height, neg_height = _perpare_axis(point)
    
    eg = empty_graph(
        pos_width   = pos_width,
        neg_width   = neg_width,
        pos_height  = pos_height,
        neg_height  = neg_height,
        step        = 1,
    )
    eg[point] = 'X'

    # TODO: need to create graph with the only point...
    graph = pyshart.graph.Graph()

    assert eg._draw() == graph._draw()

@pytest.mark.parametrize('x,y', edge_points + quarter_points)
def test_one_dot_deletion_graph(x, y):
    point = pyshart.graph.Point(x, y)
    pos_width, neg_width, pos_height, neg_height = _perpare_axis(point)

    eg = empty_graph(
        pos_width   = pos_width,
        neg_width   = neg_width,
        pos_height  = pos_height,
        neg_height  = neg_height,
        step        = 1,
    )

    # TODO: need to create graph with the only point...
    graph = pyshart.graph.Graph()
    del graph[point]

    assert eg._draw() == graph._draw()
