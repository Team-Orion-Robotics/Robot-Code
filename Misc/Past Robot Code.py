#Zachary’s code from 2017
#I think this is latest version!
from sr.robot import *
import math
import time
R = Robot()
MOTOR_LEFT = R.motors[0].m0
MOTOR_RIGHT = R.motors[0].m1
PUMP = R.motors[1].m0
LINEAR_ACTUATOR = R.motors[1].m1
ROBOT_POSITION =[0,0]
ROBOT_ROTATION = 0
SLOW = 100
FAST = 100
MARKER_TO_FETCH = -1
STATE = "FIND_TOKEN"
LINEAR_ACTUATOR.power = 100
PUMP.power = 100
wall_marker_info = {
    0: {"x": 1, "y": 8, "wall": "top"},
    1: {"x": 2, "y": 8, "wall": "top"},
    2: {"x": 3, "y": 8, "wall": "top"},
    3: {"x": 4, "y": 8, "wall": "top"},
    4: {"x": 5, "y": 8, "wall": "top"},
    5: {"x": 6, "y": 8, "wall": "top"},
    6: {"x": 7, "y": 8, "wall": "top"},
    7: {"x": 8, "y": 7, "wall": "right"},
    8: {"x": 8, "y": 6, "wall": "right"},
    9: {"x": 8, "y": 5, "wall": "right"},
    10: {"x": 8, "y": 4, "wall": "right"},
    11: {"x": 8, "y": 3, "wall": "right"},
    12: {"x": 8, "y": 2, "wall": "right"},
    13: {"x": 8, "y": 1, "wall": "right"},
    14: {"x": 7, "y": 0, "wall": "bottom"},
    15: {"x": 6, "y": 0, "wall": "bottom"},
    16: {"x": 5, "y": 0, "wall": "bottom"},
    17: {"x": 4, "y": 0, "wall": "bottom"},
    18: {"x": 3, "y": 0, "wall": "bottom"},
    19: {"x": 2, "y": 0, "wall": "bottom"},
    20: {"x": 1, "y": 0, "wall": "bottom"},
    21: {"x": 0, "y": 1, "wall": "left"},
    22: {"x": 0, "y": 2, "wall": "left"},
    23: {"x": 0, "y": 3, "wall": "left"},
    24: {"x": 0, "y": 4, "wall": "left"},
    25: {"x": 0, "y": 5, "wall": "left"},
    26: {"x": 0, "y": 6, "wall": "left"},
    27: {"x": 0, "y": 7, "wall": "left"}
}
home_positions = {
    0: {"x": 0, "y": 8},
    1: {"x": 8, "y": 8},
    2: {"x": 8, "y": 0},
    3: {"x": 0, "y": 0}
}

def get_robot_world_position_from_marker(marker):
    marker_info = wall_marker_info[marker.info.code]
    marker_x = marker_info["x"]
    marker_y = marker_info["y"]
    marker_wall = marker_info["wall"]
    angle = marker.orientation.rot_y
    distance = marker.dist
    sin_distance = math.sin(math.radians(angle)) * distance
    cos_distance = math.cos(math.radians(angle)) * distance
    x_position = 0
    y_position = 0
    if(marker_wall == "right"):
        x_position = marker_x - cos_distance
        y_position = marker_y - sin_distance
    elif(marker_wall == "bottom"):
        x_position = marker_x - sin_distance
        y_position = marker_y + cos_distance
    elif(marker_wall == "left"):
        x_position = marker_x + cos_distance
        y_position = marker_y + sin_distance
    elif(marker_wall == "top"):
        x_position = marker_x + sin_distance
        y_position = marker_y - cos_distance
    print ("(",x_position, ", ", y_position, ") from token ", marker.info.code)
    return [x_position, y_position]

def get_robot_world_rotation_from_marker(marker):
    marker_wall = wall_marker_info[marker.info.code]["wall"]
    angle = marker.orientation.rot_y
    from_robot_angle = marker.rot_y
    if(marker_wall == "right"):
        robot_world_rotation = angle + from_robot_angle
    elif(marker_wall == "bottom"):
        robot_world_rotation = 270 + (angle + from_robot_angle)
    elif(marker_wall == "left"):
        robot_world_rotation = 180 + (angle + from_robot_angle)
    elif(marker_wall == "top"):
        robot_world_rotation = 90 +(angle+ from_robot_angle)
    if(robot_world_rotation < 0):
        robot_world_rotation += 360
    print ("angle from x axis", robot_world_rotation, " from token ", marker.info.code)
    return robot_world_rotation

def get_average_world_position_from_markers(markers):
    sum_world_position = [0, 0]
    average_world_position = [0, 0]
    number_markers = 0
    for m in markers:
        if m.info.marker_type == MARKER_ARENA:
            positon_from_marker = get_robot_world_position_from_marker(m)
            sum_world_position[0] += positon_from_marker[0]
            sum_world_position[1] += positon_from_marker[1]
            number_markers += 1
    if number_markers > 0:
        average_world_position[0] = (sum_world_position[0] / number_markers)
        average_world_position[1] = (sum_world_position[1] / number_markers)
    return average_world_position

