import numpy as np


class Circle:

    def __init__(self, center=(0, 0), radius=1):
        self.center = center
        self.radius = radius
        self.area = np.pi*radius**2
