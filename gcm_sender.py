import urllib2
import json
import datetime
import time
from google.appengine.ext import db
import logging
from keys import REG_ID, AUTH_KEY

SIMPLE_TYPES = (int, long, float, bool, dict, basestring, list)

def send_sms_gcm_notify(sms):
        
    url = 'https://android.googleapis.com/gcm/send'
    
    
    headers = { 'Content-Type' : 'application/json',
                'Authorization' : 'key='+AUTH_KEY  }
    
    data = json.dumps( { 'registration_ids' : [REG_ID],
                          #'data' : { 'test' : 'test' }
                          'data' : to_dict(sms)
                          })
    
    logging.info('creating request url='+url+'\n data='+data)
    req = urllib2.Request(url, data, headers)
    
    response = urllib2.urlopen(req)
        
    logging.info('response=\n'+response.read())
    
def to_dict(model):
    output = {}

    for key, prop in model.properties().iteritems():
        value = getattr(model, key)

        if value is None or isinstance(value, SIMPLE_TYPES):
            output[key] = value
        elif isinstance(value, datetime.date):
            # Convert date/datetime to MILLISECONDS-since-epoch (JS "new Date()").
            ms = time.mktime(value.utctimetuple()) * 1000
            ms += getattr(value, 'microseconds', 0) / 1000
            output[key] = int(ms)
        elif isinstance(value, db.GeoPt):
            output[key] = {'lat': value.lat, 'lon': value.lon}
        elif isinstance(value, db.Model):
            output[key] = to_dict(value)
        else:
            raise ValueError('cannot encode ' + repr(prop))

    return output    
    