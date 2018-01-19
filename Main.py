#pip install git+https://github.com/sourcebots/robot-api

from robot import Robot
from robot import BRAKE
from robot import COAST

import math
import time
import datetime

r = Robot()
motor_board = r.motor_board

#FRONT_BARRIER = r.servo_board.servos[0] #Ensure the front barrier is connected to m0 port on servo board
#REAR_BARRIER = r.servo_board.servos[1] #Ensure the front barrier is connected to m1 port on servo board

Home_Base_Colour = str
Home_Base_Token_1 = int
Home_Base_Token_2 = int

Start_Time = datetime.datetime.now()

count = 0

#region Movement Code

def Move_forward(Speed, Time, Break_Or_Coast):
    r.motor_board.m0 = Speed
    r.motor_board.m1 = Speed
    time.sleep(Time)

    if (Break_Or_Coast == "Break"):
        r.motor_board.m0 = BRAKE
        r.motor_board.m1 = BRAKE

    elif (Break_Or_Coast == "Coast"):
        r.motor_board.m0 = COAST
        r.motor_board.m1 = COAST

    else:
        print("Im confused") #When neither Break or Coast is passed through
        
    print("Moved Forward at {Speed} power for {Time} seconds")

def Move_backwards(speed, Time, Break_Or_Coast):    #Example movement Call: Move_forward(1 (full speed), 1 (1 second), Coast (Will stop power to motors and coast) / Break (Will lock motors and stop robot))
    r.motor_board.m0 = -speed
    r.motor_board.m1 = -speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Break"):
        r.motor_board.m0 = BRAKE
        r.motor_board.m1 = BRAKE

    elif (Break_Or_Coast == "Coast"):
        r.motor_board.m0 = COAST
        r.motor_board.m1 = COAST

    else:
        print("Im confused")

    print("Moved Backwards at {Speed} power for {Time} seconds")

def Rotate_right(Speed, Time, Break_Or_Coast):
    r.motor_board.m0 = -Speed
    r.motor_board.m1 = Speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Break"):
        r.motor_board.m0 = BRAKE
        r.motor_board.m1 = BRAKE

    elif (Break_Or_Coast == "Coast"):
        r.motor_board.m0 = COAST
        r.motor_board.m1 = COAST

    else:
        print("Im confused")

    print("Rotated Right at {Speed} power for {Time} seconds")

def Rotate_left(Speed, Time, Break_Or_Coast):
    r.motor_board.m0 = Speed
    r.motor_board.m1 = -Speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Break"):
        r.motor_board.m0 = BRAKE
        r.motor_board.m1 = BRAKE

    elif (Break_Or_Coast == "Coast"):
        r.motor_board.m0 = COAST
        r.motor_board.m1 = COAST

    else:
        print("Im confused")

    print("Rotated Left at {Speed} power for {Time} seconds")

#endregion

#region Servo control
#def Lower_Front_Barrier():
#    FRONT_BARRIER.position = -1

#def Raise_Front_Barrier():
#    FRONT_BARRIER.position = 1

#def Lower_Rear_Barrier():
#    REAR_BARRIER.position = -1

#def Raise_Rear_Barrier():
#    REAR_BARRIER.position = 1

#endregion

def Check_If_Time_To_Return(): #We need to call this literally whenever possible as it will check. Will return True if time remaining is less than 45 seconds. and False if more than 45 seconds is left. This can be tweeked as needed depending on speed of Robot
    Done = False
    Stuff = False

    seconds = 0

    Difference = datetime.datetime.now() - Start_Time
    seconds = Difference.seconds
    print(seconds)

    time.sleep(0.5)

    if (seconds > 30):
        print("Time to Return")
        Done = True
        return True
    else:
        return False


def Set_Home_Tokens():
    Done = "False"

    Rotate_left(1, 0.7, "Break") #rotate 90 degress left, alter to ensure we are turning 90 degrees by changeing the time value (measured in seconds)
    
    while (Done == "False"):  #This while is being used to determine what colour our home base is. if for whatever reason we don't turn enough at the start and we can't see any tokens, the robot will turn slightly and try again. 
        Markers = r.camera.see()
        if (len(Markers) > 0):
            for m in Markers:
                if (m.id == 32 or m.id == 27):
                    Home_Base_Colour = "Pink"
                    Home_Base_Token_1 = 32
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
            Rotate_left(1, 0.05, "Break") #Rotate Left a little more in the hope of finding a home base token
            count += 1 #counts how many extra times the robot has spun so we can rotate back

    Rotate_right(1, 0.7, "Break") #Ensure this is the same as the first rotation as above as this function is used to rotate the robot back to its starting position
    
    if count > 0:
        Rotate_right(1, (0.05*count), "Break") #These numbers must be the same as in the previous while loop

    count = 0
    print("Home colour is: {Home_Base_Colour}. Home tokens are: {Home_Base_Token_1} and {Home_Base_Token_2}")
    print("Facing starting direction")

def Test_Stuff():
	Move_forward(1, 2, "Break")
	time.sleep(2)
	Move_backwards(1, 2, "Break")
	time.sleep(2)
	Rotate_right(1, 2, "Break")
	time.sleep(2)
	Rotate_left(1, 2, "Break")
	time.sleep(2)

	Done = False
	
	while (Done == False):
		if (Check_If_Time_To_Return() == True):
			Done = True
			r.motor_board.m0 = BRAKE
			r.motor_board.m1 = BRAKE
		else:
			Rotate_left(1, 1, "Coast")
			Done = False

def Home_Token_Test():
	Set_Home_Tokens()

Test_Stuff()
print("Test Successfull")
	
