from src.Cluster import Cluster
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

total_size = 10

c = Cluster(int(np.sqrt(total_size)) * 10, max_radius=5)
count = 0
while c.cluster_size < total_size:
    print("Step: " + str(count) + "; Current size = " + str(c.cluster_size))
    c.launch_walker('ol')
    count += 1

plt.title("DLA Cluster", fontsize=20)
plt.matshow(c.grid)  # plt.cm.Blues) #ocean, Paired
plt.savefig("images/cluster_ol_30.png", dpi=200)
plt.close()
