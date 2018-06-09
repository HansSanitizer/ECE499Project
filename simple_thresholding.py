# Applies a mask based on value of threshold for object detection.
# Expected use is to locate the record from the full scan.
import cv2 as cv

bw = cv.imread('grooves_128000.jpg', 0)
ret, thresh = cv.threshold(bw, 35, 225, cv.THRESH_BINARY)

height, width = bw.shape[0:2]

cv.imshow("Original BW", bw)
cv.imshow("Threshold RET", thresh)

cv.waitKey(0)
cv.destroyAllWindows()