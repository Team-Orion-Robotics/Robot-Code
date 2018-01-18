from robot import Robot
from robot import BRAKE
from robot import COAST

import math
import time

r = Robot()
motor_board = r.motor_board

RIGHT_MOTOR = r.motor_board.m0 #Ensure the right motor is plugged into the m0 plug
LEFT_MOTOR = r.motor_board.m1 #Ensure the left motor is plugged into the m1 plug

Home_Base_Colour = str
Home_Base_Token_1 = int
Home_Base_Token_2 = int

count = 0

def Move_forward(Speed, Time, Break_Or_Coast):
    RIGHT_MOTOR = Speed
    LEFT_MOTOR = Speed
    time.sleep(Time)

    if (Break_Or_Coast == "Break"):
        RIGHT_MOTOR = BREAK
        LEFT_MOTOR = BREAK

    elif (Break_Or_Coast == "Coast"):
        RIGHT_MOTOR = COAST
        LEFT_MOTOR = COAST

    else:
        print("Im confused")

    print("Moved Forward at {Speed} power for {Time} seconds")

def Move_backwards(speed, Time, Break_Or_Coast):    #Example movement Call: Move_foreward(1 (full speed), 1 (1 second), Coast (Will stop power to motors and coast) / Break (Will lock motors and stop robot))
    RIGHT_MOTOR = -speed
    LEFT_MOTOR = -speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Break"):
        RIGHT_MOTOR = BREAK
        LEFT_MOTOR = BREAK

    elif (Break_Or_Coast == "Coast"):
        RIGHT_MOTOR = COAST
        LEFT_MOTOR = COAST

    else:
        print("Im confused")

    print("Moved Backwards at {Speed} power for {Time} seconds")

def Rotate_right(Speed, Time, Break_Or_Coast):
    RIGHT_MOTOR = -Speed
    LEFT_MOTOR = Speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Break"):
        RIGHT_MOTOR = BREAK
        LEFT_MOTOR = BREAK

    elif (Break_Or_Coast == "Coast"):
        RIGHT_MOTOR = COAST
        LEFT_MOTOR = COAST

    else:
        print("Im confused")

    print("Rotated Right at {Speed} power for {Time} seconds")

def Rotate_left(Speed, Time, Break_Or_Coast):
    RIGHT_MOTOR = Speed
    LEFT_MOTOR = -Speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Break"):
        RIGHT_MOTOR = BREAK
        LEFT_MOTOR = BREAK

    elif (Break_Or_Coast == "Coast"):
        RIGHT_MOTOR = COAST
        LEFT_MOTOR = COAST

    else:
        print("Im confused")

    print("Rotated Left at {Speed} power for {Time} seconds")

def Find_Home_Tokens(Home_Base_Colour, Home_Base_Token_1, Home_Base_Token_2, count):
    Done = "False"

    Rotate_left(1, 0.1) #rotate 90 degress left, alter to ensure we are turning 90 degrees by changeing the time value (measured in seconds)
    
    while (Done == "False"):  #This while is being used to determine what colour our home base is
        Markers = r.camera.see()
        if len(Markers > 0):
            for m in Markers:
                if (m.id == 0 or m.id == 27):
                    Home_Base_Colour = "Pink"
                    Home_Base_Token_1 = 0
                    Home_Base_Token_2 = 27
                    Done = "True"

                elif (m.id == 6 or m.id == 7):
                    Home_Base_Colour = "Green"
                    Home_Base_Token_1 = 6
                    Home_Base_Token_2 = 7
                    Done = "True"

                elif (m.id == 13 or m.id == 14):
                    Home_Base_Colour = "Yellow"
                    Home_Base_Token_1 = 13
                    Home_Base_Token_2 = 14
                    Done = "True"

                elif (m.id == 20 or m.id == 21):
                    Home_Base_Colour = "Orange"
                    Home_Base_Token_1 = 20
                    Home_Base_Token_2 = 21
                    Done = "True"

                else:
                    Done = "False"
        else:
            Rotate_left(1, 0.05) #Rotate Left a little more in the hope of finding a home base token
            count += 1 #counts how many times the robot has spun

    Rotate_right(1, 0.1) #Ensure this is the same as the first rotation as above as this function is used to rotate the robot back to its starting position
    
    if count > 0:
        Rotate_right(1, (0.05*count)) #These numbers must be the same as in the previous while loop

    count = 0
    prinr("Home colour is: {Home_Base_Colour}. Home tokens are: {Home_Base_Token_1} and {Home_Base_Token_2}")
    print("Facing starting direction")

Markers = r.camera.see()


#pip install git+https://github.com/sourcebots/robot-api