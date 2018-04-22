#pip install git+https://github.com/sourcebots/robot-api
from robot import *

import random
import math
import time
import datetime

r = Robot()

Team_Tokens = [44,45,46,47,48]
Collected_Tokens = [False, False, False, False, False] #These correlate to the team tokens array above. C_T(0) = Token 44 etc...
LastTargetedMarker1 = 100

#Region Zone Tokens
Done = False
marker = 0

if r.zone == 0:
	Home_Base_Colour = "Pink"
	Zone_Number = 0
	Home_Base_Token_1 = 0
	Home_Base_Token_2 = 27

	Boxes_Zone_Token_1 = 14
	Boxes_Zone_Token_2 = 13

	marker = 44
	Done = True

elif r.zone == 1:
	Home_Base_Colour = "Green"
	Zone_Number = 1
	Home_Base_Token_1 = 7
	Home_Base_Token_2 = 6

	Boxes_Zone_Token_1 = 21
	Boxes_Zone_Token_2 = 20

	marker = 49
	Done = True

elif r.zone == 2:
	Home_Base_Colour = "Yellow"
	Zone_Number = 2
	Home_Base_Token_1 = 14
	Home_Base_Token_2 = 13

	Boxes_Zone_Token_1 = 0
	Boxes_Zone_Token_2 = 27

	marker = 54
	Done = True

elif r.zone == 3:
	Home_Base_Colour = "Orange"
	Zone_Number = 3
	Home_Base_Token_1 = 21
	Home_Base_Token_2 = 20

	Boxes_Zone_Token_1 = 7
	Boxes_Zone_Token_2 = 6

	marker = 59
	Done = True

else:
	Done = False
	print("Insert zone USB")

print(" ")

for i in range(0, 5):
	Team_Tokens[i] = marker + i

if Done == True:	
	print("Home colour is: {}. Home Markers are: {} and {}. Our Tokens corner Markers are: {} and {}".format(Home_Base_Colour, Home_Base_Token_1, Home_Base_Token_2, Boxes_Zone_Token_1, Boxes_Zone_Token_2))

if (marker != 0):
	print("Our markers are: {}".format(Team_Tokens))

print(" ")
#EndRegion


Start_Time = datetime.datetime.now()

count = 0

Current_Zone = int

#oi you fuck wombles, Servo stop speed is -0.3 not 0!

#Region Movement Code
def Move(Speed, Time, Brake_Or_Coast):

	if Speed > 1 or Speed < -1: #Need to change these values to ensure we don't overflow the motor board
		print("ATTEMPT TO CALL MOVE FUNCTION WITH INVALID SPEED")
		return
    
	r.motor_board.m0 = Speed
	r.motor_board.m1 = Speed *0.95
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
#EndRegion


#Region Ultrasound
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
		#   DTO = R

		if (DTO < Dist - Tol):
			Move(-speed,0.3,"Brake")
		elif(DTO > Dist + Tol):
			Move(speed,0.3,"Coast")
		elif(DTO > Dist - Tol and DTO < Dist + Tol):
			done = False
#EndRegion


#region Servo control
def Raise_Front_Barrier():
	print("Raising front barrier")
	r.servo_board.servos[0].position = -1 #Front Right
	r.servo_board.servos[1].position = 1 #Front Left
	time.sleep(3.2)
	r.servo_board.servos[0].position = -0.3
	r.servo_board.servos[1].position = -0.3

def Lower_Front_Barrier():
	print("Lowering front barrier")
	r.servo_board.servos[0].position = 1 #Front Right
	r.servo_board.servos[1].position = -1 #Front Left
	time.sleep(3.2)
	r.servo_board.servos[0].position = -0.3
	r.servo_board.servos[1].position = -0.3

def Raise_Rear_Barrier():
	print("Raising rear barrier")
	r.servo_board.servos[2].position = -1 #Front Right
	r.servo_board.servos[3].position = 1 #Front Left
	time.sleep(3.2)
	r.servo_board.servos[2].position = -0.3
	r.servo_board.servos[3].position = -0.3

def Lower_Rear_Barrier():
	print("Lowering rear barrier")
	r.servo_board.servos[2].position = 1 #Front Right
	r.servo_board.servos[3].position = -1 #Front Left
	time.sleep(3.2)
	r.servo_board.servos[2].position = -0.3
	r.servo_board.servos[3].position = -0.3
#EndRegion


