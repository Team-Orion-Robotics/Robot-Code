#pip install git+https://github.com/sourcebots/robot-api

from robot import Robot
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

	if (Brake_Or_Coast == "Brake"):
		r.motor_board.m0 = BRAKE
		r.motor_board.m1 = BRAKE

	elif (Brake_Or_Coast == "Coast"):
		r.motor_board.m0 = COAST
		r.motor_board.m1 = COAST

	else:
		r.motor_board.m0 = BRAKE
		r.motor_board.m1 = BRAKE #When neither Brake or Coast is passed throgh, just Brake
        
	print("Moved at {} power for {} seconds".format(Speed, Time))

def Rotate(Speed, Time, Brake_Or_Coast):

	if Speed > 1 or Speed < -1:
		print("ATTEMPT TO CALL ROTATE FUNCTION WITH INVALID SPEED")
		return
    
	r.motor_board.m0 = -Speed
	r.motor_board.m1 = Speed
	time.sleep(Time)
    
	if (Brake_Or_Coast == "Brake"):
		r.motor_board.m0 = BRAKE
		r.motor_board.m1 = BRAKE

	elif (Brake_Or_Coast == "Coast"):
		r.motor_board.m0 = COAST
		r.motor_board.m1 = COAST

	else:
		r.motor_board.m0 = BRAKE
		r.motor_board.m1 = BRAKE #When neither Brake or Coast is passed throgh, just Brake

	print("Rotated at {} power for {} seconds".format(Speed, Time))

#endregion

#region Ultrasound
def Ultrasound(Mod):
	if (Mod == 0):
		Trigger = 9
		Echo = 8
	elif(Mod == 1):
		Trigger = 9
		Echo = 8
	elif(Mod == 2):
		Trigger = 11
		Echo = 10
	elif(Mod == 3):
		Trigger = 11
		Echo = 10
	print("Returned " + str(r.servo_board.read_ultrasound(Trigger, Echo)) + " for Module " + str(Mod))
	return r.servo_board.read_ultrasound(Trigger, Echo)

def UltrasoundDist(FOR,Dist,Tol):
	speed = 1
	LEFT = 0
	RIGHT = 1
	if (FOR == "R"):
		speed = -1
		LEFT = 2
		RIGHT = 3
	done = True
	while done == True:			
		DTO = Ultrasound(LEFT)
		#R = Ultrasound(RIGHT)
		#if(DTO > R):
		#	DTO = R
		if (DTO < Dist - Tol):
			Move(-speed,0.3,"Brake")
		elif(DTO > Dist + Tol):
			Move(speed,0.3,"Coast")
		elif(DTO > Dist - Tol and DTO < Dist + Tol):
			done = False

def UltrasoundTest(Dist,Tol):
	done = True
	while done == True:
		UltrasoundDist("F",Dist,Tol)
		print("Forward done")
		time.sleep(1)
		UltrasoundDist("R",Dist,Tol)
		print("Reverse done")

#endregion

#region Servo control
def Lower_Front_Barrier():
    r.servo_board.servos[0].position = -1  #Ensure the front Servo is connected to the S0
    time.sleep(1000) #Change to ensure Barrier is fully lowered
    
def Raise_Front_Barrier():
    r.servo_board.servos[0].position = 1
    time.sleep(1000) #Change to ensure Barrier is fully lowered

def Lower_Rear_Barrier():
    r.servo_board.servos[1].position = -1 #Ensure the rear Servo is cnnected to the S1
    time.sleep(1000) #Change to ensure Barrier is fully lowered


def Raise_Rear_Barrier():
    r.servo_board.servos[1].position = 1
    time.sleep(1000) #Change to ensure Barrier is fully lowered

#endregion

def Check_If_Time_To_Return(): #We need to call this literally whenever possible as it will only check when called. Will return True if time remaining is less than 45 seconds. and False if more than 45 seconds is left. This can be tweeked as needed depending on speed of Robot
	Stuff = False

	seconds = 0

	Difference = datetime.datetime.now() - Start_Time
	seconds = Difference.seconds

	remaining_time = 150 - seconds

	print("Time remaining: {}".format(remaining_time))

	if (remaining_time < 30):
		print("Time to Return")
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
					if (m.cartesian.z < 2):#m.cartesian.z will return the distance in meters, checking the marker we are looking at
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
    
	if (count > 0):
		for x in range (1, count):
			Rotate(1, (0.05*count), "Brake") #These numbers must be the same as in the previous while loop

	count = 0
	print("Home colour is: {}. Home tokens are: {} and {}".format(Home_Base_Colour, Home_Base_Token_1, Home_Base_Token_2))
	print("Facing starting direction")
	
def Set_Team_Tokens():
	if (Home_Base_Colour == "Pink"):
		marker = 45
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
