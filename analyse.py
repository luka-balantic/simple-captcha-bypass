from solveCaptcha import solveCaptcha
from results import results
from time import *
from random import *

# configuration = {
#    'name': 'configuration-' + time.strftime("%Y-%m-%d-%H:%M")
#    'options': {
#        'blurAroungLettersRatio':  randint(1, 100)
#        'contrastLevel':  randint(1, 2)
#        'doInvert':  randint(1, 2)
#        'zoomFactor':  randint(1, 4)
#    }
# }
for index in range(50):
    configurationName = 'configuration-'
    blurAroungLettersRatio = randint(1, 100)
    contrastLevel = randint(1, 2)
    doInvert = randint(1, 2)
    zoomFactor = randint(1, 4)
    success = []

    for file in results:
        botResult = solveCaptcha(file['file'], configurationName, blurAroungLettersRatio, contrastLevel, doInvert, zoomFactor)

        if botResult == file['result']:
            success.append(True)
            print file['file']
            print configurationName
            print blurAroungLettersRatio
            print contrastLevel
            print doInvert
            print zoomFactor
            print botResult
        else:
            success.append(False)

    successfullReadings = success.count(True)
    unSuccessfullReadings = success.count(False)

#     print successfullReadings
#     print unSuccessfullReadings
#     print len(success)
    successRatio = 100 / 15 * successfullReadings

    print "This configuration has {0}% success rate! :) ({1} out of {2} solved)".format(successRatio, successfullReadings, len(success))

