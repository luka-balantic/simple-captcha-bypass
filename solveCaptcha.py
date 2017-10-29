import pytesseract as tes
import random
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps
from lib.alignLetter import alignLetter

def solveCaptcha(imagePath, colorToKeep, blurAroungLettersRatio, contrastLevel, shrapnessLevel, brightnessLevel, colorBalanceLevel, doInvert, zoomFactor, shouldConvertLuminance, readLetter, shouldAlignLetter, mixOptions=None, passedOption=None):
    def generateRandomOptionsCallingOrder(arrayOfOptions):
        functionsSet = list(range(0, len(arrayOfOptions)))
        random.shuffle(functionsSet)

        return functionsSet

    def setContrast(img, options):
        return ImageEnhance.Contrast(img).enhance(options['contrastLevel']) # add contrast to image

    def setSharpness(img, options):
        return ImageEnhance.Sharpness(img).enhance(options['shrapnessLevel']) # add contrast to image

    def setBrightness(img, options):
        return ImageEnhance.Brightness(img).enhance(options['brightnessLevel']) # add contrast to image

    def setColorBalance(img, options):
        return ImageEnhance.Color(img).enhance(options['colorBalanceLevel']) # add contrast to image

    def mixOptions(img, shouldMix, passedFunctionSet=None):
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
            {
                 "name": 'setBrightness',
                 "function": setBrightness,
                 "args": {
                    "brightnessLevel": brightnessLevel
                 }
            },
            {
                 "name": 'setColorBalance',
                 "function": setColorBalance,
                 "args": {
                    "colorBalanceLevel": colorBalanceLevel
                 }
            }
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

    def cutImageToLetters(img):
        R, G, B = img.convert('RGB').split() # split RGB layers
        r = R.load()
        g = G.load()
        b = B.load()
        width, height = img.size
        blackColumns = []
        coloredColumns = []
        startingPointsOfBlackness = []
        staringPointsOfColorness = []
        alreadySavedFirstBlackColumn = False
        for x in range(1, width):
            column = []
            for y in range(height):

                if r[x, y] == 0 and g[x, y] == 0 and b [x, y] == 0:
                   column.append(True) # If pixel is black, add True to column
                else:
                   column.append(False)

            if all(item for item in column): # If all in column are black
                blackColumns.append(x) # Add column to list of black columns
                if alreadySavedFirstBlackColumn == False:
                    startingPointsOfBlackness.append(x)
                    alreadySavedFirstBlackColumn = True
            else:
                coloredColumns.append(x) # Add column to list of colored columns
                if alreadySavedFirstBlackColumn == True:
                    staringPointsOfColorness.append(x)
                    alreadySavedFirstBlackColumn = False

        cuttingPoints = []
        for index in range(len(startingPointsOfBlackness) -1 ):
            if index != len(startingPointsOfBlackness): # If not last in array
                cuttingPoint = startingPointsOfBlackness[index] + ( (staringPointsOfColorness[index] - startingPointsOfBlackness[index] ) / 2 ) # center of blackness section
            else:
                cuttingPoint = startingPointsOfBlackness[index] + ( ( w - startingPointsOfBlackness[index] ) / 2 ) # center of blackness section (last blackness)

            cuttingPoints.append(cuttingPoint)

        cuttingPoints.append(width) # add last cutting point which is last pixel of image width

        #Create cutting section groups out of cutting points
        #Image will be cutted between each two points generate
        cuttingSections = []
        for index in range(len(cuttingPoints) - 1):
            if index != len(startingPointsOfBlackness): # If not last in array
                cuttingSection = [ cuttingPoints[index], cuttingPoints[index + 1] ]
            else:
                cuttingSection = [ cuttingPoints[index], width ]

            cuttingSections.append(cuttingSection)

        # print cuttingSections
        letters = []
        for index in range(len(cuttingSections)):
            letter = img.crop((cuttingSections[index][0], 0, cuttingSections[index][1], height)) # Crop image according to cuttingSections (cut letter out)
            factor = zoomFactor
            letter = letter.resize((letter.width * factor, letter.height * factor)) # zoom image

            letters.append(letter)

        return letters

    def convertToLuminance(img, options):
#         if options['shouldConvertLuminance']:
#             return img.convert('L')  # convert to black and white

        return img

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

    def invert(img, options):
        if options['doInvert'] == True:
            return ImageOps.invert(img)

    def readCaptcha(objectToRead, readLetter=False):
        if readLetter:
            captchaFinal = ""
            for letterImage in objectToRead:
                if (shouldAlignLetter):
                    letterImage = alignLetter(letterImage)
                letterResult = tes.image_to_string(letterImage, config='-psm 10')
                captchaFinal = captchaFinal + letterResult # read each letter

        if not readLetter:
            captchaFinal = tes.image_to_string(objectToRead)  # read each letter

        return captchaFinal

    # Start
    img = Image.open(imagePath)

    mixedOptions = mixOptions(img, False, )
    functionsOrderInfo = mixedOptions['functionsOrderInfo']
    img = mixedOptions['img']

    img = convertToLuminance(img, {"shouldConvertLuminance": shouldConvertLuminance })
    img = removeAllButOneColors(img, {
        "colorToKeep": colorToKeep,
        "blurAroungLettersRatio": blurAroungLettersRatio
    })

    img = invert(img, {"doInvert": True})

    if (readLetter):
        letters = cutImageToLetters(img)
        captchaResult = readCaptcha(letters, True)
    else:
        captchaResult = readCaptcha(img)

    return {
        "captchaResult": captchaResult,
        "functionsOrderInfo": functionsOrderInfo
    }
