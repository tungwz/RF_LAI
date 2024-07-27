# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import netCDF4 as nc4
import xarray as xr
from math import sqrt
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from flaml import AutoML
import multiprocessing as mp

def remap(in_array, out_array):
    out_array[::2,::2]  = in_array[:,:]
    out_array[1::2,::2] = in_array[:,:]
    out_array[::2,1::2] = in_array[:,:]
    out_array[1::2,1::2]= in_array[:,:]

    return out_array

def load_train_data(reg, iyear, imon):

    loop_i = 0

    for i in reg:
        mod    = 'RG_'+str(int(i[0]))+'_'+str(int(i[1]))+'_'+str(int(i[2]))+'_' \
                  +str(int(i[3]))+'.MOD'+str(iyear)+'.nc'
        mod_nc = nc4.Dataset('/tera10/yuanhua/dongwz/mksrf/srf_5x5/'+mod)
        lc     = mod_nc['LC'][:,:].flatten()

        if np.any(lc==13):
            lai = mod_nc['MONTHLY_LC_LAI'][imon,:,:].flatten()
            lat_= mod_nc['lat'][:]
            lon_= mod_nc['lon'][:]

            lat = np.repeat(np.array(lat_[:,np.newaxis]),1200,axis=1)
            lon = np.repeat(np.array(lon_[np.newaxis,:]),1200,axis=0)

            lat = lat.flatten()
            lon = lon.flatten()

            eth   = 'RG_'+str(int(i[0]))+'_'+str(int(i[1]))+'_'+str(int(i[2]))+'_'+str(int(i[3]))+'.ETH_2015.nc'
            eth_nc= nc4.Dataset('/stu01/dongwz/urban_data/urban_raw/ETH_HTOP/30m/2015/'+eth)
            htop  = eth_nc['ETH_HTOP'][:,:].flatten()

            raw = 'RG_'+str(int(i[0]))+'_'+str(int(i[1]))+'_'+str(int(i[2]))+'_'+str(int(i[3]))+'.RAW'+str(iyear)+'.nc'
            vpp = 'RG_'+str(int(i[0]))+'_'+str(int(i[1]))+'_'+str(int(i[2]))+'_'+str(int(i[3]))+'.VP.nc'
            sww = 'RG_'+str(int(i[0]))+'_'+str(int(i[1]))+'_'+str(int(i[2]))+'_'+str(int(i[3]))+'.SW.nc'

            raw_nc = nc4.Dataset('/tera12/yuanhua/mksrf/raw_5x5/'+raw)
            vp_nc  = nc4.Dataset('/stu01/dongwz/hard/forcing/meteor/vp/raw/VP_5x5/'+vpp)
            sw_nc  = nc4.Dataset('/stu01/dongwz/hard/forcing/meteor/sw/raw/SW_5x5/'+sww)

            stmax = raw_nc['TMAX'][imon,:,:]
            stmin = raw_nc['TMIN'][imon,:,:]
            sprec = raw_nc['PREC'][imon,:,:]
            svp   = vp_nc ['Band1'][imon,:,:]
            ssw   = sw_nc ['Band1'][imon,:,:]

            ltmax = np.zeros((1200,1200), dtype=float)
            ltmin = np.zeros((1200,1200), dtype=float)
            lprec = np.zeros((1200,1200), dtype=float)
            lvp   = np.zeros((1200,1200), dtype=float)
            lsw   = np.zeros((1200,1200), dtype=float)

            tmax = remap(stmax, ltmax).flatten()
            tmin = remap(stmin, ltmin).flatten()
            prec = remap(sprec, lprec).flatten()
            vp   = remap(svp  , lvp  ).flatten()
            sw   = remap(ssw  , lsw  ).flatten()

            vpd = 1/2*0.6108*(np.exp((17.269*tmax)/(237.3+tmax))+np.exp((17.269*tmin)/(237.3+tmin))) - vp
            sw  = sw*1000/86400

            vp  [lc==0] = 0
            sw  [lc==0] = 0
            tmax[lc==0] = 0
            tmin[lc==0] = 0
            prec[lc==0] = 0

            valid_indices = np.where((lai > 0) & (htop > 0) & ((lc == 1) | (lc == 2) | (lc == 3) | (lc == 4) | (lc == 5)))
            lai_reg = lai [valid_indices]
            htop_reg= htop[valid_indices]
            tmax_reg= tmax[valid_indices]
            tmin_reg= tmin[valid_indices]
            prec_reg= prec[valid_indices]
            vp_reg  = vp  [valid_indices]
            vpd_reg = vpd [valid_indices]
            sw_reg  = sw  [valid_indices]
            lat_reg = lat [valid_indices]
            lon_reg = lon [valid_indices]

            # print(len(valid_indices[0]))
            if len(valid_indices[0])>=10:
                # with part of meteorological vars but exclude DEM
                var  = np.array((lai_reg, htop_reg, tmax_reg, tmin_reg, prec_reg, sw_reg, vp_reg, vpd_reg))
                data = pd.DataFrame(var.T, columns=['lai','htop','tmax','tmin','pre','sw','vp', 'vpd'])

                # Split for traning and test data...
                x,y = data.iloc[:,1:].values,data.iloc[:,0].values.reshape(-1,1)
                x_train_,x_test_,y_train_,y_test_ = train_test_split(x,y,test_size=0.90,random_state=0)

                if loop_i==0:
                    x_train = x_train_
                    x_test  = x_test_
                    y_train = y_train_
                    y_test  = y_test_
                    loop_i += 1
                else:
                    x_train = np.concatenate((x_train,x_train_), axis=0)
                    x_test  = np.concatenate((x_test,x_test_), axis=0)
                    y_train = np.concatenate((y_train,y_train_), axis=0)
                    y_test  = np.concatenate((y_test,y_test_), axis=0)

    return x_train, x_test, y_train, y_test

