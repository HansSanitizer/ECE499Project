from matplotlib import pyplot as plt
import cv2 as cv
import numpy as np


class Circle:

    def __init__(self, center=(1,1), radius=1):
        self.center = center
        self.radius = radius
        self.area = np.pi*radius**2


print("Locating center of the record...")

bw = cv.imread('ymmly1.jpg', cv.IMREAD_GRAYSCALE)       # Note what image this is!

# Enhance edges
# parameters are all magic numbers
print("Applying filter...")
filter_window_size = 5
filter_colour_smear = 175
filter_range_smear = 175
bilateral_filtered_image = cv.bilateralFilter(bw, filter_window_size, filter_colour_smear, filter_range_smear)

# Detect edges
# Threshold is low due to shadows obscuring the edges of the centre radius.
print("Detecting edges...")
edge_thresh_min = 10
edge_thresh_max = 50
edges = cv.Canny(bilateral_filtered_image, edge_thresh_min, edge_thresh_max)

# Find contours
print("Finding contours...")
_, contours, _ = cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Find circles
# Note that min_area = 200 eliminated a lot of the dust.
# This is probably keeping some small contours because they self intersect. How detect self intersection?
print("Finding circle candidates...")
contours_circle_candidates = list()
min_area = 270      # This might be too low for practical reasons.
max_area = 700
for contour in contours:
    approx = cv.approxPolyDP(contour,0.01*cv.arcLength(contour, True), True)
    area = cv.contourArea(contour)
    if (len(approx) > 8) & (area > min_area) & (area < max_area):
        contours_circle_candidates.append(contour)
print("Number of candidates found: " + str(len(contours_circle_candidates)))

# Enclose candidate contours with circles
print("Enclosing candidates with circles...")
circles = list()
for contour in contours_circle_candidates:
    (x, y), rho = cv.minEnclosingCircle(contour)
    circles.append(Circle((int(x), int(y)), rho))
    # print("Radius: " + str(rho) + "  Center: " + str((x, y)))

# Find the best candidate for inner radius
print("Finding best candidate for inner radius...")
best_circle = Circle()
best_dif = 1
expected_area = 176460            # 1.658 cm (I guess) in pixels (I guess?)
area_tolerance = 0.05             # tolerance of five percent
for circle in circles:
    dif = np.abs(expected_area-circle.area)/expected_area
    if (dif < area_tolerance) & (dif < best_dif):
        best_circle = circle
        best_dif = dif
print("Best candidate for inner radius is " + str(best_circle.radius) + " " + str(best_circle.center))

# Results
print("Showing results...")
font = cv.FONT_HERSHEY_SIMPLEX
cv.drawContours(bw, contours_circle_candidates, -1, (255, 0, 0), 2)
for circle in circles:
    cv.circle(bw, circle.center, int(circle.radius), (0, 0, 255), -1)
    cv.putText(bw, str(circle.radius), circle.center, font, 4, (255, 255, 255), 2, cv.LINE_AA)
plt.imshow(bw)
plt.show()
print("The center is located at " + str(best_circle.center))
