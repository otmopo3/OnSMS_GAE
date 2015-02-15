# This Python file uses the following encoding: utf-8
'''
Created on 11.08.2012

@author: Alexey
'''
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import webapp2

from datastore import MoneyMovement


templates_dir=os.path.join(os.path.dirname(__file__), 'templates')

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/money"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            return

        
        if not users.is_current_user_admin():
            greeting = ("<a href=\"%s\">You are not admin. Relogin plz.</a>." %
                        users.create_login_url("/money"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            return
        
        money=MoneyMovement.all().order("-date_received").fetch(10)
        
        template_values ={
                          'money':money
                          }   
        path = os.path.join(templates_dir, 'money.html') 
        self.response.out.write(template.render(path, template_values))
        
class Zarplata(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            greeting = ("<a href=\"%s\">Sign in or register</a>." %
                        users.create_login_url("/money"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            return

        
        if not users.is_current_user_admin():
            greeting = ("<a href=\"%s\">You are not admin. Relogin plz.</a>." %
                        users.create_login_url("/money"))
            self.response.out.write("<html><body>%s</body></html>" % greeting)
            return
        
        money=MoneyMovement.all().filter("activity =", u"операция зачисления на сумму")
        #money=money.filter("result =", u"выполнена успешно.")        
        #money=money.filter("agent =", ' ')
        money=money.order("-date_received")
        money=money.fetch(10)
        template_values ={
                          'money':money
                          }   
        path = os.path.join(templates_dir, 'money.html') 
        self.response.out.write(template.render(path, template_values))
        
    
app = webapp2.WSGIApplication([('/money/zarplata', Zarplata),('/money', MainPage)], debug=True)


        
if __name__ == '__main__':
    pass