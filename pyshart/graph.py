"""
Graph module that contains the Graph class and the Point namedtuple.
Provides utilities to save and format graph information.
"""
import dataclasses
import enum
import math
import typing

from . import color


class Quarter(enum.IntFlag):
    """
    Quarter bitwise enum.
    """
    QUARTER1    = 1
    QUARTER2    = 2
    QUARTER3    = 4
    QUARTER4    = 8
    NORTH_PLANE = QUARTER1 | QUARTER2
    WEST_PLANE  = QUARTER2 | QUARTER3
    SOUTH_PLANE = QUARTER3 | QUARTER4
    EAST_PLANE  = QUARTER4 | QUARTER1
    WHOLE_PLANE = NORTH_PLANE | SOUTH_PLANE

    @property
    def plane(self) -> 'Quarter':
        """
        Plane property is the closet plane that contains the sub-planes.

        :return: The closet quarter (sub-plane).
        :rtype: Quarter.
        """
        if self.name is None:
            return Quarter.WHOLE_PLANE
        return self


@dataclasses.dataclass
class Point:
    """
    Point dataclass that holds 'x' and 'y' value on a graph.
    """
    x: int
    y: int
    quarter: int = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        if self.x >= 0:
            if self.y >= 0:
                self.quarter = Quarter.QUARTER1
            else:
                self.quarter = Quarter.QUARTER4
        if self.x < 0:
            if self.y > 0:
                self.quarter = Quarter.QUARTER2
            else:
                self.quarter = Quarter.QUARTER3

    def __mul__(self, multiplier: int) -> 'Point':
        """
        Multiply (aka scale) the point by 'multiplier'.

        :param multiplier: scale multiplier.
        :type multiplier: int
        :return: Newly scales Point.
        :rtype: Point
        """
        return Point(self.x * multiplier, self.y * multiplier)

    __rmul__ = __mul__

    def scale(self, x: int, y: int) -> None:
        """
        Scale self by multiplying 'x' and 'y' with the relating point values.

        :param x: 'x' multiplier.
        :type x: int
        :param y: 'y' multiplier
        :type y: int
        :rtype: None
        """
        self.x *= x
        self.y *= y
        return self

@dataclasses.dataclass
class VisualPoint(Point):
    """
    VisualPoint dataclass that holds the point 'token' and the point 'color'.
    """
    token : str = 'X'
    fore  : str = ''
    back  : str = ''
    style : str = ''

    def __post_init__(self):
        # Interesting, if you do not call explicitly your super __post_init__ function it won't be invoked...
        super().__post_init__()
        if len(self.token) != 1:
            raise ValueError('token length must be of size 1')

    def tokenize(self) -> color.ColoredString:
        """tokenize returns the point's colored token.
        
        :rtype: color.ColoredString
        """

        return color.ColoredString(
            value   = self.token, 
            fore    = self.fore,
            back    = self.back,
            style   = self.style,
        )


class Graph:
    """
    Graph class to store information about a graph, format it and draw it contents to the screen.

    :raises IndexError: illegal access to the underlying array (index out of bounds).
    """
    def __init__(
            self,
            points  : typing.List[VisualPoint],
            height_x: int,
            height_y: int,
            step_x: int,
            step_y: int,
            normalizer_x: int,
            normalizer_y: int,
            negative_x: bool,
            negative_y: bool
    ):
        # TODO: (Daniel) Replace negative vars with get pos_width, neg_width, pos_height, neg_height with default values.
        #                The main reason is that the graph may not be symmetric.
        self.points   = points
        self.height_x = height_x
        self.height_y = height_y
        self.step_x = step_x
        self.step_y = step_y
        self.normalizer_x = normalizer_x
        self.normalizer_y = normalizer_y
        self.negative_x = negative_x
        self.negative_y = negative_y
        self.width = (height_x*2 if negative_x else height_x) + 1
        self.height = (height_y*2 if negative_y else height_y) + 1
        self.graph = [[' ']*(self.width) for _ in range(self.height)]
        self[(0, 0)] = '0'

        for i in range(self.height_x):
            self[(i+1, 0)] = str(int(self.step_x * (i+1)) % self.normalizer_x)
            if self.negative_x:
                self[(-(i+1), 0)] = str(int(self.step_x * (i+1)) % self.normalizer_x)
        for i in range(self.height_y):
            self[(0, i+1)] = str(int(self.step_y * (i+1)) % self.normalizer_y)
            if self.negative_y:
                self[(0, -(i+1))] = str(int(self.step_y * (i+1)) % self.normalizer_y)

        for point in self.points:
            # Meanwhile collisions are not solved (last point overrides).
            # TODO: (Daniel): Solve collisions.
            self[point] = str(point.tokenize())

    def __getitem__(self, point: Point) -> str:
        point = self._validate_point(point=point)
        point = self._transform_true_point(point=point)
        return self.graph[point.x][point.y]

    def __setitem__(self, point: Point, char: str) -> None:
        point = self._validate_point(point=point)
        point = self._transform_true_point(point=point)
        self.graph[point.x][point.y] = char

    def __delitem__(self, point: Point) -> None:
        point = self._validate_point(point=point)
        point = self._transform_true_point(point=point)
        self.graph[point.x][point.y] = ' '

    def _transform_true_point(self, point: Point) -> 'Point':
        """
        Construct a "true value" for the given Point in relation to the graph.

        :return: the constructed true Point.
        :rtype: Point
        """
        true_x = point.x + self.width  // 2 if self.negative_x else point.x
        true_y = point.y + self.height // 2 if self.negative_y else point.y
        return Point(true_x, true_y)

    def _validate_point(self, point: Point) -> None:
        """
        Validate a given point against the graph.

        :param point: Point to check against the graph.
        :type point: Point
        :raises IndexError: if the Point has an illegal index (negative / out of bounds), raise.
        :rtype: None
        """
        if isinstance(point, (tuple, list)):
            point = Point(*point)
        if (point.x < 0 and not self.negative_x) or (point.y < 0 and not self.negative_y):
            raise IndexError("Illegal negative index value supplied!")
        if not -self.height_x <= point.x <= self.height_x or not -self.height_y <= point.y <= self.height_y:
            raise IndexError("Index value out of bounds!")
        return point

    def _draw(self) -> typing.List[str]:
        """
        Create a list of strings that represents the graph.

        :return: list of strings representing rows within the graph.
        :rtype: typing.List[str]
        """
        return [''.join(self.graph[i]) for i in range(len(self.graph))][::-1]

    def draw(self) -> None:
        """
        Draw the stored Graph to the screen.

        :return: this function only prints.
        :rtype: None
        """
        print('\n'.join(self._draw()))
