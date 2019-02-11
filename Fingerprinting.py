import HelperFuncs


def calculate_fingerprint_map(beacons,width,height):
    fingerprintMap = []
    for x in range(width):
        fingerprintMap.append([])
        for y in range(height):
            eachFingerprint = HelperFuncs.dist_from_beacons(beacons,x,y)
            fingerprintMap[x].append(eachFingerprint)
    return fingerprintMap


def get_closest_fingerprint(eachDistance,fingerprintMap):
    x=0
    for row in fingerprintMap:
        y = 0
        for column in row:
            if(eachDistance[0] == column[0] and eachDistance[1] == column[1] and eachDistance[2] == column[2]):
                return [x,y]
            y+=1
        x+=1
