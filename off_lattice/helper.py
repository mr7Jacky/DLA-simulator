import numpy as np
import matplotlib.pyplot as plt
from typing import List

from off_lattice.Particle import Particle


def cal_two_points_dist(loc1, loc2):
    return np.sqrt(np.power(loc1[0] - loc2[0], 2) + np.power(loc1[1] - loc2[1], 2))


def plot_lattice(lattice: List[Particle]):
    plt.axes()
    for particle in lattice:
        circle = plt.Circle(particle.loc, particle.radius, fc='white', ec="black")
        plt.gca().add_patch(circle)
    plt.axis('scaled')
    plt.show()
