from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
bw = cv.imread('Images/4800crop0.png', cv.IMREAD_GRAYSCALE)
height, width = bw.shape
print("The height is %d", height)
print("The width is %d", width)
# Find the large circle (maxima of region of interest)
bwCircle = bw.copy()
bwCircle = cv.medianBlur(bwCircle, 15)
# plt.imshow(bwCircle),plt.show()
print("Blurred image for circle finding")
rows = bwCircle.shape[0]
circles = cv.HoughCircles(bwCircle, cv.HOUGH_GRADIENT,
                          1, rows/8, param1=80, param2=30,
                          minRadius=int(width/2 - 100), maxRadius=int(width/2))
if circles is None:
    print("Found 0 Circles")
else:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        radius = i[2]
        cv.circle(bwCircle, center, 1, (0, 100, 100), 50)
        cv.circle(bwCircle, center, radius, (255, 0, 255), 50)
        print("Detected Circle", i)
        plt.imshow(bwCircle, cmap=None), plt.show()
        cv.waitKey(0)

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
