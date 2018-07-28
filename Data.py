import numpy as np
import pandas as pd
import scipy.optimize as optimize


class PointRect:

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y


class PointAngular:

    def __init__(self, r=0, theta=0):

        self.r = r
        self.theta = theta


class PointRtime:

    def __init__(self, r=0, t=0):

        self.r = r
        self.t = t


def x_in_points(points=list()):
    return [point.x for point in points]


def y_in_points(points=list()):
    return [point.y for point in points]


def r_in_points(points=list()):
    return [point.r for point in points]


def theta_in_points(points=list()):
    return [point.theta for point in points]


def t_in_points(points=list()):
    return [point.t for point in points]


def points_to_tuples(points=list()):

    tuples = list()

    for point in points:
        tuples.append((point.x, point.y))

    return tuples


def average_points(points=list(), window_size=20):

    x = x_in_points(points)
    y = y_in_points(points)

    d = pd.DataFrame({'x': x, 'y': y})
    averaged_d = d.rolling(window_size).mean()

    x = averaged_d['x'].values.tolist()
    y = averaged_d['y'].values.tolist()

    averaged_points = [PointRect(x[i], y[i]) for i in range(window_size, len(d))]

    return averaged_points


def get_unique(data):

    seen = set()
    unique = list()

    for x in data:
        if x not in seen:
            unique.append(x)
            seen.add(x)

    return unique


def rectangular_to_angular(points_rect, pixel_dimensions):
    """
    To do: theta_last calculation isn't entirely accurate. The radius at the end points of the arc
    are subtly different, and I'm not sure if the diff in x coord translates to arc length.

    :param points_rect:
    :param pixel_dimensions:
    :return:
    """

    points_angular = list()

    x_last = 0
    theta_last = 0

    for point in points_rect:

        x_new = point.x * pixel_dimensions[0]
        y = point.y * pixel_dimensions[1]
        r = np.sqrt(x_new**2 + y**2)
        theta_new = theta_last + (x_new - x_last)/r
        points_angular.append(PointAngular(r, theta_new))
        x_last = x_new
        theta_last = theta_new


    return points_angular


def angular_to_rtime(points_angular, angular_velocity):

    points_rtime = list()
    t = 0
    theta_last = 0

    for point in points_angular:

        dtheta = point.theta - theta_last
        t = t + dtheta / angular_velocity
        points_rtime.append(PointRtime(point.r, t))
        theta_last = point.theta

    return points_rtime

# Remember, this is generating a pair for points that don't have one.
def get_pairs(points):

    unique_x = get_unique(x_in_points(points))
    x_axis = x_in_points(points)
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

    pairs = get_pairs(points)
    good_points = list()

    for pair in pairs:

        y1 = pair[0].y
        y2 = pair[1].y

        width = np.abs(y2-y1)*pixel_dimensions[1]

        if width < max_width:
            good_points.extend([point for point in pair])

    return good_points


def error_function(theta, r0, c):

    return r0 + c * theta


def minimize_error_function(points):

    popt, pcov = optimize.curve_fit(error_function, theta_in_points(points), r_in_points(points))

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

