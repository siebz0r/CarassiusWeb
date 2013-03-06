'''
Created on Feb 24, 2013

@author: siebz0r
'''
import os
import sys
for x in os.listdir('lib'):
    sys.path.append(os.path.abspath('lib/%s' % x))

import jinja2
import webapp2
from webapp2_extras.routes import RedirectRoute
from carassius.web.common import RegistrationHandler
from web.common import LoginHandler

env_path = __file__
for i in range(3):
    env_path = os.path.dirname(env_path)
env_path = os.path.join(env_path, "templates")
jinja2.env = jinja2.Environment(loader=jinja2.FileSystemLoader(env_path))

routes = []
routes.append(RedirectRoute("/register", RegistrationHandler, name="registration", strict_slash=True))
routes.append(RedirectRoute("/login", LoginHandler, name="login", strict_slash=True))

app = webapp2.WSGIApplication(routes, debug=True)