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
#load_ext autoreload
#autoreload 2
#%matplotlib inline
plt.style.use('ggplot')

#%%time
global_map = mcl.values_only_occupancy_map('data/map/wean.dat.gz')
def cache_map_ranges(theta_bins=120):
    slice_theta_rad = 2*np.pi/theta_bins
    slice_theta_deg = 360/theta_bins
    map_width, map_height = 800, 800

    coord_list = [(xidx, yidx) for yidx in range(map_height) 
                               for xidx in range(map_width)]
    range_array = np.zeros([map_width,map_height,theta_bins])
    raycast_degree_values = np.linspace(0,2*np.pi, num=theta_bins)
    # pre-calculate (cache) expected distance to wall for each theta bin, at each map location
    for xidx,yidx in coord_list:
        for idx, theta in enumerate(raycast_degree_values):
            _,_,dist = mcl.raycast_bresenham(xidx*10, yidx*10, theta, global_map, freespace_min_val=0.7)
            range_array[xidx,yidx,idx] = dist
    
    np.save('./data/range_array_{}bin'.format(theta_bins), range_array, allow_pickle=False)
    return range_array

raw_array = cache_map_ranges(theta_bins=40)  # Takes ~9 minutes with theta_bins=120 on core i5 laptop

