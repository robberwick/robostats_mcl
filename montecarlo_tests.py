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
logdata = mcl.load_log('data/log/robotdata1.log.gz')

#Initialize 100 particles uniformly in valid locations on the map
laser = mcl.laser_sensor(stdv_cm=20, uniform_weight=0.2)
particle_list = [mcl.robot_particle(wean_hall_map, laser, log_prob_descale=50,
                                    sigma_fwd_pct=0.3, sigma_theta_pct=0.2)
                 for _ in range(30000)]
scan_data_gen = (msg for msg in logdata.query('type > 0.1').values)

fig, ax = plt.subplots(figsize=(40,40))
#mcl.draw_map_state(wean_hall_map, particle_list[::20], ax=ax)
new_particle_list = mcl.mcl_update(particle_list, next(scan_data_gen))
weights = pd.Series([p.weight for p in new_particle_list])
new_particle_list = mcl.mcl_update(new_particle_list, next(scan_data_gen))
weights = pd.Series([p.weight for p in new_particle_list])
#mcl.draw_map_state(wean_hall_map, new_particle_list, ax=ax)
new_particle_list = mcl.mcl_update(new_particle_list, next(scan_data_gen))
#mcl.draw_map_state(wean_hall_map, new_particle_list, ax=ax)
for _ in range(20):
    new_particle_list = mcl.mcl_update(new_particle_list, next(scan_data_gen))
#fig, ax = plt.subplots(figsize=(40,40))
#mcl.draw_map_state(wean_hall_map, new_particle_list, ax=ax)

p = mcl.robot_particle(wean_hall_map, laser)
p.new_pose_from_sample_error()

new_particle_list = mcl.mcl_update(new_particle_list, next(scan_data_gen))

print(len([p.weight for p in particle_list]))