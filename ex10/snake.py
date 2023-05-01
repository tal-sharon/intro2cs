import copy
from typing import List, Tuple

Coordinate = Tuple[int, int]
POSSIBLE_MOVES = ['Up', 'Down', 'Left', 'Right']


class Snake:
    """
    A class which represents a snake.
    A Snake has color, length, direction and location.
    A Snake can move in 4 different directions (Up, Down, Left, Right), grow, change it's direction
    it knows or know when it is hitting himself, it can also give you it's coordinates, color
    and tell you where it's going to move next.
    """

    def __init__(self, color: str, length: int, direction: str, location: Coordinate) -> None:
        """
        Initiates a Snake object.
        :param color: The snake's color
        :param length: The snake's length
        :param direction: The snake's direction of movement
        :param location: The snake's head location
        """
        self.__color = color
        self.__length = length
        self. __direction = direction
        self.__location = location
        self.__coordinates: List[Tuple[int, int]] = self.initiate_snake_coordination()
        # the coordinates is a sorted list of all the snake's links, the head is always at the beginning.

    def initiate_snake_coordination(self) -> List[Coordinate]:
        """
        Initiates Snake's 'birth' coordinates by it's length, direction and location.
        :return: A list of all the Snake's coordinates
        """
        # add the head of the snake on snake's location
        coords = []
        length = self.__length
        direct = self.__direction
        col, row = self.__location
        coords.append((col, row))

        # check direction and add all other links of the snake accordingly

        if direct == 'Up':
            for link in range(1, length):
                coords.append((col, row - link))

        if direct == 'Down':
            for link in range(1, length):
                coords.append((col, row + link))

        if direct == 'Left':
            for link in range(1, length):
                coords.append((col + link, row))

        if direct == 'Right':
            for link in range(1, length):
                coords.append((col - link, row))

        # set updated coordinates in the objects attribute
        self.__coordinates = coords
        return copy.deepcopy(coords)

    def move_target(self) -> Coordinate:
        """
        Gets the coordinate which the snake's head is moving to.
        :return: A coordinate
        """

        direct = self.__direction
        col, row = self.__location
        new_head = self.__location

        if direct == 'Up':
            new_head = (col, row + 1)

        if direct == 'Down':
            new_head = (col, row - 1)

        if direct == 'Left':
            new_head = (col - 1, row)

        if direct == 'Right':
            new_head = (col + 1, row)

        return new_head

    def move(self, is_growing=False) -> List[Coordinate]:
        """
        Moves forward in the Snake's direction
        Updates Snake's coordinates based on the current coordinates, length and direction
        Inserts new coordinate at the beginning of the coordinates list (adds a new cell at the Snake's head)
        and pops and item from it's end (removes a cell from the snake's tail) if the Snake is not growing.
        :param is_growing: True - if the Snake is currently growing. False - otherwise
        :return: The updated coordinates of the Snake.
        """

        coords = self.__coordinates
        move_to = self.move_target()

        # move forward in the snake's direction - add a link in front of the snake
        coords.insert(0, move_to)
        if not is_growing:
            # if snake didn't eat an apple, pop the snake's tail coordinate from the snake's coordinate list
            coords.pop()

        # set the updated snake's location and coordinates attributes
        self.__coordinates = coords
        self.__location = coords[0]
        return copy.deepcopy(coords)

    def set_direction(self, direction) -> bool:
        """
        Sets new direction for the Snake.
        Set direction is limited by the Snake's current direction
        Can't set direction to the opposite of the current direction
        :param direction: the new direction we wish the Snake to go
        :return: True - upon success, False - otherwise
        """

        # check if current direction is horizontal, then check if player's chosen direction is vertical
        if self.__direction in ['Left', 'Right']:
            if direction in ['Up', 'Down']:
                self.__direction = direction
                return True
            return False

        # check if current direction is vertical, then check if player's chosen direction is horizontal
        if self.__direction in ['Up', 'Down']:
            if direction in ['Left', 'Right']:
                self.__direction = direction
                return True
            return False

        # direction is not in POSSIBLE_MOVES
        return False

    def get_color(self) -> str:
        """
        Gets the color of the Snake
        :return: None
        """
        return self.__color

    def hit_himself(self) -> bool:
        """
        Notifies if the Snake hits himself while moving
        :return: True - if the Snake hits himself, False - otherwise
        """
        coords = self.__coordinates
        coords_set = set(coords)
        if len(coords) != len(coords_set):
            return True
        return False

    def get_coordinates(self) -> List[Coordinate]:
        """
        Get the list of all the Snake's coordinates
        :return: A list of coordinates
        """
        coords = copy.deepcopy(self.__coordinates)
        return coords

    def remove_head(self) -> None:
        """
        Removes the head of the Snake
        :return: None
        """
        self.__coordinates = self.__coordinates[1::]