from protorpc import message_types

from protorpc import remote

from keys import WEB_CLIENT_ID, ANDROID_CLIENT_ID, BROWSER_ID

import endpoints

import auth_helper

from sms_api_datamodel import SmsCollection, SmsConverter

IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

@endpoints.api(name='smssync', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID, BROWSER_ID,
                                   IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class SmsApi(remote.Service):    

    @endpoints.method(message_types.VoidMessage, SmsCollection,
                      path='getSmsList', http_method='GET',
                      name='smssync.getSmsList')
    def getSmsList(self, request):
        auth_helper.checkAuth()
        
        try:            
            return SmsConverter.fetchFromDb()
        except (IndexError, TypeError):
            raise endpoints.NotFoundException('Greeting %s not found.' % 
                                              (request.id,))
            
            
APPLICATION = endpoints.api_server([SmsApi])                 
