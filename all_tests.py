import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import montecarlo_localization as mcl
#%load_ext autoreload     -syntax not recognised
#%autoreload 2            -syntax not recognised
##%matplotlib inline      -syntax not recognised
plt.style.use('ggplot')

def mcl_sample_list_by_weight():
    toy_list = [l for l in 'abcd']
    weights  = [10,5,1,0.1]

    sample_list = [mcl.sample_list_by_weight(toy_list, weights, perturb=False) for _ in range(100)]
    print(sample_list[:10])
    df = pd.DataFrame(sample_list)
    print("\nValue Counts in first location:")
    print(df[0].value_counts())

def robot_particle_sample_motion():
    global_map = mcl.values_only_occupancy_map('data/map/wean.dat')
    logdata = mcl.load_log('data/log/robotdata1.log.gz')
    print(logdata.head())

def robot_paticle_sample_motion_2():
    global_map = mcl.values_only_occupancy_map('data/map/wean.dat')
    import time
    fig, ax = mcl.plt.subplots(figsize=(10,10))
    mcl.draw_map_state(global_map, ax=ax)
    for _ in range(3):
        sensor = mcl.laser_sensor()
        particle = mcl.robot_particle(global_map, sensor)
        locations = np.array([particle.sample_motion(msg)
                              for msg in logdata.values])
        location_subset = locations[::50]
        for pose in location_subset[:, 0:4]:
            mcl.plot_particle(pose, ax, pass_pose=True)
    mcl.plt.show()

robot_particle_sample_motion()
