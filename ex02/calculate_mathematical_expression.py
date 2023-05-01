#################################################################
# FILE : math_print.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that calculates
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################


def calculate_mathematical_expression(num1,num2,action):
    action_option = {':', '*', '-', '+'}
    if (action not in action_option) or (type(num1) == str or type(num2) == str):
        return None
    elif action == ':':
        if num2 == 0:
            return None
        else:
            return num1/num2
    elif action == '*':
        return num1*num2
    elif action == '-':
        return num1-num2
    elif action == '+':
        return num1+num2


def calculate_from_string(cal):
    calculation = cal.split()
    if len(calculation) == 3:
        num1_brus = float(calculation[0])
        num2_brus = float(calculation[2])
        action_brus = calculation[1]
        return calculate_mathematical_expression(num1_brus,num2_brus,action_brus)
    else:
        return None


if __name__ == "__main__" :
    calculate_mathematical_expression()
    calculate_from_string()