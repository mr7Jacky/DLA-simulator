import numpy as np
import off_lattice.helper as hp


class Particle:

    def __init__(self, loc, particle_radius):
        self.loc = loc
        self.radius = particle_radius # round(np.random.uniform(low=1, high=max_radius))

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
        for particle in lattice:
            if hp.cal_two_points_dist(particle.loc, self.loc) <= \
                    particle.radius + self.radius:
                return True
        return False

    def is_rambling(self, value, side_len):
        """
        Check if this particle is rambling out of the given range
        :param side_len: the side length of the lattice
        :param value: threshold
        :return: boolean value
        """
        mid = side_len / 2
        return hp.cal_two_points_dist(self.loc, [mid, mid]) > value

    def update_loc(self, loc):
        self.loc = loc
