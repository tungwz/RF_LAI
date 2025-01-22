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

rf_r2_train  =  [0.911294,0.902428,0.921940,0.917340,0.856510,0.730932,0.718836,0.753519,0.864153,0.909424,0.904237,0.910992]
rf_r2_test   =  [0.905040,0.896305,0.915500,0.910550,0.846604,0.716097,0.703791,0.740173,0.854272,0.902634,0.897740,0.903906]
rf_rmse_train=  [0.708019,0.718341,0.646465,0.640623,0.676566,0.763007,0.774443,0.753300,0.680219,0.647291,0.701806,0.701780]
rf_rmse_test =  [0.732536,0.740515,0.672571,0.666334,0.699434,0.783827,0.795072,0.773461,0.704458,0.671039,0.725105,0.729037]


lg_r2_train  =  [0.927759,0.935071,0.979784,0.926803,0.887112,0.756254,0.863329,0.808071,0.871489,0.948507,0.968025,0.924065]
lg_r2_test   =  [0.910683,0.905887,0.923779,0.914274,0.849360,0.725475,0.724030,0.758181,0.857434,0.901292,0.904394,0.908468]
lg_rmse_train=  [0.638941,0.585988,0.328991,0.602840,0.600099,0.726217,0.539942,0.664733,0.661596,0.488054,0.405531,0.648198]
lg_rmse_test =  [0.710437,0.705472,0.638773,0.652318,0.693123,0.770772,0.767429,0.746176,0.696772,0.675646,0.701115,0.711521]

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
        plt.plot(range(12), rf_r2_train, marker='o', c=colors[4], label='RF_Train',alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), rf_r2_test , marker='*', c=colors[4], label='RF_Test' ,alpha=0.8-1*0.06, markersize=25)
        plt.plot(range(12), lg_r2_train, marker='o', c=colors[5], label='LightGBM_Train',alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), lg_r2_test , marker='*', c=colors[5], label='LightGBM_Test' ,alpha=0.8-1*0.06, markersize=25)

        ax.set_title('(a) R$^{2}$', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("Month", fontsize=40)
    else:

        plt.plot(range(12), rf_rmse_train, marker='o', c=colors[4], label='RF_Train',alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), rf_rmse_test , marker='*', c=colors[4], label='RF_Test' ,alpha=0.8-1*0.06, markersize=25)
        plt.plot(range(12), lg_rmse_train, marker='o', c=colors[5], label='LightGBM_Train',alpha=0.8-0*0.06, markersize=20)
        plt.plot(range(12), lg_rmse_test , marker='*', c=colors[5], label='LightGBM_Test' ,alpha=0.8-1*0.06, markersize=25)
        ax.set_title('(b) RMSE (unit: m$^{2}$/m$^{2}$)', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("Month", fontsize=40)

    # ds = ds.dropna(subset=['map','mod'])
    plt.xlim(-0.5,12.1)
    plt.ylim(-0.01,1.01)

    x = range(0,12,1)
    x_label= [i for i in range(1,13,1)]

    ax.set_xticks(ticks=x)
    ax.set_xticklabels(labels=x_label,ha='center',va='top')
    ax.tick_params(axis='x',which='major',labelsize=35,direction='in',width=2,length=10)
    ax.tick_params(axis='x',which='minor',labelsize=0,direction='in',width=0,length=0)

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
plt.savefig('./Figure3.pdf', format='pdf', bbox_inches='tight', dpi=600)
plt.close()
