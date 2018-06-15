from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
print(cv.getBuildInformation())
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

# plt.imshow(bw, cmap=None), plt.show()
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

# plt.imshow(bw, cmap=None), plt.show()
print("Record Center(x, y) is: ", centerSmall)

# Take Eights of the image from centerSmall to outer edge
class vyLine:
    def __init__(self, p1x, p1y, p2x, p2y):
        self.p1x = p1x
        self.p1y = p1y
        self.p2x = p2x
        self.p2y = p2y

# Define the number of lines (segments*2) that you want to create
numLines = 48
recordLine = [0]*numLines
vinylROI = [0]*numLines
# Mask creation for finding ROI
black = np.zeros(bw.shape, np.uint8)
black2 = np.zeros(bw.shape, np.uint8)
cv.circle(black, centerSmall, radiusSmall, (255, 255, 255), 50)
cv.circle(black, centerLarge, radiusLarge, (255, 255, 255), 50)
# for x in range(0, (numLines - 1)):
x=0
recordLine[x] = vyLine(int(centerSmall[0] + radiusSmall * np.cos(x * np.pi / (numLines/2))),
                       int(centerSmall[1] - radiusSmall * np.sin(x * np.pi / (numLines/2))),
                       int(centerSmall[0] + radiusLarge * np.cos(x * np.pi / (numLines/2))),
                       int(centerSmall[1] - radiusLarge * np.sin(x * np.pi / (numLines/2))))
recordLine[x + 1] = vyLine(int(centerSmall[0] + radiusSmall * np.cos((x+1) * np.pi / (numLines/2))),
                       int(centerSmall[1] - radiusSmall * np.sin((x+1) * np.pi / (numLines/2))),
                       int(centerSmall[0] + radiusLarge * np.cos((x+1) * np.pi / (numLines/2))),
                       int(centerSmall[1] - radiusLarge * np.sin((x+1) * np.pi / (numLines/2))))
cv.line(black,
        (recordLine[x].p1x, recordLine[x].p1y),
        (recordLine[x].p2x, recordLine[x].p2y),
        (255, 255, 255), 50)
cv.line(black,
        (recordLine[x + 1].p1x, recordLine[x + 1].p1y),
        (recordLine[x + 1].p2x, recordLine[x + 1].p2y),
        (255, 255, 255), 50)
thresh_adapt = cv.adaptiveThreshold(black, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 45, 0)
im2, contours, hierarchy = cv.findContours(black, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(black2, contours, 1, (255,255,255), 50)
plt.imshow(black2), plt.show()
print(cv.contourArea(contours[1]))

# Find smallest roi contour (probably is a more elegant way to do this)
print(hierarchy)
print(type(contours))
print(len(contours))

vinylROI[x] = max(contours, key=cv.contourArea)
black2 = np.zeros(bw.shape, np.uint8)
cv.drawContours(black2, vinylROI[x], 0, (255,255,225), 50)
plt.imshow(black2), plt.show()
# #Find largest contour
# largestArea = 0
# for i in range(0, contours.size()):
#     a = cv.contourArea(contours[i])
#     if a > largestArea:
#         largestArea = a
#         largest_contour_index = i
#         bounding_rect = cv.boundingRect(contours[i])
# print("Found largest contour")






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
