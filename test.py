from robot import Robot
from robot import BRAKE
from robot import COAST

import math
import time
import datetime

r = Robot()
motor_board = r.motor_board

Start_Time = datetime.datetime.now()

def Move(Speed, Time, Brake_Or_Coast):
    if Speed > 1 or Speed < -1:
        print("ATTEMPT TO CALL MOVE FUNCTION WITH INVALID SPEED")
    else:
        print("Move at speed %f for %f seconds" % (Speed,Time) )
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
    return

def SmoothAim(AimFor): #AimFor takes a marker object, but only the id is used
    Ms=r.camera.see()
    for M in Ms:
        if M.id==AimFor.id:
            Marker=M
            D=Marker.spherical.distance_metres
            Rot=Marker.spherical.rot_y_radians
            Power=(2*3**(-abs(D))+0.5)*(0.2*Rot)+0.5
            print("Distance :%f Rotation :%f Power :%f"%(D,Rot,Power)
            if D<0.3:
                r.motor_board.m0 = 0.5
                r.motor_board.m1 = 0.5
            else:
                if Power <= 1 and Power >= -1:
                    r.motor_board.m0 = 0.5
                    r.motor_board.m1 = Power
                    print("Lesser motor power of %f" % (Power)
                else:
                    r.motor_board.m1 = -0.3
                    r.motor_board.m0 = -0.3
        else:
            r.motor_board.m0 = -0.3
            r.motor_board.m1 = -0.3
    try:
        return D
    except:
        return 100
    
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
    return



#1=find 2=search&destroy 3=done
State=1
Done=False
M=0
while not(Done):
    
    if State==1:
        Ms=r.camera.see()
        if len(Ms)==0:
            Rotate(0.5,0.2,"Brake")
            pass
        else:
            M=Ms[0]
            print(M.id)
            State=2
            
    if State ==2:
        while SmoothAim(M)>0.5:
            print("seeking")

    if State==3:
        Done=True
        print("Nailed it")
    
