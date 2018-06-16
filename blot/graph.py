"""
Graph module that contains the Graph class and the Point namedtuple.
Provides utilities to save and format graph information.
"""
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])


class Graph:
    """
    Graph class to store information about a graph, format it and draw it contents to the screen.

    :raises IndexError: illegal access to the underlying array (index out of bounds).
    """

    def __init__(
            self,
            length_x: int,
            length_y: int,
            step_x: int,
            step_y: int,
            normalizer_x: int,
            normalizer_y: int,
            negative_x: bool,
            negative_y: bool
    ):
        self.length_x = length_x
        self.length_y = length_y
        self.step_x = step_x
        self.step_y = step_y
        self.normalizer_x = normalizer_x
        self.normalizer_y = normalizer_y
        self.negative_x = negative_x
        self.negative_y = negative_y
        self.width = (length_x*2 if negative_x else length_x) + 1
        self.length = (length_y*2 if negative_y else length_y) + 1
        self.graph = [[' ']*(self.width) for _ in range(self.length)]
        self[(0, 0)] = '0'
        for i in range(self.length_x):
            self[(i+1, 0)] = str(int(self.step_x * (i+1)) % self.normalizer_x)
            if self.negative_x:
                self[(-(i+1), 0)] = str(int(self.step_x * (i+1)) % self.normalizer_x)
        for i in range(self.length_y):
            self[(0, i+1)] = str(int(self.step_y * (i+1)) % self.normalizer_y)
            if self.negative_y:
                self[(0, -(i+1))] = str(int(self.step_y * (i+1)) % self.normalizer_y)

    def __getitem__(self, point: Point) -> str:
        point = Point(*point)
        if (point.x < 0 and not self.negative_x) or (point.y < 0 and not self.negative_y):
            raise IndexError("Illegal negative index value supplied!")
        if not -self.length_x <= point.x <= self.length_x or not -self.length_y <= point.y <= self.length_y:
            raise IndexError("Index value out of bounds!")
        true_x = point.x + int(self.width / 2) if self.negative_x else point.x
        true_y = point.y + int(self.length / 2) if self.negative_y else point.y
        return self.graph[true_y][true_x]

    def __setitem__(self, point: Point, char: str) -> None:
        point = Point(*point)
        if (point.x < 0 and not self.negative_x) or (point.y < 0 and not self.negative_y):
            raise IndexError("Illegal negative index value supplied!")
        if not -self.length_x <= point.x <= self.length_x or not -self.length_y <= point.y <= self.length_y:
            raise IndexError("Index value out of bounds!")
        true_x = point.x + int(self.width / 2) if self.negative_x else point.x
        true_y = point.y + int(self.length / 2) if self.negative_y else point.y
        self.graph[true_y][true_x] = char

    def draw(self) -> None:
        """
        Draw the stored Graph to the screen.

        :return: this function only prints.
        :rtype: None
        """
        print('\n'.join([''.join(self.graph[i]) for i in range(len(self.graph))][::-1]))
