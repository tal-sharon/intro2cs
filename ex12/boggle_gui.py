import tkinter as tki
import time
import pygame.mixer
import boggle_board_randomizer
from typing import Callable, Dict, List, Any, Tuple

BUTTON_CHAR = 0
BUTTON_OBJ = 1
BUTTON_HOVER_COLOR = 'gray50'
REGULAR_COLOR = 'gray75'
BUTTON_ACTIVE_COLOR = 'slateblue'

BUTTON_STYLE = {"font": ("Courier", 30),
                "borderwidth": 1,
                "relief": tki.RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": BUTTON_ACTIVE_COLOR}


class BoggleGUI:
    """
    The Graphic User Interface of Boggle Game
    """

    def __init__(self):
        self._board = []
        self._buttons: Dict[Tuple[int, int], Tuple[str, tki.Button]] = dict()
        self._lives: List[tki.Label] = []
        self._lives_count = 5
        self._score = 0
        root = tki.Tk()
        root.title('Boggle Game')
        root.resizable(False, False)
        self._main_window = root
        self._create_start_frame(root)
        self._create_game_frame(root)
        self._create_end_frame(root)
        self._play_bg_music()

    def _create_end_frame(self, root: tki.Tk) -> None:
        """
        Creates the frame which is displayed at the end of a game
        :param root: The parent of the frame, main window of the gui.
        :return: None
        """
        # create frame and labels
        self._end_frame = tki.Frame(root, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                    highlightthickness=5)
        self._end_score_label1 = tki.Label(self._end_frame, font=("Courier", 30), bg=REGULAR_COLOR,
                                           text="You're current score is:", width=30)
        self._end_score_label2 = tki.Label(self._end_frame, font=("Courier", 30), bg=REGULAR_COLOR,
                                           text=str(self._score), width=30)
        self._play_again_label = tki.Label(self._end_frame, font=("Courier", 20), bg=REGULAR_COLOR,
                                           text="if you wish to play again, click the button below", width=50)

        self._create_replay_button()

        # pack
        self._end_score_label1.pack(side=tki.TOP)
        self._end_score_label2.pack(side=tki.TOP)
        self._play_again_label.pack(side=tki.TOP)
        self._replay_button.pack(side=tki.TOP, pady=20)

    def _create_replay_button(self) -> None:
        """
        Creates the REPLAY button appearing on the end frame
        :return: None
        """
        self._replay_btn_img = tki.PhotoImage(file="replay1_small.png")
        self._replay_btn_img = self._replay_btn_img.zoom(10)
        self._replay_btn_img = self._replay_btn_img.subsample(32)
        self._replay_btn_hover = tki.PhotoImage(file="replay31.png")
        self._replay_btn_hover = self._replay_btn_hover.zoom(10)
        self._replay_btn_hover = self._replay_btn_hover.subsample(32)
        self._replay_button = tki.Button(self._end_frame, image=self._replay_btn_img, command=self.play_again,
                                         bg=REGULAR_COLOR, relief="flat", activebackground="gray90")

        def _on_enter(event: Any) -> None:
            self._replay_button['image'] = self._replay_btn_hover

        def _on_leave(event: Any) -> None:
            self._replay_button['image'] = self._replay_btn_img

        self._replay_button.bind("<Enter>", _on_enter)
        self._replay_button.bind("<Leave>", _on_leave)

    def _create_game_frame(self, root: tki.Tk) -> None:
        """
        Creates the Frame which is displayed while a game is occuring
        :param root: The parent of the frame, main window of the gui.
        :return: None
        """
        self._game_frame = tki.Frame(root, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR, highlightthickness=5)
        # create bottom bar
        self._words_label = tki.Label(self._game_frame, font=("Courier", 30), bg="gray90", width=20, relief="groove")
        # create middle frame buttons
        self._board_frame = tki.Frame(self._game_frame, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        # create top bar
        self._top_bar_frame = tki.Frame(self._game_frame, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                        highlightthickness=5)
        self._display_label = tki.Label(self._top_bar_frame, font=("Courier", 35),
                                        bg="gray90", width=20, height=2, relief="sunken")

        # create the rest of sections
        self._create_board_in_mid_frame()
        self._create_score_frame()
        self._create_time_frame()
        self._create_lives_bar()

        # pack everything
        self._words_label.pack(side=tki.BOTTOM, fill=tki.BOTH)
        self._board_frame.pack(side=tki.BOTTOM, fill=tki.BOTH, expand=True)
        self._top_bar_frame.pack(side=tki.BOTTOM, fill=tki.BOTH)
        self._score_frame.pack(side=tki.RIGHT)
        self._display_label.pack(side=tki.RIGHT)
        self._time_frame.pack(side=tki.RIGHT)
        self._lives_frame.pack(side=tki.TOP)

    def _create_lives_bar(self) -> None:
        """
        Creates the lives bar
        :return: None
        """
        self._lives_frame = tki.Frame(self._game_frame, bg=REGULAR_COLOR)

        # create images
        self._full_heart_img = tki.PhotoImage(file="heart_full.png")
        self._full_heart_img = self._full_heart_img.zoom(4)
        self._full_heart_img = self._full_heart_img.subsample(50)
        self._empty_heart_img = tki.PhotoImage(file="heart_empty.png")
        self._empty_heart_img = self._empty_heart_img.zoom(4)
        self._empty_heart_img = self._empty_heart_img.subsample(50)

        # create and pack all hearts
        self._lives = []
        for live in range(self._lives_count):
            self._create_heart(self._full_heart_img)
        for live in range(5 - self._lives_count):
            self._create_heart(self._empty_heart_img)

    def _create_heart(self, img) -> None:
        """
        Creates a heart label representing a life
        :param img: the image of the label, full heart or empty heart
        :return: None
        """
        heart_label = tki.Label(self._lives_frame, image=img, bg=REGULAR_COLOR)
        self._lives.append(heart_label)
        heart_label.pack(side=tki.LEFT)

    def _create_start_frame(self, root: tki.Tk) -> None:
        """
        Creates the frame which is displayed at the beginning
        :param root: The parent of the frame, main window of the gui.
        :return: None
        """
        self._start_frame = tki.Frame(root, bg=REGULAR_COLOR, width=30, height=50)
        self._start_label1 = tki.Label(self._start_frame, font=("Courier", 30), bg=REGULAR_COLOR,
                                       text="Welcome to Boggle!", width=30, pady=20)
        self._start_label2 = tki.Label(self._start_frame, font=("Courier", 20), bg=REGULAR_COLOR, width=50,
                                       text="Once you click the START button,\n "
                                            "a 03:00 minutes timer will start running")

        self._create_start_button()

        # pack everything
        self._start_label1.pack(side=tki.TOP)
        self._start_label2.pack(side=tki.TOP)
        self._start_button.pack(side=tki.TOP, pady=20)

    def _create_start_button(self) -> None:
        """
        Creates the START button appearing on the start frame
        :return: None
        """
        self._start_btn_img = tki.PhotoImage(file="start1_small.png")
        self._start_btn_img = self._start_btn_img.zoom(6)
        self._start_btn_img = self._start_btn_img.subsample(40)
        self._start_btn_hover = tki.PhotoImage(file="start31.png")
        self._start_btn_hover = self._start_btn_hover.zoom(6)
        self._start_btn_hover = self._start_btn_hover.subsample(40)
        self._start_button = tki.Button(self._start_frame, image=self._start_btn_img, command=self.start_game,
                                        bg=REGULAR_COLOR, relief="flat", activebackground="gray90")

        def _on_enter(event: Any) -> None:
            self._start_button['image'] = self._start_btn_hover

        def _on_leave(event: Any) -> None:
            self._start_button['image'] = self._start_btn_img

        self._start_button.bind("<Enter>", _on_enter)
        self._start_button.bind("<Leave>", _on_leave)

    def _create_time_frame(self) -> None:
        """
        Creates the frame which displays the time at the game's frame
        :return: None
        """
        # create
        self._time_frame = tki.Frame(self._top_bar_frame, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                     highlightthickness=5)
        self._clock_frame = tki.Frame(self._time_frame, bg=REGULAR_COLOR, width=6, relief="groove")
        sec = tki.StringVar()
        self._sec_label = tki.Label(self._clock_frame, text='05', font=("Courier", 20),
                                      bg="gray90", relief="sunken")
        self._mins_label = tki.Label(self._clock_frame, text='00', font=("Courier", 20),
                                      bg="gray90", relief="sunken")
        self._time_label = tki.Label(self._time_frame, font=("Courier", 20),
                                     bg=REGULAR_COLOR, width=6, text="Time:")

        # pack
        self._time_label.pack(side=tki.TOP)
        self._clock_frame.pack(side=tki.TOP)
        self._sec_label.pack(side=tki.RIGHT)
        self._mins_label.pack(side=tki.RIGHT)

    def _create_score_frame(self) -> None:
        """
        Creates the frame which displays the score at the game's frame
        :return: None
        """
        # create
        self._score_frame = tki.Frame(self._top_bar_frame, bg=REGULAR_COLOR, highlightbackground=REGULAR_COLOR,
                                      highlightthickness=5)
        self._points_label = tki.Label(self._score_frame, font=("Courier", 30),
                                       bg=REGULAR_COLOR, width=6, relief="flat", text=str(self._score))
        self._score_label = tki.Label(self._score_frame, font=("Courier", 20),
                                      bg=REGULAR_COLOR, width=6, text="Score:")
        # pack
        self._score_label.pack(side=tki.TOP)
        self._points_label.pack(side=tki.TOP)

    def _create_game_over_frame(self) -> None:
        """
        Creates the game over frame
        :return: None
        """
        self._game_over_frame = tki.Frame(self._main_window, bg="Red4", height=1000)
        self._game_over_img = tki.PhotoImage(file="game_over.png")
        self._game_over_img = self._game_over_img.zoom(5)
        self._game_over_img = self._game_over_img.subsample(8)
        self._game_over_img_lbl = tki.Label(bg="Red4", image=self._game_over_img, width=1000, height=300)
        self._game_over_label = tki.Label(self._game_over_frame, bg="Red4", font=("Courier", 30), fg="white",
                                          text="You Lost \n You do not deserve another try", pady=25, padx=20)
        self._game_over_img_lbl.pack(side=tki.TOP)
        self._game_over_label.pack(side=tki.TOP)

    def start_game(self) -> None:
        """
        Switches frames: from start frame to game frame
        :return: None
        """
        self._game_frame.pack(fill='both', expand=1)
        self._start_frame.pack_forget()
        self._mins_label["text"] = "03"
        self._sec_label["text"] = "00"
        self._main_window.after(1000, self._timer)

    def play_again(self) -> None:
        """
        Switches frames: from end frame to game frame
        :return: None
        """
        self._create_game_frame(self._main_window)
        self._game_frame.pack(fill='both', expand=1)
        self._end_frame.pack_forget()
        self._mins_label["text"] = "03"
        self._sec_label["text"] = "00"
        self._main_window.after(1000, self._timer)

    def end_game(self) -> None:
        """
        Switches frames: from game frame to end frame
        :return:
        """
        self._end_score_label2["text"] = str(self._score)
        self._end_frame.pack(fill='both', expand=1)
        self._game_frame.pack_forget()

    def _game_over(self) -> None:
        """
        Switches frames: from game frame to game over frame
        :return: None
        """
        pygame.mixer.music.load("gameover_music.mp3")
        pygame.mixer.music.play(loops=0)
        self._create_game_over_frame()
        self._game_over_frame.pack(fill='both', expand=1)
        self._game_frame.pack_forget()

    def _create_board_in_mid_frame(self) -> None:
        """
        Creating the main frame of the game frame
        :return: None
        """
        # Arranges the Grid
        for i in range(4):
            tki.Grid.columnconfigure(self._board_frame, i, weight=1)

        for i in range(4):
            tki.Grid.rowconfigure(self._board_frame, i, weight=1)

        # Get Letters for board and create buttons accordingly
        board = boggle_board_randomizer.randomize_board()
        self._board = board
        for row in range(len(board)):
            for col in range(len(board[0])):
                self._make_button(board[row][col], row, col)

        self._spacing_label = tki.Label(self._board_frame, bg="gray75")
        self._spacing_label.grid(row=0, column=4, rowspan=4)

        # Create 'enter' and 'clear' button
        self._clear_btn = self._make_button('clear', 0, 5, rowspan=1)
        self._clear_btn['bg'] = "red3"
        self._clear_btn['activebackground'] = "tomato2"
        self._button_hover(self._clear_btn, "red3", "red4")
        self._enter_btn = self._make_button('enter', 1, 5, rowspan=1)
        self._enter_btn['bg'] = "lime green"
        self._enter_btn['activebackground'] = "palegreen"
        self._button_hover(self._enter_btn, "lime green", "forest green")
        self._create_hint_section()

    def _create_hint_section(self) -> None:
        """
        Creates the hint section of the board
        :return:
        """
        self._hint_btn = self._make_button('hint', 2, 5, rowspan=1)
        self._hint_label0 = tki.Frame(self._board_frame, bg="gray75")
        self._hint_label0.grid(row=3, column=5, sticky=tki.NSEW)
        self._hint_label1 = tki.Label(self._hint_label0, text='', bg='gray75', font=("Courier", 17))
        self._hint_label2 = tki.Label(self._hint_label0, text='hints left:', bg='gray75', font=("Courier", 12))
        self._hint_label3 = tki.Label(self._hint_label0, text='3', bg='gray75', font=("Courier", 12))
        self._hint_label1.pack(side=tki.TOP)
        self._hint_label2.pack(side=tki.TOP)
        self._hint_label3.pack(side=tki.TOP)

    def _make_button(self, button_char: str, row: int, col: int,
                     rowspan: int = 1, columnspan: int = 1) -> tki.Button:
        """
        Makes a button for the board
        :param button_char: The string displayed on the button
        :param row: The row of the button in the Grid
        :param col: The col of the button in the Grid
        :param rowspan: The row span of the button in the Grid
        :param columnspan: The column span of the button in the Grid
        :return:
        """
        button = tki.Button(self._board_frame, text=button_char, **BUTTON_STYLE)
        button.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan, sticky=tki.NSEW)
        self._buttons[row, col] = button_char, button

        self._button_hover(button, REGULAR_COLOR, BUTTON_HOVER_COLOR)
        return button

    def _button_hover(self, button, reg_color, hover_color) -> None:
        """
        Configures hover over a button
        :param button: the button
        :param reg_color: The color of the button when cursor not on button
        :param hover_color: The color of the button when cursor overs over button
        :return: None
        """
        def _on_enter(event: Any) -> None:
            button['background'] = hover_color

        def _on_leave(event: Any) -> None:
            button['background'] = reg_color

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)

    def run(self) -> None:
        """
        The method which runs the GUI
        :return: None
        """
        self._start_frame.pack(fill='both', expand=1)
        self._main_window.mainloop()

    def set_display(self, display_text: str) -> None:
        """
        Sets the text on the display label at the top bar of the game frame
        :param display_text: The text which would be displayed
        :return: None
        """
        self._display_label["text"] = display_text

    def set_button_command(self, location: Tuple[int, int], cmd: Callable[[], None]) -> None:
        """
        Set the action of a button in the main board of the game
        :param location: The coordinates of the button in the Grid
        :param cmd: The action which will be set to the buttons command, when clicked.
        :return: None
        """
        self._buttons[location][BUTTON_OBJ].configure(command=cmd)

    def get_buttons(self) -> List[Tuple[Tuple[int, int], str]]:
        """
        Gets the location (coordinates) and text of the buttons
        :return: A list of tuples made of coordinate (tuple) and a string of the button's text
        """
        buttons = []
        for key in self._buttons:
            char = self._buttons[key][BUTTON_CHAR]
            buttons.append((key, char))
        return buttons

    def set_prev_words(self, words: List[str]) -> None:
        """
        Sets the display of all previous guessed correctly words
        :param words: All the words guessed until now
        :return:
        """
        words_string = ''
        for word in words:
            words_string += str(word)
            words_string += ", "
            if 70 <= len(words_string) and "\n" not in words_string:
                words_string += "\n"

        self._words_label["text"] = words_string
        if len(words_string) > 25:
            self._words_label["font"] = ("Courier", 20)
            self._words_label["pady"] = 5
        if len(words_string) > 40:
            self._words_label["font"] = ("Courier", 15)
            self._words_label["pady"] = 10
        if len(words_string) > 50:
            self._words_label["font"] = ("Courier", 12)
            self._words_label["pady"] = 15
        # if len(words_string) > 80:
        #     self._words_label["font"] = ("Courier", 7)
        #     self._words_label["pady"] = 20

    def set_score(self, score: int) -> None:
        """
        Sets the new updated score on display and in attribute
        :param score: The score
        :return: None
        """
        self._points_label["text"] = str(score)
        self._score = score

    def _play_bg_music(self) -> None:
        """
        Plays the background music
        :return: None
        """
        pygame.mixer.init()
        pygame.mixer.music.load("bg_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def _timer(self) -> None:
        """
        Sets the timer of the game, runs the time and ends the game when time is up.
        :return: None
        """
        # Reduce a second from the timer
        times = int(self._sec_label["text"]) + (int(self._mins_label["text"])*60) - 1

        if times >= 0:
            # If the time is not over yet, set the new time to display
            minute, second = times // 60, times % 60
            if second >= 10:
                self._sec_label["text"] = str(second)
            elif second < 10:
                self._sec_label["text"] = "0" + str(second)
            if minute >= 10:
                self._mins_label["text"] = str(minute)
            elif minute < 10:
                self._mins_label["text"] = "0" + str(minute)
            self._main_window.after(1000, self._timer)
        else:
            # time is over, end the current game
            self._sec_label["text"] = '00'
            self._mins_label["text"] = '00'
            if self._lives_count > 0:
                self.end_game()

    def set_play_again_command(self, set_actions_func, delete_prev_data_func) -> None:
        """
        Set new command to the play again button, using functions of the Model of the game
        :param set_actions_func: A function setting actions to the new randomized board
        :param delete_prev_data_func: A function deleting irrelevant data from previous game round 
        :return: None
        """
        def func():
            self.play_again()
            delete_prev_data_func()
            set_actions_func()
        self._replay_button.configure(command=func)

    def get_board(self) -> List[List[str]]:
        """
        Gets the board
        :return: the Board - list of lists of strings
        """
        return self._board

    def set_hint(self, count, word) -> None:
        """
        Sets the updated hint on the board and updates the amount of hints left
        :param count: Number of hints left
        :param word: The hint
        :return: None
        """
        self._hint_label3['text'] = str(count)
        self._hint_label1['text'] = str(word)

    def reduce_lives(self, count) -> None:
        """
        Reduces a life from the lives bar
        :param count: the amount of full lives
        :return: None
        """
        if count != len(self._lives):
            self._lives[count]["image"] = self._empty_heart_img
            self._lives_count = count
        if count == 0:
            pygame.mixer.music.load("fail_sound.mp3")
            pygame.mixer.music.play(loops=0)
            self._main_window.after(2500, self._game_over)


if __name__ == "__main__":
    cg = BoggleGUI()
    cg.run()
