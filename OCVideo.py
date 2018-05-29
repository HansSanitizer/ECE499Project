import numpy as np
import cv2
from matplotlib import pyplot as plt
cap = cv2.VideoCapture(1)
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

TMin = 0
TMax = 255

while(True):
    TMin = cv2.getTrackbarPos('TMin', 'Control')
    TMax = cv2.getTrackbarPos('TMin', 'Control')
    R = cv2.getTrackbarPos('R', 'Control')
    G = cv2.getTrackbarPos('G', 'Control')
    B = cv2.getTrackbarPos('B', 'Control')

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, TMin, TMax, 0)
    im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    img = np.zeros((300, 512, 3), np.uint8)
    image = cv2.drawContours(gray, contours, -1, (B, G, R), 1)
    # Display the resulting frame
    cv2.imshow('Frame',image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

