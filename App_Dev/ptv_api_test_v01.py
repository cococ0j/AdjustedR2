# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 22:16:38 2018

@author: Owner
"""

from pyptv import PTVClient

DEVELOPER_ID    = "1900000"
API_KEY         = "abcdef66-1234-789a-abba-123456789000"

client = PTVClient(developer_id=DEVELOPER_ID, api_key=API_KEY)
client.healthcheck()

client.stops_nearby((-37.771141, 144.961599), mode='tram')
    