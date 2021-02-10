import numpy as np
from src.Particle import Particle


class Cluster:

    def __init__(self, side_len, max_radius=1):
        self.side_len = side_len
        self.grid = np.zeros((side_len, side_len))
        self.cluster_size = 0
        self.step_limit = 10000
        self.delta = 2 * np.pi
        self.put_init_seed()
        self.max_radius = max_radius

    def put_init_seed(self):
        """
        Put the initial seed at the center of the lattice
        :return: None
        """
        x = y = self.side_len // 2
        self.grid[x][y] = 1

    def get_aggr_size(self):
        """
        Calculate the distance of the most distal seed from the center
        :return: the distance
        """
        x, y = np.where(self.grid == 1)
        mid = self.side_len // 2
        return np.mean(np.sqrt(np.power(x - mid, 2) + np.power(y - mid, 2))) + 3

    def launch_walker(self, mode):
        """
        Put a new seed to the lattice
        :return: whether the seed is attached to the grid
        """
        new_seed = self.generate_random_point(self.get_aggr_size() * 2)
        print(new_seed)
        is_attached = False
        steps = 0
        phi = 0
        while True:

            if mode == "ol":
                new_seed, phi = self.off_lattice_loc(new_seed[0], new_seed[1], phi)
            if mode == "mc":
                new_seed = self.monte_carlo_location(new_seed[0], new_seed[1])
            x, y = tuple(new_seed)
            if self.is_rambling(x, y, self.get_aggr_size() * 3): # 3 * aggregation size
                break
            if self.is_near_boundary(x, y):
                break
            if steps > self.step_limit:
                break
            if self.is_near_cluster(x, y):
                self.grid[x, y] = 1
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
            if self.grid[i, j] == 1:
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

    def monte_carlo_location(self, x, y):
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
            return [i for i in [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]] if i[0] < self.side_len and i[1] < self.side_len]
