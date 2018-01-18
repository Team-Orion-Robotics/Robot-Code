from robot import Robot
import math
import time

r = Robot()
motor_board = r.motor_board
x = 0

def Move_forward(Speed):
	r.motor_board.m0 = Speed
	r.motor_board.m1 = Speed

def Move_backwards(speed):
	r.motor_board.m0 = -speed
	r.motor_board.m1 = -speed

while (x < 5):
	Move_forward(1)
	time.sleep(1)
	x+= 1

x= 0

while (x < 5):
	Move_backwards(1)
	time.sleep(1)
	x += 1
		
tokens = r.camera.see()

#pip install git+https://github.com/sourcebots/robot-api
