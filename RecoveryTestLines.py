from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
import Detection
import Conversion
import Data


n_bins = 30
inclusion_threshold = 750

lines = cv.imread('ss_line_bin.tif', cv.IMREAD_GRAYSCALE)
plt.figure('Image to Process'), plt.imshow(lines, cmap='gray')

height, width = lines.shape

points = list()

for x in range(0, width-1):
    for y in range(0, height-1):
        if lines[y, x] == 0:
            points.append(Data.Point(x, height - y))

plt.figure('Raw Data'), plt.scatter(Data.x_in_points(points), Data.y_in_points(points), s=0.2)

average = Detection.average_points(points)

plt.figure('Averaged Data'), plt.scatter(Data.x_in_points(average), Data.y_in_points(average), s=0.2), plt.show()

plt.show()

stylus = Conversion.Stylus()

grooves = Detection.points_to_grooves(hist, bin_edges, inclusion_threshold, Data.points_to_tuples(points))

for i, groove in enumerate(grooves):
    plt.scatter(groove.get_theta_axis(), groove.get_rho_axis(), s=0.2), plt.show()
    # irregular_audio.append(Conversion.Stylus(groove, i + 1))
