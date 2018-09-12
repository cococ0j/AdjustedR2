# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 19:10:12 2018

@author: rendorHaevyn
@about: Flask app
@purpose: prepare GTFS train, tram and bus data

NOTES:
> may need to correct some stop_id's so that they match myki data (ie: Sunbury and crappy Diggers rest)
> some myki stop_ids may have multiple id's for the same railway station.
> we need to do this for GTFS train, tram, bus. yay.
"""

# In[initialise]:
import pandas as pd
import numpy as np
import os

BASE_DIR        = 'e:\\Documents\\GitHub\\_gtfs'
OUT_DIR         = 'e:\Documents\GitHub\AdjustedR2\App_Dev\TrainFullApp\data'

RCOLOUR_TRAM    = '78BE20'
RCOLOUR_BUS     = 'FF8200'
RCOLOUR_TRAIN   = '0072CE'


# In[routes]:
"""
== Steps to get sequence data for routes ==
1. routes.txt
> Get distinct route_id and route_long_name
> output: distinct route_id and route_long_name
"""
def route_id(mode, fnm, fldlen=False, nchar=False):
    """
    Reads in mode (tram/train/bus) GTFS route data and gets distinct route_id and route_long_name, 
    using a subset on the route_id (var: nchar) for distinct search.
    We do a second pass on route_long_name because PTV has duped on the name for some ungodly reason.
    We restict to route_id to those with specified length (var: fldlen) to get rid of anomalous routes.
    """
#    pd.DataFrame({'trip_headsign': set(dtram_route.trip_headsign), 'route_id': set(dtram_route.route_id)})    
    dm = pd.read_csv(os.path.join(BASE_DIR,'metro_{}'.format(mode),fnm))
    if nchar:
        dm['route_id_lku'] = dm.route_id.str.slice(0,nchar)
    else:
        dm['route_id_lku'] = dm.route_id
    if fldlen:
        dm = dm[dm.route_id.str.len() == fldlen].reset_index(drop=True)
    dm = dm[['route_id','route_long_name','route_id_lku']].drop_duplicates(subset='route_id_lku').reset_index(drop=True)
    dm = dm[['route_id','route_long_name','route_id_lku']].drop_duplicates(subset='route_long_name').reset_index(drop=True)
    return dm

dtram_rt = route_id('tram','routes.txt')
dtrain_rt = route_id('train','routes.txt',13,5)
dbus_rt = route_id('bus','routes.txt',11,5)


# In[trips]:
"""
== Steps to get sequence data for routes ==
2. trips.txt
> Get first trip_id for distinct route_id
> output: trip_id to add to route data frame
"""
def trip_id(mode, fnm, droute, fldlen=False, nchar=False):
    """
    Reads in mode (tram/train/bus) GTFS trip data and gets first trip_id for distinct route_id, 
    using a subset on the route_id (var: nchar) for distinct search.
    We restict to route_id to those with specified length (var: fldlen) to get rid of anomalous routes.
    Merge with route information (var: droute).
    """
    dm = pd.read_csv(os.path.join(BASE_DIR,'metro_{}'.format(mode),fnm))
    if nchar:
        dm['route_id_lku'] = dm.route_id.str.slice(0,nchar)
    else:
        dm['route_id_lku'] = dm.route_id
    if fldlen:
        dm = dm[dm.route_id.str.len() == fldlen].reset_index(drop=True)
    dm = dm[['route_id','trip_id','route_id_lku']].drop_duplicates(subset='route_id_lku', keep='last').reset_index(drop=True)
    dm = dm.drop(axis=1,columns='route_id')
    dt = pd.merge(droute, dm, how='inner', on='route_id_lku')   
    return dt

dtram_tr = trip_id('tram','trips.txt',dtram_rt)
dtrain_tr = trip_id('train','trips.txt',dtrain_rt,13,5)
dbus_tr = trip_id('bus','trips.txt',dbus_rt,11,5)


# In[stop times]:
"""
3. stop_times.txt
> look up route_id in the trip_id
> for each distinct trip_id, find trip with greatest stop count
> use the longest stop count trip_id per route_id (A)
> from this (A), get the stop_id and stop_sequence
> output: distinct route_id, distinct trip_id, list of stop_id, list of stop_sequence
"""
def stop_times(mode, fnm, dtrip):
    """
    Reads in mode (tram/train/bus) GTFS stop data and joins on unique trips data frame (var: dtrip)
    to get stop_id, stop_sequence, and stop_distance_travelled.
    Merge with trip information (var: dtrip).
    """
    dm = pd.read_csv(os.path.join(BASE_DIR,'metro_{}'.format(mode),fnm))[['trip_id','stop_id','stop_sequence','shape_dist_traveled']]
    dt = pd.merge(dtrip, dm, how='inner', on='trip_id')   
    return dt

dtram_st = stop_times('tram','stop_times.txt',dtram_tr)
dtrain_st = stop_times('train','stop_times.txt',dtrain_tr)
dbus_st = stop_times('bus','stop_times.txt',dbus_tr)


# In[stops]:
"""
3. stops.txt
> look up each stop_id
> from this, get the stop_name, stop_lat, stop_lon
> output: distinct route_id, distinct trip_headsign, distinct trip_id, list of stop_id, list of stop_sequence, stop_name, stop_lat, stop_lon
"""
def stops(mode, fnm, dstops):
    """
    Reads in mode (tram/train/bus) GTFS stop data and joins on unified stops data frame (var: dstops)
    to get stop_name, stop_lat, stop_lon.
    Merge with trip information (var: dstops).
    """
    dm = pd.read_csv(os.path.join(BASE_DIR,'metro_{}'.format(mode),fnm))
    dt = pd.merge(dstops, dm, how='inner', on='stop_id', copy=False)   
    dt.drop(axis=1, columns='route_id_lku', inplace=True)
    dt.sort_values(axis=0, by=['route_id','stop_sequence'], ascending=True, kind='mergesort', inplace=True)
    return dt

dtram_geo = stops('tram','stops.txt',dtram_st)
dtrain_geo = stops('train','stops.txt',dtrain_st)
dbus_geo = stops('bus','stops.txt',dbus_st)


# In[save_dataframe_hd5]:

try:
    os.remove(os.path.join(OUT_DIR,'ptv_stops_2018.h5'))
except OSError:
    store = pd.HDFStore(os.path.join(OUT_DIR,'ptv_stops_2018.h5'))

#os.chmod(os.path.join(BASE_DIR,'ptv_route_2018.h5'), '0777')

# save to HDF5
store['df_tram']    = dtram_geo
store['df_train']   = dtrain_geo
store['df_bus']     = dbus_geo

print(store.info())
for i in store.items():
    print(i)
    
store.close()