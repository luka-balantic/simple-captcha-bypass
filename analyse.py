from solveCaptcha import solveCaptcha
from time import *
from random import *
from pymongo import MongoClient
import subprocess
import sys

client = MongoClient('mongodb://localhost:27018')
db = client.local
results = list(db.results.find({}))

def saveInResultInDb(blurAroundLettersRatio, contrastLevel, doInvert, zoomFactor, isSuccessful, successfullReadings):
    db.captchas.insert_one(
        {
            "blurAroundLettersRatio": blurAroundLettersRatio,
            "contrastLevel": contrastLevel,
            "doInvert": doInvert,
            "zoomFactor": zoomFactor,
            "isSuccessful": isSuccessful,
            "successfullReadings": successfullReadings
        }
    )

def writeInTerminal(configurations, files):
    sys.stdout.flush()
    printText = "\r\r Configuration tries: {0} / files scanned: {1}".format(configurations, files)
    sys.stdout.write(printText)


configurations = 0
files = 0
for index in range(1000):
    configurations = configurations + 1
    writeInTerminal(configurations, files)
    configurationName = 'configuration-'
    blurAroundLettersRatio = randint(1, 100)
    contrastLevel = randint(1, 2)
    doInvert = randint(0, 1)
    zoomFactor = randint(2, 4)
    success = []

    for file in results:
        files = files + 1
        writeInTerminal(configurations, files)
        botResult = solveCaptcha('/captcha-breaker/prepare/captcha-samples/' + file['name'], configurationName, blurAroundLettersRatio, contrastLevel, doInvert, zoomFactor)
        isSuccessful = ''

        if botResult == file['result']:
            isSuccesful = True
            success.append(True)
        else:
            isSuccessful = False
            success.append(False)


    successfullReadings = success.count(True)
    unSuccessfullReadings = success.count(False)

    successRatio = 100 / len(results) * successfullReadings
    saveInResultInDb(blurAroundLettersRatio, contrastLevel, doInvert, zoomFactor, successRatio, successfullReadings)

    print "This configuration has {0}% success rate! :) ({1} out of {2} solved)".format(successRatio, successfullReadings, len(success))
