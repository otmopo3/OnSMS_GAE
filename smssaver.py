# This Python file uses the following encoding: utf-8
'''
Created on 24.07.2012

@author: Alexey
'''
# import cgi
import os
import re

from google.appengine.api import users
from google.appengine.ext.webapp import template
import webapp2

from datastore import SMS, MoneyMovement

from gcm_sender import send_sms_gcm_notify


# from google.appengine.api import users
templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

class MainPage(webapp2.RequestHandler):
    def post(self):
        sms = SMS()
        sms.from_number = self.request.get('from_number')
        sms.sms_text = self.request.get('sms_text')    
        sms.email = self.request.get('email')
        sms.loc_lat = self.request.get('loc_lat') 
        sms.loc_long = self.request.get('loc_long')  
        sms.dev_name =   self.request.get('dev_name')  
        sms.put()
        
        if sms.from_number == '900' or sms.from_number == '+79194743313':
            op = self.getMoneyMovementFromSms(sms)
            op.sms = sms
            op.put()  
        
        send_sms_gcm_notify(sms)          
            
    def getMoneyMovementFromSms(self, sms):
        op = MoneyMovement()
        time_re = u'(\d+\.\d+\.\d+ \d+\:\d+)'
        money_re = u'(\d+\.\d+)'
        currency_re = u'(\S+)'
        agent_re = u'([A-Za-z\s\-\d\(\)@\*\.]+)'
        result_re = u'(\.?)'
        remains_digits_re = u'(\d+\.\d+)'
        re_text = u'(VISA\d+): ' + time_re + ' (.*) '
        re_text += money_re + '\s?' + currency_re + '' + agent_re + '' + result_re + ' (\D+) ' + remains_digits_re + '\s?(\D+)'
        print re_text
        match = re.match(re_text, sms.sms_text)
        op.card_number = match.group(1)
        op.local_time = match.group(2)
        op.activity = match.group(3)
        op.money = match.group(4)
        op.currency = match.group(5)
        op.agent = match.group(6)
        op.result = match.group(7)
        op.remains = match.group(9)
        op.email = sms.email
        op.loc_lat = sms.loc_lat
        op.loc_long = sms.loc_long
        op.bank_name = 'SBERBANK'
        return op
     
    def get(self):
        
        user = users.get_current_user()
        if not user:
            greeting = ("<a href=\"%s\">Sign in or register</a>." % 
                        users.create_login_url("/"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            return

        
        if not users.is_current_user_admin():
            greeting = ("<a href=\"%s\">You are not admin. Relogin plz.</a>." % 
                        users.create_login_url("/"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            return
        
        from_number = self.request.get('from_number')
        if from_number:
            smss = SMS.all().filter('from_number', from_number)
        else:
            smss = SMS.all()
        
        num = self.request.get('n')
        n = 50
        
        if num and num.isdecimal():
                n = int(num)
            
        smss = smss.order('-date_received').fetch(n)        
        
        template_values = {
                          'smss':smss
                          }   
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html') 
        self.response.out.write(template.render(path, template_values))
    
app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

    
def test_sms():
    test_one_sms("VISA9233: 23.07.12 08:28 покупка на сумму 222.00р. ARENA PERMSKI FILIAL. Баланс: 11.70р.",
                 "VISA9233", "23.07.12 08:28", "покупка на сумму", "222.00", "р.", "ARENA PERMSKI FILIAL", "11.70")
    
    test_one_sms("VISA2357: 20.07.14 11:12 операция зачисления на сумму 20000.00р. SBERBANK ONL@IN VKLAD-KARTA. Баланс: 33910.70р.",
                 "VISA2357", "20.07.14 11:12", "операция зачисления на сумму", "20000.00", "р.", "SBERBANK ONL@IN VKLAD-KARTA", "33910.70")
    
    test_one_sms("VISA2357: 21.08.14 14:05 операция зачисления на сумму 6134.00р. Баланс: 10983.22р.",
                 "VISA2357", "21.08.14 14:05", "операция зачисления на сумму", "6134.00", "р", "", "10983.22")
    
   
def test_one_sms(sms_text, card_number, local_time, activity, money, currency, agent, remains ):
    sms = SMS()
    sms.from_number = '900'
    sms.sms_text = sms_text      
    sms.email = 'test@gmail.com'
    sms.loc_lat = '' 
    sms.loc_long = ''
    mp = MainPage()
    op = mp.getMoneyMovementFromSms(sms)
    assert(op.card_number == card_number)
    assert(op.local_time == local_time)
    assert(op.activity == activity)
    assert(op.money == money)
    assert(op.currency == currency)
    assert(agent in op.agent)
    assert(op.remains == remains)
    print "Test Successful"
    
    

def run_tests():
    test_sms() 
    
if __name__ == "__main__":
    run_tests()
    pass


