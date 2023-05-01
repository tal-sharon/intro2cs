from typing import List, Union, Any
import ex7_helper


##############################################################################
# FILE: ex7.py
# EXERCISE: Intro2cs ex7 2021-2022
# WRITER: Tal Sharon, 315813980, talsharon
# DESCRIPTION: a series of different recursive functions
##############################################################################


def mult(x: float, y: int) -> float:
    """
    conducts multiplication of two numbers
    :param x: the number being multiplied
    :param y: the numbers of multiplications
    :return: the result
    """
    if y == 0 or x == 0:
        return 0
    return ex7_helper.add(x, mult(x, ex7_helper.subtract_1(y)))


def is_even(n: int) -> bool:
    """
    check if a number is even or not
    :param n: the number being checked
    :return: True: if even, False: if not even
    """
    if n == 0:
        return True
    elif n < 0:
        return False
    return is_even(ex7_helper.subtract_1(ex7_helper.subtract_1(n)))


def log_mult(x: float, y: int) -> float:
    """
    conducts multiplication of two numbers in O(log n)
    :param x: the number being multiplied
    :param y: the numbers of multiplications
    :return: the result
    """
    if y == 0 or x == 0:
        return 0
    if ex7_helper.is_odd(y):
        z = log_mult(x, ex7_helper.divide_by_2(y))
        return ex7_helper.add(x, ex7_helper.add(z, z))
    else:
        z = log_mult(x, ex7_helper.divide_by_2(y))
        return ex7_helper.add(z, z)


def is_power(b: int, x: int) -> bool:
    """
    checks if x is a power of b
    :param b: the base
    :param x: the number being checked
    :return: True: if x is a power of b, False: if it isn't
    """
    return _is_power_helper(b, x, b)


def _is_power_helper(power_base: Union[int, float], x: int, b: int) -> bool:
    """
    a sub-function which helps to determine if a number is a power of another
    :param power_base: the current base
    :param x: the number being checked
    :param b: the original base
    :return: True: if x is a power of b, False: if it isn't
    """
    if x == power_base or x == 1:
        return True
    elif b == 0 or x == 0:
        return False
    elif b == 2 and is_even(x):
        return True
    elif x < power_base:
        return False
    else:
        return _is_power_helper(log_mult(power_base, b), x, b)


def reverse(s: str) -> str:
    """
    reverse a string
    :param s: a string
    :return: the reversed string
    """
    return _reverse_helper(s, '', ex7_helper.subtract_1(len(s)))


def _reverse_helper(s: str, new_str: str, ind: int) -> str:
    """
    a sub-function which helps to reverse a string
    :param s: a string
    :param new_str: the new reversed string
    :param ind: the index in the string
    :return: the new reversed string
    """
    if len(s) <= 1:
        return s
    elif len(new_str) == len(s):
        return new_str
    new_str = ex7_helper.append_to_end(new_str, s[ind])
    return _reverse_helper(s, new_str, ex7_helper.subtract_1(ind))


def play_hanoi(Hanoi: Any, n: int, src: Any, dest: Any, temp: Any) -> None:
    """
    a function which solves Hanoi Tower game
    :param Hanoi: a complex object
    :param n: number of disks
    :param src: the source pole
    :param dest: the destination pole
    :param temp: the temporary pole
    :return: None
    """
    if n < 0 or n == 0:
        return None
    elif n == 1:
        Hanoi.move(src, dest)
        return None
    else:
        play_hanoi(Hanoi, ex7_helper.subtract_1(n), src, temp, dest)
        play_hanoi(Hanoi, 1, src, dest, temp)
        play_hanoi(Hanoi, ex7_helper.subtract_1(n), temp, dest, src)


def number_of_ones(n: int) -> int:
    """
    gets the number of ones appearing in all number smaller to n and on n itself
    :param n: the number
    :return: the number of ones
    """
    return _num_of_ones_helper(n, 0)


def ones_single_num(n: int, count: int) -> int:
    """
    a sub-function which counts the number of ones in a single number
    :param n: the number
    :param count: the general count
    :return: the new count
    """
    if n == 0:
        return count
    if n % 10 == 1:
        count += 1
    if n >= 10:
        count = ones_single_num(n // 10, count)
    return count


def _num_of_ones_helper(n: int, count: int) -> int:
    """
    a sub-function which helps count all the ones appearing in all number smaller to n and on n itself
    :param n: the number
    :param count: the count of the ones
    :return: the final count of ones
    """
    if n == 0:
        return count
    count += _num_of_ones_helper(ex7_helper.subtract_1(n), count)
    count = ones_single_num(n, count)
    return count


def compare_2d_lists(l1: List[List[int]], l2: List[List[int]]) -> bool:
    """
    compares two 2D lists and determines if they're identical
    :param l1: first list
    :param l2: second list
    :return: True: if the lists are identical, False: if they're not
    """
    if check_legal_lists(l1, l2, 0):
        if_true = _compare_lists_helper(l1, l2, 0, 0)
        return if_true
    return False


def _compare_lists_helper(l1: List[List[int]], l2: List[List[int]], row: int, column: int) -> bool:
    """
    compares each item on the in l1 and l2
    :param l1: first list
    :param l2: second list
    :param row: the row index being checked
    :param column: the column index being checked
    :return: True: if the lists are identical, False: if they're not
    """
    if row == len(l1) and column == len(l1[0]):
        return True
    if check_legal_lists(l1, l2, row):
        if_true = go_through_lists(l1, l2, row, column)
        return if_true
    else:
        return False


def check_legal_lists(l1: List[List[int]], l2: List[List[int]], row: int) -> bool:
    """
    checks if the lists are "legal" by length before comparing each item
     :param l1: first list
    :param l2: second list
    :param row: the row index being checked
    :return: True: if length of rows are equal, False: if not
    """
    if len(l1) == len(l2):
        if row == len(l1) and row == len(l2):
            return True
        if len(l1[row]) == len(l2[row]):
            if_true = check_legal_lists(l1, l2, int(ex7_helper.add(row, 1)))
            return if_true
        else:
            return False
    else:
        return False


def go_through_lists(l1: List[List[int]], l2: List[List[int]], row: int, column: int) -> bool:
    """
    goes through both lists and compares the items
    :param l1: first list
    :param l2: second list
    :param row: the row index being checked
    :param column: the column index being checked
    :return: True: if items are identical, False: if they aren't
    """
    if row == len(l1) or column == len(l1[row]):
        return True
    if l1[row][column] == l2[row][column]:
        if go_through_lists(l1, l2, row, int(ex7_helper.add(column, 1))):
            if_true = go_through_lists(l1, l2, int(ex7_helper.add(row, 1)), column)
            return if_true
        else:
            return False
    else:
        return False


def magic_list(n: int) -> List[Any]:
    """
    Creates a magic list by the number requested
    :param n: the number of items
    :return: the magic list
    """
    if n == 0:
        return []
    result: List[Any] = []
    return _magic_helper(n, result)


def _magic_helper(n: int, result: List[Any]) -> List[Any]:
    """
    a sub-function creating the magic list
    :param n: the number of items
    :param result: the current list
    :return: the new list
    """
    if n == 1:
        result.append([])
        return result[:]
    result.append(_magic_helper(n - 1, result))
    return result[:]
