# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 20:33:34 2018

@author: rendorHaevyn
@about: Flask demo
@purpose: load data for route plots and prepare dynamic outputs
"""

import os
import pandas as pd

DATADIR         = 'e:\\Documents\\GitHub\\AdjustedR2\\App_Dev\\TrainFullApp\\data'
ZIPFILE         = 'ptv_route_2018.zip'
DATAFILE        = 'ptv_route_2018.h5'

def unzip(f):
    global DATAFILE
    
    import zipfile
    with zipfile.ZipFile(f, 'r') as zip_ref:
        zip_ref.open(DATAFILE)
        print(type(zip_ref))
    return zip_ref

# ===== Load and Iterate all routes in dataset, one at a time ===== #

def load_data():
    global DATADIR, ZIPFILE
    
    f = os.path.join(DATADIR,ZIPFILE)
    ptv_data = unzip(f)    
    store = pd.HDFStore(ptv_data)
    df_bus     = store['df_bus']
    df_train   = store['df_train']
    df_tram    = store['df_tram']

# route_test = df_train.loc[df_train.shape_idTrunc == '2-SDM-E-mjp-1'][['shape_pt_lat','shape_pt_lon']].head()
# route_test = route_test.to_dict('list')

# for shp in df_train.shape_idTrunc.unique():
#     df_train.loc[df_train.shape_idTrunc == shp]

# #route 1:
# df_bus.head().to_html()

# #route 2:
# from flask import jsonify
# jsonify(df_bus.head())


def testing_zone():
    import zipfile
    import io
    
    with zipfile.ZipFile(os.path.join(DATADIR,ZIPFILE),'r') as zf:
        # d_zf = {name: zf.read(name) for name in zf.namelist()}
        l_zf = [name for name in zf.namelist()]
        # store = pd.HDFStore(zf.read(DATAFILE))
    
    with zipfile.ZipFile(os.path.join(DATADIR,ZIPFILE)) as z:
        z_data = z.read(DATAFILE)
        store = pd.HDFStore(z_data)


