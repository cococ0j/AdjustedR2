# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 11:39:03 2018

@author: rendorHaevyn
@name: app_processing
@about: does all the processing underlying the dashboarad
"""

"""
TO DO:
> Add statistical plots for data from the final table
>     
Final table:
> Stop id (nbr)
> Average current volume
> % increase volume
> Distance
> Time
"""

## ----- IMPORTS AND SETUP ----- ##

import os
import pandas as pd
import numpy as np
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
      
    HOVER_TOOLTIPS = [
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
    
    MAP_OPTIONS = GMapOptions(lat=LAT_INIT, lng=LON_INIT, map_type="roadmap", zoom=10, scale_control=True, styles=style)
    p = gmap(GOOGLE_KEY, MAP_OPTIONS, title="PTV Network Map", sizing_mode="scale_width"
             ,tools="pan,wheel_zoom,reset,help,box_zoom,tap,zoom_in,zoom_out,save")
#             ,tooltips=hover_tooltips)

#    p.add_tools(HoverTool(tooltips=HOVER_TOOLTIPS, mode='mouse'))
    
    TOOLTIPS = """
    <div>
        <div>
            <img
                src="@img" height="10" alt="@img" width="10"
                style="float: left; margin: 5px 2px 5px 2px;"
                border="0"
            ></img>
        </div>
        <div>
            <span style="font-size: 12px; font-weight: bold; color: #2F4F4F;">@stop_name</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #006400;">Stop # [@stop_sequence]</span>
        </div>
        <div>
            <span style="font-size: 10px; font-weight: italic; color: #2F4F4F;">@route_long_name</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #2F4F4F;">Geo-coords:</span>
            <span style="font-size: 10px; color: #006400;">(@stop_lat, @stop_lon)</span>
        </div>
        <div>
            <span style="font-size: 12px; color: #2F4F4F;">Journey (km):</span>
            <span style="font-size: 10px; color: #006400;">@dist_km</span>
        </div>
    </div>
    """

    p.add_tools(HoverTool(tooltips=TOOLTIPS, mode='mouse'))

    
    ## ~~~~~ RANDOM EXAMPLE ~~~~~ ##
    
#    route_test = df_train.loc[(df_train.route_id == '2-SDM-B-mjp-1') | (df_train.route_id == '2-SDM-B-mjp-1')]
#    route_test = route_test.to_dict('list')
    
    for mode, df in zip(['train','tram','bus'],[df_train,df_tram,df_bus]):       
        df['img'] = './static/img/PTV/{}.png'.format(mode)
        df['dist_km'] = np.around(df.shape_dist_traveled / 1000,2)
    
    import random
    dt_choice, COLOUR_CHOICE = random.choice([(df_train,RCOLOUR_TRAIN),(df_tram,RCOLOUR_TRAM),(df_bus,RCOLOUR_BUS)])
        
    for i, route in enumerate(set(dt_choice.route_id)):
        droute = dt_choice.loc[(dt_choice.route_id == route)]
 
        source = ColumnDataSource(
            data=droute
            )
        
        p.line(x="stop_lon", y="stop_lat", line_width=2, line_color=COLOUR_CHOICE, line_alpha=0.8, line_cap='round', source=source)
        p.circle(x="stop_lon", y="stop_lat", size=5, fill_color=COLOUR_CHOICE, fill_alpha=0.6, line_alpha=0.2, source=source)
    
    #            'e:\\Documents\\GitHub\\AdjustedR2\\App_Dev\\TrainFullApp\\static\\img\\PTV\\train.png'
#    p.image_url(url=['https://bokeh.pydata.org/en/latest/_static/images/logo.png'],x=LON_INIT, y=LAT_INIT, w=24, h=24)  
    
    
    ## Embed plot into HTML via Flask Render
    script, div = components(p)

    return script, div
