# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 14:44:24 2018

@author: rendorHaevyn
@about: Flask demo
@url: https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login
"""

## ----- IMPORTS ----- ##

from flask import Flask, render_template, g, redirect, url_for

# Get Flask secret random key
#''.join(random.choices(string.ascii_uppercase + string.digits, k=100))
from pathlib import Path
import os
root      = Path(__file__).parents[3]
f_secret  = 'flask_secret_key.txt'
with open(os.path.join(root,f_secret),'r') as f_in:
    secret_key = f_in.readline()

## ----- CONSTANTS ----- ##

FLASK_SECRET_KEY    = secret_key


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
def index():
    return render_template("index.html")


@app.route("/dashboard")
#@oidc.require_login
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
#@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
#    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == '__main__':
    app.run()

## HOW TO ##
# 1. CD to root directory of app.py
# 2. run " python app.py flask run"
# or: just hit F5 here!