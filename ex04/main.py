import hangman_helper


def update_word_pattern(word: str, pattern: str, letter: str) -> str:
    """
    updates the pattern after a guess
    :param word: a string of the full word that needs to be guessed
    :param pattern: a string of the letters that were already guessed right with blank spaces
    :param letter: a string of the next guess
    :return: the updated pattern compatible with the new guess
    """
    if letter in word:
        list_pattern = list(pattern)
        list_word = list(word)
        for i in range(len(list_word)):
            if list_word[i] == letter:
                list_pattern[i] = letter
        new_pattern = "".join(list_pattern)
        return new_pattern
    else:
        return pattern


def guess_is_letter(letter: str, score: int, updated_pattern: str, word: str, wrong_guess_lst: list)\
        -> tuple[int, str, list]:
    """
    if user guesses a letter, the function determines if the guess is right or wrong and acts accordingly.
    :param letter: the user's input.
    :param score: the current points of the player
    :param updated_pattern: the current pattern
    :param word: the word that is being guessed in the current game
    :param wrong_guess_lst: a list of all the wrong guessed letters
    :return: new sum of total points, the updated pattern and the updated wrong guess list
    """
    if letter_is_invalid(letter, updated_pattern, wrong_guess_lst):
        if letter in wrong_guess_lst:
            hangman_helper.display_state(updated_pattern, wrong_guess_lst, score,
                                         "The letter you've chosen was already guessed" + "\n")
        else:
            hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "Invalid input, try again" + "\n")
    else:
        updated_pattern = update_word_pattern(word, updated_pattern, letter)
        score += -1
        if letter in word:
            score = right_letter_guess(score, letter, updated_pattern, word, wrong_guess_lst)
        else:
            wrong_letter_guess(score, letter, updated_pattern, word, wrong_guess_lst)
    return score, updated_pattern, wrong_guess_lst


def right_letter_guess(score, letter, updated_pattern, word, wrong_guess_lst):
    score = right_letter_score(word, letter, score)
    if updated_pattern == word:
        hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "\n" + "You Won!")
    else:
        hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "\n" + "Good guess!" + "\n")
    return score


def wrong_letter_guess(score, letter, updated_pattern, word, wrong_guess_lst):
    wrong_guess_lst.append(letter)
    if score == 0:
        hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "\n" "You lost. "
                                                                              "The correct word was: " + word)
    else:
        hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "\n" + "Wrong guess :(" + "\n")


def guess_is_word(pattern: str, guessed_word: str, score: int, correct_word: str,
                  wrong_guess_lst: list) -> tuple[int, str]:
    """
    :param pattern: the current pattern
    :param guessed_word: the user's input (word guess)
    :param score: the current points of the player
    :param correct_word: the word being guessed in the current game
    :param wrong_guess_lst: a list of all the wrong guessed letters
    :return: the updated sum of total points of the player
    """
    score += -1
    if guessed_word == correct_word:
        pattern, score = right_word_guess(pattern, score, correct_word)
        hangman_helper.display_state(pattern, wrong_guess_lst, score, "Great guess!")
        return score, pattern
    else:
        if score == 0:
            hangman_helper.display_state(pattern, wrong_guess_lst, score, "\n" "You lost. The correct word was: "
                                         + correct_word)
        else:
            hangman_helper.display_state(pattern, wrong_guess_lst, score, "Wrong word :(")
    return score, pattern


def right_word_guess(updated_pattern, score, correct_word):
    space_counter = 0
    for i in updated_pattern:
        if i == "_":
            space_counter += 1
    n = space_counter
    new_points = (n * (n + 1)) // 2
    score += new_points
    updated_pattern = correct_word
    return updated_pattern, score


def letter_is_invalid(letter: str, pattern: str, guess_list: list) -> bool:
    """
    checks if the user's input is invalid by length, lowercase, if is string or already guessed before.
    :param letter: the user's input (guessed letter)
    :param pattern: the current pattern
    :param guess_list: the wrong guess list of already guessed letters
    :return: True: if the input is invalid, and False: if it's valid
    """
    invalid_input = not (isinstance(letter, str)) \
                    or not (str.islower(letter)) \
                    or (len(letter) > 1) \
                    or (letter in pattern) \
                    or letter in guess_list \
                    or not letter.isalpha()
    if invalid_input:
        return True
    else:
        return False


def right_letter_score(correct_word: str, guessed_letter: str, score: int) -> int:
    """
    adding points to the player after guessing the word right
    :param correct_word: the current word being guessed
    :param guessed_letter: the already wrong guessed letters
    :param score: the current points of the player
    :return: the updated sum of total points of the player
    """
    letter_counter = 0
    for letter in correct_word:
        if guessed_letter == letter:
            letter_counter += 1
    n = letter_counter
    new_points = (n * (n + 1)) // 2
    score += new_points
    return score


