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

global_map = mcl.occupancy_map('data/map/minesweeper.dat')
logdata = mcl.load_log('data/log/minesweeper.log')

#global_map = mcl.occupancy_map('data/map/wean.dat')
#logdata = mcl.load_log('data/log/robotdata1.log.gz')
logdata_scans = logdata.query('type > 0.1')

import matplotlib.animation as animation

sensor = mcl.laser_sensor()
particle = mcl.robot_particle(global_map, sensor, initial_pose=(130, 100, 0.07))
fig, ax = plt.subplots()

def init():    
    mcl.draw_map_state(global_map, ax=ax)

def animate(message):
    #plt.cla()
    #mcl.draw_map_state(global_map, ax=ax)
    particle.sample_motion(message)
    mcl.plot_particle(particle, ax)

ani = animation.FuncAnimation(fig, animate, logdata.values, init_func=init,
    interval=50, blit=False, repeat=False)

plt.show()