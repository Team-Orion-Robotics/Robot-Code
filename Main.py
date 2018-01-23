#pip install git+https://github.com/sourcebots/robot-api

from robot import Robot #Fucking hate this shite language
from robot import BRAKE
from robot import COAST

import math
import time
import datetime

r = Robot()
motor_board = r.motor_board

Home_Base_Colour = str
Home_Base_Token_1 = int
Home_Base_Token_2 = int

Team_Tokens = [0,0,0,0,0]

Our_Tokens

Start_Time = datetime.datetime.now()

count = 0

#region Movement Code

def Move(Speed, Time, Brake_Or_Coast):

    if Speed > 1 or Speed < -1:
        print("ATTEMPT TO CALL MOVE FUNCTION WITH INVALID SPEED")
        return
    
    r.motor_board.m0 = Speed
    r.motor_board.m1 = Speed
    time.sleep(Time)

    if (Break_Or_Coast == "Brake"):
        r.motor_board.m0 = BRAKE
        r.motor_board.m1 = BRAKE

    elif (Break_Or_Coast == "Coast"):
        r.motor_board.m0 = COAST
        r.motor_board.m1 = COAST

    else:
        print("Im confused") #When neither Break or Coast is passed through
        
    print("Moved at {} power for {} seconds".format(Speed, Time))

def Rotate(Speed, Time, Brake_Or_Coast):

    if Speed > 1 or Speed < -1:
        print("ATTEMPT TO CALL ROTATE FUNCTION WITH INVALID SPEED")
        return
    
    r.motor_board.m0 = -Speed
    r.motor_board.m1 = Speed
    time.sleep(Time)
    
    if (Break_Or_Coast == "Brake"):
        r.motor_board.m0 = BRAKE
        r.motor_board.m1 = BRAKE

    elif (Break_Or_Coast == "Coast"):
        r.motor_board.m0 = COAST
        r.motor_board.m1 = COAST

    else:
        print("Im confused")

    print("Moved Forward at {} power for {} seconds".format(Speed, Time))

#endregion

#region Servo control #Only uncomment all this shit when the servo board is connected, otherwise it will throw and error and crash
#def Lower_Front_Barrier():
#    r.servo_board.servos[0].position = -1  #Ensure the front Servo is connected to the S2

#def Raise_Front_Barrier():
#    r.servo_board.servos[0].position = 1

#def Lower_Rear_Barrier():
#    r.servo_board.servos[1].position = -1  #Ensure the rear Servo is cnnected to the S1

#def Raise_Rear_Barrier():
#    r.servo_board.servos[1].position = 1

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
    Done = False

    Rotate(1, 0.7, "Brake") #rotate 90 degress left, alter to ensure we are turning 90 degrees by changeing the time value (measured in seconds)
    				#comment out if we are allowed to start our robot facing our home base token
    while (Done == False):  #This while is being used to determine what colour our home base is. if for whatever reason we don't turn enough at the start and we can't see any tokens, the robot will turn slightly and try again. 
        markers = r.camera.see()
        if (len(Markers) > 0):
            for m in Markers:
                if (m.id == 0 or m.id == 27):
			if (m.cartesian.z < 2): #m.cartesian.z will return the distance in meters, checking the marker we are looking at
                    		Home_Base_Colour = "Pink" #is indeed ours and not another teams. if its more than 2 meters away we fucked up.
                    		Home_Base_Token_1 = 0
                    		Home_Base_Token_2 = 27
                    		Done = "True"

                elif (m.id == 6 or m.id == 7):
			if (m.cartesian.z < 2):
                    		Home_Base_Colour = "Green"
                    		Home_Base_Token_1 = 6
                   		Home_Base_Token_2 = 7
                    		Done = "True"

                elif (m.id == 13 or m.id == 14):
			if (m.cartesian.z < 2):
                    		Home_Base_Colour = "Yellow"
                    		Home_Base_Token_1 = 13
                    		Home_Base_Token_2 = 14
                    		Done = "True"

                elif (m.id == 20 or m.id == 21):
			if (m.cartesian.z < 2):
                    		Home_Base_Colour = "Orange"
                    		Home_Base_Token_1 = 20
                    		Home_Base_Token_2 = 21
                    		Done = "True"

                else:
                    Done = "False"
        else:
            Rotate(1, 0.05, "Brake") #Rotate Left a little more in the hope of finding a home base token
            count += 1 #counts how many extra times the robot has spun so we can rotate back the same number of times

    Rotate(1, 0.7, "Brake") #Ensure this is the same as the first rotation as above as this function is used to rotate the robot back to its starting position
    
    if count > 0:
        Rotate(1, (0.05*count), "Brake") #These numbers must be the same as in the previous while loop

    count = 0
    print("Home colour is: {}. Home tokens are: {} and {}".format(Home_Base_Colour, Home_Base_Token_1, Home_Base_Token_2))
    print("Facing starting direction")

def Test_Stuff():
	Move(1, 2, "Brake")
	time.sleep(2)
	Move(1, 2, "Brake")
	time.sleep(2)
	Rotate(1, 2, "Brake")
	time.sleep(2)
	Rotate(1, 2, "Brake")
	time.sleep(2)

	Done = False
	
	while (Done == False):
		if (Check_If_Time_To_Return() == True):
			Done = True
			r.motor_board.m0 = BRAKE
			r.motor_board.m1 = BRAKE
		else:
			Rotate(1, 1, "Coast")
			Done = False

def Home_Token_Test():
	Set_Home_Tokens()
	
def Set_Team_Tokens():
	if (Home_Base_Colour == "Pink"):
		marker = 44
		print("Our markers are: ")
		for x in range(0, 4):
			Team_Tokens[x] = marker + x
			print(Team_Tokens[x])
		
	elif (Home_Base_Colour == "Green"):
		marker = 50
		print("Our markers are: ")
		for x in range(0, 4):
			Team_Tokens[x] = marker + x	
			print(Team_Tokens[x])
			
	elif (Home_Base_Colour == "Yellow"):
		marker = 55
		print("Our markers are: ")
		for x in range(0, 4):
			Team_Tokens[x] = marker + x
			print(Team_Tokens[x])
			
	elif (Home_Base_Colour == "Orange"):
		marker = 60
		print("Our markers are: ")
		for x in range(0, 4):
			Team_Tokens[x] = marker + x
			print(Team_Tokens[x])
			
	else:
		print("Something went wrong, we don't have a home base colour")
