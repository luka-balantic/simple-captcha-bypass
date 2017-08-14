import pytesseract as tes
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps

def solveCaptcha(imagePath):
    img = Image.open(imagePath)
    captchaLenght = 5;
    img = ImageEnhance.Contrast(img).enhance(1) # add contrast to image
    img = img.convert('L')  # convert to black and white
    # img.show()

    R, G, B = img.convert('RGB').split() # split RGB layers
    fullimage = img.load()
    r = R.load()
    g = G.load()
    b = B.load()
    w, h = img.size
    colorBlur = 100 #change to set hardness of color selection
    # Convert non-black pixels to white
    for i in range(w):
        for j in range(h):
            if(r[i, j] > colorBlur or g[i, j] > colorBlur or b[i, j] > colorBlur):
                r[i, j] = 255
    img = Image.merge('RGB', (R, R, R)) # merge layers

    # img.show()

    img = ImageOps.invert(img) # invert image

    R, G, B = img.convert('RGB').split() # split RGB layers
    r = R.load()
    g = G.load()
    b = B.load()
    w, h = img.size
    blackColumns = []
    coloredColumns = []
    startingPointsOfBlackness = []
    staringPointsOfColorness = []
    alreadySavedFirstBlackColumn = False
    for i in range(1, w): # 91 x
        column = []
        for j in range(h): #24 x
            if r[i, j] == 0 and g[i, j] == 0 and b [i, j] == 0:
                column.append(True) # If pixel is black, add True to column
            else:
                column.append(False)

        if all(item for item in column): # If all in column are black
            blackColumns.append(i) # Add column to list of black columns
            if alreadySavedFirstBlackColumn == False:
                startingPointsOfBlackness.append(i)
                alreadySavedFirstBlackColumn = True
        else:
            coloredColumns.append(i) # Add column to list of colored columns
            if alreadySavedFirstBlackColumn == True:
                staringPointsOfColorness.append(i)
                alreadySavedFirstBlackColumn = False
    # img = Image.merge('RGB', (R, G, B))

    # print startingPointsOfBlackness
    # print staringPointsOfColorness
    # print blackColumns
    # print coloredColumns
    # print startingPointsOfBlackness[0]
    # print staringPointsOfColorness[0]

    # Calculate middle of cutting points (hit inbetween letters - as centered as possible)
    #
    cuttingPoints = []
    for index in range(len(startingPointsOfBlackness) -1 ):
        if index != len(startingPointsOfBlackness): # If not last in array
            cuttingPoint = startingPointsOfBlackness[index] + ( (staringPointsOfColorness[index] - startingPointsOfBlackness[index] ) / 2 ) # center of blackness section
        else:
            cuttingPoint = startingPointsOfBlackness[index] + ( ( w - startingPointsOfBlackness[index] ) / 2 ) # center of blackness section (last blackness)

        cuttingPoints.append(cuttingPoint)

    cuttingPoints.append(w) # add last cutting point which is last pixel of image width
    # print cuttingPoints

    cuttingSections = []

    #Create cutting section groups out of cutting points
    #Image will be cutted between each two points generated
    for index in range(len(cuttingPoints) - 1):
        if index != len(startingPointsOfBlackness): # If not last in array
            cuttingSection = [ cuttingPoints[index], cuttingPoints[index + 1] ]
        else:
            cuttingSection = [ cuttingPoints[index], w ]

        cuttingSections.append(cuttingSection)

    # print cuttingSections

    letters = []
    for index in range(len(cuttingSections)):
        letter = img.crop((cuttingSections[index][0], 0, cuttingSections[index][1], h)) # Crop image according to cuttingSections (cut letter out)
        factor = 6
        letter = letter.resize((letter.width * factor, letter.height * factor)) # zoom image

        letters.append(letter)

    captchaFinal = ""
    for letterImage in letters:
#         letterImage.show()
        captchaFinal = captchaFinal + tes.image_to_string(letterImage, config='-psm 10')  # read each letter

    return captchaFinal
#     img = ImageEnhance.Sharpness(img).enhance(1.5)

# # print solveCaptcha('captcha.png')

