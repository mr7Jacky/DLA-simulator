from off_lattice.Cluster import Cluster
import off_lattice.helper as hp
import matplotlib.pyplot as plt
import numpy as np

total_size = 100

c = Cluster(int(np.sqrt(total_size)) * 10, 3)
count = 0
prev_size = 0
while c.cluster_size < total_size:
    if c.cluster_size > prev_size:
        prev_size = c.cluster_size
        print("Step: " + str(count) + "; Current size = " + str(c.cluster_size))
    c.launch_walker()
    count += 1

plt.title("DLA Cluster", fontsize=20)
hp.plot_lattice(c.lattice)
plt.savefig("images/off_lattice_" + str(c.cluster_size) + ".png", dpi=200)
plt.close()
