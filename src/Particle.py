import numpy as np


class Particle:

    def __init__(self, loc, max_radius):
        self.loc = loc
        self.radius = round(np.random.uniform(low=1, high=max_radius))

    def is_near_boundary(self, side_len):
        """
        Check if this particle is near the boundary
        :param side_len:
        :return:
        """
        x = self.loc[0]
        y = self.loc[1]
        return x + self.radius > side_len or y + self.radius > side_len

    def is_rambling(self, value, side_len):
        """
        Check if this particle is rambling out of the given range
        :param side_len:
        :param x: the x coordinate
        :param y: the y coordinate
        :param value: threshold
        :return: boolean value
        """
        mid = side_len // 2
        return np.sqrt((self.loc[0] - mid) ** 2 + (self.loc[1] - mid) ** 2) > value
