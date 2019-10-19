import numpy as np
import cv2
import glob
import math

# these files have been removed for copyright's sake
files = sorted(glob.glob("data/brain/*.png"))


result = []

def createAtlas(volume):
    tiling = int(math.sqrt(len(volume)))
    print("tiling:", tiling)
    print(len(volume))

    resultimg = None

    for x in range(tiling):
        horizontal = None

        for y in range(tiling):
            if horizontal is None:
                horizontal = volume[x * tiling + y]
            else:
                horizontal = np.hstack((horizontal, volume[x * tiling + y]))

        if resultimg is None:
            resultimg = horizontal.copy()
        else:
            resultimg = np.vstack((resultimg, horizontal.copy()))

    return resultimg


def saveToDisk(volume, name):
    # volume = cv2.convertScaleAbs(volume * 255)
    # volume = cv2.cvtColor(volume, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(name + ".png", volume)


for fname in files:
    bslice = cv2.imread(fname)
    img = bslice[:, 251:710]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (256, 256))

    # cv2.imshow("i", img)
    # cv2.waitKey(100)

    result.append(img)
    result.append(img)



for n in range(256 - len(result)):
    empty = np.zeros((256, 256))
    result.append(empty)


volume = createAtlas(result)
saveToDisk(volume, "brainatlas")
