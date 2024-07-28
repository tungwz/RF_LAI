# Data descrption for netCDF
The data in this file are global monthly LAI used for plotting the Fig5-Fig7 in the manuscript, the data generated from GLSS LAI, reprocessed MODIS LAI and our model, all with a resolution of 0.5°.
Global_GLASS_LAI_0.5deg_2020.nc is the global urban LAI for 2020 derived from the GLASS LAI product. 
Global_MODIS_LAI_YYYY_v61.nc and Global_Urban_LAI_YYYY_v61.nc are derived from reprocessed MODIS LAI and our model predictions, respectively. However, these two datasets include not only urban areas but also LAI for other land types of trees.
**Directory:**
```bash
|—— Global_GLASS_LAI_0.5deg_2020.nc 
|	├── GLASS_LAI        # Monthly LAI drived from 500m 8-day GLASS LAI product 
│   ├── GLASS_LAI_T      # Monthly LAI is derived from the 500m 8-day GLASS LAI product and MODIS VCF data, using the formula LAI = GLASS_LAI/(Tree_percent).
│	├── GLASS_LAI_V      # Monthly LAI is derived from the 500m 8-day GLASS LAI product and MODIS VCF data, using the formula LAI = GLASS_LAI (Tree_percent+Grass_percent).
│	├── PCTT             # Tree percent in urban areas (MODIS VCF)
│   └── VCF              # Sum of tree and grass percent in urban areas (MODIS VCF)
|── Global_MODIS_LAI_YYYY_v61.nc
│   └── URBAN_TREE_LAI   # Monthly LAI drived from reprocessed MODIS LAI product, the dimension of LC from 1 to 7 represents NET, BET, NDT, BDT, MF, Urban and grid tree
└── Global_Urban_LAI_YYYY_v61.nc
    └── URBAN_TREE_LAI   # Monthly LAI drived from RF LAI product, the dimension of LC from 1 to 7 represents NET, BET, NDT, BDT, MF, Urban and grid tree
```
