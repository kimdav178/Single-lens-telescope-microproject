from PIL import Image
from math import *
import time
import numpy as np

# Working with images
st = time.time()
img = np.asarray(Image.open("100.jpg").convert('RGB'))
height = img.shape[0]
width = img.shape[1]
img1 = np.array(Image.new('RGB', (width, height)))
img2 = np.zeros((height, width, 3), dtype=np.float)


# Setup parameters
L = 3  # Distance from the lens to the object
RadL = 0.03  # Lens' radius
FDL = 0.30375  # Lens' focal distance
d = 0.0000000000001    # Distance from the lens to the objective and slit
FDO = 0.00393  # Objective's focal distance
RadO = 0.00115588  # Objective's radius
RadS = 0.0004  # Slit's radius
pixel = 0.0000009
img_width = pixel * width    # Width of the image, m.
img_height = pixel * height
k = (L + d)/FDO     # Coefficient between the object and its image on the matrix
x = 10 * pixel


def ray(x1, y1, x2, y2):
    x3 = x2 - x1
    y3 = y2 - y1
    if (abs(x2+((x3-x2)*(L+d)/FDO)) > img_width*k/2) or (abs(y2+(y3-y2)*(L+d)/FDO) > img_height*k/2):
        return 1000, 1000
    else:
        x4 = x2 + (x3 - x2) * d / FDO
        y4 = y2 + (y3 - y2) * d / FDO
        if max(abs(x4), abs(y4)) > RadL:
            return 1000, 1000
        else:
            x5 = (x2 - x4) * FDL / d
            y5 = (y2 - y4) * FDL / d
            x6 = x4 + (x5 - x4)*d/FDL
            y6 = y4 + (y5 - y4)*d/FDL
            if max(abs(x6), abs(y6)) > RadS:
                return 1000, 1000
            else:
                x7 = round((x6 - x4) * FDO/(d * pixel) + width/2)
                y7 = round((y6 - y4) * FDO/(d * pixel) + height/2)
                if (x7 < 0) or (x7 >= width) or (y7 < 0) or (y7 >= height):
                    return 1000, 1000
                else:
                    return x7, y7


for i in range(width):
    i0 = (i - width/2) * pixel
    for j in range(height):
        RR, GG, BB = img[j, i]
        j0 = (j - height/2) * pixel
        i1 = -RadO
        while i1 <= RadO:
            j1 = -sqrt(RadO * RadO - (i1 * i1))
            while j1 <= sqrt(RadO * RadO - (i1 * i1)):
                x0, y0 = ray(i0, j0, i1, j1)
                if x0 < 1000:
                    img2[y0, x0] += [RR, GG, BB]
                j1 += x
            i1 += x


k1 = 255/img2.max()
img2 = img2 * k1
for i in range(height):
    for j in range(width):
        img1[i, j, 0] = floor(img2[i, j, 0])
        img1[i, j, 1] = floor(img2[i, j, 1])
        img1[i, j, 2] = floor(img2[i, j, 2])

Image.fromarray(img1).save("0.jpg", "JPEG")
print(time.time() - st)
