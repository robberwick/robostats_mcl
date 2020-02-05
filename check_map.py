
import matplotlib.pyplot as plt
import montecarlo_localization as mcl

plt.style.use('ggplot')

global_map = mcl.occupancy_map('data/map/minesweeper.dat')
fig, ax = plt.subplots()
mcl.draw_map_state(global_map, ax=ax)


plt.show()