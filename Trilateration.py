#trialateration algorithm based on information found at:
# https://en.wikipedia.org/wiki/True_range_multilateration

#These must match offsets in HelperFuncs.py
X_BEACON_OFFSET = 100
Y_BEACON_OFFSET = 100


def calculate_loc(beacons,signal):
    U = X_BEACON_OFFSET
    W = Y_BEACON_OFFSET

    #c1 and c2 calculations
    [x,yPos,yNeg] = c1_c2(U,signal[0],signal[1])

    #c1 and c3 calculations
    [xPos,xNeg,y] = c1_c3(W,signal[0],signal[2])

    #tranlate coordinate system to canvas coordinate system
    [xFinal,yFinal] = translate(beacons[0],x,y)

    return [xFinal,yFinal]

def c1_c2(U,r1,r2):
    x = (r1*r1)-(r2*r2)+(U*U)
    x = x/(2*U)
    return [x,None,None]


def c1_c3(W,r1,r3):
    y = (r1*r1)-(r3*r3)+(W*W)
    y = y/(2*W)
    return [None, None, y]


def translate(beacon,x,y):
    originX = beacon.x
    originY = beacon.y
    x = originX + int(x)
    y = originY + int(y)
    return [x,y]