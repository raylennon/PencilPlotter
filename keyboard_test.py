import numpy as np
from scipy.optimize import least_squares
# import eel
import time
from sys import platform

kit = MotorKit()
dirs = [stepper.FORWARD, stepper.BACKWARD]
steppers = [kit.stepper1, kit.stepper2]

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper


while True:
    request = input("Instr")
    if (request.upper()=="Q"):
        kit.stepper1.onestep(style=stepper.DOUBLE, direction = stepper.FORWARD)
    if (request.upper()=="A"):
        kit.stepper1.onestep(style=stepper.DOUBLE, direction = stepper.BACKWARD)
    if (request.upper()=="W"):
        kit.stepper2.onestep(style=stepper.DOUBLE, direction = stepper.FORWARD)
    if (request.upper()=="S"):
        kit.stepper2.onestep(style=stepper.DOUBLE, direction = stepper.BACKWARD)