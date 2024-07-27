# -*- coding: utf-8 -*-
"""

@author: Wenzong Dong

"""

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import scienceplots
from matplotlib.ticker import MultipleLocator
from sklearn.metrics import mean_squared_error
from math import sqrt
import pandas as pd
import scienceplots
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap

# plt.style.use(['science','no-latex', 'retro'])
plt.rc('font', family='DejaVu Sans')

# Step 1: Read the NCL RGB file and extract RGB color values
rgb_file = "./colormap/blue_red.rgb"  # Replace with the path to your NCL RGB file
with open(rgb_file, "r") as file:
    lines = file.readlines()

rgb_data = []
for line in lines:
    if line.strip() and not line.startswith("#"):
        rgb_values = line.split()
        rgb_data.append([float(rgb_values[0]), float(rgb_values[1]), float(rgb_values[2])])

# Step 2: Normalize the color values to the range [0, 1]
norm_rgb_data = np.array(rgb_data) / 255.0

# Step 3: Create a custom colormap using the normalized color values
cmap = LinearSegmentedColormap.from_list('custom_colormap', norm_rgb_data, N=len(norm_rgb_data))

def vionlin(mod_p,rf_p, ax):
    mod = xr.open_dataset(mod_p)
    rf  = xr.open_dataset(rf_p)

    # Extract the data variable from both files
    mod_lai = mod["URBAN_TREE_LAI"][:,:,:,:]
    rf_lai  = rf ["URBAN_TREE_LAI"][:,:,:,:]

    mod_lai = xr.where(mod_lai==0,np.nan,mod_lai)
    rf_lai = xr.where(rf_lai==0,np.nan,rf_lai)

    reshaped_mod = mod_lai.values.reshape((7, -1)).T  # Transpose to have 7 columns
    reshaped_rf  = rf_lai.values.reshape((7, -1)).T  # Transpose to have 7 columns

    reshaped_mod1= np.zeros((3110400,6),dtype=float)
    reshaped_rf1 = np.zeros((3110400,6),dtype=float)

    reshaped_mod1[:,0:5]= reshaped_mod[:,0:5]
    reshaped_mod1[:,5]= reshaped_mod[:,6]
    reshaped_rf1[:,0:5]= reshaped_rf[:,0:5]
    reshaped_rf1[:,5]= reshaped_rf[:,6]

    columns = ['NET', 'BET', 'NDT', 'BDT', 'MF', 'Grid Tree']
    # Create a DataFrame for seaborn
    df1 = pd.DataFrame(reshaped_mod1, columns=columns)
    df1['Dataset'] = 'MODIS LAI'

    df2 = pd.DataFrame(reshaped_rf1, columns=columns)
    df2['Dataset'] = 'RF LAI'

    # Combine the datasets
    df = pd.concat([df1, df2])
    plt.ylim(-0.5,8.2)
    x1 = [0, 1, 2, 3, 4, 5]
    x1_label = ['NET', 'BET', 'NDT', 'BDT', 'MF', 'Grid Tree']

    ax.set_xticks(ticks=x1)
    ax.tick_params(axis='x',which='major',labelsize=35,direction='in',width=2.5,length=10,top=False, right=False)

    y1 = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    y1_label = ['0', '1', '2', '3', '4', '5', '6', '7', '8']

    ax.set_yticks(ticks=y1)
    plt.yticks(y1,y1_label, fontsize=40)
    ax.tick_params(axis='y',which='major',labelsize=40,direction='in',width=2.5,length=10,top=False, right=False)

    sns.violinplot(x="variable", y="value", hue="Dataset", inner="quartile",split=True, linewidth=2.5, data=df.melt(id_vars="Dataset"))

    plt.legend(fontsize=30)
    plt.xlim(-0.5,6.5)

    # Add labels and title
    plt.xlabel("Land Cover Type", fontsize=40)
    plt.ylabel("LAI (m$^2$/m$^2$)", fontsize=40)
    plt.title("(B) Violin Plot for MODIS and RF LAI", fontsize=40, loc='left')

    for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_linewidth(3)


