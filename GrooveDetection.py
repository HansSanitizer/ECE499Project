""" Groove Detection:

    These functions are for detecting grooves on a record.
    The order of the functions in this file is the order of
    expected use.

    These functions implement second (third? maybe formalize this first...)
    stage processing. That is, groove data is produced from image data and
    a known center point.
"""
import cv2 as cv
import numpy as np


class Groove:

    def __init__(self, angular_data=list(), next_groove=None, last_groove=None):

        self.angular_data = list()
        self.angular_data.append(angular_data)
        self.next_groove = next_groove
        self.last_groove = last_groove


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

    element = cv.getStructuringElement(cv.MORPH_CROSS, (3, 3))
    done = False
    size = np.size(image)
    skeleton = np.zeros(image.shape, np.uint8)

    while not done:
        eroded = cv.erode(thresh_adapt_copy, element)
        temp = cv.dilate(eroded, element)
        temp = cv.subtract(thresh_adapt_copy, temp)
        skeleton = cv.bitwise_or(skeleton, temp)
        thresh_adapt_copy = eroded.copy()

        zeros = size - cv.countNonZero(thresh_adapt_copy)
        if zeros == size:
            done = True

    indices = np.were(skeleton > [0])
    return indices


""" I want this to return a list of tuples (rho, theta), but I don't care
    about sorting yet.
"""
def skeleton_to_points(indices, center):

    x = indices[1][0] - center[0]
    y = center[1] - indices[0][0]
    contours_points = np.array([x, y])
    rho = np.sqrt(x ** 2 + y ** 2)
    theta = np.arctan2(y, x)

    if theta < 0:
        theta = theta + 2 * np.pi
    print(len(indices[:]))
    contours_theta_rho = np.array([theta, rho])

    for i in range(1, len(indices[0])):
        x = indices[1][i] - center[0]
        y = center[1] - indices[0][i]
        rho = np.sqrt(x ** 2 + y ** 2)
        theta = (np.arctan2(y, x))
        if theta < 0:
            theta = theta + 2 * np.pi
        # why not b.append([theta, rho]) or b.append((theta,rho))
        b = np.array([theta, rho])                                              # [[theta,rho]]
        contours_theta_rho = np.column_stack((contours_theta_rho.T, b)).T
        b = np.array([x, y])
        contours_points = np.column_stack((contours_points.T, b)).T

    # I'm not convinced that sorting is necessary yet.
    # Now I am. But I need it sorted by radius.
    # Why lex sort? Isn't this numeric data?
    contours_theta_rho_sorted = np.lexsort((contours_theta_rho[:, 1], contours_theta_rho[:, 0]))
    contours_theta_rho_sorted = contours_theta_rho[contours_theta_rho_sorted]
    return contours_theta_rho_sorted


def points_histogram(rho):

    """ I'm not sure what the best method of bin sizing is yet. """

    histogram, bin_edges = np.histogram(rho, bins="fd")

    return histogram, bin_edges


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

        There are going to be so many searches...

        I'm assuming that points is a list of tuples (rho, theta) sorted from max to min rho.
        But I'm not going to hack up skeleton_to_points yet.

    """

    grooves = list()
    points_temp = list()
    last_bin_valid = False

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
            index_min_rho = points.index((bin_edge_min,))
            """ Handling special case of final bin being [ ] (opposed to [ ) for
                other bins.
            """
            if histogram_bin != len(histogram):
                index_max_rho = points.index((bin_edge_max,))-1
            else:
                index_max_rho = points.index((bin_edge_max,))

            points_temp.append(points[index_min_rho:index_max_rho])

        """ If the current bin is invalid, and the last bin was valid, then
            we've collected the points in a groove.
            
            To do: handle linking. (if necessary, the order in the list is
            probably a sufficient way to deal with linking)
        """
        if this_bin_valid is False and last_bin_valid is True:
            grooves.append(Groove(points_temp, None, None))
            points_temp = list()

        last_bin_valid = this_bin_valid

    return grooves

