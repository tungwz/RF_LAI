# Data descrption for netCDF
The data in this file are global monthly LAI used for plotting the Fig5-Fig7 in the manuscript, the data generated from GLSS LAI, reprocessed MODIS LAI and our model, all with a resolution of 0.5°.

**GLASS LAI:**

Global_GLASS_LAI_0.5deg_2020.nc is the global urban LAI for 2020 derived from the GLASS LAI product. 
<br>

**Reprocessed MODIS LAI and RF LAI:**

Global_MODIS_LAI_YYYY_v61.nc and Global_Urban_LAI_YYYY_v61.nc are derived from reprocessed MODIS LAI and our model predictions, respectively. However, these two datasets include not only urban areas but also LAI for other land types of trees.
<br>

**Directory:**
```bash
│—— Global_GLASS_LAI_0.5deg_2020.nc 
│    ├── GLASS_LAI        # Monthly LAI drived from 250m 8-day GLASS LAI product 
│    ├── GLASS_LAI_T      # Monthly LAI is derived from the 250m 8-day GLASS LAI product and MODIS VCF data, using the formula LAI = GLASS_LAI/(Tree_percent).
│    ├── GLASS_LAI_V      # Monthly LAI is derived from the 250m 8-day GLASS LAI product and MODIS VCF data, using the formula LAI = GLASS_LAI (Tree_percent+Grass_percent).
│    ├── PCTT             # Tree percent in urban areas (MODIS VCF)
│    └── VCF              # Sum of tree and grass percent in urban areas (MODIS VCF)
│── Global_MODIS_LAI_YYYY_v61.nc
│    └── URBAN_TREE_LAI   # Monthly LAI drived from reprocessed MODIS LAI product, the dimension of LC from 1 to 7 represents NET, BET, NDT, BDT, MF, Urban and grid tree
└── Global_Urban_LAI_YYYY_v61.nc
     └── URBAN_TREE_LAI   # Monthly LAI drived from RF LAI product, the dimension of LC from 1 to 7 represents NET, BET, NDT, BDT, MF, Urban and grid tree
```
<br>

**References:**:

Lin, W., Yuan, H., Dong, W., Zhang, S., Liu, S., Wei, N., Lu, X., Wei, Z., Hu, Y., & Dai, Y. (2023). Reprocessed MODIS Version 6.1 Leaf Area Index Dataset and Its Evaluation for Land Surface and Climate Modeling. Remote Sensing, 15(7), Article 7. https://doi.org/10.3390/rs15071780

Ma, H., & Liang, S. (2022). Development of the GLASS 250-m leaf area index product (version 6) from MODIS data using the bidirectional LSTM deep learning model. Remote Sensing of Environment, 273, 112985. https://doi.org/10.1016/j.rse.2022.112985


