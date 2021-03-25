from off_lattice.StaticOffLatticeCluster import Cluster
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import sys

if len(sys.argv) != 3:
    print("Usage: python run.py <total_cluster_size> <total step>")
    exit(0)

total_size = sys.argv[1]
total_step = sys.argv[2]
method = 'mc'

c = Cluster(int(np.sqrt(total_size)) * 10)
count = 0
while c.r_max < total_size and count < total_step:
    print("Step: " + str(count) + "; Current size = " + str(c.r_max))
    c.launch_walker(method)
    count += 1

plt.title("DLA Cluster", fontsize=20)
plt.matshow(c.cluster)  # plt.cm.Blues) #ocean, Paired
fname = "images/cluster_" + method +"_" + str(c.r_max) + ".png"
plt.savefig(fname, dpi=200)
plt.close()
