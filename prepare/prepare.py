from pymongo import MongoClient
import os
from PIL import Image
from configuration import CONFIG

client = MongoClient()
db = client.local

def askForCaptchaResult(image):
    img = Image.open(CONFIG['CAPTCHA_SAMPLES_DIR'] + image)
    img.show()
    captcha = raw_input("Please correct captcha text: ")
    print "you entered", captcha

    if len(captcha) != 5 or not captcha.isalpha():
        captcha = raw_input("Please enter five letters: ")
        print "you entered", captcha

    img.close()
    return captcha

def saveCaptchaResultInD(name, result):
    result = db.results.insert_one(
        {
            "name": name,
            "result": result
        }
    )
    print result

for image in os.listdir(CONFIG['CAPTCHA_SAMPLES_DIR']):
    if image.endswith(".png"):
        result = askForCaptchaResult(image)
        saveCaptchaResultInD(image, result)
