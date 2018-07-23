class Point:

    def __init__(self, x=0, y=0):

        self.x = x
        self.y = y


def x_in_points(points=list()):
    return [point.x for point in points]


def y_in_points(points=list()):
    return [point.y for point in points]


def points_to_tuples(points=list()):

    tuples = list()

    for point in points:
        tuples.append((point.x, point.y))

    return tuples


def get_unique(data):

    seen = set()
    unique = list()

    for x in data:
        if x not in seen:
            unique.append(x)
            seen.add(x)

    return unique
