# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import netCDF4 as nc4
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scienceplots

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

sns.set(font_scale=1.5)
def draw_distribution_histogram(nums1, nums2, path, month):

  plt.xlim(0,7)
  x = np.linspace(0,7,8)

  sns.kdeplot(nums1,shade=True,color='red',label='RF Urban LAI')
  sns.kdeplot(nums2,shade=True,color='steelblue',label='GLASS Urban LAI')

  if month==9 or month==10 or month==11 or month==12:
    plt.xlabel("LAI")
    x_label= ['0','1','2','3','4','5','6','7']
    plt.xticks(x, x_label)
  else:
    x_label= [' ',' ',' ',' ',' ',' ',' ',' ']
    plt.xticks(x, x_label)


  plt.ylabel("")
  if month==1 or month==5 or month==9:
    plt.ylabel("KDE")

  if month>=1 and month<=4:

    plt.ylim(0,1.3)
    y = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    y_label= ['0','0.2','0.4','0.6','0.8','1.0','1.2']
    plt.yticks(y, y_label)

  if month>=5 and month<=8:
    plt.ylim(0,0.7)
    y = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
    y_label= ['0','0.1','0.2','0.3','0.4','0.5','0.6']
    plt.yticks(y, y_label)

  if month>=9 and month<=12:
    plt.ylim(0,1.3)
    y = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
    y_label= ['0','0.2','0.4','0.6','0.8','1.0','1.2']
    plt.yticks(y, y_label)

  if month==4:
    plt.legend(loc='upper right', prop={'size': 12})

  mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  plt.title(mons[int(month)-1])
  plt.tight_layout(pad=0.5) 

rf_nc = nc4.Dataset('../nc_data/Global_Urban_LAI_2020_v61.nc')
glass = nc4.Dataset('../nc_data/Global_GLASS_LAI_0.5deg_2020.nc')

plt.figure(figsize=(12, 8))
for i in range(12):
    rf_lai = rf_nc['URBAN_TREE_LAI'][5,i,:,:]
    rf_lai_= rf_lai[rf_lai>0]
    g_lai  = glass['GLASS_LAI'][i,:,:]
    g_lai_ = g_lai[g_lai>=0]

    n=1+i
    plt.subplot(3,4,n)
    path='./Fig7C.png'
    draw_distribution_histogram(rf_lai_, g_lai_, path, i+1)
plt.savefig(path, dpi=300)
