# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import scienceplots

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

nyear   = 1
csv_dir = "./Timecsv"
info = pd.read_excel("./Select_Site.xlsx")

ii = 0

subtitle=['(A)','(B)','(C)','(D)','(E)','(F)','(G)','(H)','(I)','(J)','(K)','(L)','(M)','(N)','(O)','(P)','(Q)','(R)','(S)','(T)']
# fig=plt.figure(figsize=(40, 70))
for i in range(len(info['site'])):
	# ax = plt.subplot(20,4,i+1)
	ds = pd.read_csv('./Timecsv/%s.csv' % info['site'][i])
	ds2= pd.read_csv('./Timecsv/%s_glass.csv' % info['site'][i])

	font2 = {
	'weight' : 'normal',
	'size'   : 25,
	}

	mod = ds['MOD_LAI'].values
	opt = ds['RF_LAI'].values
	sai = ds['SAI'].values
	gla = ds2['GLASS_LAI'].values

	lai_8day_df = pd.DataFrame({'GLASS_LAI': gla}, index=pd.date_range(start='2020-01-01', end='2020-12-31', freq='8D'))

	# Resample the 8-day LAI dataset to monthly frequency
	gla_m = lai_8day_df.resample('M').mean()

	lc = info['FCS30'][i]
	print("\n",info['site'][i],lc)


	fig=plt.figure(figsize=(10, 5))
	ax = plt.gca()

	ax.set_title(u'%s, %s' %(info['site'][i],lc), fontproperties='DejaVu Sans',fontsize=25, loc='left')

	ax.set_ylabel('LAI/SAI($m^2/m^2$)',font2)   #  $m^3s^{-1}$

	if (i>=0):
		xx = range(0,nyear*12,1)
		# print(xx)
		x = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

		plt.xticks(xx, x)
		plt.xticks(rotation=45, ha='center',fontsize=25)
		ax.tick_params(axis='x',which='major',labelsize=25,direction='in',width=2,length=10)
		ax.xaxis.set_minor_locator(MultipleLocator(1))
		ax.set_xlabel(' ',font2)
	else:
		xx = range(0,nyear*12,1)
		x = [' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']

		plt.xticks(xx, x)
		plt.xticks(rotation=45, ha='center',fontsize=25)
		ax.tick_params(axis='x',which='major',labelsize=25,direction='in',width=2,length=10)
		ax.xaxis.set_minor_locator(MultipleLocator(1))
		ax.set_xlabel(' ',font2)

	y = range(0,9,2)
	y_label = [iy for iy in range(0,9,2)]
	ax.tick_params(axis='y',which='major',labelsize=25,direction='in',width=2,length=8)
	ax.tick_params(axis='y',which='minor',labelsize=25,direction='in',width=1,length=4)
	ax.yaxis.set_minor_locator(MultipleLocator(0.5))
	ax.set_yticks(ticks=y)
	plt.yticks(y,y_label)

	plt.yticks(fontsize=25)
	plt.tick_params(labelsize=20,top='on', right='on', which='both')

	dotsize = 200

	plt.plot(range(nyear*12),opt, label='RF LAI',c='#B11927',linewidth = '4',zorder=1)
	plt.plot(range(nyear*12),sai, label='SAI',c='#ef767a',linewidth = '4',zorder=1)
	plt.plot(range(nyear*12),gla_m, label='GLASS LAI',c='#456990',linewidth = '4',zorder=1)


	if (ii==0):
		plt.legend(fontsize=25)
		ii = 1

	plt.xlim(-1,nyear*12+0.5)
	plt.ylim(-0.7,8.5)

	plt.xticks(rotation=45, ha='center',fontsize=25)
	plt.yticks(fontsize=25)
	for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_linewidth(2.5)

	plt.savefig('./Plot/%s.png' % info['site'][i], format='png', bbox_inches='tight')
	plt.close()

