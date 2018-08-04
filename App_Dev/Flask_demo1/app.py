# -*- coding: utf-8 -*-
"""
Created on Sat Aug  4 14:44:24 2018

@author: rendorHaevyn
@about: Flask demo
@url: https://developer.okta.com/blog/2018/07/12/flask-tutorial-simple-user-registration-and-login
"""

from flask import Flask, render_template

# Okta API Key for simple-flask-app (web app)
OKTA_API_KEY        = '00_28BIjc5iOGlb-QwMGK3CaNmovLbWMjCeJoN3j5Q'


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == '__main__':
    app.run()

## HOW TO ##
# 1. CD to root directory of app.py
# 2. run " python app.py flask run"
# or: just hit F5 here!