from src.Cluster import Cluster
import matplotlib.pyplot as plt
import numpy as np

total_size = 100

c = Cluster(int(np.sqrt(total_size)) * 40, 3)
count = 0
while c.cluster_size < total_size:
    print("Step: " + str(count) + "; Current size = " + str(c.cluster_size))
    c.launch_walker()
    count += 1

plt.title("DLA Cluster", fontsize=20)
plt.matshow(c.lattice)  # plt.cm.Blues) #ocean, Paired
plt.savefig("images/cluster_mc_" + str(c.cluster_size) + ".png", dpi=200)
plt.close()
