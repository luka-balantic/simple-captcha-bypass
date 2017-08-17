from solveCaptcha import solveCaptcha
from time import *
from random import *
from pymongo import MongoClient
import subprocess
import sys
import random


client = MongoClient('mongodb://localhost:27018')
db = client.test
results = list(db.results.find({}))

def saveInResultInDb(blurAroungLettersRatio, contrastLevel, shrapnessLevel, doInvert, zoomFactor, successRatio, functionsOrderInfo):
    db.captchas.insert_one(
        {
            "blurAroungLettersRatio": blurAroungLettersRatio,
            "contrastLevel": contrastLevel,
            "shrapnessLevel": shrapnessLevel,
            "doInvert": doInvert,
            "zoomFactor": zoomFactor,
            "successRatio": successRatio,
            "functionsOrderInfo": functionsOrderInfo
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
    contrastLevel = randint(1, 2)
    shrapnessLevel = randint(1, 2)
    doInvert = randint(0, 1)
    zoomFactor = randint(2, 4)
    shouldConvertLuminance = randint(0, 1)

    success = []
    for file in results:
        files = files + 1
        writeInTerminal(configurations, files)
        botResult = solveCaptcha('/captcha-breaker/prepare/captcha-samples/' + file['name'], colorToKeep, blurAroungLettersRatio, contrastLevel, shrapnessLevel, doInvert, zoomFactor, shouldConvertLuminance)
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
    saveInResultInDb(blurAroungLettersRatio, contrastLevel, shrapnessLevel, doInvert, zoomFactor, successRatio, botResult['functionsOrderInfo'])

    print "This configuration has {0}% success rate! :) ({1} out of {2} solved)".format(successRatio, successfullReadings, len(success))
