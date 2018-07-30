import numpy as np
import pandas as pd
import scipy.optimize as optimize


class PointRect:

    def __init__(self, x=0, y=0):
        """

        Container for rectangular data points.

        :param x: x coordinate
        :param y: y coordinate
        """

        self.x = x
        self.y = y


class PointAngular:

    def __init__(self, r=0, theta=0):
        """

        Container for angular data points.

        :param r: radius coordinate
        :param theta: theta coordinate
        """

        self.r = r
        self.theta = theta


class PointRtime:

    def __init__(self, r=0, t=0):
        """

        Container for time-radius data points.
        (Why is it called R-time instead of T-radius? Because it sounded better.)

        :param r: radius coordinate
        :param t: time coordinate
        """

        self.r = r
        self.t = t


def get_x_axis(points=list()):
    """

    For a list of point objects, return the x-axis.

    :param points: list of rectangular points
    :return: list of x-axis coordinates
    """
    return [point.x for point in points]


def get_y_axis(points=list()):
    """

    For a list of point objects, return y-axis.

    :param points: list of rectangular points
    :return: list of y-axis coordinates
    """
    return [point.y for point in points]


def get_r_axis(points=list()):
    """

    For a list of point objects, return r-axis.

    :param points: list of angular or r-time points
    :return: list of r-axis values
    """
    return [point.r for point in points]


def get_theta_axis(points=list()):
    """

    For a list of point objects, return theta-axis.

    :param points: list of angular points
    :return: list of theta-axis values
    """
    return [point.theta for point in points]


def get_t_axis(points=list()):
    """

    For a list of point objects, return t-axis.

    :param points: list of r-time points
    :return: list of t-ais values.
    """
    return [point.t for point in points]


def average_points(points=list(), window_width=20):
    """

    Performs a rolling average of points in a 2D list.

    :param points: 2D data set
    :param window_width: width of averaging window
    :return:
    """

    x = get_x_axis(points)
    y = get_y_axis(points)

    d = pd.DataFrame({'x': x, 'y': y})
    averaged_d = d.rolling(window_width).mean()

    x = averaged_d['x'].values.tolist()
    y = averaged_d['y'].values.tolist()

    averaged_points = [PointRect(x[i], y[i]) for i in range(window_width, len(d))]

    return averaged_points


def get_unique(data):
    """

    Returns unique elements of a list.

    :param data: list of data
    :return: unique elements of data
    """

    seen = set()
    unique = list()

    for x in data:
        if x not in seen:
            unique.append(x)
            seen.add(x)

    return unique


def rectangular_to_angular(points, pixel_dimensions):
    """

    Converts points in rectangular (pixel) coordinates to real-space (meters) angular coordinates.

    To do: theta_last calculation isn't entirely accurate. The radius at the end points of the arc
    are subtly different, and I'm not sure if the diff in x coord translates to arc length.

    :param points: list of rectangular points
    :param pixel_dimensions: tuple of form (width, height) in meters
    :return: list of angular points
    """

    points_angular = list()

    x_last = 0
    theta_last = 0

    for point in points:

        x_new = point.x * pixel_dimensions[0]
        y = point.y * pixel_dimensions[1]
        r = np.sqrt(x_new**2 + y**2)
        theta_new = theta_last + (x_new - x_last)/r
        points_angular.append(PointAngular(r, theta_new))
        x_last = x_new
        theta_last = theta_new

    return points_angular


def angular_to_rtime(points_angular, angular_velocity):
    """

    Converts points in real-space (meters) angular coordinates to the r-time coordinate system.

    :param points_angular: list of angular points
    :param angular_velocity: angular velocity of rotation of the record
    :return: list of points in r-time coordinates
    """

    points_rtime = list()
    t = 0
    theta_last = 0

    for point in points_angular:

        dtheta = point.theta - theta_last
        t = t + dtheta / angular_velocity
        points_rtime.append(PointRtime(point.r, t))
        theta_last = point.theta

    return points_rtime


def get_pairs(points):
    """

    Returns pairs (along the x-axis) of points. If a point is a lone occurrence, then a corresponding point
    is generated so that averaging works out. This is non-ideal; there is no way to know if the lone point
    was valid.

    :param points: list of rectangular points
    :return: pairs of rectangular points
    """

    unique_x = get_unique(get_x_axis(points))
    x_axis = get_x_axis(points)
    pairs = list()

    for x in unique_x:

        occurrences = x_axis.count(x)

        if occurrences == 1:
            point = points.pop(0)
            pairs.append((point, point))
        elif occurrences == 2:
            point_1 = points.pop(0)
            point_2 = points.pop(0)
            if point_1.x == point_2.x:
                pairs.append((point_1, point_2))
        elif occurrences > 2:
            point_1 = points.pop(0)
            point_2 = points.pop(0)
            for i in range(0, occurrences-2):
                points.pop(0)
            pairs.append((point_1, point_2))

    return pairs


def discard_bad_pairs(points, pixel_dimensions, max_width=200*10**-6):
    """

    Discards pairs of points if their y-axis spacing is larger than the maximum width.

    :param points: list of rectangular points
    :param pixel_dimensions: tuple of form (width, height) in meters
    :param max_width: maximum expected width in meters
    :return: list of good point-pairs
    """

    pairs = get_pairs(points)
    good_points = list()

    for pair in pairs:

        y1 = pair[0].y
        y2 = pair[1].y

        width = np.abs(y2-y1)*pixel_dimensions[1]

        if width < max_width:
            good_points.extend([point for point in pair])

    return good_points


# Dead code below this line.


def error_function(theta, r0, c):

    return r0 + c * theta


def minimize_error_function(points):

    popt, pcov = optimize.curve_fit(error_function, get_theta_axis(points), get_r_axis(points))

    return popt[0], popt[1]


def minimize_point_error(points):

    r0, c = minimize_error_function(points)
    points_p = list()

    for point in points:
        theta = point.theta
        r = point.r
        r_e = error_function(theta, r0, c)
        points_p.append(PointAngular(r - r_e, theta))

    return points_p

