#################################################################
# FILE : math_print.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that checks if vormir is safe
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################


def is_vormir_safe(temp_bar,temp_day1,temp_day2,temp_day3):
    if temp_day1 > temp_bar:
        if temp_day2 > temp_bar:
            return True
        else:
            return False
    elif temp_day2 > temp_bar:
        if temp_day3 > temp_bar:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__" :
    is_vormir_safe()