def bin_count(mod_p, rf_p, ax, fig):
    igbp_tile = ["NET","BET","NDT","BDT","MF","Urban","Grid Tree"]

    modis = xr.open_dataset(mod_p)
    rf    = xr.open_dataset(rf_p)

    for ilc in range(6,7):
        rf_lai = rf    ['URBAN_TREE_LAI'][ilc,:,:,:]
        mod_lai= modis ['URBAN_TREE_LAI'][ilc,:,:,:]

        rf_lai_ = rf_lai
        mod_lai_= mod_lai

        # Flatten the data for density scatter plot
        rf_lai_flatten = rf_lai_.values.flatten()
        mod_lai_flatten = mod_lai_.values.flatten()

        # Remove NaN and infinity values
        valid_indices = ~np.isnan(rf_lai_flatten) & ~np.isinf(rf_lai_flatten) & (rf_lai_flatten>0) & ~np.isnan(mod_lai_flatten) & ~np.isinf(mod_lai_flatten) & (mod_lai_flatten>0)
        rf_lai_flatten = rf_lai_flatten[valid_indices]
        mod_lai_flatten = mod_lai_flatten[valid_indices]

        # Create a binned scatter plot with the custom colormap
        hb = plt.hexbin(mod_lai_flatten, rf_lai_flatten, gridsize=70, bins='log', cmap=cmap)
        plt.xlim(-0.5,7.1)
        plt.ylim(-0.5,7.1)

        x = [0, 1, 2, 3, 4, 5, 6, 7]
        x_label= ['0', '1', '2', '3', '4', '5', '6', '7']
        ax.set_xticks(ticks=x)
        ax.set_xticklabels(labels=x_label,ha='center',va='top')
        ax.tick_params(axis='x',which='major',labelsize=40,direction='in',width=2.5,length=10,top=False, right=False)
        ax.tick_params(axis='x',which='minor',labelsize=40,direction='in',width=1.5,length=5,top=False, right=False)
        ax.xaxis.set_minor_locator(MultipleLocator(0.2))

        y1 = [0, 1, 2, 3, 4, 5, 6, 7]
        y1_label = ['0', '1', '2', '3', '4', '5', '6', '7']
        ax.yaxis.set_minor_locator(MultipleLocator(0.2))
        ax.set_yticks(ticks=y1)
        plt.yticks(y1,y1_label)

        ax.tick_params(axis='y',which='major',labelsize=40,direction='in',width=2.5,length=10,top=False, right=False)
        ax.tick_params(axis='y',which='minor',labelsize=40,direction='in',width=1.5,length=5,top=False, right=False)

        plt.plot((-0.5,7), (-0.5,7), ls='--', color='k', linewidth =3)

        # Add colorbar
        cb =  fig.colorbar(hb)

        cb.set_label('Counts', fontsize=35)
        cb.ax.tick_params(axis='y',which='major',labelsize=25,direction='in',width=2,length=10,top=False, right=True)
        cb.ax.tick_params(axis='y',which='minor',labelsize=25,direction='in',width=1,length=5,top=False, right=True)
        cb.outline.set_linewidth(2)

        # Set labels and title
        ax.set_xlabel('MODIS LAI (m$^2$/m$^2$)', fontsize=40)
        ax.set_ylabel('RF LAI (m$^2$/m$^2$)', fontsize=40)
        ax.set_title('(A) Grid Tree', fontsize=40, loc='left')

        for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_linewidth(3)

        correlation_matrix = np.corrcoef(rf_lai_flatten, mod_lai_flatten)
        R = correlation_matrix[0, 1]

        # Calculate RMSE
        rmse = sqrt(mean_squared_error(rf_lai_flatten, mod_lai_flatten))
        mbe = np.mean(rf_lai_flatten - mod_lai_flatten)

        # Add text to the plot with the calculated values
        texts = f"R = {R:.2f}\nRMSE = {rmse:.2f}"
        texts += f"\nMBE = {mbe:.2f}"
        x_text = 1.2  # Adjust the x-coordinate of the text
        y_text = 6  # Adjust the y-coordinate of the text

        ax.text(x_text, y_text, texts, ha="center", va="center", fontsize=35, color='k', bbox=dict(facecolor='white', edgecolor='white', boxstyle='round,pad=0.3'))


mod_p = '../nc_data/Global_MODIS_LAI_2020_v61.nc'
rf_p  = '../nc_data/Global_Urban_LAI_2020_v61.nc'

fig = plt.figure(figsize=(35, 12))
ax1 = plt.subplot(1,2,1)
bin_count(mod_p, rf_p, ax1, fig)
ax2 = plt.subplot(1,2,2)
vionlin(mod_p, rf_p, ax2)
plt.savefig('./Plot_Fig5/Fig5.png')
