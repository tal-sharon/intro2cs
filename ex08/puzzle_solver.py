from typing import List, Tuple, Set, Optional

##############################################################################
# FILE: puzzle_solver.py
# EXERCISE: Intro2cs ex8 2021-2022
# WRITER: Tal Sharon, 315813980, talsharon
# DESCRIPTION: a puzzler solver
##############################################################################


# We define the types of a partial picture and a constraint (for type checking).
Picture = List[List[int]]
Constraint = Tuple[int, int, int]


def max_seen_cells(picture: Picture, row: int, col: int) -> int:
    count = 0
    if picture[row][col] == 0:
        return count
    # up
    for up in range(row - 1, -1, -1):
        if picture[up][col] == 0:
            break
        if picture[up][col] == 1 or picture[up][col] == -1:
            count += 1
    # down
    for down in range(row, len(picture)):
        if picture[down][col] == 0:
            break
        if picture[down][col] == 1 or picture[down][col] == -1:
            count += 1
    # left
    for left in range(col - 1, -1, -1):
        if picture[row][left] == 0:
            break
        if picture[row][left] == 1 or picture[row][left] == -1:
            count += 1
    # right
    for right in range(col + 1, len(picture[0])):
        if picture[row][right] == 0:
            break
        if picture[row][right] == 1 or picture[row][right] == -1:
            count += 1
    return count


def min_seen_cells(picture: Picture, row: int, col: int) -> int:
    count = 0
    if picture[row][col] == 0 or picture[row][col] == -1:
        return count
    # up
    for up in range(row - 1, -1, -1):
        if picture[up][col] == 0 or picture[up][col] == -1:
            break
        if picture[up][col] == 1:
            count += 1
    # down
    for down in range(row, len(picture)):
        if picture[down][col] == 0 or picture[down][col] == -1:
            break
        if picture[down][col] == 1:
            count += 1
    # left
    for left in range(col - 1, -1, -1):
        if picture[row][left] == 0 or picture[row][left] == -1:
            break
        if picture[row][left] == 1:
            count += 1
    # right
    for right in range(col + 1, len(picture[0])):
        if picture[row][right] == 0 or picture[row][right] == -1:
            break
        if picture[row][right] == 1:
            count += 1
    return count


def check_constraints(picture: Picture, constraints_set: Set[Constraint]) -> int:
    all_con_valid = True
    cons_values = []
    for con in constraints_set:
        row, col, seen = con
        max_seen = max_seen_cells(picture, row, col)
        min_seen = min_seen_cells(picture, row, col)
        if seen < min_seen or seen > max_seen:
            return 0
        if min_seen <= seen <= max_seen and not min_seen == seen == max_seen:
            cons_values.append(False)
        else:
            cons_values.append(True)
    if False in cons_values:
        all_con_valid = False
    if all_con_valid:
        return 1
    else:
        return 2


def solve_puzzle(constraints_set: Set[Constraint], n: int, m: int) -> Optional[Picture]:
    board: Picture = initiate_board(constraints_set, n, m)
    picture: Picture = board[:]
    if check_constraints(picture, constraints_set) == 0:
        return None
    picture = make_move(picture, constraints_set, 0)
    if check_constraints(picture, constraints_set) == 1:
        return picture
    return None


def initiate_board(constraints_set: Set[Constraint], n: int, m: int) -> Picture:
    """
    creating the game board according the constraints
    :param constraints_set: the constraints set
    :param n: number of rows
    :param m: number of columns
    :return: the starting board
    """
    board = []
    for row in range(n):
        row_lst = []
        for col in range(m):
            row_lst.append(-1)
        board.append(row_lst)
    for con in constraints_set:
        row, col, seen = con
        if seen > 0:
            board[row][col] = 1
        else:
            board[row][col] = 0
    return board


