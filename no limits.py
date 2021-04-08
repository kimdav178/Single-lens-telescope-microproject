from PIL import Image, ImageDraw
from math import *

# Working with images
image = Image.open("2.jpg")
image = image.convert('RGB')
height = image.size[1]
width = image.size[0]
image1 = Image.new('RGB', (width, height))
image1.convert('RGB')


# Setup parameters
L = 1  # Distance from the lens to the object
RadL = 0.03  # Lens' radius
FDL = 0.3  # Lens' focal distance
d = 0.17  # Distance from the lens to the objective and slit
FDO = 0.027  # Objective's focal distance
RadO = 0.016  # Objective's radius
RadS = 0.0005  # Slit's radius
obj_width = 0.15    # Width of the book in real world, m
img_width = 0.04    # Width of the image, m
obj_img_width = 0.004   # Width of the book in the picture, m
k = (L + d)/FDO
k2 = k*width*obj_img_width/(img_width*obj_width)
#img_square = 0.00128  # Square of the image on the screen


def ray(x1, y1, x2, y2):
    x3 = x2 - x1
    y3 = y2 - y1
    if (abs(x2 + (x3 - x2) * (L + d)/FDO) > width*k/(2*k2)) and (abs(y2 + (y3 - y2) * (L + d)/FDO) > height*k/(2*k2)):
        return 1000, 1000
    else:
        x4 = x2 + (x3 - x2) * d/FDO
        y4 = y2 + (y3 - y2) * d/FDO
        if max(abs(x4), abs(y4)) > RadL:
            return 1000, 1000
        else:
            x5 = (x2 - x4)*FDL/d
            y5 = (y2 - y4)*FDL/d
            x6 = x4 + (x5 - x4)*d/FDL
            y6 = y4 + (y5 - y4)*d/FDL
            x7 = round(k2 * (x6 - x4) * FDO/d + width/2)
            y7 = round(k2 * (y6 - y4) * FDO/d + height/2)
            if (x7 < 0) or (x7 >= width) or (y7 < 0) or (y7 >= height):
                return 1000, 1000
            else:
                return x7, y7


for i in range(height):
    for j in range(width):
        RR, GG, BB = image.getpixel((j, i))
        RR = 0.01 * RR * RadS/RadO
        GG = 0.01 * GG * RadS/RadO
        BB = 0.01 * BB * RadS/RadO
        for i1 in range(-floor(RadO * k2), floor(RadO * k2)):
            for j1 in range(-round(sqrt(RadO*RadO*k2*k2-(i1^2))), round(sqrt(RadO*RadO*k2*k2-(i1^2)))):
                x0, y0 = ray((j-width/2)/k2, (i-height/2)/k2, j1/k2, i1/k2)
                if x0 < 500:
                    RRR, GGG, BBB = image1.getpixel((x0, y0))
                    r1 = RR + RRR
                    g1 = GG + GGG
                    b1 = BB + BBB
                    image1.putpixel((x0, y0), (round(r1), round(g1), round(b1)))

image1.save("0.jpg", "JPEG")
