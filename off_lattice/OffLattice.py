import numpy as np
import matplotlib.pyplot as plt
from Particle import Particle
import pickle
import sys
import time

class StaticOffLatticeCluster:

    def __init__(self, particle_radius=1, lattice_size=500, delta=2 * np.pi, max_num_particle=3000, alpha=1):
        self.lattice_size = lattice_size
        self.mid = self.lattice_size // 2
        self.cluster = []
        self.num_particle = 0
        self.r_max = 3
        self.max_num_particle = max_num_particle
        self.step_limit = 50000
        self.delta = delta
        self.alpha = alpha
        self.particle_radius = particle_radius
        self.put_init_seed()
        np.random.seed(42)
        

    def put_init_seed(self):
        """
        Put the initial seed at the center of the lattice
        :return: None
        """
        p = Particle((self.mid, self.mid), self.particle_radius)
        self.cluster.append(p)
        self.num_particle += 1

    def simulate(self, seed=42):
        np.random.seed(seed)
        # loop over particles
        num_part_launch = 0

        while (self.num_particle < self.max_num_particle) and (2 * self.r_max < self.mid - 2):
            if self.num_particle % 10 == 0:
                print("npart= ", self.num_particle, " total_launch: ", num_part_launch)
            num_part_launch += 1
            x, y = self.generate_random_point()
            walk_stop = 0
            phi = np.random.random_sample() * 2 * np.pi
            while walk_stop == 0:
                # rnd = np.random.normal(0, 1)
                x, y, phi = self.cal_next_move(x, y, phi)
                # determine distance of random walker from midpoint of lattice
                r = np.sqrt((x - self.mid) ** 2 + (y - self.mid) ** 2)
                # stop random walk if out of boundary
                if r >= 2 * self.particle_radius * self.r_max:
                    walk_stop = 1
                # stop random walk if next to cluster site
                if self.near_cluster(x, y):
                    walk_stop = 1
                    self.cluster.append(Particle((x, y), self.particle_radius))
                    self.num_particle += 1
                    if r > self.r_max:
                        self.r_max = r

    def near_cluster(self, x, y):
        """
        Check if the given location is near the cluster
        :return: true or false
        """
        # Check the square circumscribing the particle
        for particle in self.cluster:
            if self.cal_two_points_dist(particle.loc, (x, y)) <= 2 * self.particle_radius:
                return True
        return False

    def generate_random_point(self):
        """
        Randomly generate a location of starting point within given range of a circle
        :return: coordinates of the location
        """
        # start new random walker on circle with radius (RMAX+2)  (rule II)
        theta_rand = 2.0 * np.pi * np.random.random_sample()
        x = self.mid + ((self.particle_radius * self.r_max + 2) * np.cos(theta_rand))
        y = self.mid + ((self.particle_radius * self.r_max + 2) * np.sin(theta_rand))
        return x, y

    def cal_next_move(self, x, y, phi):
        eta = np.random.uniform(low=0, high=self.delta)
        new_phi = phi + eta
        new_x = x + self.alpha * np.cos(new_phi)
        new_y = y + self.alpha * np.sin(new_phi)
        return new_x, new_y, phi

    @staticmethod
    def cal_two_points_dist(loc1, loc2):
        return np.sqrt(np.power(loc1[0] - loc2[0], 2) + np.power(loc1[1] - loc2[1], 2))

    def plot_cluster(self, out_name):
        fig, ax = plt.subplots()
        # plt.title("DLA Cluster", fontsize=20)
        for particle in self.cluster:
            circle = plt.Circle(particle.loc, particle.radius, fc='black', ec="black")
            ax.add_patch(circle)
        plt.axis('off')
        plt.savefig(out_name)


if __name__ == "__main__":
    a = int(sys.argv[1])
    c = StaticOffLatticeCluster(particle_radius=a, lattice_size=1500, delta=2 * np.pi, max_num_particle=30, alpha=1)
    c.simulate()
    outfile = open('rad_' + str(a) + '.dat','wb')
    pickle.dump(c.cluster,outfile)
    outfile.close()
