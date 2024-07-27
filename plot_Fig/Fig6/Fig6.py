# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scienceplots

plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')
data1 = pd.read_csv('./R_results.csv', header=0,index_col=0)
data2 = pd.read_csv('./RMSE_results.csv', header=0,index_col=0)
df1   = pd.DataFrame(data1)
df2   = pd.DataFrame(data2)
# print(data)

#rc = {'font.sans-serif': 'SimHei',
#      'axes.unicode_minus': False}
sns.set(font_scale=3.7)#, rc=rc)  # 设置字体大小

fig=plt.figure(figsize=(65, 75))

ax = plt.subplot(2,1,1)
ax.set_title('(A) R', fontsize=65, loc='left')
heatmap=sns.heatmap(df1,
            annot=True,
            #center=0.5,
            fmt='.2f',
            linewidth=3,
            linecolor='white',
            # vmin=0, vmax=1,
            vmin=0.9, vmax=1,
            xticklabels=True, yticklabels=True,
            square=True,
            cbar=True,
            cmap=sns.cubehelix_palette(start=.5, rot=-.75, as_cmap=True),
            # cbar_kws={'shrink': 0.8, 'alpha': 10,'ticks': [0, 0.2, 0.4, 0.6, 0.8, 1]}
            # cbar_kws={'shrink': 0.8, 'alpha': 10,'ticks': [0.8, 0.85, 0.90, 0.95, 1]}
            cbar_kws={'shrink': 0.8, 'alpha': 10,'ticks': [0.9, 0.92, 0.94, 0.96, 0.98, 1]}
            )
ylabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
xlabels = [str(i) for i in range(2000,2023)]
heatmap.set_xticklabels(xlabels, rotation=90, fontsize=55)
heatmap.set_yticklabels(ylabels, rotation=0, fontsize=55)
heatmap.collections[0].colorbar.ax.tick_params(axis='y',which='minor',labelsize=55,length=18, width=4)
heatmap.collections[0].colorbar.ax.tick_params(axis='y',which='major',labelsize=55,length=20, width=5)
heatmap.collections[0].colorbar.ax.set_ylabel(ylabel='R',size=65)
# heatmap.collections[0].colorbar.ax.set_ylabel(ylabel='RMSE(m$^2$/m$^2$)',size=5,loc='center')
# plt.subplots_adjust(bottom=0.8)
# plt.tight_layout()
for text in heatmap.texts:
    value = float(text.get_text())
    if (value<0.95):
        text.set_color('black')

ax = plt.subplot(2,1,2)
ax.set_title('(B) RMSE', fontsize=65, loc='left')
heatmap=sns.heatmap(df2,
            annot=True,
            #center=0.5,
            fmt='.2f',
            linewidth=3,
            linecolor='white',
            vmin=0.4, vmax=0.8,
            # vmin=0.8, vmax=1,
            xticklabels=True, yticklabels=True,
            square=True,
            cbar=True,
            cmap=sns.color_palette("rocket_r", as_cmap=True),
            # cbar_kws={'shrink': 0.8, 'alpha': 10,'ticks': [0, 0.2, 0.4, 0.6, 0.8, 1]}
            # cbar_kws={'shrink': 0.8, 'alpha': 10,'ticks': [0.8, 0.85, 0.90, 0.95, 1]}
            cbar_kws={'shrink': 0.8, 'alpha': 10,'ticks': [0.4, 0.5, 0.6, 0.7, 0.8]}
            )

ylabels = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
xlabels = [str(i) for i in range(2000,2023)]
heatmap.set_xticklabels(xlabels, rotation=90, fontsize=55)
heatmap.set_yticklabels(ylabels, rotation=0, fontsize=55)
heatmap.collections[0].colorbar.ax.tick_params(axis='y',which='minor',labelsize=55,length=18, width=4)
heatmap.collections[0].colorbar.ax.tick_params(axis='y',which='major',labelsize=55,length=20, width=5)
# heatmap.collections[0].colorbar.ax.set_ylabel(ylabel='R',size=5)
heatmap.collections[0].colorbar.ax.set_ylabel(ylabel='RMSE(m$^2$/m$^2$)',size=65,loc='center')

# for text in heatmap.texts:
#     value = float(text.get_text())
#     if (value<0.6):
#         text.set_color('black')
# plt.savefig("R_heatmap.png", dpi=400)
# fig.tight_layout()
plt.savefig("Plot_Fig6/Fig6.png")
plt.ion()
plt.close('all')
