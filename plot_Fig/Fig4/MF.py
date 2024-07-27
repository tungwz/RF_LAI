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
info = pd.read_excel("./MF.xlsx")

ii = 0
subtitle=['(M)']

fig=plt.figure(figsize=(60, 85))
for i in range(len(info['site'])+7):

	ax = plt.subplot(8,1,i+1)
	if (i>0):
		print(i)
		ax.axis('off')
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

	ax.set_title(u'%s %s, Lat: %s, Lon: %s' %(subtitle[i], info['site'][i],info['LatFmt'][i], info['LonFmt'][i]), fontproperties='DejaVu Sans',fontsize=95,y=0.92, x=0.25, va="top")
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

	plt.yticks(fontsize=55)
	plt.tick_params(labelsize=55)#,top='False', right='false', which='both')

	dotsize = 1500
	rf_c    = '#B11927'
	plt.plot(range(nyear*12),mod, label='MODIS',c='#000000', linewidth='12', zorder=1)# '#DC143C',zorder=2)
	plt.plot(range(nyear*12),opt, label='RF LAI',c=rf_c,linewidth = '15',zorder=2, alpha=0.75)
	plt.scatter(range(nyear*12),obs, marker="^",s=dotsize,c='#456990',label='LAI reference map',zorder=3)

	plt.xlim(-2.5,nyear*12+0.5)
	plt.ylim(-0.7,9)

	plt.xticks(rotation=45, ha='center',fontsize=90)
	plt.yticks(fontsize=95)
	for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_linewidth(4.5)

fig.suptitle('Mixed Forest', fontproperties='DejaVu Sans',fontsize=120)
fig.subplots_adjust(top=0.95)
plt.savefig('./Plot_time_Fig4/MF.png', format='png', bbox_inches='tight')