def get_average_world_rotation_from_markers(markers):
    sum_world_rotation = 0
    number_markers = 0
    average_world_rotation = 0
    for m in markers:
        if m.info.marker_type == MARKER_ARENA:
            angle_from_marker = get_robot_world_rotation_from_marker(m)
            sum_world_rotation += angle_from_marker
            number_markers += 1
    if number_markers > 0:
        average_world_rotation = sum_world_rotation / number_markers
    return average_world_rotation

def get_angle_from_robot_to_coordinates(robot_position, coordinates):
    dx = coordinates[0] - robot_position[0] 
    dy = coordinates[1] - robot_position[1]
    if(dx == 0):
        angle = 90
    else:
        angle = math.degrees(math.atan2(dy, dx))
    if angle < 0:
        angle += 360
    return angle

def rotate_left(power):
    MOTOR_LEFT.power = power
    MOTOR_RIGHT.power = -power

def rotate_right(power):
    MOTOR_LEFT.power = -power
    MOTOR_RIGHT.power = power

def move_forward(power):
    MOTOR_LEFT.power = power
    MOTOR_RIGHT.power = power

def stop_moving():
    MOTOR_LEFT.power = 0
    MOTOR_RIGHT.power = 0

def rotate_towards_world_angle(robot_angle, desired_angle):
    if(abs(desired_angle - robot_angle) < 10):
        move_forward(SLOW)
        print("going forward")
    elif((desired_angle - robot_angle) < -10):
        rotate_right(SLOW)
        print("rotate left")
    else:
        rotate_left(SLOW)
        print("rotate right")

def rotate_towards_relative_angle(angle):
    if angle > 10:
        rotate_right(SLOW)
    elif angle < -10:
        rotate_left(SLOW)
    else:
        move_forward(SLOW)

def get_closest_marker(markers, token_types = [MARKER_TOKEN_A, MARKER_TOKEN_B, MARKER_TOKEN_C]):
    closest_marker = None
    closest_distance = 99999
    for m in markers:
        if m.info.marker_type in token_types:
            if m.dist < closest_distance:
                closest_marker = m
    return closest_marker

def find_token_by_code(markers, code):
    token_to_return = None
    for m in markers:
        if m.info.code == code:
            token_to_return = m
    return token_to_return

while True:
    markers = R.see()
    print (STATE)
    if(len(markers) < 1):
        # this is really bad..
        # lets spin a bit and hope things get bette
        print ("I DIDN'T SEE ANY MARKERS :(")
        rotate_left(SLOW)
        
    else:
        ROBOT_POSITION = get_average_world_position_from_markers(markers)
        ROBOT_ROTATION = get_average_world_rotation_from_markers(markers)
        print ("ROBOT AT (", ROBOT_POSITION[0], ",", ROBOT_POSITION[1], ")")
        print ("ROBOT ROTATION: ", ROBOT_ROTATION)
    
        if STATE == "FIND_TOKEN":
            closest_marker = get_closest_marker(markers)
            if(closest_marker):
                MARKER_TO_FETCH = closest_marker.info.code
                print ("TRYING TO FETCH:",MARKER_TO_FETCH)
                STATE = "GOING_TO_TOKEN"
        if STATE == "GOING_TO_TOKEN":
            token_we_want = find_token_by_code(markers, MARKER_TO_FETCH)
            if token_we_want:
                if token_we_want.dist < 1:
                    print ("APPROACHING:", MARKER_TO_FETCH)
                    STATE = "APROACH_TOKEN"
                else:
                    rotate_towards_relative_angle(token_we_want.rot_y)
            else:
                print ("LOST SIGHT OF:", MARKER_TO_FETCH)
                STATE = "FIND_TOKEN"
        if STATE =="APROACH_TOKEN":
            move_forward(FAST)
            time.sleep(2)
            STATE = "PICK_UP_BOX"
        if STATE =="PICK_UP_BOX":
            # plz be able to use linear actuator and pump
            move_forward(0)
            LINEAR_ACTUATOR.power = 100
            PUMP.power = 100
            time.sleep(2)
            STATE = "GOING_HOME"
        if STATE == "GOING_HOME":
            token_thingy = None
            for m in markers:
                if(R.zone == 0 and (m.info.code == 0 or m.info.code == 27)):
                    token_thingy = m
                elif(R.zone == 1 and (m.info.code == 6 or m.info.code == 7)):
                    token_thingy = m
                elif(R.zone == 2 and (m.info.code == 13 or m.info.code == 14)):
                    token_thingy = m
                elif(R.zone == 3 and (m.info.code == 20 or m.info.code == 21)):
                    token_thingy = m
                
            if token_thingy:
                if token_thingy.dist < 1:
                    move_forward(FAST)
                    time.sleep(2)
                    LINEAR_ACTUATOR.power = -100
                    PUMP.power = 0
                    move_forward(0)
                    time.sleep(5)
                    STATE = "FIND_TOKEN"
                    move_forward(-FAST)
                    time.sleep(2)
                    
                    # 
                else:
                    rotate_towards_relative_angle(token_thingy.rot_y)
                
                
            else:  
                HOME_ANGLE = get_angle_from_robot_to_coordinates(ROBOT_POSITION, [home_positions[R.zone]["x"], home_positions[R.zone]["y"]])
                rotate_towards_world_angle(ROBOT_ROTATION, HOME_ANGLE)
                print ("HOME ANGLE: ",HOME_ANGLE)