import numpy as np
import cv2
import math

size = (256, 256)
height = 256

def createCube():
    cube = []

    for l in range(height):
        if l in [0, 1, height-2, height-1]:
            layer = np.zeros(size)
            cube.append(layer.copy())
        else:
            layer = np.ones(size)
            cube.append(layer.copy())

    return cube

def createSphere():
    sphere = []
    center = int(size[0] / 2), int(size[1] / 2)

    for i in range(int(height / 2)):
        layer = np.zeros(size)
        layer = cv2.circle(layer, center, i, (1.0), -1)
        sphere.append(layer)

    for i in reversed(range(int(height / 2))):
        layer = np.zeros(size)
        layer = cv2.circle(layer, center, i, (1.0), -1)
        sphere.append(layer)

    return sphere

def createAtlas(volume):
    tiling = int(math.sqrt(height))
    print("tiling:", tiling)

    result = None

    for x in range(tiling):
        horizontal = None

        for y in range(tiling):
            if horizontal is None:
                horizontal = volume[x * tiling + y]
            else:
                horizontal = np.hstack((horizontal, volume[x * tiling +y]))

        if result is None:
            result = horizontal.copy()
        else:
            result = np.vstack((result, horizontal.copy()))

    return result

def saveToDisk(volume, name):
    volume = cv2.convertScaleAbs(volume * 255)
    volume = cv2.cvtColor(volume, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(name + ".png", volume)


def main():
   obj = createSphere()
   obj = createAtlas(obj)
   saveToDisk(obj, "sphere256")



if __name__ == "__main__":
    main()
