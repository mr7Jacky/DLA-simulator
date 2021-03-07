import numpy as np
from typing import List

import off_lattice.helper as hp
from off_lattice.Particle import Particle


class Cluster:

    def __init__(self, side_len: float, max_radius: float):
        self.side_len = side_len
        self.lattice = []
        self.cluster_size = 0
        self.step_limit = 10000
        self.delta = 2 * np.pi
        self.max_rad = max_radius
        self.all_particles = []

        self.put_init_seed()

    def put_init_seed(self):
        """
        Put the initial seed at the center of the lattice
        :return: None
        """
        loc = [self.side_len // 2, self.side_len // 2]
        p = Particle(loc, self.max_rad)
        self.lattice.append(p)

    def get_aggr_size(self):
        """
        Calculate the distance of the most distal seed from the center
        :return: the distance
        """
        max_dist = 0
        mid = self.side_len / 2
        for particle in self.lattice:
            cur_dist = hp.cal_two_points_dist(particle.loc, [mid, mid])
            if cur_dist > max_dist:
                max_dist = cur_dist
        return self.max_rad * max_dist + 3

    def launch_walker(self):
        """
        Put a new seed to the lattice
        :return: whether the seed is attached to the grid
        """
        new_loc = self.generate_random_point(self.get_aggr_size() * 2)
        p = Particle(new_loc, self.max_rad)
        is_attached = False
        steps = 0
        phi = 0
        while True:
            new_loc, phi = self.off_lattice_loc(p.loc[0], p.loc[1], phi)
            p.update_loc(new_loc)
            if p.is_rambling(self.get_aggr_size() * 3, self.side_len):
                break
            if p.is_near_boundary(self.side_len):
                break
            if steps > self.step_limit:
                break
            if p.is_near_cluster(self.lattice):
                self.lattice.append(p)
                self.cluster_size += 1
                is_attached = True
                break
            steps += 1
        return is_attached

    def generate_random_point(self, radius: float) -> List[float]:
        """
        Randomly generate a location of starting point within given range of a circle
        :param radius: the radius of the circle
        :return: coordinates of the location
        """
        mid = self.side_len // 2
        theta = 2 * np.pi * np.random.random()
        x = radius * np.cos(theta) + mid
        y = radius * np.sin(theta) + mid
        return [x, y]

    def off_lattice_loc(self, x, y, phi):
        eta = np.random.uniform(low=0, high=self.delta)
        new_phi = phi + eta
        alpha = 2
        new_x = x + int(alpha * np.cos(new_phi))
        new_y = y + int(alpha * np.sin(new_phi))
        return [new_x, new_y], phi
