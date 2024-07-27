import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Patch
import netCDF4 as nc4
import numpy as np
import os
import scienceplots
from matplotlib import cm
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from matplotlib.patches import Circle
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap

plt.style.use(['science','no-latex', 'retro'])
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

projection = ccrs.PlateCarree()

fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(15, 10))

ax.add_feature(cfeature.LAND, edgecolor='lightgray', facecolor='lightgray')
ax.add_feature(cfeature.COASTLINE.with_scale('10m'),linewidth=0.25)
ax.add_feature(cfeature.BORDERS.with_scale('10m'), linewidth=0.2, color='grey')
# ax.gridlines(draw_labels=True, linewidth=1.5, color='gray', alpha=0.5, linestyle='--')

gl = ax.gridlines(crs=projection, draw_labels=["bottom","left"], linewidth=1.5, color='gray', alpha=0.5, linestyle='--')
gl.xlabels_top = False
# gl.ylabels_left = True
gl.ylabels_right = False
gl.xlabel_style = {'size': 15}  # Set the size of longitude labels
gl.ylabel_style = {'size': 15}  # Set the size of latitude labels
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER

# Add custom polygon patch for Arctic region
antarctic_polygon = Polygon([(-180, -90), (180, -90), (180, -66.33), (-180, -66.33)], facecolor='white', edgecolor='none', transform=ccrs.PlateCarree())
ax.add_patch(antarctic_polygon)

for spine in ax.spines.values():
    spine.set_linewidth(2)

nurb = 0
color = cmap(np.linspace(0, 1, 144000))
for reglat in range(90,-90,-5):
    for reglon in range(-180,180,5):

        reg_slat = reglat
        reg_elat = reglat - 5
        reg_slon = reglon
        reg_elon = reglon + 5
        reg_mod   = 'RG_'+str(reg_slat)+'_'+str(reg_slon)+'_'+str(reg_elat)+'_'+str(reg_elon)+'.MOD2020.nc'

        if os.path.exists('/tera10/yuanhua/dongwz/mksrf/srf_5x5/'+str(reg_mod)):
            reg_eth= 'RG_'+str(reg_slat)+'_'+str(reg_slon)+'_'+str(reg_elat)+'_'+str(reg_elon)+'.ETH.nc'

            mod_nc = nc4.Dataset('/tera10/yuanhua/dongwz/mksrf/srf_5x5/'+str(reg_mod))
            eth_nc = nc4.Dataset('/stu01/dongwz/urban_data/urban_raw/urban_5x5/ETH_5x5_/'+str(reg_eth))
            urb    = mod_nc['PCT_URBAN'][:,:]
            lc     = mod_nc['LC'][:,:].flatten()
            lai    = mod_nc['MONTHLY_LC_LAI'][5,:,:].flatten()
            htop   = eth_nc['ETH_htop'][:,:].flatten()

            if np.any(urb>0):
                valid_indices = np.where((lai>0) & (htop>0) & ((lc==1) | (lc==2) | (lc==3) | (lc==4) | (lc==5)))

                if (len(valid_indices[0])>=10):
                    print('Processing '+str(reg_mod))

                    nurb+= 1
                    lon1 = reg_slon
                    lon2 = reg_elon
                    lat1 = reg_elat
                    lat2 = reg_slat

                    val   = int(len(valid_indices[0])*0.1)
                    print(val)

                    ax.add_patch(Circle(xy=(np.mean([lon1, lon2]), np.mean([lat1, lat2])), radius=2, color=color[val], transform=projection))
                    # ax.fill_between([lon1, lon2], lat1, lat2, color=color[val], alpha=0.5, linewidth=0, edgecolor='white', interpolate=True)
            else:
                lon1 = reg_slon
                lon2 = reg_elon
                lat1 = reg_elat
                lat2 = reg_slat

                # ax.fill_between([lon1, lon2], lat1, lat2, color='green', alpha=0.5)

ax.set_extent([-180, 180, -90, 90], crs=projection)

# cmap = cm.jet
print(len(color))
norm = plt.Normalize(0, len(color))
cb = plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, orientation='vertical',shrink=0.75)
cb.ax.tick_params(axis='y',which='major',labelsize=15,direction='in',width=1,length=8,top=False, right=True)
cb.ax.tick_params(axis='y',which='minor',labelsize=15,direction='in',width=0.5,length=4,top=False, right=True)
cb.set_label('Data Numbers of Valid Regions', fontsize=20)
cb.outline.set_linewidth(1.5)

ax.set_title('Training Region For Meachine Learning', fontsize=25)

plt.tight_layout()

plt.savefig('region.png', format='png')
plt.show()