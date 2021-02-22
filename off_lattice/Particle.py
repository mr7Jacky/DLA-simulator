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
        return x + self.radius >= side_len or y + self.radius >= side_len

    def is_near_cluster(self, lattice):
        """
        Check if the given location is near the cluster
        :param lattice:
        :return: true or false
        """
        # Check the square circumscribing the particle
        for i in range(self.loc[0] - self.radius, self.loc[0] + self.radius + 1):
            for j in range(self.loc[1] - self.radius, self.loc[1] + self.radius + 1):
                # Check points within the particle
                if (i - self.loc[0]) ** 2 + (j - self.loc[1]) ** 2 <= self.radius ** 2 + 1:
                    # If there is a point is 1, then they are connected
                    if lattice[i][j] == 1:
                        return True
        return False

    def is_rambling(self, value, side_len):
        """
        Check if this particle is rambling out of the given range
        :param side_len: the side length of the lattice
        :param value: threshold
        :return: boolean value
        """
        mid = side_len // 2
        return np.sqrt((self.loc[0] - mid) ** 2 + (self.loc[1] - mid) ** 2) > value

    def set_particle(self, lattice):
        """
        mark all points within the radius to 1
        :param lattice: the simulating lattice
        """
        # Draw a square of size N*N.
        for i in range(self.loc[0] - self.radius, self.loc[0] + self.radius + 1):
            for j in range(self.loc[1] - self.radius, self.loc[1] + self.radius + 1):
                if (i - self.loc[0]) ** 2 + (j - self.loc[1]) ** 2 <= self.radius ** 2 + 1:
                    lattice[i][j] = 1

    def update_loc(self, loc):
        self.loc = loc
