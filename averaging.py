import os
import numpy as np
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

N = len(imlist10)
# max dimension: 7801, 7651
hf = 7801
wf = 7651
template = np.zeros((hf,wf), np.float)
imlist10_modified = []
for im in imlist10[50:]:
    h = (len(im))
    w = (len(im[0]))
    im = np.hstack((im, np.full((h, wf-w), 0)))
    h = (len(im))
    w = (len(im[0]))
    im = np.vstack((im, np.full((hf-h,w), 0)))
    template += im/N
np.savetxt("averaged_safah.txt", template)