#Region Timing Stuff
def Check_If_Time_To_Return(): #We need to call this literally whenever possible as it will only check when called. Will return True if time remaining is less than 30 seconds. and False if more than 30 seconds is left. This can be tweeked as needed depending on speed of Robot
	Stuff = False

	seconds = 0

	Difference = datetime.datetime.now() - Start_Time
	seconds = Difference.seconds

	remaining_time = 150 - seconds #Make sure this is set to about 150 for the competition.

	print("Time remaining: {}".format(remaining_time))

	if (remaining_time < 40): #Change this number to change how long the program dedicates to getting home
		print("Time to Return")
		return True
	else:
		return False

def Check_If_Time_To_Leave_Zone(ArrivalTime):
	CurrentTime = datetime.datetime.now()
	Difference = ArrivalTime - CurrentTime
    
	seconds = difference.seconds
    
	if (seconds > 20):
		print("Time to move on to next zone")
		return True
	else:
		return False
#EndRegion


#Region Coordinate Code
def coord(D1,A1,D2,A2,M1ID,M2ID,SideWall):
	theta = abs(A1) + abs(A2)	
	print("WallFacing:" + SideWall)
	print("D1:" + str(D1))
	print("D2:" + str(D2))
	print("A1:" + str(A1))
	print("A2:" + str(A2))
	print("theta:" + str(theta))
	WD = math.sqrt((D1*D1)+(D2*D2)-(2*D1*D2*(math.cos(theta))))
	print("D: " + str(WD))
	D1 = D1*(1/WD)
	D2 = D2*(1/WD)
	AA1 = math.asin(D2*(math.sin(theta))/WD)
	print("AA1:" + str(AA1))
	AA2 = math.asin(D1*(math.sin(theta))/WD)
	print("AA2:" + str(AA2))
	Dx1 = D1*(math.sin(AA1))
	print("Dx1:" + str(Dx1))
	Dy1 = D1*(math.cos(AA1))
	print("Dy1:" + str(Dy1))
	Dx2 = D2*(math.sin(AA2))
	print("Dx2:" + str(Dx2))
	Dy2 = D2*(math.cos(AA2))	
	print("Dy2:" + str(Dy2))
	Dx = (Dx1 + Dx2)/2
	Dy = (Dy1 + Dy2)/2
	loc = int(M1ID) 
	while loc > 6:
		loc = loc - 7
	print("loc: " + str(loc))	
	if (SideWall == "N"):
		y = Dy
		x = Dx + loc		
	elif(SideWall == "E"):
		y = Dx + loc
		x = 8 - Dy
	elif(SideWall == "S"): 
		y = 8 - Dy 
		x = 8 - Dx - loc
	elif(SideWall == "W"):    
		y = 8 - Dx - loc 
		x = Dy
                
	location = str(x) + "," + str(y)
	print(location)
	return location
            
def WhereAmI():
	highestnum = 0
	while highestnum < 2:
		alltokens = r.camera.see()
		WallTokens = []
		for m in alltokens:
			if int(m.id) < 28:
				WallTokens.append(m)
		if len(WallTokens) > 1:
			SideWallE = 0
			SideWallW = 0
			SideWallN = 0
			SideWallS = 0
			for m in WallTokens:
				print(m.id)
				if (int(m.id) > 6 and int(m.id) < 14):
					SideWallE += 1
				elif(int(m.id) > 20 and int(m.id)< 28):
					SideWallW += 1
				elif(int(m.id) > 0 and int(m.id) < 7): 
					SideWallN += 1
				elif(int(m.id) > 13 and int(m.id) < 21):
					SideWallS += 1
			highest = "E"
			highestnum = SideWallE
			if SideWallW > highestnum:
				highestnum = SideWallW
				highest = "W"
			if SideWallN > highestnum:
				highestnum = SideWallN
				highest = "N"
			if SideWallS > highestnum:
				highestnum = SideWallS
				highest = "S"
			specifiedwalltokens = []
			for m in WallTokens:
				if (int(m.id) > 6 and int(m.id) < 14 and highest == "E"):
					specifiedwalltokens.append(m)
				elif(int(m.id) > 20 and int(m.id)< 28 and highest == "W"):
					specifiedwalltokens.append(m)
				elif(int(m.id) > 0 and int(m.id) < 7 and highest == "N"): 
					specifiedwalltokens.append(m)
				elif(int(m.id) > 13 and int(m.id) < 21 and highest == "S"):    
					specifiedwalltokens.append(m)
			if highestnum > 2:
				m1 = specifiedwalltokens[0]
				m2 = specifiedwalltokens[1]
				D = abs(int(m1.id) - int(m2.id))
				A1 = m1.spherical.rot_y_radians
				A2 = m2.spherical.rot_y_radians
				D1 = m1.distance_metres
				D2 = m2.distance_metres
				m1id = m1.id
				m2id = m2.id
				return coord(D1,A1,D2,A2,m1id,m2id,highest)
			else:
				return("0,0")
		else:
			return("0,0")

