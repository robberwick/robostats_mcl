from PIL import Image, ImageOps, ImageEnhance
import numpy as np
import os, os.path, time
import csv
map = "minesweeper"
folder = "data/map/" 
file =  folder + map + ".png"
image = ImageOps.grayscale(Image.open(file))
img = np.array(image)/255
resolution = [10]

def csvWriter(fil_name, nparray):
  example = nparray.tolist()
  with open(folder+fil_name+'.dat', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ')
    writer.writerow(resolution)
    writer.writerows(example)

csvWriter(map, img)