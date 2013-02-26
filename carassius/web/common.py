'''
Created on Feb 24, 2013

@author: siebz0r
'''
import webapp2
import jinja2

class RegistrationHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja2.env.get_template("register.html")
        self.response.out.write(template.render())
        
    def post(self):
        username = self.request.get("username")
        self.response.out.write(username)
