from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np
import Detection
import Conversion
import Data

n_bins = 30
inclusion_threshold = 750
pixel_width = 2.2*10**-6
pixel_height = 2.3*10**-6
magnification = 200
pixel_dimensions_m = (pixel_width/magnification, pixel_height/magnification)
y_displacement_m = 120.65 * 10 ** -3
arc_length_m = 2*np.pi*y_displacement_m
y_displacement_pixels = int(y_displacement_m / pixel_dimensions_m[1])

lines = cv.imread('ss_line_bin.tif', cv.IMREAD_GRAYSCALE)
#plt.figure('Image to Process'), plt.imshow(lines, cmap='gray')

height, width = lines.shape

points_pixel = list()

for x in range(0, width-1):
    for y in range(0, height-1):
        if lines[y, x] == 0:
            points_pixel.append(Data.Point(x, height - y + y_displacement_pixels))

plt.figure('Raw Data'), plt.scatter(Data.x_in_points(points_pixel), Data.y_in_points(points_pixel), s=0.2)

good_points = Data.discard_bad_pairs(points_pixel, pixel_dimensions_m)

average = Data.average_points(good_points)

points_rtime = Data.pixel_to_rtime(average, pixel_dimensions_m)

plt.figure('Radius Time Data'), plt.xlabel('t [s]'), plt.ylabel('r [m]'), plt.grid(True),\
    plt.scatter(Data.t_in_points(points_rtime), Data.r_in_points(points_rtime), s=0.2)

plt.show()

stylus = Conversion.Stylus(average)

plt.figure('Velocity ?'), plt.xlabel('t [s]'), plt.ylabel('v [m/s]'), \
    plt.grid(True), plt.scatter(stylus.get_time_axis(), stylus.get_velocity_axis(), s=0.2)

grooves = Detection.points_to_grooves(hist, bin_edges, inclusion_threshold, Data.points_to_tuples(points_pixel))

for i, groove in enumerate(grooves):
    plt.scatter(groove.get_theta_axis(), groove.get_rho_axis(), s=0.2), plt.show()
    # irregular_audio.append(Conversion.Stylus(groove, i + 1))
