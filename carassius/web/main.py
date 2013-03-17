'''
Created on Feb 24, 2013

@author: siebz0r
'''
import os
import sys
import webapp2
from web.common import ActivationHandler
from web.common import RegistrationHandler
from web.common import LoginHandler

for x in os.listdir('lib'):
    sys.path.append(os.path.abspath('lib/%s' % x))

routes = [(r"/register/?", RegistrationHandler),
          (r"/login/?", LoginHandler),
          (r"/activate/([A-Za-z0-9]+)/?", ActivationHandler)]

app = webapp2.WSGIApplication(routes, debug=True)