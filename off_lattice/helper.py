import numpy as np
import matplotlib.pyplot as plt
from typing import List

from off_lattice.Particle import Particle


def cal_two_points_dist(loc1, loc2):
    return np.sqrt(np.power(loc1[0] - loc2[0], 2) + np.power(loc1[1] - loc2[1], 2))