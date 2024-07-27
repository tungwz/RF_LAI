# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:36:41 2021

@author: Wanyi

"""

import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os
from matplotlib.ticker import MultipleLocator
import scienceplots

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

nyear   = 23
csv_dir = "./Timecsv"
info = pd.read_excel("./NET.xlsx")
# lcf = pd.read_csv("../comb_all.csv")
ii = 0
subtitle=['(I)','(J)','(K)','(L)','(M)','(N)']

fig=plt.figure(figsize=(60, 85))
for i in range(len(info['site'])+2):
	ax = plt.subplot(8,1,i+1)
	if (i>3):
		ax.axis('off')
		continue
	# 	legend_axe = plt.subplot(8,1,7)
	# 	legend_axe.legend(*ax.get_legend_handles_labels(),loc='upper right',
	# 	                    labelspacing=0.4, markerscale=1, bbox_to_anchor=(1.03, 1.03),fontsize=20)
	# 	# # legend_axe.get_title().set_fontsize(fontsize=35)
	# 	legend_axe.axis('off')
	# 	break
	ds = pd.read_csv('./Timecsv/%s.csv' % info['site'][i])
	ds2= pd.read_csv('./map_site/%s_map.csv' % info['site'][i])

	font2 = {
	'weight' : 'normal',
	'size'   : 120,
	}


	# date = ds['date'].values
	# map = ds['map'].values
	mod = ds['MOD_LAI'].values
	opt = ds['RF_LAI'].values
	obs = ds2['Map_LAI'][0:276].values
	# qc = ds['qc_max'].values

	# lc = lcf.loc[lcf['site']==sites[i],'lc'].values[0]
	lc = info['lc'][i]
	print("\n",info['site'][i],lc)

	# fig=plt.figure(figsize=(20, 5))

	# ax = plt.gca()
	# plt.grid()
	if (i==0):
		ax.spines['bottom'].set_visible(False)
		plt.subplots_adjust(hspace=0.05)
	if (i>0 and i<3):
		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		plt.subplots_adjust(hspace=0.05)
	if (i==3):
		ax.spines['top'].set_visible(False)
		ax.spines['bottom'].set_visible(True)
		plt.subplots_adjust(hspace=0.05)

	if (i>3):
		ax.spines['top'].set_visible(True)
		ax.spines['bottom'].set_visible(True)
		plt.subplots_adjust(hspace=0.05)

	# if (i!=0):
	ax.set_title(u'%s %s, Lat: %s, Lon: %s' %(subtitle[i], info['site'][i],info['LatFmt'][i], info['LonFmt'][i]), fontproperties='DejaVu Sans',fontsize=95,y=0.92, x=0.27, va="top")
	# ax.set_xlabel('Year',font2)
	if (i==2):
		ax.set_ylabel('LAI($m^2/m^2$)',font2)   #  $m^3s^{-1}$

	# xx = range(0,nyear*12,6)
	# x  = ['2000-01','2000-07','2001-01','2001-07','2002-01','2002-07','2003-01','2003-07',\
	# '2004-01','2004-07','2005-01','2005-07', '2006-01','2006-07','2007-01','2007-07',\
	# '2008-01','2008-07','2009-01','2009-07','2010-01','2010-07','2011-01', '2011-07',\
	# '2012-01','2012-07','2013-01','2013-07','2014-01','2014-07','2015-01','2015-07',\
	# '2016-01','2016-07','2017-01','2017-07','2018-01','2018-07','2019-01','2019-07',\
	# '2020-01','2020-07']#,'2021-01','2021-07']

	if (i>=3):
		xx = range(0,nyear*12,12)
		print(xx)
		# x  = ['2000-01','2001-01','2002-01','2003-01',\
		# '2004-01','2005-01', '2006-01','2007-01',\
		# '2008-01','2009-01','2010-01','2011-01',\
		# '2012-01','2013-01','2014-01','2015-01',\
		# '2016-01','2017-01','2018-01','2019-01',\
		# '2020-01']
		x  = ['2000','2001','2002','2003',\
		'2004','2005', '2006','2007',\
		'2008','2009','2010','2011',\
		'2012','2013','2014','2015',\
		'2016','2017','2018','2019',\
		'2020','2021','2022']

		plt.xticks(xx, x)
		# plt.xticks(rotation=45, ha='center',fontsize=55)
		ax.tick_params(axis='x',which='major',labelsize=90,direction='in',width=5,length=30,top=False)
		ax.tick_params(axis='x',which='minor',labelsize=90,direction='in',width=5,length=20,top=False)
		ax.xaxis.set_minor_locator(MultipleLocator(3))
	else:
		ax.xaxis.set_major_locator(plt.NullLocator())
	# 	xx = range(0,nyear*12,12)
	# 	# print(xx)
	# 	x  = [' ',' ',' ',' ',\
	# 	' ',' ', ' ',' ',\
	# 	' ',' ',' ',' ',\
	# 	' ',' ',' ',' ',\
	# 	' ',' ',' ',' ',\
	# 	' ']

	# 	plt.xticks(xx, x)
	# 	plt.xticks(rotation=45, ha='center',fontsize=30)
	# 	ax.tick_params(axis='x',which='major',labelsize=30,direction='in',width=2.5,length=10)
	# 	ax.tick_params(axis='x',which='minor',labelsize=30,direction='in',width=1.5,length=5)
	# 	ax.xaxis.set_minor_locator(MultipleLocator(3))
	# 	ax.set_xlabel(' ',font2)

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
	# plt.plot(range(nyear*12),opt, label='RF LAI',c='#f5688a',linewidth = '8',zorder=1)
	# plt.plot(range(nyear*12),opt, label='RF LAI',c='#ef767a',linewidth = '15',zorder=2, alpha=0.75)
	plt.plot(range(nyear*12),opt, label='RF LAI',c=rf_c,linewidth = '15',zorder=2, alpha=0.75)
	plt.scatter(range(nyear*12),obs, marker="^",s=dotsize,c='#456990',label='LAI reference map',zorder=3)

	# if (i==0):
	# 	ax.legend(loc='lower right',fontsize=55)
	# 	ii+=1
	# if np.count_nonzero(~np.isnan(map))<20:
	# 	dotsize = 400
	# else:
	# 	dotsize = 35
	# plt.scatter(range(120),map, marker="^",s=dotsize,c='g',label='LAI reference map',zorder=3)
	# plt.legend(bbox_to_anchor=(1.05, 0),loc=3,borderaxespad=0, fontsize=25)


	# qc------------------------------------------------------------------
	# types = [1,2,3,4,5]
	# colors = ["skyblue", "pink", "red", "yellow", "gray"]
	# labels = ['Main','With cloud','With saturation', 'Back-up','Unretrieved']
	# ds['xf'] = range(1012)

	plt.xlim(-2.5,nyear*12+0.5)
	plt.ylim(-0.7,9)

	# for j in range(len(types) ):
	# 	xt = ds.loc[ds['qc_max']==types[j],'xf'].values
	# 	yt = [np.nanmax(opt)*1.5]*len(xt)

	# 	plt.scatter(xt, yt, s=1000, marker='|', linewidths=1.7, c=colors[j], label=labels[j])
	# 	plt.legend(bbox_to_anchor=(1.01, 0), loc=3, borderaxespad=0,markerscale=0.5,fontsize=16)

	plt.xticks(rotation=45, ha='center',fontsize=90)
	plt.yticks(fontsize=95)
	for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_linewidth(4.5)

	# plt.show()
	# plt.savefig('./Plot_sma/%s.png' % info['site'][i], format='png', bbox_inches='tight')
	# plt.savefig('./Plot/%s.pdf' % sites[i],  format='pdf', bbox_inches='tight')
	# plt.close()
fig.subplots_adjust(hspace=0.05)
fig.suptitle('Evergreen Needleleaved Tree', fontproperties='DejaVu Sans',fontsize=120)
# fig.tight_layout()
fig.subplots_adjust(top=0.95)
plt.savefig('./Plot_sma/NET.png', format='png', bbox_inches='tight')
