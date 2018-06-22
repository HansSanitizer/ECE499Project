from matplotlib import pyplot as plt
import cv2 as cv
print(cv.__version__)
import numpy as np
bw = cv.imread('Images/ymmly2.jpg', cv.IMREAD_GRAYSCALE)
plt.imshow(bw, cmap='gray'), plt.show()

# IF THIS NEXT LINE CAUSES TROUBLE, JUST REMOVE IT, IT IS SUPPOSED TO SPEED THINGS UP USING OPENCL
# REFLINK: https://www.learnopencv.com/opencv-transparent-api/
bwUmat = cv.UMat(bw)
height, width = bw.shape
print("The original image height is ", height)
print("The original image width is ", width)
black = np.zeros(bw.shape, np.uint8)
# bwCircle = bw.copy()
# bwCircleUmat = cv.UMat(bwCircle)
# bwCircleBlurred = cv.UMat.get(cv.medianBlur(bwCircleUmat, 15))
# # plt.imshow(bwCircle),plt.show()
# print("Blurred image for circle finding")
# rows = bwCircle.shape[0]
#
# # Find the small circle (minima of region of interest, also better for center of record determination)
# circles = cv.HoughCircles(bwCircleBlurred, cv.HOUGH_GRADIENT,
#                           1, rows/8, param1=90, param2=50,
#                           minRadius=int(1600), maxRadius=int(1800))
# if circles is None:
#     print("Found 0 Circles")
# else:
#     circles = np.uint16(np.around(circles))
#     for i in circles[0, :]:
#         centerSmall = (i[0], i[1])
#         #
#         radiusSmall = i[2] + 800
#         # Draw the center of the circle
#         cv.circle(bw, centerSmall, 1, (0, 100, 100), 50)
#         # Draw the roi on a black image
#         cv.circle(black, centerSmall, (radiusSmall + 1000), (255,255,255), 20)
#         cv.circle(black, centerSmall, (radiusSmall + 1100), (255,255,255), 20)
#         # Draw the circle found on the original image
#         cv.circle(bw, centerSmall, radiusSmall, (255, 0, 255), 50)
#         print("Detected Small Circle", i)

# Pre-determined magic numbers, see above for attempted method
centerSmall = (6790, 8775)
radiusSmall = 10000 - 6790


plt.imshow(bw, cmap='gray'), plt.show()
plt.imshow(black, cmap='gray'), plt.show()
print("Record Center(x, y) is: ", centerSmall)

black2 = np.zeros(bw.shape, np.uint8)
circOut = cv.circle(black2, centerSmall, (radiusSmall + 3100), (255, 255, 255), -1)
circIn = cv.circle(black2, centerSmall, (radiusSmall + 3000), (0, 0, 0), -1)
fin = cv.bitwise_and(bw, black2)
# plt.imshow(fin, cmap='gray'), plt.show()

# Apply Threshold and detect contours
thresh_adapt = cv.adaptiveThreshold(fin, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 45, 0)
im2, contours, hierarchy = cv.findContours(thresh_adapt, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
print("Detected number of contours:")
print(len(contours))

# Find largest contour
largestArea = 0
for i in range(0, len(contours)):
    a = cv.contourArea(contours[i])
    if a > largestArea:
        # print("Found a larger contour:")
        print(a)
        largestArea = a
        largest_contour_index = i
        bounding_rect = cv.boundingRect(contours[i])
    # else:
        # print("didn't work")
print("Found largest contour:")
print(largestArea)
print("Largest contour was at index:")
print(i)
cv.drawContours(fin, contours[i], -1, (255,255,255), 1)
plt.imshow(fin), plt.show()
print("Contour Contents:")
print(contours[i])
# Try canny edge detection as a method instead

edges = cv.Canny(fin, 100, 255)
plt.imshow(edges, cmap='gray'), plt.show()

# thresh_adapt = cv.adaptiveThreshold(bw, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 45, 0)
# im2, contours, hierarchy = cv.findContours(thresh_adapt, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
# print(len(contours))
# black = np.zeros(bw.shape, np.uint8)
# cv.drawContours(black, contours, -1, (255, 255, 255), 50)
# plt.imshow(bw), plt.show()
