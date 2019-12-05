import os
import numpy as np
# File manipulation
from glob import glob
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio

files = os.listdir("../Data/Bulk Order 1047194/Landsat 8 OLI_TIRS C1 Level-1/")
imlist10 = []
meta_data = []
for f in files:
    if f == ".DS_Store":
        continue
    fdir = os.path.join("../Data/Bulk Order 1047194/Landsat 8 OLI_TIRS C1 Level-1/", f)
    if os.path.isdir(fdir):
        for i in os.listdir(fdir):
            imfile = os.path.join(fdir, i)
            if i.endswith("B10.TIF") and i[0] != '.':
                with rio.open(imfile) as src:
                    imlist10.append(os.path.join(fdir, i))
                    meta_data.append(src.meta)
dates = []
for f in files:
    if f == ".DS_Store":
        continue
    if f[0] != '.':
        dates.append(f[17:25])
rain_dates = np.genfromtxt("../1959022.csv", delimiter=',', skip_header=1)
rain_dates = [[rain_dates[i, 2], rain_dates[i, 3]] for i in range(len(rain_dates)) if(str(rain_dates[i, 3]) != 'nan' and rain_dates[i, 3] > 0)]
dates = [float(i) for i in dates]
target_dates = np.unique([[dates.index(i) for i in dates if np.abs(i-j[0]) < 2] for j in rain_dates])[1:]
target_dates = [i[0] for i in target_dates]
N = len(imlist10)
# max dimension: 7801, 7651
hf = 7801
wf = 7651
template = np.loadtxt("averaged_safah.txt")
for i in target_dates:
    date = dates[i]
    im = rio.open(imlist10[i]).read(1, masked=True)
    h = (len(im))
    w = (len(im[0]))
    im = np.hstack((im, np.full((h, wf-w), 0)))
    h = (len(im))
    w = (len(im[0]))
    im = np.vstack((im, np.full((hf-h,w), 0)))
    matrix = im
    matrix = matrix * template.mean()/matrix.mean()
    subtract_image = matrix - template
    plt.imshow(subtract_image)
    # plt.show()
    templt = np.where(subtract_image > 0, 0, subtract_image)
    #tempgt = np.where(subtract_image < 0, 0, subtract_image)
    plt.imshow(templt)
    # plt.show()
    #plt.imshow(tempgt)
    # plt.show()
    lower_lim = subtract_image.min()
    print(lower_lim)
    templt = np.where(subtract_image > 0, 0, subtract_image)
    templt = np.where(subtract_image < lower_lim, lower_lim, subtract_image)
    templt = -templt
    templt = templt.astype(np.uint16)
    #templt = templt*2**16/np.max(templt)
    #templt = templt.astype(np.uint16)
    #fig, ax = plt.subplots()
    #ax.imshow(templt, cmap='bwr')
    #ax.axis('off')
    # plt.show()
    out_path = "./"+str(int(date))+"_final.tif"
    with rio.open(out_path, 'w', **meta_data[3]) as outf:
        outf.write(templt, 1)



