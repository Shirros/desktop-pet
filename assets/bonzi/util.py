"""
Util I made to get rid of the cyan backgrounds that were originally on the bonzi buddy images.
"""
import cv2
from os import listdir
from os.path import join
import numpy as np

low_green = np.array([254, 254, 0, 0])
high_green = np.array([255, 255, 0, 255])

def remove_background(file_name):
    img = cv2.imread(file_name)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    mask = cv2.inRange(img, low_green, high_green)
    mask = 255-mask
    img[:, :, 3] = mask
    cv2.imwrite(file_name, img)

for f in listdir("assets/bonzi"):
    if f.endswith(".png"):
        print("doing", f)
        remove_background(join("assets/bonzi", f))
print("Done!")