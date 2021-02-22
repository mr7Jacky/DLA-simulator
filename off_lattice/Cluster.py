import numpy as np
from off_lattice.Particle import Particle


class Cluster:

    def __init__(self, side_len, max_radius):
        self.side_len = side_len
        self.lattice = np.zeros((side_len, side_len))
        self.cluster_size = 0
        self.step_limit = 10000
        self.delta = 2 * np.pi
        self.put_init_seed()
        self.max_rad = max_radius
        self.all_particles = []

    def put_init_seed(self):
        """
        Put the initial seed at the center of the lattice
        :return: None
        """
        loc = [self.side_len // 2, self.side_len // 2]
        p = Particle(loc, 1)
        p.set_particle(self.lattice)

    def get_aggr_size(self):
        """
        Calculate the distance of the most distal seed from the center
        :return: the distance
        """
        x, y = np.where(self.lattice == 1)
        mid = self.side_len // 2
        return self.max_rad * np.mean(np.sqrt(np.power(x - mid, 2) + np.power(y - mid, 2))) + 3

    def launch_walker(self, mode):
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
            if mode == "ol":
                new_loc, phi = self.off_lattice_loc(p.loc[0], p.loc[1], phi)
            if mode == "mc":
                new_loc = self.monte_carlo_location(p.loc[0], p.loc[1])
            p.update_loc(new_loc)
            if p.is_rambling(self.get_aggr_size() * 3, self.side_len):
                break
            if p.is_near_boundary(self.side_len):
                break
            if steps > self.step_limit:
                break
            if p.is_near_cluster(self.lattice):
                p.set_particle(self.lattice)
                self.cluster_size += 1
                is_attached = True
                break
            steps += 1
        return is_attached

    def generate_random_point(self, radius):
        """
        Randomly generate a location of starting point within given range of a circle
        :param radius: the radius of the circle
        :return: coordinates of the location
        """
        mid = self.side_len // 2
        theta = 2 * np.pi * np.random.random()
        x = int(radius * np.cos(theta)) + mid
        y = int(radius * np.sin(theta)) + mid
        return [x, y]

    def is_near_cluster(self, x, y):
        """
        Check if the given location is near the cluster
        :param x: the x coordinate
        :param y: the y coordinate
        :return: true or false
        """
        loc = self.get_directions(x, y, 4)
        for i, j in loc:
            if self.lattice[i, j] == 1:
                return True
        return False

    def is_rambling(self, x, y, value):
        """
        Check if a point is rambling out of the given range
        :param x: the x coordinate
        :param y: the y coordinate
        :param value: threshold
        :return: boolean value
        """
        mid = self.side_len // 2
        return np.sqrt((x - mid) ** 2 + (y - mid) ** 2) > value

    def is_near_boundary(self, x, y):
        v = [x, x - 1, x + 1]
        h = [y, y - 1, y + 1]
        loc = np.array([[i, j] for i in v for j in h])
        for i, j in loc:
            if i >= self.side_len or y >= self.side_len:
                return True
        return False

    @staticmethod
    def monte_carlo_location(x, y):
        act = np.random.uniform(low=0, high=1)
        if act < 0.25:
            return [x + 1, y]
        elif act < 0.5:
            return [x - 1, y]
        elif act < 0.75:
            return [x, y + 1]
        else:
            return [x, y - 1]

    def off_lattice_loc(self, x, y, phi):
        eta = np.random.uniform(low=0, high=self.delta)
        new_phi = phi + eta
        alpha = 2
        new_x = x + int(alpha * np.cos(new_phi))
        new_y = y + int(alpha * np.sin(new_phi))
        return [new_x, new_y], phi

    def get_directions(self, x, y, mode):
        if mode == 8:
            v = [x, x - 1, x + 1]
            h = [y, y - 1, y + 1]
            return np.array([[i, j] for i in v for j in h if i < self.side_len and j < self.side_len])
        else:
            direct = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
            return [i for i in direct if i[0] < self.side_len and i[1] < self.side_len]
