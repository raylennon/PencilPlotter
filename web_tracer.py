import numpy as np
from scipy.optimize import least_squares
import eel

# Initialize the eel library
eel.init('web')

time = 0

BASE_SEPARATION = 120
UPPER_LENGTH = 142.5
FOREARM_LENGTH = 140

posx = 0
posy = 150

find_cosa1 = lambda x : (posx-(UPPER_LENGTH*x-BASE_SEPARATION/2))**2 + (posy-UPPER_LENGTH*np.sqrt(1-x**2))**2 - FOREARM_LENGTH**2
find_cosa2 = lambda x : (posx-(UPPER_LENGTH*x+BASE_SEPARATION/2))**2 + (posy-UPPER_LENGTH*np.sqrt(1-x**2))**2 - FOREARM_LENGTH**2

current_a1 = -np.pi/2
current_a2 = np.pi/2

# Expose the function to get the current angle
@eel.expose
def get_rotation_angle():
    global time, posx, posy, current_a1, current_a2
    time += 4
    # r = 0.5*(np.sin(0.001 * time) + 2.0)
    r = 1
    posx = 30 * r * np.cos(time * np.pi/180) 
    posy = 30 * r * np.sin(time * np.pi/180) + 200

    # posx  = 0
    # posy = 100
    cos_a1 = least_squares(find_cosa1, -0.2,  bounds=(-1, 0)).x[0]
    a1 = np.arccos(cos_a1)
    cos_a2 = least_squares(find_cosa2, 0.2,  bounds=(0, 1)).x[0]
    a2 = np.arccos(cos_a2)

    a1 = round(a1 * 200/(2*np.pi))*2*np.pi/200
    a2 = round(a2 * 200/(2*np.pi))*2*np.pi/200

    a3 = np.arctan2(posy- UPPER_LENGTH*np.sin(a1), posx - (UPPER_LENGTH*np.cos(a1)-BASE_SEPARATION/2))
    a4 = np.arctan2(posy- UPPER_LENGTH*np.sin(a2), posx - (UPPER_LENGTH*np.cos(a2)+BASE_SEPARATION/2))
    
    # print(f"Time: {time}\ta1: {a1}\ta2: {a2}")
    print(f"Time: {time}\tcos(a2): {cos_a2}")
    # ang = 2*np.pi * time / 200
    return [a1, a2, a3, a4, posx, posy] #baseL, baseR, foreL, foreR

@eel.expose
def get_sizes():
    return [BASE_SEPARATION, UPPER_LENGTH, FOREARM_LENGTH] #baseL, baseR, foreL, foreR
# Start the angle update in a separate thread

# Start the eel application
eel.start('index.html', size=(600, 400))
