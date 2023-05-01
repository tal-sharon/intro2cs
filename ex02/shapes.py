#################################################################
# FILE : math_print.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex2 2021
# DESCRIPTION: A simple program that gets the area of a shape
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################


import math


def shape_area():
    shape_input = input("Choose shape (1=circle, 2=rectangle, 3=triangle): ")
    options = ["1","2","3"]
    if shape_input not in options:
        return None
    elif shape_input == "1":
        circle_radius = float(input())
        circle_area = math.pi * (circle_radius)**2
        return circle_area
    elif shape_input == "2":
        side_1 = float(input())
        side_2 = float(input())
        rectangle_area = side_1 * side_2
        return rectangle_area
    else:
        triangle_side = float(input())
        triangl_area = (triangle_side**2 * math.sqrt(3)) / 4
        return triangl_area


if __name__ == "__main__" :
    shape_area()