# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 22:16:38 2018

@author: rendorHaevyn
@about:  Using PTVCLient, had to make a number of changes for Python 3 and PTV API V3 compliance...
"""

from pyptv import PTVClient

DEVELOPER_ID    = "3000035"
API_KEY         = "3aefee2c-4cbc-4d39-88df-fa0cc91b93fe"

client = PTVClient(developer_id=DEVELOPER_ID, api_key=API_KEY)

result = client.stops_nearby((-37.771141, 144.961599), mode='bus', limit=10, max_distance=1000, with_distance=True)
print(result)

## RESULTS LOOK LIKE :
#[(<BusStop: (25381) Sydney Rd/Glenlyon Rd >, 0.04689142545321165), (<BusStop: (25380) 18 Dawson St >, 0.22727122419852144), 
#(<BusStop: (25382) Blair St/Glenlyon Rd >, 0.23381457093524963), (<BusStop: (25663) Charles St/Glenlyon Rd >, 0.23384103586025456), 
#(<BusStop: (25379) Police Complex/20 Dawson St >, 0.3588512030720104), (<BusStop: (25660) 31 Dawson St >, 0.3667296069729777), 
#(<BusStop: (25383) Bruce St/Glenlyon Rd >, 0.3938918109282562), (<BusStop: (27828) Barkly Square SC/Weston St >, 0.4494843944700287), 
#(<BusStop: (11070) Sydney Rd/Victoria St >, 0.4680522797769535), (<BusStop: (11069) Brunswick Railway Station/Victoria St >, 0.5065472831224442)]