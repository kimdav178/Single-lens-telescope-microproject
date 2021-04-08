from PIL import Image, ImageDraw
import numpy as np
from math import *

# Working with images
image = Image.open("a2.jpg")
image = image.convert('RGB')
height = image.size[1]
width = image.size[0]
image1 = Image.new('RGB', (width, height))
image1 = image1.convert('RGB')
#R = np.zeros((width, height))
#G = np.zeros((width, height))
#B = np.zeros((width, height))
# image_path = sys.argv[1]


# Setup parameters
L = 1.17  # Distance from the lens to the object
RadL = 0.03  # Lens' radius
FDL = 0.2  # Lens' focal distance
d = 0.17  # Distance from the lens to the objective and slit
RadF = 0.002  # Objective's radius
FDO = 0.05  # Objective's focal distance
RadS = 0.0005  # Slit's radius
img_square = 0.00025  # Square of the image on the screen
k = (L + d)/FDO
k2 = sqrt(height*width/img_square)


"""
def backward_ray1(x1, y1, x2, y2, rp, gp, bp):
    x3 = x2 - x1
    y3 = y2 - y1
    if max(x2 + (x3 - x2) * d / FDO, y2 + (y3 - y2) * d / FDO) > RadL:
        return 0, 0, 0, 0, 0
    else:
        x4 = x2 + (x3 - x2) * d / FDO
        y4 = y2 + (y3 - y2) * d / FDO
        x5 = (x4 - x2) * FDL / d
        y5 = (y4 - y2) * FDL / d
        if (abs(x4 + (x5 - x4) * L/FDL) > k2*width * k/2) or (abs(y4 + (y5 - y4) * L/FDL) > k2*height * k/2):
            return 0, 0, 0, 0, 0
        else:
            x6 = x4 + (x5 - x4) * L / FDL
            y6 = y4 + (y5 - y4) * L / FDL
            return x6, y6, rp/(k2*4*pi*((L+d+FDO)*(L+d+FDO))), gp/(k2*4*pi*((L+d+FDO)*(L+d+FDO))), bp/(k2*4*pi*((L+d+FDO)*L+d+FDO))
"""


def backward_ray(x1, y1, x2, y2, rp, gp, bp):
    x3 = x2 - x1
    y3 = y2 - y1
    if (abs(x2 + (x3 - x2) * (L + d)/FDO) > width*k/(2*k2)) and (abs(y2 + (y3 - y2) * (L + d)/FDO) > height*k/(2*k2)):
        return 0, 0, 0, 0, 0
    else:
        x4 = x2 + (x3 - x2) * (L + d)/FDO
        y4 = y2 + (y3 - y2) * (L + d)/FDO
        return x4, y4, rp/(k2*4*pi*((L+d+FDO)*(L+d+FDO))), gp/(k2*4*pi*((L+d+FDO)*(L+d+FDO))), bp/(k2*4*pi*((L+d+FDO)*L+d+FDO))


def straight_ray(x6, y6, x7, y7, rp, gp, bp, imag):
    #imag = Image.new('RGB', (width, height))
    imag1 = imag
    x8 = (x7 - x6) * FDL / L
    y8 = (y7 - y6) * FDL / L
    if max(abs(x7 + (x8 - x7) * d / FDL), abs(y7 + (y8 - y7) * d / FDL)) <= RadS:
        x9 = x7 + (x8 - x7) * d / FDL
        y9 = y7 + (y8 - y7) * d / FDL
        x10 = (x9 - x7) * FDO / d
        y10 = (y9 - y7) * FDO / d
        x11 = round(x10*k2+width/2)
        y11 = round(y10*k2+height/2)
        if (y11>=0) and (x11>=0) and (x11<width) and (y11<height):
            imag1.putpixel((x11, y11), (imag1.getpixel((x11, y11))[0]+rp, imag1.getpixel((x11, y11))[1]+gp, imag1.getpixel((x11, y11))[2]+bp))
    return imag1


for i in range(height):
    for j in range(width):
        RR, GG, BB = image.getpixel((j, i))
        for i1 in range(-round(RadS * k2), round(RadS * k2)):
            for j1 in range(-round(sqrt(RadS*RadS*k2*k2-(i1^2))), round(sqrt(RadS*RadS*k2*k2-(i1^2)))):
                x0, y0, r1, g1, b1 = backward_ray((j-width/2)/k2, (i-height/2)/k2, j1/k2, i1/k2, RR, GG, BB)
                for i2 in range(-round(RadL * k2), round(RadL * k2)):
                    for j2 in range(-round(sqrt(RadL*RadL*k2*k2 - (i2^2))), round(sqrt(RadL*RadL*k2*k2 - (i2^2)))):
                        image1 = straight_ray(x0, y0, i2/k2, j2/k2, round(r1), round(g1), round(b1), image1)
                        #for j3 in range(height):
                         #   for i3 in range(width):
                          #      image1.putpixel((i3, j3), (image1.getpixel((i3, j3))[0]+imag.getpixel((i3, j3))[0], image1.getpixel((i3, j3))[1]+imag.getpixel((i3, j3))[1], image1.getpixel((i3, j3))[2]+imag.getpixel((i3, j3))[2]))

image1.save("result2.jpg", "JPEG")


"""
for i in range(height):
    for j in range(width):
        RR, GG, BB = im.getpixel((i, j))
        for x in range(k):
            for y in range(k):
                R[k * (i - 1) + x, k * (j - 1) + y] = int(RR)
                G[k * (i - 1) + x, k * (j - 1) + y] = int(GG)
                B[k * (i - 1) + x, k * (j - 1) + y] = int(BB)
                ImageDraw.Draw(image1).point((k * (i - 1) + x, k * (j - 1) + y), (RR, GG, BB))
image1.save("result.jpg", "JPEG")
"""