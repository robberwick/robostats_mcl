import csv
import numpy as np
import os
import math
import montecarlo_localization as mcl
global_map = mcl.occupancy_map('data/map/minesweeper.dat')

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "data/log/"
filename = "minesweeperL.log"
abs_file_path = os.path.join(script_dir, rel_path, filename)
with open(abs_file_path, mode='w') as log_file:
    log_writer = csv.writer(log_file, delimiter=' ', lineterminator='\n', quoting=csv.QUOTE_NONE)
    log_writer.writerow(['L', 40, 0, 0, -88.567719, -164.303391, 1.57, 66, 66, 66, 66, 66, 66, 66, 65, 66, 66, 66, 66, 66, 66, 66, 66, 67, 66, 67, 66, 67, 68, 67, 68, 68, 68, 69, 67, 530, 514, 505, 508, 494, 481, 470, 458, 445, 419, 411, 401, 393, 386, 379, 371, 365, 362, 363, 364, 358, 353, 349, 344, 339, 334, 332, 328, 324, 321, 304, 299, 298, 294, 291, 288, 287, 284, 282, 281, 278, 277, 275, 274, 273, 271, 269, 268, 267, 266, 265, 265, 264, 263, 263, 262, 261, 261, 261, 261, 261, 261, 193, 190, 189, 189, 193, 262, 263, 264, 193, 190, 190, 190, 194, 270, 271, 272, 274, 275, 277, 278, 278, 281, 283, 285, 288, 290, 292, 295, 298, 300, 303, 306, 309, 313, 318, 321, 326, 330, 335, 340, 360, 366, 372, 379, 384, 93, 92, 91, 89, 88, 87, 86, 85, 84, 84, 82, 82, 81, 81, 80, 79, 78, 78, 77, 77, 76, 76, 75, 75, 74, 74, 73, 73, 72, 72, 72, 71, 72, 71, 71, 71, 71, 71, 71, 70, 70, 70, 70, 70, 70, 0])

    start_time = 0
    end_time = 300
    interval = 0.1
        #sensor offsets are relative to chassis centre, in x, y and theta (anti-clockwise from forwards)
        #sensor indexes are 3, 4, 5, 6, 7, 1, 0, 2 from the front, clockwise
    sensor_offsets = [[9.12, 2.42, 45], 
        [8.23, 3.69, 77.5], 
        [9.5, 7.3, 15], 
        [9.5, -7.3, -15], 
        [9.12, -2.42, 45], 
        [8.23, -3.69, -77.5],
        [-8.75, 2.56, 135], 
        [-8.75, -2.56, -135]]
    dist = [0] * 8
    for t in np.arange(start_time, end_time, interval):
        
        x =  55 * math.cos(0.4 * t)
        y =  55 * math.sin(0.4 * t)
        w = (0.4 * t + np.pi) % (2 * np.pi) - np.pi #removed + 0.5 np.pi
        log_writer.writerow(['O', x, y, w, t])
        x_offset, y_offset, theta_offset = 90, 90, 1.57
        for sensor_number in range(8):
            sensor_x = x + x_offset + sensor_offsets[sensor_number][0] * math.cos(w) - sensor_offsets[sensor_number][1] * math.sin(w)
            sensor_y = y + y_offset + sensor_offsets[sensor_number][0] * math.sin(w) + sensor_offsets[sensor_number][1] * math.cos(w)
            sensor_theta = w + theta_offset + math.radians(sensor_offsets[sensor_number][2])
            print(sensor_offsets[sensor_number][0], sensor_offsets[sensor_number][1]) 
            print(x, y, sensor_x, sensor_y, t)
            wx, wy, dist[sensor_number] = mcl.raycast_bresenham(sensor_x, sensor_y, sensor_theta, global_map)
        log_writer.writerow(['L', x, y, w, x, y, w, dist[0], dist[1], dist[2], dist[3], dist[4], dist[5], dist[6], dist[7], t])
