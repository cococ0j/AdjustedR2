# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 14:44:24 2018

@author: rendorHaevyn
@about: Flask demo
@url: https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login
"""

## ----- IMPORTS ----- ##

from flask import Flask, render_template, g, redirect, url_for
from flask_oidc import OpenIDConnect
from okta import UsersClient

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
# Okta API Key for simple-flask-app (web app)
OKTA_API_KEY        = '00_28BIjc5iOGlb-QwMGK3CaNmovLbWMjCeJoN3j5Q'
OKTA_ORG_URL        = 'https://dev-548896.oktapreview.com'


## ----- APP CONFIGURATION ----- ##

app = Flask(__name__)
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = FLASK_SECRET_KEY
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "oidc_token"
oidc = OpenIDConnect(app)
okta_client = UsersClient(OKTA_ORG_URL, OKTA_API_KEY)


## ----- APP DEFINITIONS ----- ##

@app.before_request
def before_request():
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
    else:
        g.user = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
@oidc.require_login
def dashboard():
    return render_template("dashboard.html")


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for(".dashboard"))


@app.route("/logout")
def logout():
    oidc.logout()
    return redirect(url_for(".index"))


if __name__ == '__main__':
    app.run()

## HOW TO ##
# 1. CD to root directory of app.py
# 2. run " python app.py flask run"
# or: just hit F5 here!