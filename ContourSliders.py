import numpy as np
import cv2
from matplotlib import pyplot as plt
def nothing(x):
    pass

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)
cv2.namedWindow('Control')

# create trackbars for color change
cv2.createTrackbar('TMin','Control',0,255,nothing)
cv2.createTrackbar('TMax','Control',0,255,nothing)
cv2.createTrackbar('R','Control',0,255,nothing)
cv2.createTrackbar('G','Control',0,255,nothing)
cv2.createTrackbar('B','Control',0,255,nothing)

TMin = 100
TMax = 255
R=100
G=0
B=0
im = cv2.imread('Images/TBCFC1.png')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
first = True
while(True):
    TMaxOld = TMax
    TMinOld = TMin
    rOld=R
    gOld=G
    bOld=B
    TMin = cv2.getTrackbarPos('TMin', 'Control')
    TMax = cv2.getTrackbarPos('TMin', 'Control')
    R = cv2.getTrackbarPos('R', 'Control')
    G = cv2.getTrackbarPos('G', 'Control')
    B = cv2.getTrackbarPos('B', 'Control')
    if first is True or rOld is not R or gOld is not G or bOld is not B or TMaxOld is not TMax or TMinOld is not TMin :
        ret, thresh = cv2.threshold(imgray, TMin, TMax, 0)
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
        image = cv2.drawContours(im, contours, -1, (B,G,R), 3)
        cv2.imshow("Frame", image)
        first = False


# When everything done, close windows
cv2.destroyAllWindows()

