from typing import List, Tuple
from ex12_utils import find_length_n_paths


class BoggleModel:
    """
    the logic part of the game. responsible for the game role and update
    """

    def __init__(self):
        self._start_game()

    def _start_game(self) -> None:
        """
        create the object attribute with difult value for new game
        :return: None
        """
        self._cur_word: str = ""
        self._score: int = 0
        self._word_path: List[Tuple[int, int]] = []
        self._all_prev_words: List[str] = []
        self._last_clicked: str = 'enter'
        self._word_dict: List[str] = self._load_words_dict()
        self._sum_hints = 3
        self._hints = []
        self._cur_hint = 'hint'
        self._lives = 5


    def play_again(self) -> None:
        """
        change the values of the object attribute for new round
        :return: None
        """
        self._cur_word: str = ""
        self._word_path: List[Tuple[int, int]] = []
        self._all_prev_words: List[str] = []
        self._last_clicked: str = 'enter'
        self._word_dict: List[str] = self._load_words_dict()
        self._sum_hints = 3
        self._hints = []
        self._cur_hint = ''
        self._lives = 5


    def _load_words_dict(self) -> List[str]:
        """
        load the word dict of the game from an outside file
        :return: list of words
        """
        words = open('boggle_dict.txt', "r")
        return [word.strip() for word in words]

    def get_cur_word(self) -> str:
        """
        :return: the current word that writen by the user
        """
        return self._cur_word

    def get_all_prev_words(self) -> List[str]:
        """
        :return: all the last words that all ready discovered by the user
        """
        return self._all_prev_words

    def get_score(self) -> int:
        """
        :return: the score of the game
        """
        return self._score

    def get_cur_hint(self) -> str:
        return self._cur_hint

    def get_sum_hints(self) -> int:
        return self._sum_hints

    def get_lives(self) -> int:
        return self._lives

    def type_in(self, c: str, cord: Tuple[int, int]) -> None:
        """
        check which button was press and act accordingly
        :param c: the str of the button press
        :param cord: the coordinates of the button
        :return: None
        """
        # clear button
        if cord == (0, 5):
            self._do_clear()
        # enter button
        elif cord == (1, 5):
            self._do_enter()
        elif cord == (2, 5):
            self._do_hint()
        # chars buttons
        else:
            self._do_char_clicked(c, cord)

    def _do_char_clicked(self, c: str, cord: Tuple[int, int]) -> None:
        """
        if it is a valid click - add the char clicked to the current word, and update the path
        :param c: the str of the button press
        :param cord: the coordinates of the button
        :return: None
        """
        if self._last_clicked == 'enter':
            self._cur_word = c
            self._word_path.append(cord)
            self._last_clicked = 'char'
        else:
            if self._is_cur_click_valid(cord):
                self._cur_word += c
                self._word_path.append(cord)
                self._last_clicked = 'char'

    def _do_enter(self) -> None:
        """
        if the word is valid update the score and clear the current word
        :return: None
        """
        if self._is_word_valid():
            self.update_score()
            self._all_prev_words.append(self._cur_word)
        else:
            self._lives -= 1
        self._cur_word = ""
        self._word_path = []
        self._last_clicked = 'enter'

    def make_hints(self, board: List[List[str]]) -> None:
        """

        :param board: list of lists of chars
        :param words: an object that include all the legal words on boards
        :return: list of all the max score's paths
        """
        for n in range(8, 0, -1):
            if len(self._hints) > self._sum_hints:
                break
            paths_length_n = (find_length_n_paths(n, board, self._word_dict))
            if len(paths_length_n) != 0:
                for path in paths_length_n:
                    word = ''
                    for cord in path:
                        row, col = cord
                        word += board[row][col]
                    if word not in self._hints:
                        self._hints.append(word)

    def _do_hint(self) -> None:
        """

        :return: the longest valid word on board
        """
        if self._sum_hints >= 0:
            self._sum_hints -= 1
            self._cur_hint = self._hints[self._sum_hints + 1]
        if self._sum_hints < 0:
            self._sum_hints = 0
            self._cur_hint = "no hint"

    def _do_clear(self) -> None:
        """
        clear the current word and path
        :return: None
        """
        self._cur_word = ""
        self._word_path = []
        self._last_clicked = 'enter'

    def update_score(self) -> None:
        """
        update the score by current word path length
        :return: None
        """
        self._score += len(self._word_path) ** 2

    def _is_word_valid(self) -> bool:
        """
        check if the word is in the word dict and that isn't chosen before in the game
        :return: True if valid word, else False
        """
        if self._cur_word in self._all_prev_words:
            return False
        if self._cur_word != '':
            for word in self._word_dict:
                if self._cur_word == word:
                    return True
        return False

    def _is_cur_click_valid(self, cord: Tuple[int, int]) -> bool:
        """
        check if letter bottom click was valid path: the path is move only from neighbors to neighbors,
         and coordinate isn't in path already
        :return: True if click is valid else False
        """
        last_row, last_col = self._word_path[-1]
        row, col = cord
        # check that cord isn't clicked before
        if cord in self._word_path:
            return False
        # check that cord is a neighbors
        if last_row-1 <= row <= last_row+1 and last_col-1 <= col <= last_col+1:
            return True
        return False
