import xarray as xr
import numpy as np
import pandas as pd

# Function to calculate R and RMSE
def calculate_metrics(var1, var2):
    # Calculate correlation coefficient (R)
    correlation_coefficient = np.corrcoef(var1, var2)[0, 1]

    # Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(np.mean((var1 - var2)**2))

    return correlation_coefficient, rmse

# Initialize dictionaries to store R and RMSE for each year and month
r_dict = {year: [] for year in range(2000, 2023)}
rmse_dict = {year: [] for year in range(2000, 2023)}

for i in range(2000, 2023):
    print('Processing ' + str(i))
    path = '/tera10/yuanhua/dongwz/RF_LAI/MOD_LAI/C61/global_0.5/'
    rf_file = path + 'Global_Urban_LAI_' + str(i) + '_v61.nc'
    mod_file = path + 'Global_MODIS_LAI_' + str(i) + '_v61.nc'

    data1 = xr.open_dataset(rf_file)
    data2 = xr.open_dataset(mod_file)

    for imon in range(12):
        var1 = data1['URBAN_TREE_LAI'][6, imon, :, :]
        var2 = data2['URBAN_TREE_LAI'][6, imon, :, :]

        rflai = np.array(var1).flatten()
        modlai = np.array(var2).flatten()
        nan_mask = np.isnan(rflai)
        rf_mask = rflai[~nan_mask]
        mod_mask = modlai[~nan_mask]

        r, rmse = calculate_metrics(rf_mask, mod_mask)
        r_dict[i].append(r)
        rmse_dict[i].append(rmse)
        print(r)

# Create DataFrames from the dictionaries
r_df = pd.DataFrame(r_dict)
rmse_df = pd.DataFrame(rmse_dict)

# Add month row as the first row
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
r_df.insert(0, '', months)
rmse_df.insert(0, '', months)

# Save results to CSV
r_df.to_csv('R_results.csv', index=False)
rmse_df.to_csv('RMSE_results.csv', index=False)