def make_move(picture: Picture, constraints_set: Set[Constraint], ind: int):
    """
    makes a move in the puzzle
    :param picture: the temp_picture
    :param constraints_set: the constraints set
    :param ind: the index of the square
    :return: the updated picture
    """
    row, col = ind // len(picture[0]), ind % len(picture[0])
    if ind == len(picture) * len(picture[0]):
        return picture

    # if square is already black or white go on to the next square on the board
    if picture[row][col] != -1:
        if check_constraints(picture, constraints_set) == 1:
            complete_pic(picture)
        make_move(picture, constraints_set, ind + 1)
        return picture

    # get the next move according to the status of the board
    legal_rank = check_constraints(picture, constraints_set)
    for value in range(2):
        if legal_rank == 1:
            complete_pic(picture)
            return picture
        elif legal_rank == 2:
            picture[row][col] = value
            make_move(picture, constraints_set, ind + 1)
            if check_constraints(picture, constraints_set) == 1:
                complete_pic(picture)
                return picture
        else:
            break
    picture[row][col] = -1
    return picture


def complete_pic(picture):
    """
    completes a temp picture into a final full solution
    :param picture: the picture
    :return: the completed picture
    """
    for row in range(len(picture)):
        for col in range(len(picture[0])):
            if picture[row][col] == -1:
                picture[row][col] = 0


def how_many_solutions(constraints_set: Set[Constraint], n: int, m: int) -> int:
    board: Picture = initiate_board(constraints_set, n, m)
    picture: Picture = board[:]
    complete = is_complete(picture)
    if complete:
        return 1
    count = make_move_count(picture, constraints_set, 0, 0)
    return count


def is_complete(picture):
    """
    checks if the board is completed or not
    :param picture: the temp picture-board
    :return: bool - True: if the board is completed, False: if it isn't
    """
    is_finished = True
    for i in range(len(picture)):
        if -1 in picture[i]:
            is_finished = False
            break
    return is_finished


def make_move_count(picture: Picture, constraints_set: Set[Constraint], ind: int, count: int) -> int:
    """
    makes a move towards a solution, count one when found and goes on.
    :param picture: the temp picture
    :param constraints_set: the constraints set
    :param ind: the index of the square
    :param count: the count of solutions
    :return: the number of solutions found so far
    """
    row, col = ind // len(picture[0]), ind % len(picture[0])
    if ind == len(picture) * len(picture[0]):
        return count

    # if square is already black or white go on to the next square on the board
    if picture[row][col] != -1:
        count = make_move_count(picture, constraints_set, ind + 1, count)
        return count

    # get the next move according to the status of the board
    legal_rank = check_constraints(picture, constraints_set)
    for value in range(2):
        if legal_rank == 1:
            picture[row][col] = value
            count = make_move_count(picture, constraints_set, ind + 1, count)
            if is_complete(picture):
                count += 1
        elif legal_rank == 2:
            picture[row][col] = value
            count = make_move_count(picture, constraints_set, ind + 1, count)
            if check_constraints(picture, constraints_set) == 1:
                if is_complete(picture):
                    count += 1
        else:
            break
    picture[row][col] = -1
    return count


def generate_puzzle(picture: Picture) -> Set[Constraint]:
    constraints_lst = get_all_pos_cons(picture)
    essential_cons = []
    copy_cons = constraints_lst[:]
    for con in range(len(constraints_lst) - 1, -1, -1):
        copy_cons.pop()
        if is_essential(picture, copy_cons):
            essential_cons.append(constraints_lst[con])
            copy_cons.insert(0, constraints_lst[con])
    return set(essential_cons)


def is_essential(picture: Picture, constraints_set: List[Constraint]) -> bool:
    """
    checks the number a solutions of a certain constraints set
    :param picture: the picture being checked
    :param constraints_set: the constraints set
    :return: True: if there are more than 1 solution -> the constraint which was removed is essential
                False: if number of solutions remains 1
    """
    if len(constraints_set) == 0:
        return True
    sol_num = how_many_solutions(set(constraints_set), len(picture), len(picture[0]))
    if sol_num == 1:
        return False
    if sol_num > 1:
        return True


def get_all_pos_cons(picture: Picture) -> List[Constraint]:
    """
    gets all possible constraints out of a solution
    :param picture: the picture and solution
    :return: the possible constraints list
    """
    constraints_set = []
    for row in range(len(picture)):
        for col in range(len(picture[0])):
            if picture[row][col] == 0:
                constraints_set.append((row, col, 0))
            else:
                seen = min_seen_cells(picture, row, col)
                constraints_set.append((row, col, seen))
    return constraints_set
