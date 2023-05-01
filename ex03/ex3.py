#################################################################
# FILE : ex3.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex1 2021
# DESCRIPTION: A program which includes functions of ex3
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES:
#################################################################


def input_list():
    """
    :return: Sum of all the user's inputs
    """
    nums_input_lst = []
    user_input = None
    while user_input != "":
        user_input = input()
        if user_input != "":
            nums_input_lst.append(float(user_input))
    lst_num = 0
    for i in range(len(nums_input_lst)):
        lst_num += nums_input_lst[i]
    nums_input_lst.append(lst_num)
    return nums_input_lst


#################################################################


def inner_product(vec_1, vec_2):
    """
    :param vec_1: A list of vector 1 entries
    :param vec_2: A list of vector 1 entries
    :return: The inner product of vector 1 and vector 2
    """
    product = 0
    if len(vec_1) != len(vec_2):
        return None
    elif len(vec_1) == 0:
        return 0
    else:
        for j in range(len(vec_1)):
            product += vec_1[j] * vec_2[j]
        return product


#################################################################


def sequence_monotonicity(sequence):
    """
    :param sequence: A list of 4 numbers
    :return: Monotonicity of the sequence
    """
    bool_table = [True, True, True, True]

    for i in range(len(sequence)-1):
        """ Check if increasing """
        if sequence[i] <= sequence[i+1]:
            bool_table[0] = True
        else:
            bool_table[0] = False
            break

    for i in range(len(sequence) - 1):
        """ Check if strictly increasing """
        if sequence[i] < sequence[i + 1]:
            bool_table[1] = True
        else:
            bool_table[1] = False
            break

    for i in range(len(sequence) - 1):
        """ Check if decreasing """
        if sequence[i] >= sequence[i + 1]:
            bool_table[2] = True
        else:
            bool_table[2] = False
            break

    for i in range(len(sequence) - 1):
        """ Check if strictly decreasing """
        if sequence[i] > sequence[i + 1]:
            bool_table[3] = True
        else:
            bool_table[3] = False
            break
    return bool_table


#################################################################


def monotonicity_inverse(bool_list):
    """
    :param bool_list: A list of 4 boolean values for monotonicity type
                        [increasing, strictly increasing, decreasing, strictly decreasing]
    :return: An example of a 4 numbers sequence matching the boolean list
    """
    increasing = bool_list[0]
    strictly_increasing = bool_list[1]
    decreasing = bool_list[2]
    strictly_decreasing = bool_list[3]

    if (increasing and strictly_increasing) and not (decreasing or strictly_decreasing):
        return [1, 2, 3, 4]

    elif increasing and not (strictly_increasing or decreasing or strictly_decreasing):
        return [1, 2, 2, 3]

    elif decreasing and not (increasing or strictly_increasing or strictly_decreasing):
        return [3, 2, 2, 1]

    elif (decreasing and strictly_decreasing) and not (increasing or strictly_increasing):
        return [4, 3, 2, 1]

    elif (increasing and decreasing) and not (strictly_increasing or strictly_decreasing):
        return [1, 1, 1, 1]

    elif not (increasing or strictly_increasing or decreasing or strictly_decreasing):
        return [1, 0, -1, 1]

    else:
        return None


#################################################################


def primes_for_asafi(n):
    """
    :param n: A number representing the amount of first prime numbers asafi wants
    :return: The first 'n' prime numbers
    """
    divisors = []
    primes = []

    if n > 0:
        for i in range(2, 10*n):
            if len(primes) >= n:
                break
            is_prime = True
            for j in divisors:
                if i % j == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(i)
                divisors.append(i)
        return primes
    else:
        primes = []
        return primes


#################################################################


def sum_of_vectors(vec_lst):
    """
    :param vec_lst: A list of lists -
                    Every sub-list is a vector represented by the list of the vector's entries
                    All sub-lists must be in the same length
    :return: The sum of all the vectors in the list
    """
    if len(vec_lst) == 0:
        """ no vectors in list """
        return None
    elif len(vec_lst[0]) == 0:
        """ vectors are 'empty' """
        return []
    else:
        """ calculate the sum """
        vectors_sum = []
        for i in range(len(vec_lst[0])):
            vectors_sum.append(0)
            for j in range(len(vec_lst)):
                vectors_sum[i] = vectors_sum[i] + vec_lst[j][i]
        return vectors_sum


#################################################################


def num_of_orthogonal(vectors):
    """
    :param vectors: A list of lists = Every sub-list is a vector
    :return: Number of orthogonal pairs from the vectors list
    """
    num_of_pairs = 0
    for i in range((len(vectors)//2)+1):
        for j in vectors[-1:i:-1]:
            if inner_product(vectors[i], j) == 0:
                num_of_pairs += 1
    return num_of_pairs


#################################################################


if __name__ == "__main__":
    input_list()
    inner_product()
    sequence_monotonicity()
    monotonicity_inverse()
    primes_for_asafi()
    sum_of_vectors()
    num_of_orthogonal()
