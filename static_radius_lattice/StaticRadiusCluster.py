import numpy as np
import matplotlib.pyplot as plt


class StaticRadiusCluster:

    def __init__(self, radius, max_launch_num, direction_num=4):
        """
        Initialization
        :param radius: the max radius
        :param max_launch_num: total number of launch num
        :param direction_num: check the all the surround or only 4 directions
        """
        self.radius = radius
        self.side_len = 2 * radius + 5
        self.lattice = np.zeros((self.side_len, self.side_len))
        self.cluster_size = 0
        self.step_limit = 10000
        self.max_random_walker = max_launch_num
        self.put_init_seed()
        self.direction_num = direction_num

    def put_init_seed(self):
        """
        Put the initial seed at the center of the lattice
        :return: None
        """
        mid = self.radius + 2
        for row in range(0, self.side_len):
            for col in range(0, self.side_len):
                # put a seed particle
                if row == mid and col == mid:
                    self.lattice[row][col] = 1
                # define field outside of circle
                elif np.sqrt((col - mid) ** 2 + (row - mid) ** 2) > self.radius:
                    self.lattice[row][col] = 2

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
            # Check if it is near boundary with value 2
            if self.is_near_value(x, y, 2) and is_attached:
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
            # Check if it is near value 1 indicate the cluster
            if self.is_near_value(x, y, 1):
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

    def is_near_value(self, x, y, value):
        """
        Check if the given location is near some value
        :param x: the x coordinate
        :param y: the y coordinate
        :param value: the value to check
        :return: true or false
        """
        loc = self.get_directions(x, y, self.direction_num)
        for loc_x, loc_y in loc:
            if self.lattice[loc_x, loc_y] == value:
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

    @staticmethod
    def walk(x, y):
        """
        Generate a random direction with location based on current location
        :param x: current x
        :param y: current y
        :return: next location
        """
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
        """
        Get all the direction around the current location
        :param x: location x
        :param y: location y
        :param mode: either 4 or 8
        :return: a list of surrounding points
        """
        if mode == 8:
            v = [x, x - 1, x + 1]
            h = [y, y - 1, y + 1]
            return np.array([[loc_x, loc_y] for loc_x in v for loc_y in h
                             if loc_x < self.radius * 2 and loc_y < self.radius * 2])
        else:
            direct = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]
            return [point for point in direct if point[0] < self.radius * 2 and point[1] < self.radius * 2]


if __name__ == "__main__":
    c = StaticRadiusCluster(100, 1000)
    c.run()
    i, j = np.where(c.lattice == 2)
    for n, m in zip(i, j):
        c.lattice[n, m] = 0

    plt.title("DLA Cluster", fontsize=20)
    plt.matshow(c.lattice)  # plt.cm.Blues) #ocean, Paired
    plt.savefig("images/fix_rad_cluster_" + str(c.cluster_size) + ".png", dpi=200)
    plt.close()
