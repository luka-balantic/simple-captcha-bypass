import pytesseract as tes
from PIL import ImageEnhance
from PIL import Image
from PIL import ImageOps

img = Image.open('captcha.png')
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
for i in range(w): # 91 x

    column = []
    for j in range(h): #24 x
        if r[i, j] == 0 and g[i, j] == 0 and b [i, j] == 0:
            column.append(True)
        else:
            column.append(False)

    if all(item for item in column):
        blackColumns.append(i)

print blackColumns
for blackColumn in blackColumns:
    for j in range(h):
        r[blackColumn, j] = 160
        g[blackColumn, j] = 10
        b[blackColumn, j] = 10

img = Image.merge('RGB', (R, G, B))

factor = 3
img = img.resize((img.width * factor, img.height * factor))
img = ImageEnhance.Sharpness(img).enhance(1.5)

img.show()

print tes.image_to_string(img)
