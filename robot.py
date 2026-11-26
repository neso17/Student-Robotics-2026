from sr.robot3 import Robot, Colour, LED_A, LED_B, LED_C, INPUT_PULLUP, OUTPUT, BRAKE, Note
import math
import cv2

from Movement import *
from Vision import *
from Mechanism import *
from Helpers import *
import Strategy

robot = Robot(wait_for_start=False)

servo1 = robot.servo_board.servos[0]
servo2 = robot.servo_board.servos[1]
servoTop = robot.servo_board.servos[2]
sweep(robot, servoTop)
robot.wait_start()

markerIDs["home"] = getHomeMarkerIds(robot)
Strategy.lastMinStrategy(robot, servo1, servo2, servoTop)
CAMHEIGHT = 120 # Height of the camera from the ground in metres

# Motor control:
# 700 counts of the encoder per one full rotation of the motor
#When the motor is rotating anticlockwise the A output's square wave is before the B output's and vice versa.

my_motor_board = robot.motor_board      # Declarations
my_arduino_board = robot.arduino
my_power_board = robot.power_board

robot.arduino.pins[3].mode = INPUT_PULLUP # Encoder inputs need to be pullup or the motor won't run (learnt the hard way)
robot.arduino.pins[2].mode = INPUT_PULLUP
robot.arduino.pins[5].mode = INPUT_PULLUP
robot.arduino.pins[4].mode = INPUT_PULLUP



def initialise():
    marker = findTargetMarker(robot)
    if marker is not None:
        if marker.id in range(20):
            print("Arena marker found")
        elif marker.id in range(100, 140):
            print("Acid marker found")
            collecting = "acid"                 #Store the type of marker we are collecting so we can check if we are collecting the right one later (doesn’t matter for now)
        elif marker.id in range(140, 180):
            print("Base marker found")
            collecting = "base"
    my_home_ids = getHomeMarkerIds(robot)

def arduinoSet(pin, outState): #self explanatory.
    robot.arduino.pins[pin].digital_write(outState)

def arduinoGet(pin): #self explanatory.
    return robot.arduino.pins[pin].digital_read()

