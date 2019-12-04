import os
import numpy as np
# File manipulation
from glob import glob
import matplotlib.pyplot as plt
import geopandas as gpd
import rasterio as rio

files = os.listdir("../Data/Bulk Order 1047194/Landsat 8 OLI_TIRS C1 Level-1/")
imlist10 = []
imlist11 = []
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
                    imlist10.append(src.read(1, masked=True))
                    meta_data.append(src.meta)
dates = []
for f in files:
    if f == ".DS_Store":
        continue
    if f[0] != '.':
        dates.append((f[17:25], f[26:34]))
print(len(dates))
print(dates.index(('20190202', '20190206')))
N = len(imlist10)
# max dimension: 7801, 7651
hf = 7801
wf = 7651
imlist10_modified = []
for im in imlist10:
    h = (len(im))
    w = (len(im[0]))
    im = np.hstack((im, np.full((h, wf-w), 0)))
    h = (len(im))
    w = (len(im[0]))
    im = np.vstack((im, np.full((hf-h,w), 0)))
    imlist10_modified.append(im)
template = np.loadtxt("averaged_safah.txt")
matrix = imlist10_modified[63]
matrix = matrix * template.mean()/matrix.mean()
subtract_image = matrix - template
plt.imshow(subtract_image)
plt.hist(subtract_image)
plt.show()
templt = np.where(subtract_image > 0, 0, subtract_image)
tempgt = np.where(subtract_image < 0, 0, subtract_image)
plt.imshow(templt)
plt.hist(templt)
plt.show()
plt.imshow(tempgt)
plt.hist(tempgt)
plt.show()
templt = np.where(subtract_image > -400, 0, subtract_image)
templt = np.where(subtract_image < -10000, -10000, subtract_image)
templt = -templt
templt = templt.astype(np.uint16)
print(np.min(templt))
print(np.max(templt))
templt = templt*2**16/np.max(templt)
templt = templt.astype(np.uint16)
print(np.min(templt))
print(np.max(templt))
fig, ax = plt.subplots()
ax.imshow(templt, cmap='bwr')
ax.axis('off')
out_path = "./test_rio.tif"
with rio.open(out_path, 'w', **meta_data[3]) as outf:
    outf.write(templt, 1)



