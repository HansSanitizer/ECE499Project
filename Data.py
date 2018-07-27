import numpy as np
import pandas as pd
import warnings

class Point:

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y


def x_in_points(points=list()):
    return [point.x for point in points]


def y_in_points(points=list()):
    return [point.y for point in points]


def r_in_points(points=list()):
    return [point.x for point in points]


def t_in_points(points=list()):
    return [point.y for point in points]


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

    averaged_points = [Point(x[i], y[i]) for i in range(window_size, len(d))]

    return averaged_points


def get_unique(data):

    seen = set()
    unique = list()

    for x in data:
        if x not in seen:
            unique.append(x)
            seen.add(x)

    return unique

# time isn't right
def pixel_to_rtime(points_rect, pixel_dimenions):

    points_angular = list()
    t = 0
    x1_m = 0

    for point in points_rect:
        x2_m = point.x * pixel_dimenions[0]
        y = point.y * pixel_dimenions[1]
        r = np.sqrt(x2_m ** 2 + y ** 2)
        dx_m = x2_m - x1_m
        t = t + (dx_m / (2.6*np.pi*r))
        points_angular.append(Point(r, t))
        x1_m = x2_m

    return points_angular


def get_pairs(points):

    unique_x = get_unique(x_in_points(points))
    x_axis = x_in_points(points)
    pairs = list()

    for x in unique_x:

        occurrences = x_axis.count(x)

        if occurrences == 1:
            point = points.pop(0)
            #pairs.append((point, point))
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






