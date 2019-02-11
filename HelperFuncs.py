import math
from random import randint
import Beacon
X_BEACON_OFFSET = 100
Y_BEACON_OFFSET = 100
PERSON_SIZE = 16

def create_beacons(num,height,width):
    #beacons must be in 'L' shape to work with trilateration
    #origin can be at a random location
    minHeight = 50
    maxHeight = int(height) - 150
    minWidth = 50
    maxWidth = int(width) - 150
    xOrigin = randint(minWidth,maxWidth)
    yOrigin = randint(minHeight,maxHeight)

    if(num != 3):
        print('\033[93m'+"Currently only supports 3 beacons"+'\033[0m')

    beacon1 = Beacon.Beacon(xOrigin,yOrigin)
    beacon2 = Beacon.Beacon(xOrigin + X_BEACON_OFFSET, yOrigin)
    beacon3 = Beacon.Beacon(xOrigin, yOrigin + Y_BEACON_OFFSET)
    return [beacon1,beacon2,beacon3]


def calculate_distance(x1,y1,x2,y2):
    xDiff = x2-x1
    yDiff = y2-y1
    xSqr = xDiff*xDiff
    ySqr = yDiff*yDiff
    tot = xSqr+ySqr
    dist = math.sqrt(tot)
    return int(dist)


def dist_from_beacons(beacons,x,y):
    distances = [0, 0, 0]
    distances[0] = calculate_distance(beacons[0].x, beacons[0].y, x, y)
    distances[1] = calculate_distance(beacons[1].x, beacons[1].y, x, y)
    distances[2] = calculate_distance(beacons[2].x, beacons[2].y, x, y)
    return distances


def is_error_in_estimation(personLoc,estimate):
    if(personLoc[0] != estimate[0] or personLoc[1] != estimate[1]):
        return True
    else:
        return False

def print_statistics(numSteps, fingerprintingData, triangulationData):
    print("Average trilateration error:\t\t%.2f" % triangulationData['avgError'])
    print("Average fingerprint error:\t\t%.2f" % fingerprintingData['avgError'])


def percent_error_vs_distance(personLoc,estimate,dist):
    minDist = min(dist)
    totalDistanceError = total_error(personLoc,estimate)
    percentOfDist = float(totalDistanceError/minDist)*100
    return percentOfDist


def total_error(personLoc,estimate):
    xError = personLoc[0]-estimate[0]
    yError = personLoc[0]-estimate[0]
    hypotenuseSquared = (xError*xError)+(yError*yError)
    totalError = math.sqrt(hypotenuseSquared)
    return totalError