from src.Cluster import Cluster
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

c = Cluster(100)
count = 0
while c.cluster_size < 1000:
    c.employ_seed()
    count += 1

plt.title("DLA Cluster", fontsize=20)
plt.matshow(c.grid)  # plt.cm.Blues) #ocean, Paired
plt.savefig("images/cluster.png", dpi=200)
plt.close()
