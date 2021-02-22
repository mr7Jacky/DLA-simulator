import numpy as np
import matplotlib.pyplot as plt


class RCluster:

    def __init__(self, radius, max_launch_num):
        self.radius = radius
        self.side_len = 2 * radius + 5
        self.lattice = np.zeros((self.side_len, self.side_len))
        self.cluster_size = 0
        self.step_limit = 10000
        self.max_random_walker = max_launch_num
        self.put_init_seed()

    def put_init_seed(self):
        """
        Put the initial seed at the center of the lattice
        :return: None
        """

        mid = self.radius + 2
        print(mid)
        for r in range(0, self.side_len):
            for c in range(0, self.side_len):
                # put a seed particle
                if r == mid and c == mid:
                    self.lattice[r][c] = 1
                # define field outside of circle
                elif np.sqrt((c - mid) ** 2 + (r - mid) ** 2) > self.radius:
                    self.lattice[r][c] = 2

    def get_aggr_size(self):
        """
        Calculate the distance of the most distal seed from the center
        :return: the distance
        """
        x, y = np.where(self.lattice == 1)
        mid = self.radius + 2
        return np.max(np.sqrt(np.power(x - mid, 2) + np.power(y - mid, 2))) + 1

    def run(self):
        random_walk_count = 0
        complete_cluster = False
        while not complete_cluster:
            random_walk_count += 1
            x, y, is_attached = self.launch_walker()
            if is_attached:
                self.cluster_size += 1
            print("Step: " + str(random_walk_count) + "; Current size = " + str(self.cluster_size))
            if random_walk_count == self.max_random_walker:
                print("[WARNING] Exceed the max number of random walker.")
                complete_cluster = True
            if self.is_near_boundary(x, y) and is_attached:
                complete_cluster = True

    def launch_walker(self):
        """
        Put a new seed to the lattice
        :return: whether the seed is attached to the grid
        """
        new_seed = self.generate_random_point(self.get_aggr_size() * 2)
        is_attached = False
        steps = 0
        while True:
            new_seed = self.walk(new_seed[0], new_seed[1])
            x, y = tuple(new_seed)
            if self.is_near_cluster(x, y):
                self.lattice[x, y] = 1
                is_attached = True
                break
            if self.is_rambling(x, y, self.get_aggr_size() * 3):
                break
            if steps > self.step_limit:
                break
            steps += 1
        return x, y, is_attached

    def generate_random_point(self, radius):
        """
        Randomly generate a location of starting point within given range of a circle
        :param radius: the radius of the circle
        :return: coordinates of the location
        """
        mid = self.radius + 2
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
        mid = self.radius + 2
        return np.sqrt(np.power(x - mid, 2) + np.power(y - mid, 2)) > value

    def is_near_boundary(self, x, y):
        loc = self.get_directions(x, y, 4)
        for i, j in loc:
            if self.lattice[i, j] == 2:
                return True
        return False

    @staticmethod
    def walk(x, y):
        act = np.random.uniform(low=0, high=1)
        if act < 0.25:
            return [x + 1, y]
        elif act < 0.5:
            return [x - 1, y]
        elif act < 0.75:
            return [x, y + 1]
        else:
            return [x, y - 1]

    def get_directions(self, x, y, mode):
        if mode == 8:
            v = [x, x - 1, x + 1]
            h = [y, y - 1, y + 1]
            return np.array([[i, j] for i in v for j in h if i < self.radius * 2 and j < self.radius * 2])
        else:
            direct = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
            return [i for i in direct if i[0] < self.radius * 2 and i[1] < self.radius * 2]


if __name__ == "__main__":
    c = RCluster(100, 1000)
    c.run()
    i, j = np.where(c.lattice == 2)
    for n, m in zip(i, j):
        c.lattice[n, m] = 0

    plt.title("DLA Cluster", fontsize=20)
    plt.matshow(c.lattice)  # plt.cm.Blues) #ocean, Paired
    plt.savefig("../images/Rcluster_mc_" + str(c.cluster_size) + ".png", dpi=200)
    plt.close()
