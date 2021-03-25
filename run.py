from off_lattice.StaticOffLatticeCluster import StaticOffLatticeCluster
from on_lattice.StaticOnLatticeCluster import StaticOnLatticeCluster
import off_lattice.helper as hp
import matplotlib.pyplot as plt
import numpy as np

c = StaticOffLatticeCluster(particle_radius=1, lattice_size=500, delta=2 * np.pi, max_num_particle=3000)
c.simulate()
c.plot_cluster("images/off_lattice_" + str(c.num_particle) + ".png")

c = StaticOnLatticeCluster(lattice_size=500, max_num_particle=3000)
c.simulate()
c.plot_cluster("images/StaticRadiusOnLattice.png")