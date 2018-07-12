import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

im = cv.imread('Images/VTD2.png')
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(imgray, 180, 255, 0)
im2, contours, hierarchy = cv.findContours(thresh, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)
image = cv.drawContours(im, contours, -1, (0,255,0), 3)
plt.imshow(image),plt.show()
print (contours)