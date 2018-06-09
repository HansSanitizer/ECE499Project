import cv2 as cv

bw = cv.imread('grooves_128000.jpg', 0)
cv.imshow("Original BW", bw)

ret, thresh_basic = cv.threshold(bw, 30, 255, cv.THRESH_BINARY)
cv.imshow("Basic Binary", thresh_basic)

thresh_adapt = cv.adaptiveThreshold(bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 45, 0)
cv.imshow("Adaptive Threshold", thresh_adapt)

_, contours, heirarchy = cv.findContours(thresh_adapt, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
bw2 = bw.copy()
index = -1
thickness = 1
color = (255,0,255)

cv.drawContours(bw2, contours, index, color, thickness)
cv.imshow("Contours", bw2)

edges = cv.Canny(bw, 15, 5)
cv.imshow("Canny Edges", edges)

# May be useful to deal with dust on the record. But we should probably clean them ahead of time.
sub = thresh_adapt - edges
cv.imshow("Subtract Test", sub)

cv.waitKey(0)
cv.destroyAllWindows()