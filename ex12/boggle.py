from typing import Callable, Tuple
from boggle_model import BoggleModel
from boggle_gui import BoggleGUI


class BoggleController:
    """
    marge between tha gui to the logic of the bogal game, make the game run
    """

    def __init__(self) -> None:
        self._gui = BoggleGUI()
        self._model = BoggleModel()
        self.set_actions()
        self._gui.set_play_again_command(self.set_actions, self._model.play_again)

    def set_actions(self) -> None:
        """
        combine between a button from the BoggleGui object to a function from the BoggleModel object
        :return: None
        """
        for button in self._gui.get_buttons():
            button_locat, button_text = button
            action = self.create_button_action(button_locat, button_text)
            self._gui.set_button_command(button_locat, action)
        self._model.make_hints(self._gui.get_board())

    def create_button_action(self, button_locat: Tuple[int, int], button_text: str) -> Callable:
        """
        build a function that call the relevent function from the BoggleModel class for a spesifc button from the BoggleGui class
        :param button_locat: the coordinates of the button
        :param button_text: the str of the button press
        :return: function that will be activate when button will be press
        """
        def fun() -> None:
            self._model.type_in(button_text, button_locat)
            self._gui.set_display(self._model.get_cur_word())
            self._gui.set_score(self._model.get_score())
            self._gui.set_prev_words(self._model.get_all_prev_words())
            self._gui.set_hint(self._model.get_sum_hints(), self._model.get_cur_hint())
            self._gui.reduce_lives(self._model.get_lives())
        return fun

    def run(self) -> None:
        """
        make the game begin!
        :return: None
        """
        self._gui.run()


if __name__ == '__main__':
    BoggleController().run()



