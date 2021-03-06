from PIL import Image, ImageDraw
from math import *
import time
import numpy as np

# Working with images
st = time.time()
#image = Image.open("2.jpg").convert('RGB')
#height = image.size[1]
#width = image.size[0]
#image1 = Image.new('RGB', (width, height))
img = np.asarray(Image.open("2.jpg").convert('RGB'))
height = img.shape[0]
width = img.shape[1]
img1 = np.array(Image.new('RGB', (width, height)))
img2 = np.zeros((height, width, 3), dtype=np.float)
#img1.setflags(write=1)
#img0 = np.zeros((height, width))


# Setup parameters
L = 1  # Distance from the lens to the object
RadL = 0.03  # Lens' radius
FDL = 0.3  # Lens' focal distance
d = 0.17  # Distance from the lens to the objective and slit
FDO = 0.00393  # Objective's focal distance
RadO = 0.0023  # Objective's radius
RadS = 0.0023  # Slit's radius
obj_width = 0.15    # Width of the book in real world, m
img_width = 0.0046728    # Width of the image, m. 176 пикс
img_height = img_width * 144 / 176
obj_img_width = 0.00046728   # Width of the book in the picture, m
pixel = 0.00002655   # Width of a single pixel, m. 0,9 um *(4248 pix/144 pix)
k = (L + d)/FDO
#k2 = k*width*obj_img_width/(img_width*obj_width)
#img_square = 0.00128  # Square of the image on the screen


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
            """
            if max(abs(x6), abs(y6)) > RadS:
                return 1000, 1000
            else:
            """
            x7 = round((x6 - x4) * FDO/(d * pixel) + width/2)
            y7 = round((y6 - y4) * FDO/(d * pixel) + height/2)
            if (x7 < 0) or (x7 >= width) or (y7 < 0) or (y7 >= height):
                return 1000, 1000
            else:
                return x7, y7


for i in range(width):
    for j in range(height):
        #RR, GG, BB = image.getpixel((i, j))
        RR, GG, BB = img[j, i]
        #RR, GG, BB = img[i, j]
        #RR = 0.0023 * RR
        #GG = 0.0023 * GG
        #BB = 0.0023 * BB
        i0 = (i - width/2) * pixel
        j0 = (j - height/2) * pixel
        RadO0 = floor(RadO/pixel)
        for i1 in range(-RadO0, RadO0):
            for j1 in range(-round(sqrt(RadO0*RadO0-(i1*i1))), round(sqrt(RadO0*RadO0-(i1*i1)))):
                x0, y0 = ray(i0, j0, i1*pixel, j1*pixel)
                if x0 < 500:
                    #RRR, GGG, BBB = image1.getpixel((x0, y0))
                    #RRR, GGG, BBB = img2[y0, x0]
                    #r1 = RR + RRR
                    #g1 = GG + GGG
                    #b1 = BB + BBB
                    #image1.putpixel((x0, y0), (r1, g1, b1))
                    img2[y0, x0] += [RR, GG, BB]

#k1 = 255/(img2.max() - img2.min())
k1 = 255/img2.max()
img2 = img2 * k1
for i in range(height):
    for j in range(width):
        img1[i, j, 0] = floor(img2[i, j, 0])
        img1[i, j, 1] = floor(img2[i, j, 1])
        img1[i, j, 2] = floor(img2[i, j, 2])
        #img1[i, j] = img2[i, j]

"""
for i in range(width):
    for j in range(height):
        r, g, b = image1.getpixel((i, j))
        r = round(r * 0.0023)
        g = round(g * 0.0023)
        b = round(b * 0.0023)
        image1.putpixel((i, j), (r, g, b))
"""

Image.fromarray(img1).save("0.jpg", "JPEG")
#image1.save("0.jpg", "JPEG")
print(time.time() - st)
