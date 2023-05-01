import json
import sys
from car import Car
from board import Board


class Game:
    """
    A rush hour game containing a board which can contain cars
    A game of class Game has specific rules such as: limited car names and length.
    A game play is over once a car gets to the target location of the board
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        # You may assume board follows the API
        # implement your code here (and then delete the next line - 'pass')
        self.__board = board
        print(self.__board)

    def __single_turn(self) -> bool:
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it.

        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.

        Before and after every stage of a turn, you may print additional
        information for the user, e.g., printing the board. In particular,
        you may support additional features, (e.g., hints) as long as they
        don't interfere with the API.
        :return bool: False - if the player's input is '!', meaning he wants to quit. True, otherwise.
        """
        # implement your code here (and then delete the next line - 'pass')

        # get user's input
        user_input = input("Choose a car and direction, for example 'Y,d'. If you wish to exit the game, Choose '!': ")
        print()
        if user_input == '!':
            # player wants to quit
            return False

        # check technical validation of input
        if len(user_input) == 3:
            if user_input[1] == ',':
                user_input = user_input.split(',')
                name, movekey = user_input[0], user_input[1]
            else:
                print("invalid input, choose car and direction such as: 'Y,d'.", '\n')
                return True
        else:
            print("invalid input", '\n')
            return True

        valid_input = False

        # check if car is on board
        for cell in self.__board.cell_list():
            if self.__board.cell_content(cell) == name:
                valid_input = True
                break
        if not valid_input:
            print("You chose a car which doesn't exist on the board.", '\n')

        # check if movekey is valid
        if movekey not in ['u', 'd', 'l', 'r']:
            print("You chose an invalid direction for the car, you can choose 'u' for up, 'd' for down 'l' " +
                  "for left, or 'r' for right.", '\n')
            valid_input = False

        # if all is valid - move car
        if valid_input:
            self.__board.move_car(name, movekey)
            print(self.__board)
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        # implement your code here (and then delete the next line - 'pass')
        while True:
            if not self.__single_turn():
                # player want to stop an ongoing game
                break

            # check if there is an horizontal car on the target location
            car_on_target = self.__board.cell_content(self.__board.target_location())
            if car_on_target:
                is_finished = False
                for move in self.__board.possible_moves():
                    if car_on_target == move[0] and move[1] == 'l':
                        is_finished = True
                        break
                if is_finished:
                    break


if __name__== "__main__":
    # Your code here
    # All access to files, non API constructors, and such must be in this
    # section, or in functions called from this section.
    game_board = Board()

    with open(sys.argv[1], 'r') as file:
        car_config = json.load(file)
    # now car_config is a dictionary equivalent to the JSON file

    # go over all cars in JSON file
    for car in car_config:
        details = car_config.get(car)
        some_car = Car(car, details[0], details[1], details[2])

        # check if car's name is legal
        car_name = some_car.get_name()
        if car_name in ['R', 'G', 'W', 'O', 'B', 'Y']:

            # check the length of the car
            if 2 <= len(some_car.car_coordinates()) <= 4:
                game_board.add_car(some_car)

    game = Game(game_board)
    game.play()
