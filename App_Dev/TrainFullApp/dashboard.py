# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 20:33:34 2018

@author: rendorHaevyn
@about: Flask demo
@purpose: load data for route plots and prepare dynamic outputs
"""

import os
import pandas as pd

WKDIR       = "e:\\Documents\\GitHub\\_gtfs\\test_data"
os.chdir(WKDIR)

# ===== Load and Iterate all routes in dataset, one at a time ===== #
    
store = pd.HDFStore('ptv_routes.h5')
df_bus     = store['df_bus']
df_train   = store['df_train']
df_tram    = store['df_tram']

for shp in df_tram.shape_idTrunc.unique():
    df_tram.loc[df_tram.shape_idTrunc == shp]


#route 1:
df_bus.head().to_html()

#route 2:
from flask import jsonify
jsonify(df_bus.head())