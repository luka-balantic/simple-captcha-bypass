from solveCaptcha import solveCaptcha
from time import *
from random import *
from pymongo import MongoClient
import subprocess
import sys
import random
import decimal
import random
import timeit
from config import ROOT_DIR

client = MongoClient('mongodb://localhost:27018')
db = client.test
results = list(db.results.find({}))
start_time = timeit.default_timer()

def measureTimeOfExecution():
    secondsPassed = timeit.default_timer() - start_time
    minute, second = divmod(secondsPassed, 60)
    hour, minute = divmod(minute, 60)
    return "%d:%02d:%02d" % (hour, minute, second)

def getRandomDecimal(firstNumberMax, decimalMax):
    return decimal.Decimal('%d.%d' % (random.randint(0,firstNumberMax),random.randint(0,decimalMax)))

def saveInResultInDb(blurAroungLettersRatio, contrastLevel, shrapnessLevel, brightnessLevel, colorBalanceLevel, doInvert, zoomFactor, successRatio, functionsOrderInfo, readLetter):
    db.captchas.insert_one(
        {
            "blurAroungLettersRatio": blurAroungLettersRatio,
            "contrastLevel": str(contrastLevel),
            "shrapnessLevel": str(shrapnessLevel),
            "brightnessLevel": str(brightnessLevel),
            "colorBalanceLevel": str(colorBalanceLevel),
            "doInvert": doInvert,
            "zoomFactor": zoomFactor,
            "successRatio": successRatio,
            "functionsOrderInfo": functionsOrderInfo,
            "readByLetter": readLetter
        }
    )

def writeInTerminal(configurations, files):
    sys.stdout.flush()
    printText = "\r\r Configuration tries: {0} / files scanned: {1}".format(configurations, files)
#     sys.stdout.write(printText)


def generateRandomOptionsCallingOrder(optionsArray):
    functionsSet = range(0, len(optionsArray))
    random.shuffle(functionsSet)

    return functionSet

configurations = 0
files = 0
for index in range(1000):
    configurations = configurations + 1
    writeInTerminal(configurations, files)

    colorToKeep = 255;
    blurAroungLettersRatio = randint(35, 100)
    contrastLevel = getRandomDecimal(1,9)
    shrapnessLevel = getRandomDecimal(1,9)
    brightnessLevel = getRandomDecimal(1,9)
    colorBalanceLevel = getRandomDecimal(1,9)
    doInvert = randint(0, 1)
    zoomFactor = randint(2, 4)
    shouldConvertLuminance = randint(0, 1)
    readLetter = randint(0, 1)

    success = []
    for file in results:
        files = files + 1
        writeInTerminal(configurations, files)
        botResult = solveCaptcha(ROOT_DIR + '/prepare/captcha-samples/' + file['name'], colorToKeep, blurAroungLettersRatio, contrastLevel, shrapnessLevel, brightnessLevel, colorBalanceLevel, doInvert, zoomFactor, shouldConvertLuminance, readLetter)
        isSuccessful = ''

        if botResult['captchaResult'] == file['result']:
            isSuccesful = True
            success.append(True)
        else:
            isSuccessful = False
            success.append(False)


    successfullReadings = success.count(True)
    unSuccessfullReadings = success.count(False)

    successRatio = 100 / len(results) * successfullReadings
    saveInResultInDb(blurAroungLettersRatio, contrastLevel, shrapnessLevel, brightnessLevel, colorBalanceLevel, doInvert, zoomFactor, successRatio, botResult['functionsOrderInfo'], readLetter)

    print "This configuration has {0}% success rate! :) ({1} out of {2} solved) | Time running: {3}".format(successRatio, successfullReadings, len(success), measureTimeOfExecution())
