from solveCaptcha import solveCaptcha
files = [
    {
       'file': 'captcha-1.png',
       'result': 'NJDMK'
    },
    {
        'file': 'captcha-2.png',
        'result': 'PRDIV'
    },
    {
        'file': 'captcha-3.png',
        'result': 'YYPBD'
    },
    {
        'file': 'captcha-4.png',
        'result': 'WVDXR'
    },
    {
        'file': 'captcha-5.png',
        'result': 'NJDMK'
    },
    {
        'file': 'captcha-6.png',
        'result': 'HUXKN'
    },
    {
        'file': 'captcha-7.png',
        'result': 'VAODB'
    },
    {
        'file': 'captcha-8.png',
        'result': 'MJGYZ'
    },
    {
        'file': 'captcha-9.png',
        'result': 'LOAAM'
    },
    {
        'file': 'captcha-10.png',
        'result': 'LGYGN'
    },
    {
        'file': 'captcha-11.png',
        'result': 'LGMHB'
    },
    {
        'file': 'captcha-12.png',
        'result': 'NGEDZ'
    },
    {
        'file': 'captcha-13.png',
        'result': 'JRLIT'
    },
    {
        'file': 'captcha-14.png',
        'result': 'XXPDG'
    },
    {
        'file': 'captcha-15.png',
        'result': 'NXUIL'
    },

]

success = []
for file in files:
    botResult = solveCaptcha(file['file'])

    if botResult == file['result']:
        success.append(True)
        print file['file']
    else:
        success.append(False)

successfullReadings = success.count(True)
unSuccessfullReadings = success.count(False)

successRatio = len(success) / 100 * successfullReadings

print "This configuration has {0}% success rate! :)".format(successRatio)