def filter_words_list(words: list, pattern: str, wrong_guess_lst: list) -> list:
    """
    filters words for a hint which is a list of words
    :param words: word bank which is the origin of the hint and guessed word
    :param pattern: the current pattern
    :param wrong_guess_lst: the wrong guess list of already guessed letters
    :return: a list of suggested words as a hint
    """
    matches = []
    for word in words:
        match = is_match(pattern, word, wrong_guess_lst)
        if match:
            matches.append(word)
    if len(matches) > hangman_helper.HINT_LENGTH:
        return shrink_hint_list(matches)
    else:
        return matches


def shrink_hint_list(matches):
    n = len(matches)
    new_matches = []
    for i in range(hangman_helper.HINT_LENGTH):
        new_matches.append(matches[(i * n) // hangman_helper.HINT_LENGTH])
    return new_matches


def is_match(pattern: str, word: str, wrong_guess_lst: list) -> bool:
    """
    checks if a word is a good match for a hint.
    :param pattern: the pattern the func compare the word to
    :param word: the word the func checks
    :param wrong_guess_lst: a list of the wrong guesses until now
    :return: bool - True: if match to hint, False: doesn't match
    """
    match = True
    if len(word) == len(pattern):
        for i in range(len(pattern)):
            if pattern[i] == "_":
                if word[i] in pattern:
                    match = False
                elif word[i] in wrong_guess_lst:
                    match = False
                else:
                    pass
            elif pattern[i] == word[i]:
                pass
            else:
                match = False
    else:
        match = False
    return match


def get_hint(score: int, updated_pattern: str, wrong_guess_lst: list, words_list: list, correct_word: str) -> int:
    """
    actions after a player asks for a hint
    :param correct_word:
    :param score: the current points of the player so far
    :param updated_pattern: the current pattern
    :param wrong_guess_lst: the wrong guess list of already guessed letters
    :param words_list: a bank of words for the hint
    :return: the amount of point the player has left after asking for a hint
    """
    score += -1
    matches = filter_words_list(words_list, updated_pattern, wrong_guess_lst)
    hangman_helper.show_suggestions(matches)
    if score == 0:
        hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "\n" "You lost. "
                                                                              "The correct word was: " + correct_word)
    else:
        hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "Here's your hint." + "\n")
    return score


def run_single_game(words_list: list, score: int = hangman_helper.POINTS_INITIAL) -> int:
    """
    runs a single game
    :param words_list: the list of word which we play with as a word bank
    :param score: the score at the beginning of the game
    :return: the score at the end of the game
    """
    updated_pattern, word, wrong_guess_lst = initiate_single_game(score, words_list)
    end_game = False
    while not end_game:
        (type_of_input, the_input) = hangman_helper.get_input()
        if type_of_input == hangman_helper.LETTER:
            # player guessed a letter
            score, updated_pattern, wrong_guess_lst = guess_is_letter(the_input, score, updated_pattern, word,
                                                                      wrong_guess_lst)
        elif type_of_input == hangman_helper.WORD:
            # player guessed a word
            score, updated_pattern = guess_is_word(updated_pattern, the_input, score, word, wrong_guess_lst)
        elif type_of_input == hangman_helper.HINT:
            # player asked for a hint
            score = get_hint(score, updated_pattern, wrong_guess_lst, words_list, word)
        else:
            return score
        if score <= 0 or updated_pattern == word:
            end_game = True
            break
    return score


def initiate_single_game(score, words_list):
    word = hangman_helper.get_random_word(words_list)
    pattern = "_" * (len(word))
    updated_pattern = pattern
    wrong_guess_lst = []
    hangman_helper.display_state(updated_pattern, wrong_guess_lst, score, "Lets start!" + "\n")
    return updated_pattern, word, wrong_guess_lst


def main() -> None:
    words_list = hangman_helper.load_words()
    round_of_games(words_list)


def round_of_games(words_list: list) -> None:
    play_again = True
    game_counter = 0
    score = hangman_helper.POINTS_INITIAL
    while play_again:
        game_counter += 1
        score = run_single_game(words_list, score)
        msg_points = str(score)
        msg_rounds = str(game_counter)
        play_again = another_round(msg_points, msg_rounds, play_again, score, words_list)
        if not play_again:
            break
        else:
            pass


def another_round(msg_points, msg_rounds, play_again, score, words_list):
    if score > 0:
        if hangman_helper.play_again("Your current score is have " + msg_points + " points, and played "
                                     + msg_rounds + " games. Would you like to play one more game?"):
            play_again = True
            return play_again
        else:
            play_again = False
            return play_again
    elif hangman_helper.play_again("You survived " + msg_rounds + " games. Would you like to try again?"):
        play_again = True
        round_of_games(words_list)
    else:
        play_again = False
        return play_again


if __name__ == "__main__":
    main()
