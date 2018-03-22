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

Team_Tokens = [44,45,46,47,48]
Collected_Tokens = [False, False, False, False, False] #These correlate to the team tokens array above. C_T(0) = Token 44 etc...

Start_Time = datetime.datetime.now()

count = 0

STATE = "Drive To Our Boxes"  

#region Movement Code
def MotorBoardTest():
        for i in range(0, 1, 0.05):
                try:
                        Move(i, 0.5, "Brake")
                except:
                        print("Fucked it. Read last speed value")

def Move(Speed, Time, Brake_Or_Coast):

	if Speed > 1 or Speed < -1: #Need to change these values to ensure we don't overflow the motor board
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

	if Speed > 1 or Speed < -1: #Negative speed will rotate the robot left, positive speed right
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
		Trigger = 13
		Echo = 12
		
	print("Returned " + str(r.servo_board.read_ultrasound(Trigger, Echo)) + " for Module " + str(Mod))
	return r.servo_board.read_ultrasound(Trigger, Echo)

def UltrasoundDist(Direction, Dist, Tol):
	speed = 1
	LEFT = 0
	RIGHT = 1
	
	if (Direction == "R"):
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

def UltrasoundTest(Dist, Tol):
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

def Set_Home_Tokens(): #Shouldn't be needed as were assuming were in zone 0. However I have left it incase. 
	Done = False

	Rotate(1, 0.7, "Brake") #rotate 90 degress left, alter to ensure we are turning 90 degrees by changeing the time value (measured in seconds)
    				#comment out if we are allowed to start our robot facing our home base token
	while (Done == False):  #This while is being used to determine what colour our home base is. if for whatever reason we don't turn enough at the start and we can't see any tokens, the robot will turn slightly and try again. 
		markers = r.camera.see()
		if (len(Markers) > 0):
			for m in Markers:
				if (m.id == 0 or m.id == 27):
					if (m.spherical.distance_metres < 2):#m.cartesian.z will return the distance in meters, checking the marker we are looking at
						Home_Base_Colour = "Pink" #is indeed ours and not another teams. if its more than 2 meters away we fucked up.
						Home_Base_Token_1 = 0
						Home_Base_Token_2 = 27
						Done = "True"
				elif (m.id == 6 or m.id == 7):
					if (m.spherical.distance_metres < 2):
						Home_Base_Colour = "Green"
						Home_Base_Token_1 = 6
						Home_Base_Token_2 = 7
						Done = "True"
				elif (m.id == 13 or m.id == 14):
					if (m.spherical.distance_metres < 2):
						Home_Base_Colour = "Yellow"
						Home_Base_Token_1 = 13
						Home_Base_Token_2 = 14
						Done = "True"
				elif (m.id == 20 or m.id == 21):
					if (m.spherical.distance_metres < 2):
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
	
def Set_Team_Tokens(): #Shouldn't be needed, as we start in zone 0. However I am keeping it just in case. 
	marker = 0    
    
	if (Home_Base_Colour == "Pink"):
		marker = 44
	elif (Home_Base_Colour == "Green"):
		marker = 49
	elif (Home_Base_Colour == "Yellow"):
		marker = 54
	elif (Home_Base_Colour == "Orange"):
		marker = 59
	else:
		print("We don't have a home base colour, call Set_Home_Tokens() first")

		if (marker != 0):
			print("Our markers are: ")
			for x in range(0, 5):
				Team_Tokens[x] = marker + x
				print(Team_Tokens[x])

def SmoothAim(AimFor): #AimFor takes a marker object, but only the id is used
	D=AimFor.spherical.distance_metres
	Rot=AimFor.spherical.rot_y_radians
	
	Power=(7*4**(-abs(D))+0.5)*(0.2*Rot)+0.5
	
	print("Distance :%f Rotation :%f Power :%f"%(D,Rot,Power))
	
	if D<0.3:
		r.motor_board.m0 = 0.5
		r.motor_board.m1 = 0.5
	else:
	
		if Power <= 1 and Power >= -1:
			r.motor_board.m0 = 0.5
			r.motor_board.m1 = Power
			print("Lesser motor power of %f" % (Power))
		else:
			print("failed due to power issues")
			Move(-0.3,2,"Brake")
			
	try:
		return D
		
	except:
		print("Confused. Something crashed")
		return 100  
                
