# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 19:29:00 2018

@author: Owner
"""

'''
Unofficial Python wrapper for Public Transport Victoria API
Read the full API documentation here: http://stevage.github.io/PTV-API-doc/

Documentation in "quotes" here is verbatim from PTV.
Source: Licensed from Public Transport Victoria under a Creative Commons Attribution 3.0 Australia Licence.

This Python module itself is licensed under WTFPL.

To use it, rename the included apikey.example to apikey.py and include your API key and DevID.
Don't have one? Email APIKeyRequest@ptv.vic.gov.au with subject "PTV Timetable API - request for key"

Dependencies:

sudo pip install python-dateutil

'''
import urllib
import json, datetime


DEVELOPER_ID    = "3000035"
API_KEY         = "3aefee2c-4cbc-4d39-88df-fa0cc91b93fe"


def nownomicro():
  ''' Returns current time, without microseconds, as required by PTV API.'''
  return datetime.datetime.utcnow().replace(microsecond=0)

def now8601():
  ''' Returns current time, without microseconds, as required by PTV API, in 8601 format.'''
  return nownomicro().isoformat()


def callAPI(api, **kwargs):
  ''' Makes the specified API call, handling signature computation and developer id.'''
  import hmac, hashlib 
  ptvbase="http://timetableapi.ptv.vic.gov.au"
  preamble = "/v3/"
  kwargs['devid'] = DEVELOPER_ID
  call = preamble + api + "?" + urllib.parse.urlencode(kwargs)

  try:
      sig=hmac.new(API_KEY, call, hashlib.sha1).hexdigest().upper()
  except:
      sig=hmac.new(b"%b" % API_KEY.encode('utf-8'), call.encode('utf-8'), hashlib.sha1).hexdigest().upper()
  url=ptvbase + call + "&signature=" + sig
  print(url)
  response = urllib.request.urlopen(url)
  
  return json.load(response)


def healthCheck():
  ''' Verifies that devID and key are correct so future calls will succeed.
  "A check on the timely availability, connectivity and reachability of the services that deliver security, caching and data to web clients. A health status report is returned."
  '''
  # eg: healthCheck()
  h = callAPI("healthcheck", { "timestamp": now8601() } )
  print(h)
  if not h['securityTokenOK'] or not h['databaseOK'] :
    raise Exception('Failed healthchck')
  return h

def stopsNearby(latitude, longitude, **kwargs):
  '''Stops Nearby returns up to 30 stops nearest to a specified coordinate."'''
  # stopsNearby(-38, 145)
  return callAPI("stops/location/{},{}".format(latitude, longitude), **kwargs)
  

def transportPOIsByMap(poi, lat1, long1, lat2, long2, griddepth, limit):
  '''"Transport POIs by Map returns a set of locations consisting of stops and/or myki ticket outlets 
  (collectively known as points of interest - i.e. POIs) within a region demarcated on a map through 
  a set of latitude and longitude coordinates.
  POI codes:
    0 Train (metropolitan)
    1 Tram
    2 Bus (metropolitan and regional, but not V/Line)
    3 V/Line regional train and coach
    4 NightRider
    100 Ticket outlet
  "'''

  # transportPOIsByMap(2,-37,145,-37.5,145.5,3,10)
  return callAPI("poi/%s/lat1/%d/long1/%d/lat2/%d/long2/%d/griddepth/%d/limit/%d" %
           (str(poi), lat1, long1, lat2, long2, griddepth, limit))
  

def search(query):
  '''"The Search API returns all stops and lines that match the input search text."'''
  # search("Hoddle St")
  
  return callAPI("search/" + urllib.quote(str(query)))

#TODO: convert incoming dates to datetimes, using dateutil.parser
def broadNextDepartures(mode, stop, limit, for_utc=nownomicro()):
  '''"Broad Next Departures returns the next departure times at a prescribed stop irrespective of the line and direction of the service. For example, if the stop is Camberwell Station, Broad Next Departures will return the times for all three lines (Belgrave, Lilydale and Alamein) running in both directions (towards the city and away from the city)."
  Note: since the result is wrapped in a 'values' object, we return the contents of that object.
  '''
  # This and all functions that have a 'mode' argument also allow strings: train,tram,bus,vline,nightrider
  # broadNextDepartures(0,1104,2)
  # Note: for_utc is undocumented.

  return callAPI("mode/%d/stop/%d/departures/by-destination/limit/%d" % (modeFromString(mode), stop, limit),
                 {"for_utc": for_utc.isoformat() })['values']

def specificNextDepartures(mode, line, stop, directionid, limit, for_utc=nownomicro()):
  '''"Specific Next Departures returns the times for the next departures at a prescribed stop for a specific mode, line and direction. For example, if the stop is Camberwell Station, Specific Next Departures returns only the times for one line running in one direction (for example, the Belgrave line running towards the city)."'''
  # specificNextDepartures(1,1881,2026,24,1)

  return callAPI("mode/%d/line/%d/stop/%d/directionid/%d/departures/all/limit/%d" % 
            (modeFromString(mode), line, stop, directionid, limit))
            #{"for_utc": for_utc.isoformat() })

def stoppingPattern(mode,run,stop,for_utc=nownomicro()):
  ''' "The Stopping Pattern API returns the stopping pattern for a specific run (i.e. transport service) from a prescribed 
  stop at a prescribed time. The stopping pattern is comprised of timetable values ordered by stopping order."'''
  # stoppingPattern(0,4780,1104)
  # /v2/mode/%@/run/%@/stop/%@/stopping-pattern?for_utc=%@&devid=%@&signature=%@
  return callAPI("mode/%d/run/%d/stop/%d/stopping-pattern" % (modeFromString(mode), run, stop), 
    {"for_utc": for_utc.isoformat()})

def stopsOnALine(mode,line):
  '''"The Stops on a Line API returns a list of all the stops for a requested line, ordered by location name.
  '''
  # stopsOnALine(4,'1818')
  return  callAPI("mode/%d/line/%d/stops-for-line" % (modeFromString(mode), line))

### End official part. Now higher level functions.

def modeFromString (modestr):
  # Allows you to pass string modes to the API rather than their 0,1,2,3 etc.
  #Mode:  0 Train (metropolitan) 
  #       1 Tram 
  #       2 Bus (metropolitan and regional, but not V/Line) 
  #       3 V/Line train and coach 
  #       4 NightRider
  if type(modestr) == type(0):
    return modestr
  return ['train','tram','bus','vline','nightrider'].index(modestr)

def melbourneTime(isostr):

  from dateutil import parser, tz
  d = parser.parse(isostr)
  d.replace(tzinfo=tz.gettz('UTC')) # Not sure if needed
  return d.astimezone(tz.gettz('Australia/Melbourne'))


def findThing(name, stoporline, transport_type=''):
  out = []
  for x in search(name):
    if x['type'] != stoporline:
      continue
    r = x['result']
    if transport_type not in ('', r['transport_type']):
      continue
    r.pop('distance',None)
    out += [r]
  return out

def findLine(name, transport_type=''):
  return findThing(name, 'line', transport_type)


def findStop(name, transport_type=''):
  return findThing(name, 'stop', transport_type)
  # transport_type: bus, vline, train, tram [vline is both coach and train!]
  # Very broad queries (eg 'Railway Station') seem to return incomplete sets.
  #stops = filter(lambda x: x['type'] == 'stop', search(name))    
  #stops = map(lambda x: x['result'], stops)
  #if transport_type:
  #  stops = filter(lambda x: x['transport_type'] == transport_type, stops)
  #return stops
  
def main(): 
#    result = healthCheck()
    result = stopsNearby(-37.56161, 145.00012, **{'route_types':1,'max_results':5,'max_distance':3000})
    #timetableapi.ptv.vic.gov.au/v3/stops/location/-37,145?route_types=tram&max_results=5&max_distance=100&devid=3000035&signature=F1CBCC747776503A05A60C874EC26B11E2A516D5

if __name__ == '__main__':
    main()