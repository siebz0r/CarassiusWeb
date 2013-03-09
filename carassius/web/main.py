'''
Created on Feb 24, 2013

@author: siebz0r
'''
import jinja2
import os
import sys
import webapp2
from web.common import ActivationHandler
from web.common import RegistrationHandler
from web.common import LoginHandler

for x in os.listdir('lib'):
    sys.path.append(os.path.abspath('lib/%s' % x))

env_path = __file__
for i in range(3):
    env_path = os.path.dirname(env_path)
env_path = os.path.join(env_path, "templates")
jinja2.env = jinja2.Environment(loader=jinja2.FileSystemLoader(env_path))

routes = [(r"/register/?", RegistrationHandler),
          (r"/login/?", LoginHandler),
          (r"/activate/([A-Za-z0-9]+)/?", ActivationHandler)]

app = webapp2.WSGIApplication(routes, debug=True)