def InTokenZone(tol):
	IZ = False
	WAI = str(WhereAmI())
	print(WAI)
	xy = WAI.split(",")
	cz = Zone_Number
	x = 5.6
	y = 5.6
	if cz == 1:
		x = 2.4
		y = 5.6
	elif cz == 2:
		x = 2.4
		y = 2.4
	elif cz == 3:
		x = 5.6
		y = 2.4
	
	print(xy)
	a = xy[0]
	b = xy[1]
	if float(a) <= x + tol and float(a) >= x - tol:
		if float(b) <= y + tol and float(b) >= y - tol:
			IZ = True	
	return IZ

def InHomeZone(tol):
	IZ = False
	WAI = str(WhereAmI())
	print(WAI)
	xy = WAI.split(",")
	cz = Zone_Number
	x = 2.4
	y = 2.4
	if cz == 1:
		x = 5.6
		y = 2.4
	elif cz == 2:
		x = 5.6
		y = 5.6
	elif cz == 3:
		x = 2.4
		y = 5.6
	
	print(xy)
	a = xy[0]
	b = xy[1]
	if float(a) <= x + tol and float(a) >= x - tol:
		if float(b) <= y + tol and float(b) >= y - tol:
			IZ = True	
	return IZ

def Backup(tol):
	IZ = False
	WAI = str(WhereAmI())
	print(WAI)
	xy = WAI.split(",")
	cz = 3
	x = 2.4
	y = 2.4
	if cz == 1:
		x = 5.6
		y = 2.4
	elif cz == 2:
		x = 5.6
		y = 5.6
	elif cz == 3:
		x = 2.4
		y = 5.6
	
	print(xy)
	a = xy[0]
	b = xy[1]
	if float(a) <= x + tol or float(a) >= x - tol:
		if float(b) <= y + tol or float(b) >= y - tol:
			IZ = True	
	return IZ  #Where the or's are still indeed or's. 
#EndRegion


#Region Marker Targeting
def Target(M,Token):  #Takes a marker object and a boolean variable
	print("Targeting Marker: {}".format(M.id))
	Target.id=M.id
	Target_Done=False

	while Target_Done == False:
		Markers=r.camera.see()
		Rot=100
		D=100

		for m in Markers:
			if m.id==Target.id:
				Rot=m.spherical.rot_y_degrees
				D=m.spherical.distance_metres

		if not(D==100):
			print(Rot)
			if Rot<-5:
				if Rot < 0:
					Rotate(-0.5,-Rot/100,"Coast")
				else:
					Rotate(-0.5,Rot/100,"Coast")

			elif Rot>5:
				if Rot < 0:
					Rotate(0.5,-Rot/100,"Coast")
				else:
					Rotate(0.5,Rot/100,"Coast")

			else:
				Target_Done=True
				#markers = r.camera.see()

				#or i in markers:
					#if i.id == M.id:
						#print("We are pointed at marker {}, with a distance of {}".format(m.id, m.spherical.distance_metres))
						#D = m.spherical.distance_metres
		else:
			print("Can't see the token, so didn't collect it")
			return

	if D > 2:
		Move(0.65,((D-2)/0.22), "Coast")
		print("Moving to below 2 meters away")
		if Token:
			Target(M,True)
		else:
			return
	elif Token:
		print(D)
		Move(0.65,(D/0.22)+1, "Coast")
		print("Attempting to collect the box")

		Collected_Tokens[(M.id - Team_Tokens[0])] = True #Sets the collected token to collected so we know when we have it.
		print("{}: {}, {}: {}, {}: {}, {}: {}, {}: {}".format(Team_Tokens[0], Collected_Tokens[0], Team_Tokens[1], Collected_Tokens[1], Team_Tokens[2], Collected_Tokens[2], Team_Tokens[3], Collected_Tokens[3], Team_Tokens[4], Collected_Tokens[4]))
		print("Box Collected")
		return

def SmoothAim(AimFor): #AimFor takes a marker object
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
#EndRegion


