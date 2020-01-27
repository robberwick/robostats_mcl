# Map exists which all robot particles operate in
# Particles each have a motion model and a measurement model

# Need to sample:
#   Motion model for particle (given location of particle, map)
#           Motion model (in this case) comes from log + noise. 
#   Measurement model for particle (given location, map)
#           True measurements come from log

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
from scipy.spatial import distance
import base64
from IPython.display import HTML
import montecarlo_localization as mcl

plt.style.use('ggplot')

import matplotlib.animation as animation

wean_hall_map = mcl.occupancy_map('data/map/wean.dat')
print("1")
logdata = mcl.load_log('data/log/robotdata1.log.gz')
print("2")
logdata_scans = logdata.query('type > 0.1')
print("3")

#Initialize 100 particles uniformly in valid locations on the map
laser = mcl.laser_sensor(stdv_cm=20, uniform_weight=0.2)
print("3")
particle_list = [mcl.robot_particle(wean_hall_map, laser, log_prob_descale=100,
                                    sigma_fwd_pct=0.3, sigma_theta_pct=0.2)
                 for _ in range(300)]

print("4")
# Pre-run first couple steps - hard to draw on screen
#for message in logdata_scans.values[:30:10]:
#    particle_list = mcl.mcl_update(particle_list, message, 
#                                    target_particles=300) # Update

class ParticleMap(object):
    def __init__(self, ax, global_map, particle_list):
        self.ax = ax
        self.global_map = global_map
        self.particle_list = particle_list
        mcl.draw_map_state(global_map, particle_list[::50], ax=self.ax)
        self.i = 1

    def update(self, message):
        self.particle_list = mcl.mcl_update(self.particle_list, message, 
                                            target_particles=300) # Update
        if self.i % 20 == 0:# Plot every 10th message
            plt.cla()        
            mcl.draw_map_state(self.global_map, self.particle_list, self.ax)
            #print(self.i, "  ", len(self.particle_list))
            print(pd.Series([p.weight for p in particle_list]).describe())
        self.i += 1

fig, ax = plt.subplots()
pmap = ParticleMap(ax, wean_hall_map, particle_list)

print("5")
#plt.show()
# pass a generator in "emitter" to produce data for the update func
ani = animation.FuncAnimation(fig, pmap.update, logdata_scans.values, interval=50,
                              blit=False, repeat=False)
print("6")
plt.show()