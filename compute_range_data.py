

import numpy as np
import montecarlo_localization as mcl
import os, sys

global_map = mcl.values_only_occupancy_map('data/map/minesweeper.dat')

def cache_map_ranges(theta_bins=120):
    slice_theta_rad = 2*np.pi/theta_bins
    slice_theta_deg = 360/theta_bins
    map_width, map_height = global_map.values.shape

    coord_list = [(xidx, yidx) for yidx in range(map_height) 
                               for xidx in range(map_width)]
    range_array = np.zeros([map_width,map_height,theta_bins])
    raycast_degree_values = np.linspace(0,2*np.pi, num=theta_bins)
    # pre-calculate (cache) expected distance to wall for each theta bin, at each map location
    for xidx,yidx in coord_list:
        for idx, theta in enumerate(raycast_degree_values):
            _,_,dist = mcl.raycast_bresenham(xidx*10, yidx*10, theta, global_map, freespace_min_val=0.7)
            range_array[xidx,yidx,idx] = dist
        progress = 'fraction complete: {0:.2f}'.format((xidx + yidx * map_width) / map_height / map_width)
        print(progress, end='\r')
        sys.stdout.flush()
    print("Finished")
    map_filename = os.path.basename(global_map.map_filename)
    map_filename = os.path.splitext(map_filename)[0]
    range_array_filename = './data/' + map_filename + '_range_array_{}bin'.format(theta_bins)

    np.save(range_array_filename, range_array, allow_pickle=False)
    return range_array
raw_array = cache_map_ranges(theta_bins=120)  # Takes ~9 minutes with theta_bins=120 for an 800x800 map on core i5 laptop