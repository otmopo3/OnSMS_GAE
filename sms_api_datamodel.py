from protorpc import messages
from datastore import SMS

class Sms(messages.Message):
    """Greeting that stores a message."""
    from_number = messages.StringField(1)
    sms_text = messages.StringField(2)
    date_received = messages.StringField(3)
    loc_lat = messages.StringField(4)
    loc_long = messages.StringField(5)
    ds_key = messages.StringField(6)        
    
    
class SmsCollection(messages.Message):
    """Collection of Greetings."""
    items = messages.MessageField(Sms, 1, repeated=True)    
    
   
    
class SmsConverter:
    @staticmethod
    def fromSms(sms):
        smsMessage = Sms(sms_text=sms.sms_text,
                         from_number=sms.from_number,
                         date_received=str(sms.date_received),
                         loc_lat=sms.loc_lat,
                         loc_long=sms.loc_long,
                          ds_key=str(sms.key()))
        return smsMessage 
    
    @staticmethod
    def fetchFromDb(count=50, offset=0):
        smss = SMS.all().order('-date_received').fetch(count, offset)
        sms_array = []
        for sms in smss:
            sms_array.append(SmsConverter.fromSms(sms))
            
        return SmsCollection(items=sms_array)   
        


