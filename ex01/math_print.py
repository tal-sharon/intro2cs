#################################################################
# FILE : math_print.py
# WRITER : Tal Sharon , talsharon , 315813980
# EXERCISE : intro2cs2 ex1 2020
# DESCRIPTION: A simple program that prints
# STUDENTS I DISCUSSED THE EXERCISE WITH:
# WEB PAGES I USED:
# NOTES: ...
#################################################################
import math

def golden_ratio():
    print((1+5**0.5)/2)

def six_squared():
    print(6**2)

def hypotenuse():
    print(math.sqrt(12**2+5**2))

def pi():
    print(math.pi)

def e():
    print(math.e)

def squares_area():
    print(1*1,2*2,3*3,4*4,5*5,6*6,7*7,8*8,9*9,10*10)

if __name__ == "__main__" :
    golden_ratio()
    six_squared()
    hypotenuse()
    pi()
    e()
    squares_area()
