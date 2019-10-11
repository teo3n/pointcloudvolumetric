import numpy as np

depthLUT = np.array(
        [[0, 1, 2, 3],
        [4, 5, 6, 7],
        [8, 9, 10, 11],
        [12, 13, 14, 15]])

        
def lutGen(x):
    x_ = 0

    for i in range(0, 64, 16):
        if x >= i and x < i+16:
                print(x_)
                return
        x_ += 1

def getSampleCoord2(index):
    x = 0
    y = 0

    for i in range(index):
        if x == 63:
            y += 1
            x = 0
        else:
            x += 1

    return x, y

def getSampleCoord(index):
    return (index % 64, int(index / 64))

def getVolumeCoord(sCoord):
    return (sCoord[0] % 16, sCoord[1] % 16)

def getTile(x):

    if x >= 0 and x < 16:
        return 0
    elif x >= 16 and x < 2*16:
        return 1
    elif x >= 2*16 and x < 3*16:
        return 2
    else:
        return 3

    return 0

def getTileCoords(sCoords):
    x = sCoord[0]
    y = sCoord[1]

    x = getTile(x)
    y = getTile(y)

    return x, y


for i in range(64):
    lutGen(i)

quit()
for i in range(4096):
    sCoord = getSampleCoord2(i)
    tCoord = getTileCoords(sCoord)
    vCoord = getVolumeCoord(sCoord)
    print(vCoord, depthLUT[tCoord[1], tCoord[0]])
#    print(getVolumeCoord(sCoord))
