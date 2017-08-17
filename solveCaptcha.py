import pytesseract as tes
import random
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps

def solveCaptcha(imagePath, colorToKeep, blurAroungLettersRatio, contrastLevel, shrapnessLevel, doInvert, zoomFactor, shouldConvertLuminance):
    def generateRandomOptionsCallingOrder(arrayOfOptions):
        functionsSet = range(0, len(arrayOfOptions))
        random.shuffle(functionsSet)

        return functionsSet

    def setContrast(img, options):
        return ImageEnhance.Contrast(img).enhance(options['contrastLevel']) # add contrast to image

    def setSharpness(img, options):
        return ImageEnhance.Sharpness(img).enhance(options['shrapnessLevel']) # add contrast to image

    def mixOptions(img):
        arrayOfOptions = [
            {
                "name": 'setContrast',
                "function": setContrast,
                "args": {
                    "contrastLevel": contrastLevel
                }
            },
            {
                 "name": 'setSharpness',
                 "function": setSharpness,
                 "args": {
                    "shrapnessLevel": shrapnessLevel
                 }
            },
#             {
#                  "function": removeAllButOneColors,
#                  "name": "removeAllButOneColors",
#                  "args": {
#                     "colorToKeep": colorToKeep,
#                      "blurAroungLettersRatio": blurAroungLettersRatio
#                  }
#             },
#             {
#                  "function": invert,
#                  "name": "invert",
#                  "args": {
#                     "doInvert": doInvert
#                  }
#             }
        ]

        functionsSet = generateRandomOptionsCallingOrder(arrayOfOptions)
        functionsOrderInfo = []
        for index, function in enumerate(functionsSet):
            functionObject = arrayOfOptions[function]
            functionDef = functionObject['function']
            functionName = functionObject['name']
            functionArgs = functionObject['args']
            functionInfo = {
                "order": index,
                "functionName": functionName,
            }

            functionsOrderInfo.append(functionInfo)

            img = functionDef(img, functionArgs)

        return {
            "img": img,
            "functionsOrderInfo": functionsOrderInfo
        }

    def convertToLuminance(img, options):
#         if options['shouldConvertLuminance']:
#             return img.convert('L')  # convert to black and white

        return img


    # img.show()
    def removeAllButOneColors(img, options):
        R, G, B = img.convert('RGB').split() # split RGB layers
        red = R.load()
        green = G.load()
        blue = B.load()
        width, height = img.size
        for x in range(width):
            for y in range(height):
                if(red[x, y] > options['blurAroungLettersRatio'] or green[x, y] > options['blurAroungLettersRatio'] or blue[x, y] > options['blurAroungLettersRatio']):
                    red[x, y] = 255
        return Image.merge('RGB', (R, R, R))

    # img.show()

    def invert(img, options):
        if options['doInvert'] == True:
            return ImageOps.invert(img)

    img = Image.open(imagePath)

    mixedOptions = mixOptions(img)
    functionsOrderInfo = mixedOptions['functionsOrderInfo']
    img = mixedOptions['img']
    img = convertToLuminance(img, {"shouldConvertLuminance": shouldConvertLuminance })
    img = removeAllButOneColors(img, {
        "colorToKeep": colorToKeep,
        "blurAroungLettersRatio": blurAroungLettersRatio
    })

    img = invert(img, {"doInvert": True})

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
#     img.show()
#     print startingPointsOfBlackness
#     print staringPointsOfColorness
#     print "black"
#     print blackColumns
#     print 'color'
#     print coloredColumns
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
        factor = zoomFactor
        letter = letter.resize((letter.width * factor, letter.height * factor)) # zoom image

        letters.append(letter)

    captchaFinal = ""
    for letterImage in letters:
        captchaFinal = captchaFinal + tes.image_to_string(letterImage, config='-psm 10')  # read each letter

#     print captchaFinal
    return {
        "captchaResult": captchaFinal,
        "functionsOrderInfo": functionsOrderInfo
    }

# # print solveCaptcha('captcha.png')

