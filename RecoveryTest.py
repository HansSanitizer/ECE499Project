from matplotlib import pyplot as plt
import cv2 as cv
print(cv.__version__)
import numpy as np
import Detection

bw = cv.imread('tbcfc2.jpg', cv.IMREAD_GRAYSCALE)
#plt.imshow(bw, cmap='gray'), plt.show()

# IF THIS NEXT LINE CAUSES TROUBLE, JUST REMOVE IT, IT IS SUPPOSED TO SPEED THINGS UP USING OPENCL
# REFLINK: https://www.learnopencv.com/opencv-transparent-api/
bwUmat = cv.UMat(bw)
height, width = bw.shape
print("The original image height is ", height)
print("The original image width is ", width)
black = np.zeros(bw.shape, np.uint8)
retval, dst = cv.threshold(bw, 45, 255, cv.THRESH_BINARY)
# plt.imshow(dst), plt.show()

centerSmall = (7330, 5832)
#centerSmall = (8765, 6782)
radiusSmall = 2100

print("Record Center(x, y) is: ", centerSmall)
black2 = np.zeros(bw.shape, np.uint8)
circOut = cv.circle(black2, centerSmall, (radiusSmall + 1100), (255, 255, 255), -1)
circIn = cv.circle(black2, centerSmall, (radiusSmall + 1000), (0, 0, 0), -1)
fin = cv.bitwise_and(bw, black2)
#plt.imshow(fin), plt.show()

# Apply Threshold and detect contours
thresh_adapt = cv.adaptiveThreshold(fin, 80, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 57, 0)
plt.imshow(thresh_adapt), plt.show()

thresh_adapt_copy = thresh_adapt
element = cv.getStructuringElement(cv.MORPH_CROSS,(3,3))
done = False
size = np.size(bw)
skel = np.zeros(bw.shape,np.uint8)
while not done:
    eroded = cv.erode(thresh_adapt_copy,element)
    temp = cv.dilate(eroded,element)
    temp = cv.subtract(thresh_adapt_copy,temp)
    skel = cv.bitwise_or(skel,temp)
    thresh_adapt_copy = eroded.copy()

    zeros = size - cv.countNonZero(thresh_adapt_copy)
    if zeros==size:
        done = True

plt.imshow(skel), plt.show()
# Need to convert skel to xy locations, rather than rows and columns of intensity values,
# where rows and column index's are positions
indices = np.where(skel > [0])

rhos = list()
points = list()
x = indices[1][0] - centerSmall[0]
y = centerSmall[1] - indices[0][1]
contoursXY = np.array([x, y])
rho = np.sqrt(x**2 + y**2)
theta = np.arctan2(y, x)
if theta < 0:
    theta = theta + 2*np.pi
print(len(indices[:]))
contoursThetaRho = np.array([theta, rho])
print("Printing Theta Rho:")
print(contoursThetaRho)
for i in range(1, len(indices[0])):
    x = indices[1][i] - centerSmall[0]
    y = centerSmall[1] - indices[0][i]
    rho = np.sqrt(x**2 + y**2)
    theta = (np.arctan2(y, x))
    if theta < 0:
        theta = theta + 2*np.pi
    points.append((rho, theta))

plt.scatter([point[1] for point in points], [point[0] for point in points], s=0.2)
plt.show()

# Ignoring the distorted (?) regions.
points_truncated = [point for point in points if 2 <= point[1] <= 4.5 and point[0] > 3105]
#plt.scatter([point[1] for point in points_truncated], [point[0] for point in points_truncated], s=0.2)
#plt.show()

h, bin_edges = Detection.points_histogram([point[0] for point in points_truncated])
#plt.hist([point[0] for point in points_truncated], bin_edges)
#plt.show()

# To do: the inclusion threshold would be a good thing to expose to the user
grooves = Detection.points_to_grooves(h, bin_edges, 1000, points_truncated)

for groove in grooves:
    plt.scatter(groove.get_theta_axis(), groove.get_rho_axis(), s=0.2)
    plt.show()
