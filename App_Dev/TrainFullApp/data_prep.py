# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:10:12 2018

@author: rendorHaevyn
@about: Flask demo
@purpose: prepare test data for route plots
"""

import os
import pandas as pd

WKDIR       = "e:\\Documents\\GitHub\\_gtfs\\test_data"

os.chdir(WKDIR)
for i,f in enumerate(os.scandir(WKDIR)):    
    fnm_base = os.path.splitext(f.name)[0]
    if fnm_base.endswith('.txt'):
        exec("df_{} = pd.read_csv('{}')".format(fnm_base,f.name))

#kudos: https://stackoverflow.com/questions/17116814/pandas-how-do-i-split-text-in-a-column-into-multiple-rows#answer-21032532    
df_bus_shapes['shape_idTrunc'] = df_bus_shapes.shape_id.str.split('.',expand=True)[0]
df_train_shapes['shape_idTrunc'] = df_train_shapes.shape_id.str.split('.',expand=True)[0]
df_tram_shapes['shape_idTrunc'] = df_tram_shapes.shape_id.str.split('.',expand=True)[0]


df_bus = pd.merge(df_bus_shapes, df_bus_routes, how='inner', left_on='shape_idTrunc', right_on='route_id')
df_train = pd.merge(df_train_shapes, df_train_routes, how='inner', left_on='shape_idTrunc', right_on='route_id')
df_tram = pd.merge(df_tram_shapes, df_tram_routes, how='inner', left_on='shape_idTrunc', right_on='route_id')


# ===== Save dataframes / compress ===== #

store = pd.HDFStore('ptv_routes.h5')

# save to HDF5
store['df_bus']     = df_bus
store['df_train']   = df_train
store['df_tram']    = df_tram

store.info()
store.items()

# ===== Load and Iterate all routes in dataset, one at a time ===== #

#store = pd.HDFStore('ptv_routes.h5')
#df_bus     = store['df_bus']
#df_train   = store['df_train']
#df_tram    = store['df_tram']

#for shp in df_tram.shape_idTrunc.unique():
#    df_tram.loc[df_tram.shape_idTrunc == shp]
   