def load_predict_data(reg, iyear, imon):

    mod    = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_' \
              +str(int(reg[3]))+'.MOD'+str(iyear)+'.nc'
    mod_nc = nc4.Dataset('/tera10/yuanhua/dongwz/mksrf/srf_5x5/'+mod)
    lc     = mod_nc['LC'][:,:].flatten()
    lat    = mod_nc['lat'][:]
    lon    = mod_nc['lon'][:]

    if (iyear>=2000 and iyear<2005):
        eth   = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.ETH_2000.nc'
        eth_nc= nc4.Dataset('/stu01/dongwz/urban_data/urban_raw/ETH_HTOP/30m/2000/'+eth)
    elif(iyear>=2005 and iyear<2010):
        eth   = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.ETH_2005.nc'
        eth_nc= nc4.Dataset('/stu01/dongwz/urban_data/urban_raw/ETH_HTOP/30m/2005/'+eth)
    elif(iyear>=2010 and iyear<2015):
        eth   = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.ETH_2010.nc'
        eth_nc= nc4.Dataset('/stu01/dongwz/urban_data/urban_raw/ETH_HTOP/30m/2010/'+eth)
    elif(iyear>=2015):
        eth   = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.ETH_2015.nc'
        eth_nc= nc4.Dataset('/stu01/dongwz/urban_data/urban_raw/ETH_HTOP/30m/2015/'+eth)

    htop  = eth_nc['ETH_HTOP'][:,:].flatten()

    raw = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.RAW'+str(iyear)+'.nc'
    vpp = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.VP.nc'
    sww = 'RG_'+str(int(reg[0]))+'_'+str(int(reg[1]))+'_'+str(int(reg[2]))+'_'+str(int(reg[3]))+'.SW.nc'

    raw_nc = nc4.Dataset('/tera12/yuanhua/mksrf/raw_5x5/'+raw)
    vp_nc  = nc4.Dataset('/stu01/dongwz/hard/forcing/meteor/vp/raw/VP_5x5/'+vpp)
    sw_nc  = nc4.Dataset('/stu01/dongwz/hard/forcing/meteor/sw/raw/SW_5x5/'+sww)

    stmax = raw_nc['TMAX'][imon,:,:]
    stmin = raw_nc['TMIN'][imon,:,:]
    sprec = raw_nc['PREC'][imon,:,:]
    svp   = vp_nc ['Band1'][imon,:,:]
    ssw   = sw_nc ['Band1'][imon,:,:]

    ltmax = np.zeros((1200,1200), dtype=float)
    ltmin = np.zeros((1200,1200), dtype=float)
    lprec = np.zeros((1200,1200), dtype=float)
    lvp   = np.zeros((1200,1200), dtype=float)
    lsw   = np.zeros((1200,1200), dtype=float)

    tmax = remap(stmax, ltmax).flatten()
    tmin = remap(stmin, ltmin).flatten()
    prec = remap(sprec, lprec).flatten()
    vp   = remap(svp  , lvp  ).flatten()
    sw   = remap(ssw  , lsw  ).flatten()

    vpd = 1/2*0.6108*(np.exp((17.269*tmax)/(237.3+tmax))+np.exp((17.269*tmin)/(237.3+tmin))) - vp
    sw  = sw*1000/86400

    vp  [lc==0] = 0
    sw  [lc==0] = 0
    tmax[lc==0] = 0
    tmin[lc==0] = 0
    prec[lc==0] = 0

    return lc, lat, lon, htop, tmax, tmin, prec, vp, sw, vpd #, lat_, lon_