#Region Driving To Places
def GoHome(LastTargetedMarker):
	print("Going home")
	FoundMarker=False
	Markers=r.camera.see()

	print(LastTargetedMarker)

	#for M in Markers:
	#	if False:
		#if (M.id == (Home_Base_Token_1+3) % 28 or (Home_Base_Token_1+24) % 28 == M.id) and M.id != LastTargetedMarker:
	#		LastTargetedMarker=M.id
	#		print("Home function targeting marker {}".format(M.id))
	#		FoundMarker=True
	#		Target(M,False)
	#		return LastTargetedMarker

	Skip = False

	for M in Markers:
		if M.id == Boxes_Zone_Token_1 % 28 or M.id == Boxes_Zone_Token_2 % 28 or M.id == (Boxes_Zone_Token_1 + 1) % 28 or M.id == (Boxes_Zone_Token_2 - 1) % 28 or M.id == (Boxes_Zone_Token_1 + 2) % 28 or M.id == (Boxes_Zone_Token_2 - 2) % 28 :
			Rotate(0.65, 3.75, "Coast")
			Skip = True

	if Skip == False:
		for M in Markers:
			if (M.id == (Home_Base_Token_1 + 2) % 28 or (Home_Base_Token_1 + 25) % 28 == M.id) and M.id != LastTargetedMarker: #Middle - 1
				print("Home function targeting marker {}".format(M.id))
				FoundMarker=True
				LastTargetedMarker=M.id
				Target(M,False)
				Skip = True

				return LastTargetedMarker

	if Skip == False:
		for M in Markers:
			if (M.id == (Home_Base_Token_1 + 1) % 28 or (Home_Base_Token_1 + 24) % 28 == M.id) and M.id != LastTargetedMarker: #Middle - 2
				print("Home function targeting marker {}".format(M.id))
				FoundMarker=True
				LastTargetedMarker=M.id
				Target(M,False)
				Skip = True

				return LastTargetedMarker

	if Skip == False:
		for M in Markers:
			if (M.id == (Home_Base_Token_1) % 28 or (Home_Base_Token_2) % 28 == M.id) and M.id != LastTargetedMarker: #Inside corners
				print("Home function targeting marker {}".format(M.id))
				FoundMarker=True
				LastTargetedMarker=M.id
				Target(M,False)
				Skip = True

				return LastTargetedMarker

	if Skip == False:
		for M in Markers:
			if (M.id == (Home_Base_Token_1+7) % 28 or (Home_Base_Token_1+20) % 28 == M.id) and M.id != LastTargetedMarker: #Other side middles
				print("Home function targeting marker {}".format(M.id))
				FoundMarker=True
				LastTargetedMarker=M.id
				Target(M,False)
				Skip = False

				return LastTargetedMarker

	if FoundMarker == False:
		print("Can't see any wall markers")
		if random.randint(1,5)==1:
			Move(-0.65,3,"Coast")
		else:
			Rotate(0.6,0.5,"Coast")

		return(100)

def DriveToBoxes():
	print("Driving to Boxes")
	FoundMarker=False
	Markers=r.camera.see()

	for M in Markers:
		if (M.id == (Home_Base_Token_1+3) % 28 or (Home_Base_Token_1+24) % 28 == M.id) and M.id!=LastTargetedMarker:
			print("Home function targeting marker {}".format(M.id))
			FoundMarker=True
			LastTargetedMarker=M.id
			Target(M,False)

	else:
		for M in Markers:
			if (M.id == (Home_Base_Token_1) % 28 or (Home_Base_Token_2) % 28 == M.id) and M.id!=LastTargetedMarker:
				print("Home function targeting marker {}".format(M.id))
				FoundMarker=True
				LastTargetedMarker=M.id
				Target(M,False)
		else:
			for M in Markers:
				if (M.id == (Home_Base_Token_1+10) % 28 or (Home_Base_Token_1+17) % 28 == M.id) and M.id!=LastTargetedMarker:
					print("Home function targeting marker {}".format(M.id))
					FoundMarker=True
					LastTargetedMarker=M.id
					Target(M,False)

	if not(FoundMarker):
		print("Can't see any wall markers")
		Rotate(0.6,1,"Coast")
#EndRegion

