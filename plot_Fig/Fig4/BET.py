# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MultipleLocator
import scienceplots

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

nyear   = 23
info = pd.read_excel("./BET.xlsx")

ii = 0
subtitle=['(N)']

fig=plt.figure(figsize=(60, 85))
for i in range(len(info['site'])+7):
	if (i!=1):
		ax = plt.subplot(8,1,i+1)
	if (i>1):
		print(i)
		ax.axis('off')
		continue
	if (i==1):
		legend_axe = plt.subplot(8,1,2)
		handles, labels = ax.get_legend_handles_labels()
		leenge_=legend_axe.legend(*ax.get_legend_handles_labels(),loc='upper right',
			labelspacing=0.4, markerscale=2, bbox_to_anchor=(1.03, 0.6),fontsize=105, handlelength=2, ncol=len(handles))
		legend_axe.axis('off')
		for legobj in leenge_.legendHandles:
			legobj.set_linewidth(30.0)
		continue
		
	ds = pd.read_csv('../Timecsv/%s.csv' % info['site'][i])
	ds2= pd.read_csv('../map_site/%s_map.csv' % info['site'][i])

	font2 = {
	'weight' : 'normal',
	'size'   : 120,
	}

	mod = ds['MOD_LAI'].values
	opt = ds['RF_LAI'].values
	obs = ds2['Map_LAI'][0:276].values
	
	lc = info['lc'][i]
	print("\n",info['site'][i],lc)

	ax.set_title(u'%s %s, Lat: %s, Lon: %s' %(subtitle[i], info['site'][i],info['LatFmt'][i], info['LonFmt'][i]), fontproperties='DejaVu Sans',fontsize=95,y=0.92, x=0.26, va="top")
	ax.set_ylabel('LAI($m^2/m^2$)',font2)

	if (i==0 or i==1):
		xx = range(0,nyear*12,12)
		# print(xx)
		x  = ['2000','2001','2002','2003',\
		'2004','2005', '2006','2007',\
		'2008','2009','2010','2011',\
		'2012','2013','2014','2015',\
		'2016','2017','2018','2019',\
		'2020','2021','2022']

		plt.xticks(xx, x)
		ax.tick_params(axis='x',which='major',labelsize=90,direction='in',width=5,length=30,top=False)
		ax.tick_params(axis='x',which='minor',labelsize=90,direction='in',width=5,length=20,top=False)
		ax.xaxis.set_minor_locator(MultipleLocator(3))
	else:
		ax.xaxis.set_major_locator(plt.NullLocator())
	
	y = range(0,9,2)
	y_label = [iy for iy in range(0,9,2)]
	ax.tick_params(axis='y',which='major',labelsize=95,direction='out',width=5,length=30, right=False)
	ax.tick_params(axis='y',which='minor',labelsize=95,direction='out',width=5,length=20,  right=False)
	ax.yaxis.set_minor_locator(MultipleLocator(0.5))
	ax.set_yticks(ticks=y)
	plt.yticks(y,y_label)

	dotsize = 1500
	rf_c    = '#B11927'
	plt.plot(range(nyear*12),mod, label='MODIS',c='#000000', linewidth='12', zorder=1)# '#DC143C',zorder=2)
	plt.plot(range(nyear*12),opt, label='RF LAI',c=rf_c,linewidth = '15',zorder=2, alpha=0.75)
	plt.scatter(range(nyear*12),obs, marker="^",s=dotsize,c='#456990',label='LAI reference map',zorder=3)

	plt.xlim(-2.5,nyear*12+0.5)
	plt.ylim(-0.7,9)

	plt.yticks(fontsize=95)
	for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_linewidth(4.5)

fig.suptitle('Broadleaved Evergreen Tree', fontproperties='DejaVu Sans',fontsize=120)
fig.subplots_adjust(top=0.95)
plt.savefig('./Plot_time_Fig4/BET.png', format='png', bbox_inches='tight')
