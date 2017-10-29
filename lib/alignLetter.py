import pytesseract as tes
import random
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps
from PIL import ImageDraw
import numpy as np
import math


def dot(vA, vB):
    return vA[0] * vB[0] + vA[1] * vB[1]

def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0] - lineA[1][0]), (lineA[0][1] - lineA[1][1])]
    vB = [(lineB[0][0] - lineB[1][0]), (lineB[0][1] - lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA) ** 0.5
    magB = dot(vB, vB) ** 0.5
    # Get cosine value
    cos_ = dot_prod / magA / magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod / magB / magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg - 180 >= 0:
        # As in if statement
        return 360 - ang_deg
    else:
        return ang_deg

def alignLetter(img):
    R, G, B = img.convert('RGB').split() # split RGB layers
    r = R.load()
    g = G.load()
    b = B.load()
    width, height = img.size

    #horizontal
    endingPointOfLetterHorizontal = 1
    startingPointOfLetterHorizontal = 0
    alreadySavedFirstBlackColumn = False

    for xH in range(1, width):
        column = []
        for yH in range(height):

            if r[xH, yH] == 0 and g[xH, yH] == 0 and b[xH, yH] == 0:
               column.append(True)
            else:
               column.append(False)

        if all(item for item in column):
            if alreadySavedFirstBlackColumn == False:
                    endingPointOfLetterHorizontal = xH
                    alreadySavedFirstBlackColumn = True
        else:
            if alreadySavedFirstBlackColumn == True:
                startingPointOfLetterHorizontal = xH
                alreadySavedFirstBlackColumn = False

    #vertical
    endingPointOfLetterVertical = 1
    startingPointOfLetterVertical = 0
    alreadySavedFirstBlackRow = False

    for yV in range(1, height):
        row = []
        for xV in range(width):

            if r[xV, yV] == 0 and g[xV, yV] == 0 and b[xV, yV] == 0:
               row.append(True) # If pixel is black, add True to row
            else:
               row.append(False)

        if all(item for item in row): # If all in row are black
            if alreadySavedFirstBlackRow == False:
                endingPointOfLetterVertical = yV
                alreadySavedFirstBlackRow = True
        else:
            if alreadySavedFirstBlackRow == True:
                startingPointOfLetterVertical = yV
                alreadySavedFirstBlackRow = False


    #demo stuff
    for x in range(1, width):
        column = []
        for y in range(height):

            if x > startingPointOfLetterHorizontal and x < endingPointOfLetterHorizontal:
                if y > startingPointOfLetterVertical and y < endingPointOfLetterVertical:
                    r[x, y] = 128
                    g[x, y] = 128
                    b[x, y] = 128

#     print("endingPointOfLetterHorizontal: {0}".format(endingPointOfLetterHorizontal))
#     print("startingPointOfLetterHorizontal: {0}".format(startingPointOfLetterHorizontal))
#     print("endingPointOfLetterVertical: {0}".format(endingPointOfLetterVertical))
#     print("startingPointOfLetterVertical: {0}".format(startingPointOfLetterVertical))

    point1 = startingPointOfLetterHorizontal, endingPointOfLetterVertical
    point2 = endingPointOfLetterHorizontal, startingPointOfLetterVertical

    angle = ang(
    ( (point1), (point2) ),
    ( (0, 0), (0, img.height) )
    )

    img.rotate((angle - 90))
    return img
