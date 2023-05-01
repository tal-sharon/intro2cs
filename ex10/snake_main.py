import game_parameters
from game_display import GameDisplay
from board import Board
from snake import Snake
from apple import Apple
from bomb import Bomb
from typing import Tuple, List, Optional

COLORS = {'apple': 'green', 'bomb': 'red', 'blast': 'orange', 'snake': 'black'}
FEEDBACK_SNAKE = {'hit border': 0, 'hit himself': 1, 'hit bomb': 2, 'eat apple': 3, 'all ok': 4}


def draw_first_run(board: Board, gd: GameDisplay) -> None:
    """
    call draw_cell function for all object's cells in board. by the specific order: snake, bomb, apples
    :param board: a board object
    :param gd: a GameDisplay object
    :return: None
    """
    for player in board.get_board_objects():
        for cell in player.get_coordinates():
            gd.draw_cell(cell[0], cell[1], player.get_color())


def draw(board: Board, gd: GameDisplay) -> None:
    """
    call draw_cell function for all object's cells in board. by the specific order: apples, snake, bomb
    :param board: a board object
    :param gd: a GameDisplay object
    :return: None
    """
    for player in board.get_board_objects_order2():
        if player:
            for cell in player.get_coordinates():
                gd.draw_cell(cell[0], cell[1], player.get_color())


def is_growing(timer: int) -> bool:
    """
    check if snake still growing due to eating an apple
    :param timer: the rounds pass from eaten an apple
    :return: True means that snake still growing after it eat an apple, else False
    """
    if timer > 0:
        return True
    return False


def create_bomb(board_game) -> None:
    """
    create bomb object with random data and add to given board
    :param board_game: a board object
    :return: NONE
    """
    bomb_added = False
    while not bomb_added:
        x, y, radius, time = game_parameters.get_random_bomb_data()
        bomb_game = Bomb(x, y, radius, time, COLORS['bomb'], COLORS['blast'])
        if board_game.add_object(bomb_game):
            bomb_added = True


def create_apple(board_game, number: int) -> bool:
    """
    create apple objects by given amount (number) with random data and add to given board
    :param board_game: a board object
    :param number: num of apples you want to create
    :return: True - upon success, False when there is no place on the board
    """
    if board_game.empty_cells() >= number:
        for num in range(number):
            apple_added = False
            while not apple_added:
                x, y, score = game_parameters.get_random_apple_data()
                if board_game.add_object(Apple(x, y, score, COLORS['apple'])):
                    apple_added = True
        return True
    return False


def initiate_snake_game(gd) -> Board:
    """
    Initiates all the needed objects (Snake, Apples, Bomb) and add them to the game Board
    :param gd: GameDisplay object
    :return: Board object
    """
    board_game = Board(game_parameters.WIDTH, game_parameters.HEIGHT)
    snake_game = Snake(COLORS['snake'], 3, 'Up', (10, 10))
    board_game.add_object(snake_game)
    create_bomb(board_game)
    create_apple(board_game, 3)
    return board_game


def main_loop(gd: GameDisplay) -> None:
    """
    Runs the SNAKE GAME in a loop until you lose!
    :param gd: a GameDisplay object
    :return: None
    """
    score = 0
    gd.show_score(score)
    board_game = initiate_snake_game(gd)
    snake_timer: int = 0
    draw_first_run(board_game, gd)
    gd.end_round()
    while True:
        key_clicked = gd.get_key_clicked()

        # move snake and act accordingly
        snakes_act, eaten_apple = board_game.move_snake(key_clicked, is_growing(snake_timer))
        if is_growing(snake_timer):
            snake_timer -= 1
        if snakes_act in [FEEDBACK_SNAKE['hit border'], FEEDBACK_SNAKE['hit himself'], FEEDBACK_SNAKE['hit bomb']]:
            draw(board_game, gd)
            break
        if snakes_act == FEEDBACK_SNAKE['eat apple']:
            score += eaten_apple.get_score()
            gd.show_score(score)
            snake_timer += 3
            if not create_apple(board_game, 1):
                draw(board_game, gd)
                break

        # 'move' bomb forward in it's sequence and act accordingly
        is_bomb_exists, bombs_hits = board_game.move_bomb()
        if not is_bomb_exists:
            create_bomb(board_game)
        if 'snake' in bombs_hits:
            draw(board_game, gd)
            break
        if 'apple' in bombs_hits:
            if not create_apple(board_game, 1):
                draw(board_game, gd)
                break

        # draw board and end round
        draw(board_game, gd)
        gd.end_round()
    gd.end_round()
