from robot import Robot
from sr.robot import *
import math
import time

#Test comment
r = Robot()

tokens = r.camera.see()

x = 1

while (x =- 1):
    Move_Forward(100)

def Move_forward(Speed)
	MOTOR_LEFT.power = Speed
    MOTOR_RIGHT.power = Speed

#pip install git+https://github.com/sourcebots/robot-ap
