# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 14:44:24 2018

@author: rendorHaevyn
@about: Flask Train Full App
@url: https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login
"""

## ----- IMPORTS ----- ##

from flask import Flask, render_template, g, redirect, url_for
from pathlib import Path
import os

ROOT        = Path(__file__).parents[3]
F_SECRET    = 'flask_secret_key.txt'
F_GGL       = 'Google_API_Key.txt'

## ----- LOAD KEYS ----- ##
#''.join(random.choices(string.ascii_uppercase + string.digits, k=100))

# Flask secret random key
with open(os.path.join(ROOT,F_SECRET),'r') as f_in:
    secret_key = f_in.readline()

# Google API key
with open(os.path.join(ROOT,F_GGL),'r') as f_in:
    ggl_key = f_in.readline()

## ----- CONSTANTS ----- ##

FLASK_SECRET_KEY    = secret_key


## ----- BOKEH MAP ----- ##

from bokeh.models import ColumnDataSource, GMapOptions
from bokeh.plotting import gmap
from bokeh.embed import components

#map_options = GMapOptions(lat=30.2861, lng=-97.7394, map_type="roadmap", zoom=11)
#p = gmap(ggl_key, map_options, title="Austin")
#source = ColumnDataSource(
#    data=dict(lat=[ 30.29,  30.20,  30.29],
#              lon=[-97.70, -97.74, -97.78])
#    )
#p.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)

import pandas as pd
import os
WKDIR       = "e:\\Documents\\GitHub\\_gtfs\\test_data"
os.chdir(WKDIR)
   
store = pd.HDFStore(os.path.join(WKDIR,'ptv_route_2018.h5'))
df_train   = store['df_train']

route_test = df_train.loc[(df_train.shape_id == '2-SDM-E-mjp-1.1.H') | (df_train.shape_id == '2-SDM-E-mjp-1.1.R')][['shape_pt_lat','shape_pt_lon']]
route_test = route_test.to_dict('list')

LAT_INIT = route_test['shape_pt_lat'][0]
LON_INIT = route_test['shape_pt_lon'][0]

map_options = GMapOptions(lat=LAT_INIT, lng=LON_INIT, map_type="roadmap", zoom=11)
p = gmap(ggl_key, map_options, title="PTV_Sandringham_Line")
source = ColumnDataSource(
    data=route_test
    )

p.line(x="shape_pt_lon", y="shape_pt_lat", line_width=2, line_color="blue", line_alpha=0.8, line_cap='round', source=source)

#            'e:\\Documents\\GitHub\\AdjustedR2\\App_Dev\\TrainFullApp\\static\\img\\PTV\\train.png'
p.image_url(url=['https://bokeh.pydata.org/en/latest/_static/images/logo.png']
            ,x=LON_INIT, y=LAT_INIT, w=24, h=24)

p.circle(x=LON_INIT, y=LAT_INIT, size=10, fill_color='blue', fill_alpha=0.8)

## Embed plot into HTML via Flask Render
script, div = components(p)

## ----- APP CONFIGURATION ----- ##

app = Flask(__name__)
app.config["SECRET_KEY"] = FLASK_SECRET_KEY


## ----- APP DEFINITIONS ----- ##

#@app.before_request
#def before_request():
#    if oidc.user_loggedin:
#        g.user = okta_client.get_user(oidc.user_getfield("sub"))
#    else:
#        g.user = None


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/dashboard")
#@oidc.require_login
def dashboard(): 
    return render_template("dashboard.html", script=script, div=div)


@app.route("/login")
#@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
#    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)

## HOW TO ##
# 1. CD to root directory of app.py
# 2. run " python app.py flask run"
# or: just hit F5 here!