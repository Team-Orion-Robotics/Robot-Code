def US(Mod):
# needs to be checked on the day that the echo and trigger pins are correct for each module
	if (Mod == 0):
		Trigger = 1
		Echo = 2
	elif(Mod == 1):
		Trigger = 7
		Echo = 8
	elif(Mod == 2):
		Trigger = 3
		Echo = 4
	elif(Mod == 3):
		Trigger = 5
		Echo = 6
	RUS = r.servo_board.read_ultrasound(Trigger, Echo)
	print("Returned " + str(RUS) + " for Module " + str(Mod))
	return RUS

def USDist(FOR,Dist,Tol):
	speed = 1
	LEFT = 0
	RIGHT = 1
	if (FOR == "R"):
		speed = -1
		LEFT = 2
		RIGHT = 3
	done = True
	while done == True:			
		L = US(LEFT)
		R = US(RIGHT)		
		if(L > R):
			DTO = R
		else:
			DTO = L
		if (DTO < Dist - Tol):
			Move(-speed,0.3,"Brake")
		elif(DTO > Dist + Tol):
			Move(speed,0.3,"Coast")
		elif(DTO > Dist - Tol and DTO < Dist + Tol):
			done = False		
	
#drives forward until it is within the distance and tolerance to the closest object infront
#then drives backwards and does the same after 1 second wait
def USTest(Dist,Tol):
	done = True
	while done == True:
		USDist("F",Dist,Tol)
		print("Forward done")
		time.sleep(1)
		USDist("R",Dist,Tol)
		print("Reverse done")

USTest(1,0.1)
