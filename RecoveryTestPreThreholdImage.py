from matplotlib import pyplot as plt
import cv2 as cv
print(cv.__version__)
import numpy as np
import GrooveDetection
import DataConversion

bw = cv.imread('Images/tbcfc2ThreshTest.tif', cv.IMREAD_GRAYSCALE)
#plt.imshow(bw, cmap='gray'), plt.show()

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
plt.imshow(fin), plt.show()

indices = np.where(fin > [0])

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

h, bin_edges = GrooveDetection.points_histogram([point[0] for point in points_truncated])
#plt.hist([point[0] for point in points_truncated], bin_edges)
#plt.show()

# To do: the inclusion threshold would be a good thing to expose to the user
grooves = GrooveDetection.points_to_grooves(h, bin_edges, 1000, points_truncated)

for groove in grooves:
    plt.scatter(groove.get_theta_axis(), groove.get_rho_axis(), s=0.2)
    plt.show()
    irregular_audio = DataConversion.IrregularAudio(groove)
    audio = DataConversion.Audio(irregular_audio)
    plt.scatter(audio.get_time_axis(), audio.get_amplitude_axis(), s=0.2)
    plt.show()