def process_region(ireg):
    reg_lc, reg_lat, reg_lon, reg_htop, reg_tmax, reg_tmin, reg_prec, reg_vp, reg_sw, reg_vpd = load_predict_data(ireg, iyear, i)

    reg_var  = np.array((reg_htop, reg_tmax, reg_tmin, reg_prec, reg_sw, reg_vp, reg_vpd)).T

    reg_pre = automl.predict(reg_var).reshape(1200,1200)

    reg_pre[reg_lc.reshape(1200,1200)==0 ]=0
    reg_pre[reg_lc.reshape(1200,1200)==16]=0
    reg_pre[reg_lc.reshape(1200,1200)==17]=0
    reg_pre[reg_htop.reshape(1200,1200)<=0]=0

    dataset = xr.Dataset(data_vars={'LAI': (('lat', 'lon'), reg_pre)},
                         coords={'lat': reg_lat,
                                 'lon': reg_lon})
    encoding= {}
    encoding['LAI'] = {'zlib': True, 'complevel': 6}
    dataset.to_netcdf('LAI_'+str(iyear)+'/RG_'+str(int(ireg[0]))+'_'+str(int(ireg[1]))+'_'+str(int(ireg[2]))+'_' \
      +str(int(ireg[3]))+'.UrbLAI_'+str(iyear)+'_'+str(i+1).zfill(2)+'.nc', encoding=encoding)
    dataset.close()


reg_ = np.loadtxt('reg_5x5')

r2  = np.zeros((12,1), dtype=float)
rmse= np.zeros((12,1), dtype=float)
mae = np.zeros((12,1), dtype=float)

# loop for iyear
for iyear in range(2000,2021,1):

    print('Processing for '+str(iyear)+' ......')
    reg = np.loadtxt('reg_5x5_'+str(iyear))

    for i in range(12):
        print('Regressing '+' month '+str(i+1))

        x_train, x_test, y_train, y_test = load_train_data(reg, iyear, i)

        automl = AutoML()

        setting = {
            "time_budget":1800,
            "metric": 'rmse',
            "task": 'regression',
            "estimator_list": ['rf'],
        }

        print('Traning for AutoML Regressor...')
        automl.fit(x_train, y_train, **setting)
        print('Best ML model:', automl.model)
        print('Best hyperparameter config:', automl.best_config)
        print('Importance ', automl.model.estimator.feature_importances_)
        train_pre = automl.predict(x_train)
        test_pre  = automl.predict(x_test )

        r2  [i,0] = r2_score(y_test, test_pre)
        rmse[i,0] = sqrt(mean_squared_error(y_test, test_pre))
        mae [i,0] = mean_absolute_error(y_test, test_pre)

        print(" Train r2_score is %f, RMSE is %f, MAE is %f" %(r2_score(y_train, train_pre),sqrt(mean_squared_error(y_train, train_pre)),mean_absolute_error(y_train, train_pre)))
        print(" Test r2_score is %f, RMSE is %f, MAE is %f" %(r2_score(y_test, test_pre), sqrt(mean_squared_error(y_test, test_pre)),mean_absolute_error(y_test, test_pre)))

        num_processes = 50
        pool = mp.Pool(processes=num_processes)

        pool.map(process_region, reg_)

        pool.close()
        pool.join()
