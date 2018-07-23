from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
import Detection
import Conversion


bw = cv.imread('scb.tif', cv.IMREAD_GRAYSCALE)
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
# plt.imshow(fin), plt.show()

indices = np.where(fin > [0])

# I need Jared to explain wht this is doing. I have no idea how it knows its following data.
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

#plt.scatter([point[1] for point in points], [point[0] for point in points], s=0.2)
#plt.show()

# Ignoring the distorted (?) regions.
#points_truncated = [point for point in points if 2 <= point[1] <= 4.5 and point[0] > 3105]
#plt.scatter([point[1] for point in points_truncated], [point[0] for point in points_truncated], s=0.2)
#plt.show()

h, bin_edges = Detection.points_histogram([point[0] for point in points_truncated])
#plt.hist([point[0] for point in points_truncated], bin_edges)
#plt.show()

# To do: the inclusion threshold would be a good thing to expose to the user
grooves = Detection.points_to_grooves(h, bin_edges, 1000, points_truncated)

irregular_audio = Conversion.Stylus()

for i, groove in enumerate(grooves):
    #plt.scatter(groove.get_theta_axis(), groove.get_rho_axis(), s=0.2), plt.show()
    irregular_audio.append(Conversion.Stylus(groove, i + 1))

# print("Max Gap: " + str(irregular_audio.get_max_gap()))
plt.scatter(range(len(irregular_audio.data)), irregular_audio.data, s=0.2), plt.show()

# audio = DataConversion.Audio(48000, irregular_audio)
# plt.scatter([i for i in range(len(audio.data))], audio.data, s=0.2), plt.show()

Conversion.audio_to_wave(irregular_audio.data)
