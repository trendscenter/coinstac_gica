#!/usr/bin/env python
import sys
import matplotlib
matplotlib.use('Agg')

from scipy import reshape, zeros, where, std, argmax, sqrt, ceil, sign, \
    negative, linspace
from scipy.signal import detrend
from scipy import io
from nipy import save_image, load_image
from nipy.core.api import xyz_affine
from nipy.labs.viz import plot_map, coord_transform, mni_sform
import numpy as np
from pylab import savefig, subplot, \
    subplots_adjust, figure, title, rc, cm, text

# These two parameters can be changed
# better allow configuring them through environment variables
thr = 2 # setting threshold for significance assuming unit variance
iscale = 3

def reindex_cmap_list(tpl):
   new_tpl = []
   idx = linspace(0,1,len(tpl))
   for i in range(0,len(tpl)):
      new_tpl.append((idx[i], tpl[i][1], tpl[i][2]))
   return tuple(new_tpl)

# colormap processing
cdict = {'red': ((0.0, 0.0, 0.0),
                 (0.25, 0.2, 0.2),
                 (0.45, 0.0, 0.0),
                 (0.5, 0.5, 0.5),
                 (0.55, 0.0, 0.0),
                 (0.75, 0.8, 0.8),
                 (1.0,  1.0, 1.0)),
         'green': ((0.0, 0.0, 1.0),
                   (0.25, 0.0, 0.0),
                   (0.45, 0.0, 0.0),
                   (0.5, 0.5, 0.5),
                   (0.55, 0.0, 0.0),
                   (0.75, 0.0, 0.0),
                   (1.0,  1.0, 1.0)),
         'blue':  ((0.0, 0.0, 1.0),
                   (0.25, 0.8, 0.8),
                   (0.45, 0.0, 0.0),
                   (0.5, 0.5, 0.5),
                   (0.55, 0.0, 0.0),
                   (0.75, 0.0, 0.0),
                   (1.0,  0.0, 0.0)),}

ndict = {'red': ((0.0, 0.0, 0.0),
                 (0.5, 0.2, 0.2),
                 (0.9, 0.0, 0.0),
                 (1.0, 0.5, 0.5)),
         'green': ((0.0, 0.0, 1.0),
                   (0.5, 0.0, 0.0),
                   (0.9, 0.0, 0.0),
                   (1.0, 0.5, 0.5)),
         'blue':  ((0.0, 0.0, 1.0),
                   (0.5, 0.8, 0.8),
                   (0.9, 0.0, 0.0),
                   (1.0, 0.5, 0.5))}
pdict = {'red':  ((0.0, 0.5, 0.5),
                 (0.1, 0.0, 0.0),
                 (0.5, 0.8, 0.8),
                 (1.0,  1.0, 1.0)),
         'green': (
                   (0.0, 0.5, 0.5),
                   (0.1, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (1.0,  1.0, 1.0)),
         'blue':  (
                   (0.0, 0.5, 0.5),
                   (0.1, 0.0, 0.0),
                   (0.5, 0.0, 0.0),
                   (1.0,  0.0, 0.0)),}

both_cmap = matplotlib.colors.LinearSegmentedColormap('brian_combined',
                                                      cdict,256)
pos_cmap = matplotlib.colors.LinearSegmentedColormap('brain_above',
                                                      pdict,256)
neg_cmap = matplotlib.colors.LinearSegmentedColormap('brain_below',
                                                      ndict,256)
cmaps = [neg_cmap, both_cmap, pos_cmap]

def save_montage(NIFTI, ANAT, ONAME, SGN):

   nifti = load_image(NIFTI)
   anat  = load_image(ANAT)

   imax = nifti.get_data().max()
   imin = nifti.get_data().min()

   imshow_args = {'vmax': imax, 
                  'vmin': imin}

   mcmap = cmaps[SGN+1]

   num_features = nifti.shape[-1]
   y = max([1,int(round(sqrt(num_features/3)))])
   x = int(ceil(num_features/y)+1)

   font = {'size': 8}
   rc('font',**font)

   f=figure(figsize=[iscale*y,iscale*x/3])
   subplots_adjust(left=0.01, right=0.99, bottom=0.01, 
                   top=0.99, wspace=0.1, hspace=0)

   for i in range(0,num_features):
      data = nifti.get_data()[:,:,:,i]
      data[sign(data) == negative(SGN)] = 0
      if max(abs(data.flatten())) > thr+0.2:
         ax = subplot(x,y,i+1)
         max_idx = np.unravel_index(argmax(data),data.shape)
         plot_map(data, xyz_affine(nifti), anat=anat.get_data(), 
                  anat_affine=xyz_affine(anat), black_bg=True, 
                  threshold=thr, 
                  cut_coords=coord_transform(max_idx[0],
                                             max_idx[1],
                                             max_idx[2], 
                                             xyz_affine(nifti)), 
                  annotate=False, axes=ax, cmap=mcmap, 
                  draw_cross=False, **imshow_args)
         text(0., 0.95, str(i), transform=ax.transAxes, 
              horizontalalignment='center',color=(1,1,1))
   savefig(ONAME,facecolor=(0,0,0))

if __name__ == '__main__':
   if len(sys.argv) != 5:
      print('usage : montage_nii.py <nifti> <anat> <outname> <sign>\n' +\
         'You must specify: \n' +\
         '    - <nifti> a 4D nifti to convert to images \n' +\
         '    - <anat> anatomical image to use as underlay \n' +\
         '    - <outname> output image filename (out.png)\n' +\
         '    - <sign> pos (1), neg (-1), or both (0)')
      sys.exit(1)
   save_montage(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]))
