import numpy as np
import matplotlib.pyplot as plt


class StaticOnLatticeCluster:

    def __init__(self, lattice_size=500, max_num_particle=3000):
        """
        Initialization
        :param lattice_size: the side length of the lattice
        :param max_num_particle: the max number of particles
        """
        self.lattice_size = lattice_size
        self.mid = int(lattice_size / 2)
        self.lattice = np.zeros((self.lattice_size, self.lattice_size))
        self.lattice[self.mid, self.mid] = 1
        self.num_particle = 1
        self.r_max = 3
        self.step_limit = 10000
        self.max_num_particle = max_num_particle

    def simulate(self):
        count = 0
        plt.gca().invert_yaxis()
        # initialize
        np.random.seed(11)
        # initialize lattice  (rule I)
        # loop over particles
        while (self.num_particle <= self.max_num_particle) and (2 * self.r_max < self.mid - 2):
            if self.num_particle % 10 == 0:
                print("npart= ", self.num_particle, " total_launch: ", count)
            count += 1
            # start new random walker on circle with radius (RMAX+2)  (rule II)
            x, y = self.generate_random_point()
            # loop over random walk steps (rule III)
            walk_stop = 0
            while walk_stop == 0:
                x, y = self.walk(x, y)
                # determine distance of random walker from midpoint of lattice
                r = np.sqrt((x - self.mid) ** 2 + (y - self.mid) ** 2)
                # stop random walk if r >= 2* Rmax   (rule IV)
                if r >= 2 * self.r_max:
                    walk_stop = 1
                # stop random walk if next to cluster site, i.e. up,down,right,left from
                #    already grown cluster, update npart,lattice and RMAX   (rule V)
                if (self.lattice[x, y + 1] + self.lattice[x, y - 1] +
                    self.lattice[x + 1, y] + self.lattice[x - 1, y]) != 0:
                    walk_stop = 1
                    self.num_particle += 1
                    self.lattice[x, y] = 1
                    if r > self.r_max:
                        self.r_max = r

    def plot_cluster(self, out_name):
        plt.figure()
        plt.matshow(self.lattice[int(self.mid - self.r_max - 5):int(self.mid + self.r_max + 5),
                    int(self.mid - self.r_max - 5):int(self.mid + self.r_max + 5)],
                    interpolation='nearest',
                    extent=[-self.r_max - 5, self.r_max + 5, self.r_max + 5, - self.r_max - 5])
        plt.savefig(out_name)

        leni, lenj = self.lattice.shape  # .shape gives you mxn of array
        print(leni, lenj)  # test that read in worked and how to get length and width

    def generate_random_point(self):
        """
        Randomly generate a location of starting point within given range of a circle
        :return: coordinates of the location
        """
        theta_rand = 2.0 * np.pi * np.random.random_sample()
        x = self.mid + int((self.r_max + 2) * np.cos(theta_rand))
        y = self.mid + int((self.r_max + 2) * np.sin(theta_rand))
        return x, y

    @staticmethod
    def walk(x, y):
        """
        Generate a random direction with location based on current location
        :param x: current x
        :param y: current y
        :return: next location
        """
        act = np.random.random_sample()
        if act < 0.25:
            return x + 1, y
        elif act < 0.5:
            return x - 1, y
        elif act < 0.75:
            return x, y + 1
        else:
            return x, y - 1


if __name__ == "__main__":
    c = StaticOnLatticeCluster(lattice_size=500, max_num_particle=3000)
    c.simulate()
    fname = "OnLattice" + str(c.num_particle)
    c.plot_cluster("images/"+fname + ".png")
    np.savetxt(fname + '.dat', c.lattice)
