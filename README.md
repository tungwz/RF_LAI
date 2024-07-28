# Urban tree LAI for urban climate modeling 

This repository is used to produce urban tree LAI and data analysis associated with the manuscript:
> "A Global Urban Tree Leaf Area Index Dataset for Urban Climate Modeling"

The Code for model training and producing data can be found in the model_code directory.
The Code and data used to create figures in the manuscript are available at plot_Fig directory.

<br>

**Directory:**
```bash
├── model_code                 # Code for training model and predicting LAI       
└── plot_Fig                   # Code and data for plotting 
    ├── FigX                   # Code for plotting Fig1-Fig7
    ├── TableX                 # Code for plotting figures of Table 3
    ├── nc_data                # 0.5 deg global LAI data for plotting Fig 5/6/7
    ├── map_site               # 14 sites observation LAI from GBOV/VALERI/Boston University
    └── Timecsv                # RF LAI and reprocessed MODIS LAI for 14 sites
```
<br>

**Usage**
<br>
Code is mostly written in Python with dependencies including sklearn, flaml, numpy, pandas, xarray, matplotlib, seaborn, scienceplots and cartopy. The rest of the code is written by NCL
