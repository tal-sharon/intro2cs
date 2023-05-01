#################################################################
# FILE : math_print.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that solves quadratic equations
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################


def quadratic_equation(a,b,c):
    solution01 = (-b + (b**2 - (4*a*c))**0.5)/2*a
    solution02 = (-b - (b**2 - (4*a*c))**0.5)/2*a
    if solution01 == solution02:
        solution02 = None
        return solution01, solution02
    elif (b**2 - (4*a*c)) < 0:
        solution01 = None
        solution02 = None
        return solution01,solution02
    else:
        return solution01, solution02


def quadratic_equation_user_input():
    coefficients = input("Insert coefficients a, b, and c: ")
    input_split = coefficients.split()
    input_num_a = float(input_split[0])
    input_num_b = float(input_split[1])
    input_num_c = float(input_split[2])
    sol_1, sol_2 = quadratic_equation(input_num_a,input_num_b,input_num_c)

    if input_num_a == 0:
        print("The parameter 'a' may not equal 0")
    elif sol_1 == None:
        print("The equation has no solutions")
    elif sol_2 == None:
        print("The equation has 1 solution:", sol_1)
    else:
        print("The equation has 2 solutions:", sol_1, "and", sol_2)


if __name__ == "__main__" :
    quadratic_equation_user_input()