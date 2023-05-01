from typing import Tuple, List

Coordinate = Tuple[int, int]


class Apple:
    """
    A class representing an Apple.
    An Apple has a location, a color and contains a score.
    An Apple can tell you it's location, color and score.
    """

    def __init__(self, x: int, y: int, score: int, color: str):
        self.__score = score
        self.__location = x, y
        self.__color = color

    def get_color(self) -> str:
        """
        Gets the color of the apple
        :return:
        """
        return self.__color

    def get_coordinates(self) -> List[Coordinate]:
        """
        Gets a list of all the coordinates of the apple
        :return:
        """
        return [self.__location]

    def get_score(self):
        """
        Gets the score an apple contains
        :return:
        """
        return self.__score