import pytesseract as tes
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps

img = Image.open('captcha.png')
captchaLenght = 5;
img = ImageEnhance.Contrast(img).enhance(2)
img = img.convert('L')

R, G, B = img.convert('RGB').split()
fullimage = img.load()
r = R.load()
g = G.load()
b = B.load()
w, h = img.size
colorBlur = 55
# Convert non-black pixels to white
for i in range(w):
    for j in range(h):
        if(r[i, j] > colorBlur or g[i, j] > colorBlur or b[i, j] > colorBlur):
            r[i, j] = 255
img = Image.merge('RGB', (R, R, R))

img = ImageOps.invert(img)

R, G, B = img.convert('RGB').split()
fullimage = img.load()
r = R.load()
g = G.load()
b = B.load()
w, h = img.size  #91 x 24
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

print startingPointsOfBlackness
print staringPointsOfColorness
print blackColumns
print coloredColumns
print startingPointsOfBlackness[0]
print staringPointsOfColorness[0]

cuttingPoints = []
for index in range(len(startingPointsOfBlackness) - 1):
    if index != len(startingPointsOfBlackness): # If not last in array
        cuttingPoint = startingPointsOfBlackness[index] + ( (staringPointsOfColorness[index] - startingPointsOfBlackness[index] ) / 2 )
    else:
        cuttingPoint = startingPointsOfBlackness[index] + ( ( w - startingPointsOfBlackness[index] ) / 2 )

    cuttingPoints.append(cuttingPoint)

print cuttingPoints

cuttingSections = []

for index in range(len(cuttingPoints) - 1):
    if index != len(startingPointsOfBlackness): # If not last in array
        cuttingSection = [ cuttingPoints[index], cuttingPoints[index + 1] ]
    else:
        cuttingSection = [ cuttingPoints[index], w ]

    cuttingSections.append(cuttingSection)

print cuttingSections


img = Image.merge('RGB', (R, G, B))
img = img.crop((cuttingSections[1][0], 0, cuttingSections[1][1], h))

factor = 3
img = img.resize((img.width * factor, img.height * factor))
img = ImageEnhance.Sharpness(img).enhance(1.5)

img.show()

print tes.image_to_string(img)