def Run():         
	STATE = "Box Collection" #This needs to be set to "Drive to Our Boxes" for the competition. 

	Move(0.65, 19, "Coast") #Uncomment
	Lower_Rear_Barrier()

	while True: #Main STATE code

		if STATE == "Box Collection":
			Count = 0
			Return = False
			#Raise_Front_Barrier() #Ready to accept new boxes #UNCOMMENT

			while STATE == "Box Collection":
				Done = True
				for i in range(0, 5):
					if Collected_Tokens[i] == False:
						Done = False #We still have some boxes to collect
						Count += 1
						
				if Check_If_Time_To_Return():
					Return = True
					Done = True #We are out of time, break out of loop and return home. What we currently have in our possession will have to do.
					print("Time to go home")

				if Done == False: #Still have boxes to collect
					print("Gotta get {} more".format(Count))
					Count = 0
					
					markers = r.camera.see()
					print("Looking for boxes")

					for m in markers: #Scans all the boxes we can see to see if we have dropped one. If the robot sees one we think is in our posetion, set it back to False
						for i in range(0, 5):
							if m.id == Team_Tokens[i] and Collected_Tokens[i] == True:
								Collected_Tokens[i] == False

					Skip = True #Used to determine if one of the tokens we see is one were hunting for or not.
					
					if (len(markers) != 0): #we can see atleast 1 marker
						print("Can see a marker!")
						for m in markers:
							for i in range(0, 5):
								if m.id == Team_Tokens[i]: #One of the boxes we see, is one of our tokens
									print("Can see one of our tokens!")
									Skip = False #As we saw a box of ours, we don't need to rotate away
									Target(m,True) #Targets the current marker, and 'hopefully' collects it. Should probably add a fail case

						if Skip == True: #Didn't see one of our boxes. Time to rotate
							Rotate(0.6, 0.7, "Coast") #Rotate and try the above again. Keep rotating until we see one of our tokens basically.
							time.sleep(1) 
					else:
						Rotate(0.6, 0.7, "Brake") #Rotate until we can see a box
						if random.randint(1,10)==1:
							Lower_Front_Barrier()
							Move(-0.65,3,"Coast")
							Raise_Front_Barrier()
						print("Can't see a box")
						time.sleep(1)
					print(" ")

				else:
					if Return == True:
						Lower_Front_Barrier()
						STATE = "Return To Base" #Don't have time to check, just need to return to our base and drop current boxes
					else:
						STATE = "Check For Collected Tokens" #We have all our boxes, break out of the loop and do a 360 as a final check.
						print("Checking collected tokens")
						Lower_Front_Barrier() #Close barrier as we are done with box collection.


		elif STATE == "Check For Collected Tokens": #Do a final check of our zone to ensure we have all our boxes, and we havn't dropped or forgotten any while collecting.
			while STATE == "Check For Collected Tokens":
				Done = False
				for i in range(0, 15): #Makes the robot do a full 360
					if Check_If_Time_To_Return():
						Done = True
						STATE = "Return To Base"

					if Done == False: #If its time to return to our home, doing this should speed this state up a lot as the Robot won't have to do anything. only loop nothing 15 times. 
						Rotate(0.6, 0.7, "Coast")
						markers = r.camera.see()

						for m in markers:
							for i in range(0, 4):
								if m.id == Team_Tokens[i]:
									Collected_Tokens[i] = False
									STATE = "Box Collection"
									
								elif m.id < 64 and m.id > 43:
									print("Looking at Token: %f, however this isn't one of ours."%(m.id))

				if STATE == "Check For Collected Tokens": #The Robot didn't see any of our tokens in its rotation, so were probably good
					if Check_If_Time_To_Return == False:
						print("Done full 360, and didn't find any of our tokens")
						STATE = "Zone 1" #Move to zone 1 and start messing with their shit
					else: #Time to return as were out of time
						STATE = "Return To Base"


		elif STATE == "Drive To Our Boxes":
			Move(0.65, 4, "Coast")
			while STATE == "Drive To Our Boxes":
				DriveToBoxes()
				if InTokenZone(0.7):
					STATE = "Box Collection"


		elif STATE == "Return To Base": 
			while STATE == "Return To Base":
				LastTargetMarker1 = GoHome(LastTargetedMarker1)


		elif STATE == "Enemy Zone": #Needs a lot of work, as currently its shit. 
			Arrival_Time = datetime.datetime.now()

			while STATE == "Zone 1":
				if Check_If_Time_To_Return() == True:
					STATE == "Return To Base"
				elif Check_If_Time_To_Leave_Zone(Arrival_Time) == True:
					STATE == "Zone 2"
	  

		elif STATE == "Home Zone": #Home State. we need to use this state to ensure boxes are pushed out of our zone when weve returned
			while STATE == "Zone 0":
				print("Something")
				#Might be good to try and add some box clearence stuff here

Run()
