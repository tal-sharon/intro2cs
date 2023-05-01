from typing import List, Tuple, Dict
import copy


class Car:
    """
    A car with a name, length, location and orientation
    A car can move in different direction according it's orientation
    """
    def __init__(self, name: str, length: int, location: Tuple[int, int], orientation: int) -> None:
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col) location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        # Note that this function is required in your Car implementation.
        # However, is not part of the API for general car types.
        # implement your code and erase the "pass"

        self.__name = name
        self.__length = int(length)
        self.__location = location
        self.__orientation = orientation
        # Orientation and length are static and unchangeable once a Car is initiated
        # You can get the orientation of the Car by possible_moves: up and down - vertical, left and right - horizontal
        # You can get the length of the car by the length of the list of car_coordinates it's in

    def car_coordinates(self) -> List[Tuple[int, int]]:
        """
        :return: A list of coordinates the car is in
        """
        # implement your code and erase the "pass"
        car_coor = []
        for cell in range(self.__length):
            if self.__orientation == 0:
                car_coor.append((self.__location[0] + cell, self.__location[1]))
            if self.__orientation == 1:
                car_coor.append((self.__location[0], self.__location[1] + cell))
        coor_copy = copy.deepcopy(car_coor)
        return coor_copy

    def possible_moves(self) -> Dict[str, str]:
        """
        :return: A dictionary of strings describing possible movements permitted by this car.
        """
        # For this car type, keys are from 'udrl'
        # The keys for vertical cars are 'u' and 'd'.
        # The keys for horizontal cars are 'l' and 'r'.
        # You may choose appropriate strings.
        # implement your code and erase the "pass"
        # The dictionary returned should look something like this:
        # result = {'f': "cause the car to fly and reach the Moon",
        #          'd': "cause the car to dig and reach the core of Earth",
        #          'a': "another unknown action"}
        # A car returning this dictionary supports the commands 'f','d','a'.
        pos_moves = dict()
        if self.__orientation == 0:
            pos_moves['u'] = "cause the car to move up the board"
            pos_moves['d'] = "cause the car to move down the board"
        if self.__orientation == 1:
            pos_moves['l'] = "cause the car to move left on the board"
            pos_moves['r'] = "cause the car to move right on the board"
        pos_moves_copy = copy.deepcopy(pos_moves)
        return pos_moves_copy

    def movement_requirements(self, movekey: str) -> List[Tuple[int, int]]:
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this move to be legal.
        """
        # For example, a car in locations [(1,2),(2,2)] requires [(3,2)] to
        # be empty in order to move down (with a key 'd').
        # implement your code and erase the "pass"
        req = []
        coor = self.car_coordinates()
        if movekey in self.possible_moves():
            if movekey == 'u':
                row, col = coor[0][0] - 1, coor[0][1]
                req.append((row, col))
            if movekey == 'd':
                row, col = coor[len(coor) - 1][0] + 1, coor[0][1]
                req.append((row, col))
            if movekey == 'l':
                row, col = coor[0][0], coor[0][1] - 1
                req.append((row, col))
            if movekey == 'r':
                row, col = coor[0][0], coor[len(coor) - 1][1] + 1
                req.append((row, col))
        req_copy = copy.deepcopy(req)
        return req_copy

    def move(self, movekey: str) -> bool:
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"
        if movekey in self.possible_moves():
            row, col = self.__location
            if movekey == 'u':
                self.__location = (row-1, col)
            if movekey == 'd':
                self.__location = (row+1, col)
            if movekey == 'l':
                self.__location = (row, col-1)
            if movekey == 'r':
                self.__location = (row, col+1)
            car_coor = self.car_coordinates()
            return True
        return False

    def get_name(self) -> str:
        """
        :return: The name of this car.
        """
        # implement your code and erase the "pass"
        return self.__name
