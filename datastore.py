'''
Created on 09.08.2012

@author: Alexey
'''

from google.appengine.ext import db


class SMS(db.Expando):
    email = db.EmailProperty()
    from_number = db.StringProperty(indexed=True)
    sms_text = db.StringProperty()
    date_received = db.DateTimeProperty(auto_now=True)
    loc_lat = db.StringProperty()
    loc_long = db.StringProperty()
    dev_name = db.StringProperty()
   
    
class MoneyMovement(db.Model):    
    email = db.EmailProperty()
    card_number = db.StringProperty()
    local_time = db.StringProperty()
    activity = db.StringProperty()
    money = db.StringProperty()
    currency = db.StringProperty()
    agent = db.StringProperty()
    result = db.StringProperty()
    remains = db.StringProperty()
    date_received = db.DateTimeProperty(auto_now=True)
    loc_lat = db.StringProperty()
    loc_long = db.StringProperty()
    sms = db.ReferenceProperty(SMS, collection_name='money')
    bank_name = db.StringProperty()

class GcmRegistration(db.Model):
    email = db.EmailProperty()
    registration_id = db.StringProperty()