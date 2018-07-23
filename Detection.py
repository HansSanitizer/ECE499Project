""" Groove Detection:

    These functions are for detecting grooves on a record.
    The order of the functions in this file is the order of
    expected use.

    Groove data is produced from image data and
    a known center point.
"""
import cv2 as cv
import numpy as np
import pandas as pd
import operator
import Data



class Groove:

    def __init__(self, angular_data=list(), next_groove=None, last_groove=None):

        self.angular_data = angular_data
        best_fit = np.polyfit(self.get_theta_axis(), self.get_rho_axis(), 1)
        self.slope = best_fit[0]
        self.next_groove = next_groove
        self.last_groove = last_groove

    def get_theta_axis(self):

        return [point[0] for point in self.angular_data]

    def get_rho_axis(self):

        return [point[1] for point in self.angular_data]


def load_grey_scale(path):

    bw = cv.imread(path, cv.IMREAD_GRAYSCALE)

    return bw


def slice_image(image, center, inner_radius, outer_slice_radius, inner_slice_radius):

    black2 = np.zeros(image.shape, np.uint8)
    cv.circle(black2, center, (inner_radius + outer_slice_radius), (255, 255, 255), -1)
    cv.circle(black2, center, (inner_radius + inner_slice_radius), (0, 0, 0), -1)
    return cv.bitwise_and(image, black2)


def apply_threshold(image):

    image_threshold = cv.adaptiveThreshold(image, 80, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 57, 0)

    return image_threshold


def image_to_skeleton(image):

    element = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
    done = False
    size = np.size(image)
    skeleton = np.zeros(image.shape, np.uint8)

    while not done:
        eroded = cv.erode(image, element)
        temp = cv.dilate(eroded, element)
        temp = cv.subtract(image, temp)
        skeleton = cv.bitwise_or(skeleton, temp)
        image = eroded.copy()

        zeros = size - cv.countNonZero(image)
        if zeros == size:
            done = True

    indices = np.where(skeleton > [0])

    return indices


""" I want this to return a list of tuples (rho, theta), and I don't care about sorting.

    Not doing the sort here really sped things up. (That needs to be implemented here. It's in the
    test script)
"""
def skeleton_to_points(indices, center):

    points = list()
    x = indices[1][0] - centerSmall[0]
    y = centerSmall[1] - indices[0][1]
    rho = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)
    if theta < 0:
        theta = theta + 2 * np.pi
    print(len(indices[:]))
    contoursThetaRho = np.array([theta, rho])
    print("Printing Theta Rho:")
    print(contoursThetaRho)
    for i in range(1, len(indices[0])):
        x = indices[1][i] - centerSmall[0]
        y = centerSmall[1] - indices[0][i]
        rho = np.sqrt(x ** 2 + y ** 2)
        theta = (np.arctan2(y, x))
        if theta < 0:
            theta = theta + 2 * np.pi
        points.append((rho, theta))

    return points


def average_points(points=list(), window_size=20):

    x = Data.x_in_points(points)
    y = Data.y_in_points(points)

    d = pd.DataFrame({'x': x, 'y': y})
    averaged_d = d.rolling(window_size).mean()

    x = averaged_d['x'].values.tolist()
    y = averaged_d['y'].values.tolist()

    averaged_points = [Data.Point(x[i], y[i]) for i in range(len(d))]

    return averaged_points


def points_to_grooves(histogram, bin_edges, inclusion_threshold, points=list()):

    """ The histogram tells us the distribution of points in the data set.
        The more points in a bin, the more likely that there's a groove in the bin.

        Moving through the histogram array backwards, check if the bin meets the
        inclusion threshold. If the bin meets the inclusion threshold, then
        take the points in that bin, and instantiate a Groove object.

        Inclusion threshold will depend on bin sizing. This could support adding points
        from multiple bins. For example, find a bin that meets inclusion and keep including
        bins until the inclusion threshold isn't met anymore.

        h: [30, 291, 546, ...]
        bin_edges: [-3.20, -1.83, -0.45, ..]
        bin_0 contains 30 values and it spans [-3.20, -1.83) (last bin is [])

        I'm assuming that points is a list of tuples (rho, theta) sorted from max to min rho.
        But I'm not going to hack up skeleton_to_points yet.

        This might be improved by tacking the bin that proceed the first valid on. There's a kind of cut-off
        going on right now.
    """

    grooves = list()
    points_temp = list()
    last_bin_valid = False

    # it might be worth checking for duplicates (not sure it's possible, but a check might be worth it)

    """ This for loop is currently running in the wrong direction.
        This was done on purpose. (I didn't want to think about the
        problem backwards yet)
    """
    for histogram_bin in range(len(histogram)):

        this_bin_valid = False

        if histogram[histogram_bin] > inclusion_threshold:

            this_bin_valid = True
            bin_edge_min = bin_edges[histogram_bin]
            bin_edge_max = bin_edges[histogram_bin + 1]

            """ Handling special case of final bin being [ ] (opposed to [ ) for
                other bins.
                
                This will go through the entire list. Might be worth finding a better way.
            """
            if histogram_bin != len(histogram):
                [points_temp.append(point) for point in points if (bin_edge_min <= point[1] < bin_edge_max)]
            else:
                [points_temp.append(point) for point in points if (bin_edge_min <= point[1] <= bin_edge_max)]

        """ If the current bin is invalid, and the last bin was valid, then
            we've collected the points in a groove.

            To do: handle linking. (if necessary, the order in the list is
            probably a sufficient way to deal with linking). Handling this here
            might deal with that "I did it backwards" thing.
        """
        if this_bin_valid is False and last_bin_valid is True:

            # I'm not convinced that rejecting outliers is useful.
            #points_temp = points_reject_rho_outliers(points_temp, m=3)
            #points_temp = points_reject_theta_outliers(points_temp)

            # Sort by radius in order of increasing angle.
            points_temp.sort(key=operator.itemgetter(1))

            grooves.append(Groove(points_temp, None, None))
            points_temp = list()

        last_bin_valid = this_bin_valid

    if len(grooves) == 0:
        raise RuntimeError('no grooves were found, try adjusting the inclusion threshold and number of bins used.')

    return grooves


def points_reject_rho_outliers(data, m=2):
    rhos = [point[0] for point in data]
    median = np.median(rhos)
    d = [np.abs(rho - median) for rho in rhos]
    median_d = np.median(d)
    s = d/median_d if median_d else 0
    return [point for i, point in enumerate(data) if s[i] < m]


def points_reject_theta_outliers(data, m=2):
    thetas = [point[1] for point in data]
    median = np.median(thetas)
    d = [np.abs(theta - median) for theta in thetas]
    median_d = np.median(d)
    s = d/median_d if median_d else 0
    return [point for i, point in enumerate(data) if s[i] < m]
