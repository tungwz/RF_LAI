# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import netCDF4 as nc4
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scienceplots

# plt.rcParams.update({'font.sans-serif':'Times New Roman'})
plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')


sns.set(font_scale=1.5)
def draw_distribution_histogram(nums, nums1, nums2, path, month):

  plt.xlim(0,20)
  x = np.linspace(0,20,11)

  sns.kdeplot(nums ,shade=True,color='steelblue',label='GLASS')
  sns.kdeplot(nums1,shade=True,color='red',label='GLASS/%Tree')
  sns.kdeplot(nums2,shade=True,color='purple',label='GLASS/%(Tree+Grass)')

  if month==9 or month==10 or month==11 or month==12:
    plt.xlabel("LAI")
    x_label= ['0','2','4','6','8','10','12','14','16','18','20']
    plt.xticks(x, x_label, fontsize=10)
  else:
    x_label= [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
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
    plt.legend(loc='upper right', prop={'size': 10})

  mons = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  plt.title(mons[int(month)-1])
  plt.tight_layout(pad=0.5)

lai_nc = nc4.Dataset('../nc_data/Global_GLASS_LAI_0.5deg_2020.nc')
plt.figure(figsize=(12, 8))
for i in range(12):
    glai_= lai_nc['GLASS_LAI'][i,:,:]
    glai = glai_[glai_>0]

    tlai_= lai_nc['GLASS_LAI_T'][i,:,:]
    tlai = tlai_[tlai_>0]

    vlai_= lai_nc['GLASS_LAI_V'][i,:,:]
    vlai = vlai_[vlai_>0]

    n=1+i
    plt.subplot(3,4,n)
    path='./Fig8D.png'
    draw_distribution_histogram(glai, tlai, vlai, path, i+1)
plt.savefig(path, dpi=300)
