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

global_map = mcl.values_only_occupancy_map('data/map/lava.dat')
mcl.draw_map_state(global_map, title=global_map.map_filename, rotate=True)
mcl.plt.show()