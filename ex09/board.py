from typing import List, Tuple, Optional, Dict
from car import Car
import copy


class Board:
    """
    A game board of 7x7 and an additional exit cell on the middle of it's right column (3, 7)
    The board contains cars which can't run over each other and can't be placed out of the boards borders
    """

    def __init__(self) -> None:
        # implement your code and erase the "pass"
        # Note that this function is required in your Board implementation.
        # However, is not part of the API for general board types.
        self.__board = []
        for row in range(7):
            row_lst = []
            for col in range(7):
                row_lst.append([(row, col), '_'])
            if row == 3:
                row_lst.append([(row, 7), 'E'])
            self.__board.append(row_lst)
        self.__cars: Dict[str, Car] = dict()

    def __str__(self) -> str:
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        # The game may assume this function returns a reasonable representation
        # of the board for printing, but may not assume details about it.
        string = []
        for row in range(len(self.__board)):
            row_str = []
            for col in range(len(self.__board[0])):
                row_str.append(self.__board[row][col][1])
                row_str.append(' ')
            if row == 3:
                row_str.append('E')
            else:
                row_str.append('*')
            row_str.append('\n')
            row_str = ''.join(row_str)
            string.append(row_str)
        string = ''.join(string)
        return string

    def cell_list(self) -> List[Tuple[int, int]]:
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        # In this board, returns a list containing the cells in the square
        # from (0,0) to (6,6) and the target cell (3,7)
        cell_lst = []
        for row in range(len(self.__board)):
            for col in range(len(self.__board[0])):
                cell_lst.append(self.__board[row][col][0])
            if row == 3:
                cell_lst.append(self.target_location())
        cells_copy = copy.deepcopy(cell_lst)
        return cells_copy

    def possible_moves(self) -> List[Tuple[str, str, str]]:
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name, movekey, description)
                 representing legal moves
        """
        # From the provided example car_config.json file, the return value could be
        # [('O','d',"some description"),('R','r',"some description"),('O','u',"some description")]

        cars = list(self.__cars.values())
        pos_moves = []
        for car in cars:
            coor = car.car_coordinates()
            pos = car.possible_moves()
            for move in pos:
                # for every move, check if move is out of border than check if another car is blocking the way
                if move == 'u' and coor[0][0] > 0:
                    row, col = coor[0]
                    if not self.cell_content((row-1, col)):
                        pos_moves.append((car.get_name(), move, pos[move]))

                if move == 'd' and coor[len(coor) - 1][0] < 6:
                    row, col = coor[len(coor) - 1]
                    if not self.cell_content((row+1, col)):
                        pos_moves.append((car.get_name(), move, pos[move]))

                if move == 'l' and coor[0][1] > 0:
                    row, col = coor[0]
                    if not self.cell_content((row, col-1)):
                        pos_moves.append((car.get_name(), move, pos[move]))

                if move == 'r' and coor[len(coor) - 1][1] < 7:
                    row, col = coor[len(coor) - 1]
                    if not self.cell_content((row, col+1)):
                        pos_moves.append((car.get_name(), move, pos[move]))

        moves_copy = copy.deepcopy(pos_moves)
        return moves_copy

    def target_location(self) -> Tuple[int, int]:
        """
        This function returns the coordinates of the location which is to be filled for victory.
        :return: (row,col) of goal location
        """
        # In this board, returns (3,7)
        return 3, 7

    def cell_content(self, coordinate) -> Optional[str]:
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        # implement your code and erase the "pass"
        for car in self.__cars.values():
            for coor in car.car_coordinates():
                if coor == coordinate:
                    return car.get_name()
        return None

    def add_car(self, car) -> bool:
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        # Remember to consider all the reasons adding a car can fail.
        # You may assume the car is a legal car object following the API.
        # implement your code and erase the "pass"

        car_name = car.get_name()
        # check if there is already a car with the same name on the board
        for name in self.__cars.keys():
            if name == car_name:
                return False

        for coor in car.car_coordinates():
            for value in coor:
                # check if car coordinates match the board's borders
                if not 0 <= value <= 6:
                    return False
            if self.cell_content(coor):
                # check if the designated coordinates of the car are empty
                return False

        # add car to dict of cars on board and to display
        self.__cars[car_name] = car
        for coor in car.car_coordinates():
            row, col = coor
            self.__board[row][col][1] = car_name
        return True

    def move_car(self, name, movekey) -> bool:
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        # implement your code and erase the "pass"

        # check if car is on board
        if name not in self.__cars.keys():
            return False

        car = self.__cars.get(name)

        # check if designated cells are empty
        for cell in car.movement_requirements(movekey):
            if self.cell_content(cell):
                return False

        # check if move is possible
        pos_moves = self.possible_moves()
        for move in pos_moves:
            if move[0] == name and move[1] == movekey:

                # delete current car displayed on board
                for coor in car.car_coordinates():
                    row, col = coor
                    self.__board[row][col][1] = '_'

                # move car and add to board display new coordinates
                car.move(movekey)
                for coor in car.car_coordinates():
                    row, col = coor
                    self.__board[row][col][1] = name
                return True

        return False