def Check_If_Time_To_Leave_Zone(ArrivalTime):
	CurrentTime = datetime.datetime.now()
	Difference = ArrivalTime - CurrentTime
	
	seconds = difference.seconds
	
	if (seconds > 20):
		print("Time to move on to next zone")
		return True
	else
		return False

		
While True: #Main STATE code
	if STATE == "BoxCollection":
		Return = False
		Raise_Front_Barrier() #Ready to accept new boxes

		while STATE == "BoxCollection"
			Done = True
			for i in range(0, 5):
				if CollectedTokens(i) == False:
					Done = False #We still have some boxes to collect

			if TimeToReturn() == True
				Return = True
				Done = True #We are out of time, break out of loop and return home. What we currently have in our possession will do. 

			if Done == False #Still have some boxes of ours to collect
				markers = r.camera.see()
				
				for m in markers: #Scans all the boxes we can see to see if we have dropped one. If the robot sees one we think is in our posetion, set it back to False
					for i in range(0, 5):
						if m.id == Team_Tokens(i) and Collected_Tokens(i) == True:
							Collected_Tokens(i) == False
							
					Skip = True #Used to determine if one of the tokens we see is one were hunting for or not.

					if len(markers) != 0: #we can see atleast 1 box
						for m in markers:
							for i in range(0, 5):
								if m.id == Team_Tokens(i): #One of the boxes we see, is one of our tokens
									Skip = False #As we saw a box of ours, we don't need to rotate away
									SmoothAim(m)
									#if Front Light Gate is triggered. Add that when the function is done. May insert this into smooth aim function
									Collected_Tokens((44 - m.id)) = True #Sets the collecte token to collected so we know when we have it.

							if Skip == True: #Didn't see one of our boxes. Time to rotate
								Rotate(1, 0.2, "Brake") #Rotate and try the above again. Keep rotating until we see one of our tokens basically.
								time.sleep(1) 
					else:
						Rotate(1, 0.2, "Brake") #Rotate until we can see a box
						time.sleep(1)
			else:
				if Return = True:
					STATE = "Return To Base" #Don't have time to check, just need to return to our base and drop current boxes
				else:
					STATE = "Check For Collected Tokens" #We have all our boxes, break out of the loop and do a 360 as a final check.
					Close_Front_Barrier() #Close barrier as we are done with box collection. 

	elif STATE == "Check For Collected Tokens" #Do a final check of Zone 0 to ensure we have all our boxes, and we havn't dropped or forgotten any while collecting.
		while STATE == "Check For Collected Tokens"
			for i in range(0, 5): #Make the second number the number of rotation calls it takes to do a full 360
				markers = r.camera.see()

				for m in markers:
					for i in range(0, 5):
						if m.id == Team_Tokens(i):
							Collected_Tokens(i) = False
							STATE = "BoxCollection"

			if STATE == "Check For Collected Tokens": #The Robot didn't see any of our tokens in its rotation, so were probably good
				if Check_If_Time_To_Return == False:
					STATE = "Zone 1" #Move to zone 1 and start messing with their shit
				else: #Time to return as were out of time
					STATE = "Return To Base"

	elif STATE == "Return To Base" #Need to wait till Dan's coord code works and is implemented to try and get this one working
		while STATE == "Return To Base" #When were in our base, set STATE to 'Zone 0'
			print("Something")
	
	elif STATE == "Zone 1" #Zone 1 State
		Arrival_Time = datetime.datetime.now()
		
		while STATE == "Zone 1":
			if Check_If_Time_To_Return == True:
				STATE == "Return To Base"
			elif Check_If_Time_To_Leave_Zone == True:
				STATE == "Zone 2"
				
	elif STATE == "Zone 2" #Zone 2 State
		Arrival_Time = datetime.datetime.now()
		
		while STATE == "Zone ":
			if Check_If_Time_To_Return == True:
				STATE == "Return To Base"
			elif Check_If_Time_To_Leave_Zone == True:
				STATE == "Zone 3"
		
	elif STATE == "Zone 3" #Zone 3 State
		Arrival_Time = datetime.datetime.now()
		
		while STATE == "Zone 3":
			if Check_If_Time_To_Return == True:
				STATE == "Return To Base"
			elif Check_If_Time_To_Leave_Zone == True:
				STATE == "Zone 1"
			
	elif STATE == "Zone 0" #Home State. we need to use this state to ensure boxes are pushed out of our zone when weve returned
		while STATE == "Zone 0"
			print("Something")
