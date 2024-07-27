# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scienceplots
from matplotlib.ticker import MultipleLocator

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

csv_dir = "../Timecsv"
info = pd.read_excel("./Select_Site.xlsx")

fig  = plt.figure(figsize=(25,25))
nrow = 2
ncol = 2

types = np.asarray(['NET','BET','NDT','BDT', 'MF'])
colors= ['#4477AA','#66CCEE','#228833','#CCBB44','#EE6677','#AA3377','#BBBBBB']

plt.subplots_adjust(hspace=0.25, wspace=0.25)
for irow in range(3):
    ax = fig.add_subplot(nrow,ncol,irow+1)

    net_mod = []
    net_rf  = []
    ndt_mod = []
    ndt_rf  = []
    bet_mod = []
    bet_rf  = []
    bdt_mod = []
    bdt_rf  = []
    mf_mod  = []
    mf_rf   = []
    net_obs = []
    ndt_obs = []
    bet_obs = []
    bdt_obs = []
    mf_obs  = []

    mod = []
    rf  = []
    obs = []
    for i in range(len(info['site'])):
        ds = pd.read_csv(csv_dir+'/%s.csv' % info['site'][i])
        ds2= pd.read_csv('../map_site/%s_map.csv' % info['site'][i])
        font2 = {
                'weight' : 'normal',
                'size'   : 23,
                }

        if irow==0:
            mod.append(ds['MOD_LAI'].values)
            rf.append(ds['RF_LAI'].values)

            if info['lc'][i]=='NET':
                net_mod.append(ds['MOD_LAI'].values)
                net_rf.append(ds['RF_LAI'].values)
            elif info['lc'][i]=='BET':
                bet_mod.append(ds['MOD_LAI'].values)
                bet_rf.append(ds['RF_LAI'].values)
            elif info['lc'][i]=='BDT':
                bdt_mod.append(ds['MOD_LAI'].values)
                bdt_rf.append(ds['RF_LAI'].values)
            elif info['lc'][i]=='MF':
                mf_mod.append(ds['MOD_LAI'].values)
                mf_rf.append(ds['RF_LAI'].values)

        if irow==1:
            obs.append(ds2['Map_LAI'][0:276].values)
            rf.append(ds['RF_LAI'].values)

            if info['lc'][i]=='NET':
                net_obs.append(ds2['Map_LAI'][0:276].values)
                net_rf.append(ds['RF_LAI'].values)
            elif info['lc'][i]=='BET':
                bet_obs.append(ds2['Map_LAI'][0:276].values)
                bet_rf.append(ds['RF_LAI'].values)
            elif info['lc'][i]=='BDT':
                bdt_obs.append(ds2['Map_LAI'][0:276].values)
                bdt_rf.append(ds['RF_LAI'].values)
            elif info['lc'][i]=='MF':
                mf_obs.append(ds2['Map_LAI'][0:276].values)
                mf_rf.append(ds['RF_LAI'].values)

        if irow==2:
            obs.append(ds2['Map_LAI'][0:276].values)
            mod.append(ds['MOD_LAI'].values)
            if info['lc'][i]=='NET':
                net_obs.append(ds2['Map_LAI'][0:276].values)
                net_mod.append(ds['MOD_LAI'].values)
            elif info['lc'][i]=='BET':
                bet_obs.append(ds2['Map_LAI'][0:276].values)
                bet_mod.append(ds['MOD_LAI'].values)
            elif info['lc'][i]=='BDT':
                bdt_obs.append(ds2['Map_LAI'][0:276].values)
                bdt_mod.append(ds['MOD_LAI'].values)
            elif info['lc'][i]=='MF':
                mf_obs.append(ds2['Map_LAI'][0:276].values)
                mf_mod.append(ds['MOD_LAI'].values)

    s_size = 400

    if (irow==0):
        plt.scatter(net_mod, net_rf, s=s_size, c=colors[0], linewidths=0.5, label=types[0],alpha=0.8-0*0.06)
        plt.scatter(bet_mod, bet_rf, s=s_size, c=colors[1], linewidths=0.5, label=types[1],alpha=0.8-1*0.06)
        plt.scatter(bdt_mod, bdt_rf, s=s_size, c=colors[2], linewidths=0.5, label=types[3],alpha=0.8-3*0.06)
        plt.scatter(mf_mod , mf_rf , s=s_size, c=colors[4], linewidths=0.5, label=types[4],alpha=0.8-4*0.06)

        rf   = np.array(rf).flatten()
        mod  = np.array(mod).flatten()
        r    = np.corrcoef(mod, rf)
        rmse = np.sqrt(np.mean((rf - mod)**2))
        mae  = np.mean(np.abs(rf - mod))
        print(r)

        lc = info['lc'][i]
        print("\n",info['site'][i],lc)

        plt.text(0, 5.5, 'R = %s\nRMSE = %s\nMAE = %s' % (round(r[0,1],2), round(rmse,2), round(mae,2)), dict(size=35))
        ax.set_title('(A) 14 Sites MODIS LAI vs RF LAI', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("MODIS LAI (m$^{2}$/m$^{2}$)", fontsize=35)
    if (irow==1):
        print(net_obs)
        print(net_rf)
        plt.scatter(net_obs, net_rf, s=s_size, c=colors[0], linewidths=0.5, label=types[0],alpha=0.8-0*0.06)
        plt.scatter(bet_obs, bet_rf, s=s_size, c=colors[1], linewidths=0.5, label=types[1],alpha=0.8-1*0.06)
        plt.scatter(bdt_obs, bdt_rf, s=s_size, c=colors[2], linewidths=0.5, label=types[3],alpha=0.8-3*0.06)
        plt.scatter(mf_obs , mf_rf , s=s_size, c=colors[4], linewidths=0.5, label=types[4],alpha=0.8-4*0.06)

        rf = np.array(rf).flatten()
        obs = np.array(obs).flatten()
        nan_mask = np.isnan(obs)
        rf_mask  = rf[~nan_mask]
        obs_maks = obs[~nan_mask]

        r    = np.corrcoef(obs_maks, rf_mask)
        rmse = np.sqrt(np.mean((rf_mask - obs_maks)**2))
        mae  = np.mean(np.abs(rf_mask - obs_maks))
        print(r)
        lc = info['lc'][i]
        print("\n",info['site'][i],lc)

        plt.text(0, 5.5, 'R = %s\nRMSE = %s\nMAE = %s' % (round(r[0,1],2), round(rmse,2), round(mae,2)), dict(size=35))
        ax.set_title('(B) 14 Sites OBS LAI vs RF LAI', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("Site LAI (m$^{2}$/m$^{2}$)", fontsize=35)
    if (irow==2):
        plt.scatter(net_obs, net_mod, s=s_size, c=colors[0], linewidths=0.5, label=types[0],alpha=0.8-0*0.06)
        plt.scatter(bet_obs, bet_mod, s=s_size, c=colors[1], linewidths=0.5, label=types[1],alpha=0.8-1*0.06)
        plt.scatter(bdt_obs, bdt_mod, s=s_size, c=colors[2], linewidths=0.5, label=types[3],alpha=0.8-3*0.06)
        plt.scatter(mf_obs , mf_mod , s=s_size, c=colors[4], linewidths=0.5, label=types[4],alpha=0.8-4*0.06)

        mod = np.array(mod).flatten()
        obs = np.array(obs).flatten()
        nan_mask = np.isnan(obs)
        mod_mask  = mod[~nan_mask]
        obs_maks = obs[~nan_mask]

        r    = np.corrcoef(obs_maks, mod_mask)
        rmse = np.sqrt(np.mean((mod_mask - obs_maks)**2))
        mae  = np.mean(np.abs(mod_mask - obs_maks))

        lc = info['lc'][i]
        print("\n",info['site'][i],lc)

        plt.text(0, 5.5, 'R = %s\nRMSE = %s\nMAE = %s' % (round(r[0,1],2), round(rmse,2), round(mae,2)), dict(size=35))
        ax.set_title('(C) 14 Sites OBS LAI vs MODIS LAI', fontproperties='DejaVu Sans',fontsize=35,loc='left')
        plt.xlabel("Site LAI (m$^{2}$/m$^{2}$)", fontsize=35)

    plt.xlim(-0.5,7.1)
    plt.ylim(-0.5,7.1)

    x = range(0,8,1)
    x_label= [i for i in range(0,8,1)]

    ax.set_xticks(ticks=x)
    ax.set_xticklabels(labels=x_label,ha='center',va='top')
    ax.tick_params(axis='x',which='major',labelsize=40,direction='in',width=2,length=10)
    ax.tick_params(axis='x',which='minor',labelsize=40,direction='in',width=1,length=5)
    ax.xaxis.set_minor_locator(MultipleLocator(0.25))

    y = range(0,8,1)
    y_label = [i for i in range(0,8,1)]
    ax.tick_params(axis='y',which='major',labelsize=40,direction='in',width=2,length=10)
    ax.tick_params(axis='y',which='minor',labelsize=40,direction='in',width=1,length=5)
    ax.yaxis.set_minor_locator(MultipleLocator(0.25))
    ax.set_yticks(ticks=y)
    plt.yticks(y,y_label)

    if irow==2:
        plt.ylabel("MODIS LAI (m$^{2}$/m$^{2}$)", fontsize=35)
    else:
        plt.ylabel("RF LAI (m$^{2}$/m$^{2}$)", fontsize=35)

    plt.plot((-1, 10), (-1, 10), linewidth=4, ls='--', c='black', label='1:1 line')
    ax.set_aspect('equal', adjustable='box') 
    for location in ['left', 'right', 'top', 'bottom']:
        ax.spines[location].set_linewidth(2.5)

# Add the last subplot for the legend only
legend_axe = plt.subplot(nrow, ncol, 4)
handles, labels = ax.get_legend_handles_labels()
leenge_=legend_axe.legend(*ax.get_legend_handles_labels(),loc='lower left',
    labelspacing=0.4, markerscale=1.5, bbox_to_anchor=(0.2, 0.3),fontsize=40)
legend_axe.axis('off')

plt.savefig('./Scatter_plot_sma/como_Sites.png', format='png', bbox_inches='tight')
plt.close()
