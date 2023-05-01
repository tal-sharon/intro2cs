import copy
from boggle_board_randomizer import randomize_board, LETTERS
from typing import List, Tuple, Union, Optional

LEGAL_MOVES = [(0, 1), (0, -1), (1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1)]
FIND_PATHS = []
FIND_WORDS = ''


def is_valid_path(board: List[List[str]], path: List[Tuple[int, int]], words) -> Optional[str]:
    """
    check that the path and the word is valid
    :param board: list of lists of chars
    :param path: list of Tuples, each tuple represent coordinates of char on the board
    :param words: list/dict that include all the legal words on boards
    :return: the word (str) if the path and the word is valid, else None
    """
    # check if there is duplicates coordinates in path
    path_set = set(path)
    if len(path_set) != len(path):
        return None
    if len(path) == 0:
        return None
    last_row, last_col = path[0]
    if 0 > last_row or last_row >= len(board) or 0 > last_col or last_col >= len(board[0]):
        return None
    for cord in path[1:]:
        row, col = cord[0], cord[1]
        # check if there is coordinates in path out of game board
        if 0 > row or row >= len(board) or 0 > col or col >= len(board[0]):
            return None
        # check valid path - all the coordinates are neighbours
        if last_row-1 > row or row > last_row+1 or last_col-1 > col or col > last_col+1:
            return None
        last_row, last_col = row, col

    # check valid word
    the_word: str = ''
    for cord in path:
        row, col = cord[0], cord[1]
        the_word += board[row][col]
    for word in words:
        if the_word == word:
            return the_word
    return None


def possible_word(suspect, words) -> bool:
    """
    Check if a given string is part of a word from a words list
    :param suspect: The suspected string
    :param words: The words list ("bank")
    :return: True - the string is in one of the words from the list, False - otherwise
    """
    if words:
        for word in words:
            if suspect in word:
                return True
    return False


def helper_n_paths(n, board, words, word, row, col, paths_lst, path, obj) -> Optional[List[List[Tuple[int, int]]]]:
    """
    A 'generic' helper function for both 'find_length_n_paths' and 'find_length_n_words'
    :param n: The wanted length
    :param board: A list of lists of strings representing the board
    :param words: A list or of the words "bank"
    :param word: The current word
    :param row: The current row
    :param col: The current col
    :param paths_lst: The full paths list
    :param path: The current path
    :param obj: The type of wanted object: List (path) or String (word)
    :return: Optional - List of paths or None
    """
    # append current location to current path and update current word accordingly
    path.append((row, col))
    new_word = word + board[row][col]

    # check what kind of object we are looking for
    if isinstance(obj, list):
        obj = path
    else:
        obj = new_word

    # check if current word is possible by the words dictionary
    if not possible_word(word, words):
        return None

    # if reached the target length of the object check if the word is in the dictionary, of so, append path to list.
    if len(obj) == n and words:
        if new_word in words:
            match = copy.deepcopy(path)
            paths_lst.append(match)
            return paths_lst

    # move forward by the possible moves and legal conditions
    if len(obj) < n:
        for move in LEGAL_MOVES:
            y_move, x_move = move
            n_row = row+y_move
            n_col = col+x_move
            if (0 <= n_row <= 3 and 0 <= n_col <= 3) and (n_row, n_col) not in path:
                helper_n_paths(n, board, words, new_word, n_row, n_col, paths_lst, path, obj)
                path.pop()

    return paths_lst


def words_by_board(word: str, board_letters: List[str]) -> bool:
    """
    Check if all word's letter are on the board
    :param word: A string of the checked word
    :param board_letters: A list of the board's letter
    :return: True - if all the word's letters are on the board, False - otherwise
    """
    for letter in word:
        if letter not in board_letters:
            for cell in board_letters:
                if letter in cell:
                    if cell in word:
                        return True
            return False
    return True


def find_length_n_general(n: int, board: List[List[str]], words: List[str], obj: Union[list, str]) \
        -> List[List[Tuple[int, int]]]:
    """
    Finds all correct paths of words from the list on the board
     by length n of the requested object (List - for path, String - for word)
    :param n: The wanted length
    :param board: A list of lists of strings representing the board
    :param words: A list or of the words "bank"
    :param obj: The type of wanted object: List (path) or String (word)
    :return:
    """
    paths_lst = []

    # filter the words from the list which all it's letters are on the board
    board_letters = [letter for row in board for letter in row]
    filtered_words = list(filter(lambda letter: words_by_board(letter, board_letters), words))

    # if filtered words list is not empty, go find all wanted paths, each time start from different cell on the board.
    if filtered_words:
        for cell in range(16):
            row = cell // 4
            col = cell % 4
            paths_lst += helper_n_paths(n, board, filtered_words, '', row, col, [], [], obj)
    return paths_lst


def find_length_n_paths(n, board, words) -> List[List[Tuple[int, int]]]:
    """
    Finds all length n paths on a board which gets words from the words list
    :param n: the wanted length
    :param board: A list of lists of strings representing a game board
    :param words: A list of given words (strings)
    :return: A list of lists of all paths in length n which represents words from the words list
    """
    return find_length_n_general(n, board, words, FIND_PATHS)


def find_length_n_words(n, board, words) -> List[List[Tuple[int, int]]]:
    """
    Finds all paths on a board which gets length n words from the words list
    :param n: the wanted length
    :param board: A list of lists of strings representing a game board
    :param words: A list of given words (strings)
    :return: A list of lists of all paths which represents length n words from the words list
    """
    return find_length_n_general(n, board, words, FIND_WORDS)


def max_score_paths(board, words) -> List[List[Tuple[int, int]]]:
    """

    :param board: list of lists of chars
    :param words: an object that include all the legal words on boards
    :return: list of all the max score's paths
    """
    paths_results = []
    words_lst = []
    board_size = len(board) * len(board[0])
    for n in range(board_size, 0, -1):
        if len(find_length_n_paths(n, board, words)) != 0:
            paths_length_n = (find_length_n_paths(n, board, words))
            for path in paths_length_n:
                word = ''
                for cord in path:
                    row, col = cord
                    word += board[row][col]
                if word not in words_lst:
                    words_lst.append(word)
                    paths_results.append(path)
    return paths_results[::-1]