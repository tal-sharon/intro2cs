#################################################################
# FILE : math_print.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that returns max and min
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################

###########################################################################################
# I chose these tests to cover different inputs which would lead the the function to use
# different conditions and may result different errors and uncover mistakes in the code.
# First two given tests covers results of:
# (only one largest = c, only one smallest = b), (two numbers are the smallest = b, c).
# I added to more test for: (two numbers are largest), (all numbers are even).
###########################################################################################

def largest_and_smallest(num1,num2,num3):
    largest = num1
    smallest = num1
    if num1 < num2:
        largest = num2
        if num2 < num3:
            largest = num3
            return largest,smallest
        elif num1 < num3:
            return largest,smallest
        else:
            smallest = num3
            return largest,smallest
    elif num3 < num2:
        smallest = num3
        return largest,smallest
    elif num1 < num3:
        largest = num3
        smallest = num2
        return largest,smallest
    else:
        smallest = num2
        return  largest,smallest


def check_largest_and_smallest():
    if largest_and_smallest(6,1,17) == (17,1):
        if largest_and_smallest(2,1,1) == (2,1):
            if largest_and_smallest(4,2,4) == (4,2):
                if largest_and_smallest(7,7,7) == (7,7):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:()
        return False


if __name__ == "__main__" :
    check_largest_and_smallest()