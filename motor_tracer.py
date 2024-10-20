import numpy as np
from scipy.optimize import least_squares
# import eel
import time
from sys import platform
kit, steppers = [None]*2
if platform == 'linux':
    from adafruit_motorkit import MotorKit
    from adafruit_motor import stepper
    
    kit = MotorKit(steppers_microsteps=16)
    dirs = [stepper.FORWARD, stepper.BACKWARD]
    steppers = [kit.stepper1, kit.stepper2]

t = 0

BASE_SEPARATION = 120
UPPER_LENGTH = 137.5
FOREARM_LENGTH = 135

posx = 0
posy = 190

find_cosa1 = lambda x : (posx-(UPPER_LENGTH*x-BASE_SEPARATION/2))**2 + (posy-UPPER_LENGTH*np.sqrt(1-x**2))**2 - FOREARM_LENGTH**2
find_cosa2 = lambda x : (posx-(UPPER_LENGTH*x+BASE_SEPARATION/2))**2 + (posy-UPPER_LENGTH*np.sqrt(1-x**2))**2 - FOREARM_LENGTH**2

fac= 200 #* 16

# Expose the function to get the current angle
def get_rotation_angle():
    global posx, posy
    
    cos_a1 = least_squares(find_cosa1, -0.2,  bounds=(-1, 0)).x[0]
    a1 = np.arccos(cos_a1)
    
    cos_a2 = least_squares(find_cosa2, 0.2,  bounds=(0, 1)).x[0]
    a2 = np.arccos(cos_a2)

    return a1, a2

moved_from_start = False
inc = 5
while True:

    if not moved_from_start:
        current_a1 = np.arccos(least_squares(find_cosa1, -0.2,  bounds=(-1, 0)).x[0])
        current_a2 = np.arccos(least_squares(find_cosa2, 0.2,  bounds=(0, 1)).x[0])
        # current_a1 = np.pi/2
        # current_a2 = np.pi/2

        moved_from_start = True

    t += inc

    # r = 0.9*(np.sin(0.001 * t) + 1.0)
    r = 1
    posx = 20 * r * np.cos(t * np.pi/180) 
    posy = 20 * r * np.sin(t * np.pi/180) + 200
    a1, a2 = get_rotation_angle()
    print(f"From {current_a1*(180/np.pi):.2f},{current_a2*(180/np.pi):.2f} to {a1*(180/np.pi):.2f},{a2*(180/np.pi):.2f}")
    motor1_steps = round((a1-current_a1) * fac/(2*np.pi))
    motor2_steps = round((a2-current_a2) * fac/(2*np.pi))
    if (max(abs(motor1_steps), abs(motor2_steps)))==0:
        continue
    # motor1_steps = int((a1-current_a1)*(fac/(2*np.pi)))
    # motor2_steps = int((a2-current_a2)*(fac/(2*np.pi)))
    
    # print(f"Rotate A by {180/np.pi * (a1-current_a1):.2f}°\t={motor1_steps} steps")
    # print(f"Rotate B by {180/np.pi * (a2-current_a2):.2f}°\t={motor2_steps} steps\n")

    if (fac <= 200):
        style_val = stepper.SINGLE
        # style_val = stepper.DOUBLE
    else :
        style_val = stepper.MICROSTEP

    current_a1 += motor1_steps * (2*np.pi/fac)
    current_a2 += motor2_steps * (2*np.pi/fac)
    # print(f"\t{(t )%360}")
    if platform == 'linux':
        for i in range(max(abs(motor1_steps), abs(motor2_steps))):
            if abs(motor1_steps)>0:
                kit.stepper1.onestep(style=style_val, direction = dirs[motor1_steps<0])
                motor1_steps -= 1 *np.sign(motor1_steps)
            if abs(motor2_steps)>0:
                kit.stepper2.onestep(style=style_val, direction = dirs[motor2_steps<0])
                motor2_steps += 1 *np.sign(motor2_steps)
            time.sleep(0.1)

    time.sleep(0.1)

