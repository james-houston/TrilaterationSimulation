from tkinter import *
import Beacon
import Fingerprinting
import time
import HelperFuncs
import Trilateration
from random import randint

MANUAL_TESTING = False
continueExecution = True
DEBUG = False
startTime = 0
#information on the map
HEIGHT = 500
WIDTH = 800
SPEED = 5
NUM_BEACONS = 3
beacons = []
radarCircles = []
distLines = []
numSteps = 0
currWalkDirection = "Down"
#data on fingerprinting technique
fingerprintData = {}
fingerprintData['allFingerprintTimes'] = []
fingerprintData['numErrors'] = 0
fingerprintData['runningTotalError'] = 0
fingerprintData['avgError'] = 0
#data on triangulation technique
triangulationData = {}
triangulationData['allTrilaterationTimes'] = []
triangulationData['numErrors'] = 0
triangulationData['runningTotalError'] = 0
triangulationData['avgError'] = 0

window = Tk()
window.title("Locator")
c = Canvas(window, width=WIDTH, height=HEIGHT, bg="darkblue")
c.pack()
person = c.create_oval(-8, -8, 8, 8, outline="black", fill="green")
personLoc = [0,0]
c.update()


def key_event(event):
    if event.keysym == "q":
        end_prog()
    move_person(event.keysym)
    update_radar()
    run_calculations()


def run_calculations():
    global numSteps
    numSteps += 1
    #signal represents rssi for BLE taken from distances
    signal = HelperFuncs.dist_from_beacons(beacons, personLoc[0], personLoc[1])

    #fingerprinting estimates
    locEstTimeStart = time.time()
    est = Fingerprinting.get_closest_fingerprint(signal, fingerprintMap)
    locEstTimeTot = time.time() - locEstTimeStart
    isFingerprintError = HelperFuncs.is_error_in_estimation(personLoc,est)
    if(isFingerprintError):
        global fingerprintData
        fingerprintData = error_calculations(fingerprintData,personLoc,est,signal)
        fError = HelperFuncs.total_error(personLoc,est)
    fingerprintData['allFingerprintTimes'].append(locEstTimeTot)

    #trilateration estiamtes
    locEstTimeStart = time.time()
    est = Trilateration.calculate_loc(beacons,signal)
    locEstTimeTot = time.time() - locEstTimeStart
    isTrilaterationError = HelperFuncs.is_error_in_estimation(personLoc, est)
    if(isTrilaterationError):
        global triangulationData
        triangulationData = error_calculations(triangulationData,personLoc,est,signal)
        tError = HelperFuncs.total_error(personLoc,est)
    triangulationData['allTrilaterationTimes'].append(locEstTimeTot)

    #compare error
    if(isFingerprintError and isTrilaterationError):
        if(tError > fError):
            fillColor = "orange"
        else:
            fillColor = "purple"
        c.create_oval(personLoc[0]-3,personLoc[1]-3,personLoc[0]+3,personLoc[1]+3,fill=fillColor)

def error_calculations(data,actualLoc,estLoc,singal):
    data['numErrors'] += 1
    error = HelperFuncs.total_error(actualLoc,estLoc)
    data['runningTotalError'] += error
    data['avgError'] = data['runningTotalError'] / data['numErrors']
    if (DEBUG):
        print("Error in estimate. Estimate location: [" + str(estLoc[0]) + "," + str(estLoc[1]) + "], actual: [" +
              str(actualLoc[0]) + "," + str(actualLoc[1]) + "]" )
    return data


def move_person(event):
    global personLoc
    if event == "Up":
        c.move(person, 0, -SPEED)
        personLoc[1] -= SPEED
    elif event == "Down":
        c.move(person, 0, SPEED)
        personLoc[1] += SPEED
    elif event == "Left":
        c.move(person,  -SPEED, 0)
        personLoc[0] -= SPEED
    elif event == "Right":
        c.move(person,  SPEED, 0)
        personLoc[0] += SPEED


def update_radar():
    for i in range(NUM_BEACONS):
        c.delete(radarCircles[i])
        c.delete(distLines[i])
        dist = HelperFuncs.calculate_distance(personLoc[0], personLoc[1], beacons[i].x, beacons[i].y)
        radarCircles[i] = c.create_oval(beacons[i].x-dist,beacons[i].y-dist,
            beacons[i].x+dist,beacons[i].y+dist,outline="red")
        distLines[i] = c.create_line(beacons[i].x,beacons[i].y,personLoc[0],personLoc[1],fill="yellow")
    c.update()


def auto_move_person():
    global currWalkDirection
    if (currWalkDirection == "Down"):
        if (HEIGHT - personLoc[1] <= SPEED):
            if(WIDTH - personLoc[0] <= SPEED):
                end_prog()
            else:
                move_person("Right")
                currWalkDirection = "Up"
        else:
            move_person(currWalkDirection)
    else:
        if(personLoc[1] <= SPEED):
            move_person("Right")
            currWalkDirection = "Down"
            update_radar()
        else:
            move_person(currWalkDirection)


def free_walk():
    stepped = False
    while not stepped:
        #1 = left, 2 = up, 3 = right, 4 = down
        step = randint(1,4)
        if(step == 1):
            if(personLoc[0] > SPEED):
                move_person("Left")
                stepped = True
        if(step == 2):
            if(personLoc[1] > SPEED):
                move_person("Up")
                stepped = True
        if(step == 3):
            if(WIDTH - personLoc[0] > SPEED):
                move_person("Right")
                stepped = True
        if(step == 4):
            if(HEIGHT - personLoc[1] > SPEED):
                move_person("Down")
                stepped = True



def end_prog():
    HelperFuncs.print_statistics(numSteps,fingerprintData,triangulationData)
    while True:
        time.sleep(1)
    global continueExecution
    continueExecution = False


def timing(start,end):
    tot = end-start
    print("Took %f seconds" % tot)


c.bind_all('<Key>', key_event)
#create the beacons
beacons = HelperFuncs.create_beacons(NUM_BEACONS,HEIGHT,WIDTH)
for i in range(NUM_BEACONS):
    c.create_rectangle(beacons[i].x-4,beacons[i].y-4,beacons[i].x+4,beacons[i].y+4,fill="black",outline="red")
    dist = HelperFuncs.calculate_distance(0, 0, beacons[i].x, beacons[i].y)
    radarCircles.append(c.create_oval(beacons[i].x-dist,beacons[i].y-dist,
        beacons[i].x+dist,beacons[i].y+dist,outline="red"))
    distLines.append(c.create_line(beacons[i].x,beacons[i].y,0,0,fill="yellow"))

#fingerprinting precalculations
mapCalcStartTime = time.time()
fingerprintMap = Fingerprinting.calculate_fingerprint_map(beacons, WIDTH, HEIGHT)
mapCalcTime = time.time() - mapCalcStartTime
print("Fingerprint calculation time:",mapCalcTime)

if MANUAL_TESTING:
    while continueExecution:
        c.update_idletasks()
        c.update()
        time.sleep(.01)
else:
    while continueExecution:
        #free_walk()
        auto_move_person()
        #update_radar()
        run_calculations()

