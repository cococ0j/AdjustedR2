# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 11:39:03 2018

@author: rendorHaevyn
@name: app_processing
@about: does all the processing underlying the dashboarad
"""

"""
TO DO:
==>This is to find stops in the CBD
Step 1: create CBD square box (get the log and lat for the 4 points)
Step2: find out the stops id within the CBD fringe

==>Find route going to city through myki  (A)
Step1: filter the myki data based on cbd stop flag
Step2: group by touch on stop id and group by route id

==>Find nearest stop to the closed stop (B)
Step1: find nearest stop based on geo location

==>Map A& B, to find out the nearest stop that going to CBD
==>Then calculate the historical volume of these route
==>Volume after nude the stop  , allocate to the nearest stop

Final table:
> Stop id (n
> Average current volume
> % increase volume
> Distance
> Time
"""

## ----- IMPORTS AND SETUP ----- ##

import os
import pandas as pd
from bokeh.models import ColumnDataSource, GMapOptions, HoverTool
from bokeh.plotting import gmap
from bokeh.embed import components


ROOT        = 'e:\\Documents\\GitHub'
F_GGL           = 'Google_API_Key.txt'

# Google API key
with open(os.path.join(ROOT,F_GGL),'r') as f_in:
    ggl_key = f_in.readline()


## ----- CONSTANTS ----- ##
GOOGLE_KEY          = ggl_key

RCOLOUR_TRAM    = '#78BE20'
RCOLOUR_BUS     = '#FF8200'
RCOLOUR_TRAIN   = '#0072CE'


## ----- LOAD DATA ----- ##
def load_data_chk():
    """
    Loads data frames of route data from the h5 store created by gtf_data_prep.py
    """
    store = pd.HDFStore('.\data\ptv_stops_2018.h5')
    df_bus     = store['df_bus']
    df_train   = store['df_train']
    df_tram    = store['df_tram']
    
    return df_bus, df_train, df_tram


## ----- BOKEH MAP ----- ##
def bokeh_magic(df_bus, df_train, df_tram):
    
    # Load JSON Gmap style, 
    # https://snazzymaps.com/style/72543/assassins-creed-iv
    # https://snazzymaps.com/style/27725/minimal-v3
    style = open('.\static\json\gmap_style_minv3.json','r').read()   
    
    #map_options = GMapOptions(lat=30.2861, lng=-97.7394, map_type="roadmap", zoom=11)
    #p = gmap(ggl_key, map_options, title="Austin")
    #source = ColumnDataSource(
    #    data=dict(lat=[ 30.29,  30.20,  30.29],
    #              lon=[-97.70, -97.74, -97.78])
    #    )
    #p.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)
      
    hover_tooltips = [
            ("Index", "$index"),
            ("Route", "@route_long_name"),
            ("Stop ID", "@stop_id"),
            ("Sequence", "@stop_sequence"),
            ("Stop Name", "@stop_name"),            
            ("Lon,Lat", "@stop_lon, @stop_lat"),
            ("Distance (m)","@shape_dist_traveled{0,0.0}"),
    ]        

    LAT_INIT = -37.818
    LON_INIT = 144.967
    
    map_options = GMapOptions(lat=LAT_INIT, lng=LON_INIT, map_type="roadmap", zoom=10, scale_control=True, styles=style)
    p = gmap(GOOGLE_KEY, map_options, title="PTV Network Map", sizing_mode="scale_width"
             ,tools="pan,wheel_zoom,reset,help,box_zoom,tap,zoom_in,zoom_out,save")
#             ,tooltips=hover_tooltips)

    p.add_tools(HoverTool(tooltips=hover_tooltips, mode='mouse'))
    
    ## ~~~~~ TRAIN EXAMPLE ~~~~~ ##
    
#    route_test = df_train.loc[(df_train.route_id == '2-SDM-B-mjp-1') | (df_train.route_id == '2-SDM-B-mjp-1')]
#    route_test = route_test.to_dict('list')
    
    for i, route in enumerate(set(df_train.route_id)):
        droute = df_train.loc[(df_train.route_id == route)]
    
        source = ColumnDataSource(
            data=droute
            )
        
        p.line(x="stop_lon", y="stop_lat", line_width=2, line_color=RCOLOUR_TRAIN, line_alpha=0.8, line_cap='round', source=source)
        p.circle(x="stop_lon", y="stop_lat", size=5, fill_color=RCOLOUR_TRAIN, fill_alpha=0.6, source=source)
    
    #            'e:\\Documents\\GitHub\\AdjustedR2\\App_Dev\\TrainFullApp\\static\\img\\PTV\\train.png'
#    p.image_url(url=['https://bokeh.pydata.org/en/latest/_static/images/logo.png'],x=LON_INIT, y=LAT_INIT, w=24, h=24)  
    
    
    ## Embed plot into HTML via Flask Render
    script, div = components(p)

    return script, div
