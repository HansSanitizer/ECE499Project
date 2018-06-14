from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np

# Open scanned image

bw = cv.imread('Images/4800dpitest.jpg', cv.IMREAD_GRAYSCALE)
height, width = bw.shape
print("The original image height is ", height)
print("The original image width is ", width)



bwCircle = bw.copy()
bwCircle = cv.medianBlur(bwCircle, 15)
# plt.imshow(bwCircle),plt.show()
print("Blurred image for circle finding")
rows = bwCircle.shape[0]

# Find the small circle (minima of region of interest, also better for center of record determination)
circles = cv.HoughCircles(bwCircle, cv.HOUGH_GRADIENT,
                          1, rows/8, param1=80, param2=30,
                          minRadius=int(1600), maxRadius=int(1800))
if circles is None:
    print("Found 0 Circles")
else:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        centerSmall = (i[0], i[1])
        #
        radiusSmall = i[2] + 800
        # Draw the center of the circle
        cv.circle(bw, centerSmall, 1, (0, 100, 100), 50)
        # Draw the circle
        cv.circle(bw, centerSmall, radiusSmall, (255, 0, 255), 50)
        print("Detected Small Circle", i)

plt.imshow(bw, cmap=None), plt.show()
 # For now it appears as though the small circle produced a more center of record result, will change large circle to
 # match

# Find the large circle (maxima of region of interest)
circles = cv.HoughCircles(bwCircle, cv.HOUGH_GRADIENT,
                          1, rows/8, param1=80, param2=30,
                          minRadius=int(5700), maxRadius=int(6000))
if circles is None:
    print("Found 0 Circles")
else:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        centerLarge = (i[0], i[1])
        radiusLarge = i[2] - 100
        # Draw the center of the circle
        cv.circle(bw, centerSmall, 1, (0, 100, 100), 50)
        # Draw the circle
        cv.circle(bw, centerSmall, radiusLarge, (255, 0, 255), 50)
        print("Detected Large Circle", i)

plt.imshow(bw, cmap=None), plt.show()
print("Record Center(x, y) is: ", centerSmall)

# Take Eights of the image from centerSmall to outer edge
class vyLine:
    def __init__(self, p1x, p1y, p2x, p2y):
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y


#Taken from 0 degrees counter clockwise
lineOne = vyLine(centerSmall[0] + radiusSmall, centerSmall[1], centerSmall[0] + radiusLarge, centerSmall[1])


cv.line(bw, (lineOne.p1x, lineOne.p1y), (lineOne.p2x, lineOne.p2y),
        (255, 0, 255), 50)

plt.imshow(bw, cmap=None), plt.show()









# 6153,5827 is approximate center (x,y)
#
# # Take a quarter of the image
# bwQ1 = bw[0:11705, 5827:11655]
# plt.imshow(bwQ1), plt.show()
# plt.imshow(bw), plt.show()
# thresh_adapt = cv.adaptiveThreshold(bwQ1, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 45, 0)
# # cv.imshow("Adaptive Threshold", thresh_adapt)
# print("adaptive threshold complete")
# _, contours, heirarchy = cv.findContours(thresh_adapt, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# print("finding contours complete")
# bwQ1_2 = bwQ1.copy()
# index = -1
# thickness = 1
# color = (255, 0, 255)
#
# #Find largest contour
# largestArea = 0
# for i in range(0, contours.size()):
#     a = cv.contourArea(contours[i])
#     if a > largestArea:
#         largestArea = a
#         largest_contour_index = i
#         bounding_rect = cv.boundingRect(contours[i])
# print("Found largest contour")
#
#
# # Draw found contours
# cv.drawContours(bwQ1_2, contours[i], index, color, thickness)
# print("made it past drawContours")
#
# # Display contours on top of vinyl
# plt.imshow(bwQ1_2), plt.show()
#
# cv.waitKey(0)
# cv.destroyAllWindows()
