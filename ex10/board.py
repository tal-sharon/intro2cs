from apple import Apple
from bomb import Bomb
from snake import Snake
import functools as ft
from typing import Tuple, Any, List, Optional

Coordinate = Tuple[int, int]


class Board:
    """
    the class BOARD is responsible for all game's objects location and make them move
    A Board object has size: width and  height, list of Apples objects, Snake object and Bomb object
    A Board object can add snake/apple/bomb object, check a cell content, count empty cells in board, move snake on board,
     move bomb blast's, make list of all game's objects
    """

    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__apples = []
        self.__bombs = None
        self.__snake = None

    def cell_content(self, cell) -> Any:
        """
        Checks the content of a given cell
        :param cell: Coordinates of the checked cell
        :return: None if empty, otherwise - the object inside the cell
        """
        for player in self.get_board_objects():
            if player is not None:
                for cord in player.get_coordinates():
                    if cell == cord:
                        return player
        return None

    def add_object(self, game_obj: Any) -> bool:
        """
        Adds an object to the board, checking that the cells are empty and are in the board borders
        :param game_obj: it can be Apple, Snake or Bomb object
        :return: True if sucsess, else False
        """
        for cell in game_obj.get_coordinates():
            # chek that all object's cells are in the board boarder
            if 0 > cell[0] >= self.__height or 0 > cell[1] >= self.__width:
                return False
            # check if all the object's cells are empty
            if self.cell_content(cell) is not None:
                return False
        if type(game_obj) is Apple:
            self.__apples.append(game_obj)
        if type(game_obj) is Bomb:
            self.__bombs = game_obj
        if type(game_obj) is Snake:
            self.__snake = game_obj
        return True

    def empty_cells(self) -> int:
        """
        check how many empty cells is in the board
        :return: number of empty cells in the board
        """
        result = 0
        for player in self.get_board_objects():
            result += ft.reduce(lambda a, x: a+len(x), player.get_coordinates(), 0)
        return (self.__width * self.__height) - result

    def move_bomb(self) -> Tuple[bool, List[str]]:
        """
        "moves" bomb to the next "frame" in the sequence, from creation to end of blast.
        :param bomb: the object, index: the sequence of the bomb
        :return: Tuple of: False if needed new bomb(blast out of range or blast sequnce over), else True.
                            and list of object that hart by the blast move:
                            NONE if didnt hart something
                            'snake' if hart snake
                            'apple' if hart apple
        """
        bomb_hits = []
        target_cells: List[Coordinate] = self.__bombs.target_cells()
        # there is no blast seqence
        if target_cells is None:
            self.__bombs = None
            return False, bomb_hits
        # checking if blast out of range
        for cell in target_cells:
            col, row = cell
            if 0 > col or col >= self.__width or 0 > row or row >= self.__height:
                self.__bombs = None
                return False, bomb_hits
        # checking if blast hart apple or snake
        for cell in target_cells:
            if type(self.cell_content(cell)) is Apple:
                bomb_hits.append('apple')
                self.__apples.remove(self.cell_content(cell))
            if type(self.cell_content(cell)) is Snake:
                bomb_hits.append('snake')
        self.__bombs.move()
        return True, bomb_hits

    def move_snake(self, movekey=None, eat_apple=False) -> Tuple[int, Optional[Apple]]:
        """
        Moves snake every iteration according the movekey
        :param movekey: 'Up' / 'Down' / 'Right' / 'Left' represent the user choose
        :param eat_apple: True - apple was eatn by the snake during the last 3 rounds of the game, otherwise False
        :return: Tuple of int:
                0 if move out of boarder
                1 if move to him self
                2 if snake on bomb
                3 if snake eat apple
                4 if move and no thing happened
                and if 3 it will return the apple object that was eatn(for the score) to
        """
        apple = None
        # edit the snake direction if got
        if movekey is not None:
            self.__snake.set_direction(movekey)
        target_cell = self.__snake.move_target()
        col, row = target_cell
        snake_tail = self.__snake.get_coordinates()[-1]
        # check if the snake move is out the border
        if 0 > col or col >= self.__width or 0 > row or row >= self.__height:
            self.__snake.move(eat_apple)
            self.__snake.remove_head()
            output = 0
            return output, apple
        # check if snake move to himself
        elif type(self.cell_content(target_cell)) is Snake:
            if target_cell != snake_tail:
                output = 1
            elif (target_cell == snake_tail) and eat_apple:
                # if snake is growing, the tail is not going to move away when snake is going forward
                output = 1
            else:
                output = 4
        # check if snake move to bomb
        elif type(self.cell_content(target_cell)) is Bomb:
            output = 2
        # check if snake move to apple
        elif type(self.cell_content(target_cell)) is Apple:
            apple = self.cell_content(target_cell)
            self.__apples.remove(self.cell_content(target_cell))
            output = 3
        # it mean that snake move to an empty cell
        else:
            output = 4
        self.__snake.move(eat_apple)
        return output, apple

    def get_board_objects(self) -> List[Any]:
        """
        make a list of all the game's objects for the first round
        :return: list of all the game's objects by order: snake, bomb, apples
        """
        lst_players = [self.__snake, self.__bombs]
        for apple in self.__apples:
            lst_players.append(apple)
        return lst_players

    def get_board_objects_order2(self) -> List[Any]:
        """
        make a list of all the game's objects for the second round and above
        :return: list of all the game's objects by order: apples, snake, bomb
        """
        lst_players = []
        for apple in self.__apples:
            lst_players.append(apple)
        lst_players.append(self.__snake)
        lst_players.append(self.__bombs)
        return lst_players
