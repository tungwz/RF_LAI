# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import numpy as np
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.ticker import MultipleLocator

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

rf_r2_train  =  [0.911092,0.903365,0.921678,0.915044,0.856886,0.728905,0.713267,0.749664,0.861772,0.908407,0.904067,0.911385]
rf_r2_test   =  [0.904759,0.896950,0.915380,0.908581,0.847050,0.714065,0.697842,0.735386,0.852079,0.901546,0.897828,0.904409]
rf_rmse_train=  [0.708823,0.714886,0.647552,0.649457,0.675679,0.765876,0.782075,0.759168,0.686155,0.650915,0.702427,0.700228]
rf_rmse_test =  [0.733618,0.738209,0.673045,0.673629,0.698417,0.786626,0.803016,0.780554,0.709737,0.674777,0.724791,0.727129]


lg_r2_train  =  [0.909094,0.914757,0.938926,0.951258,0.872486,0.772666,0.759333,0.906469,0.920522,0.984323,0.961543,0.949967]
lg_r2_test   =  [0.904367,0.901381,0.922548,0.919804,0.856022,0.729257,0.723524,0.768214,0.870010,0.910651,0.906475,0.911520]
lg_rmse_train=  [0.716743,0.671424,0.571821,0.491934,0.637791,0.701341,0.716502,0.464039,0.520291,0.269296,0.444741,0.526156]
lg_rmse_test =  [0.735126,0.722164,0.643911,0.630928,0.677622,0.765444,0.768132,0.730534,0.665331,0.642819,0.693442,0.699557]

fig  = plt.figure(figsize=(30,10))
nrow = 1
ncol = 2

types = np.asarray(['NET','BET','NDT','BDT', 'MF'])
# colors= ['#4477AA','#66CCEE','#228833','#CCBB44','#EE6677','#AA3377','#BBBBBB']
# colors= ['#4477AA','#66CCEE','#228833','#CCBB44','#1f77b4','#ff7f0e','#BBBBBB']
colors= ['#4477AA','#66CCEE','#228833','#CCBB44','#ef767a','#456990','#BBBBBB']

plt.subplots_adjust(top=0.91, bottom=0.12, left=0.09, right=0.97, hspace=0.57, wspace=0.42)
for irow in range(2):
    ax = fig.add_subplot(nrow,ncol,irow+1)


    s_size = 400

    if (irow==0):
        plt.plot(range(12), rf_r2_train, marker='o', c=colors[4], label='RF_Train'      ,alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), rf_r2_test , marker='*', c=colors[4], label='RF_Test'       ,alpha=0.8-1*0.06, markersize=25)
        plt.plot(range(12), lg_r2_train, marker='o', c=colors[5], label='LightGBM_Train',alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), lg_r2_test , marker='*', c=colors[5], label='LightGBM_Test' ,alpha=0.8-1*0.06, markersize=25)

        ax.set_title('(A) R$^{2}$', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("Month", fontsize=40)
    else:

        plt.plot(range(12), rf_rmse_train, marker='o', c=colors[4], label='RF_Train'      ,alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), rf_rmse_test , marker='*', c=colors[4], label='RF_Test'       ,alpha=0.8-1*0.06, markersize=25)
        plt.plot(range(12), lg_rmse_train, marker='o', c=colors[5], label='LightGBM_Train',alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), lg_rmse_test , marker='*', c=colors[5], label='LightGBM_Test' ,alpha=0.8-1*0.06, markersize=25)
        ax.set_title('(B) RMSE (unit: m$^{2}$/m$^{2}$)', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("Month", fontsize=40)

    # ds = ds.dropna(subset=['map','mod'])
    plt.xlim(-0.5,12.1)
    plt.ylim(-0.01,1.01)

    x = range(0,12,1)
    x_label= [i for i in range(1,13,1)]

    ax.set_xticks(ticks=x)
    ax.set_xticklabels(labels=x_label,ha='center',va='top')
    ax.tick_params(axis='x',which='major',labelsize=35,direction='in',width=2,length=10)

    y = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    y_label = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    ax.tick_params(axis='y',which='major',labelsize=30,direction='in',width=2,length=10)
    ax.tick_params(axis='y',which='minor',labelsize=30,direction='in',width=1,length=5)
    ax.yaxis.set_minor_locator(MultipleLocator(0.05))
    ax.set_yticks(ticks=y)
    plt.yticks(y,y_label)

    plt.legend(loc='lower left', prop={'size': 25})
    for location in ['left', 'right', 'top', 'bottom']:
        ax.spines[location].set_linewidth(2.5)
plt.savefig('./como_Sites.png', format='png', bbox_inches='tight')
plt.close()
