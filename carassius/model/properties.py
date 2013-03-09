'''
Created on Feb 25, 2013

@author: siebz0r
'''
from google.appengine.ext import ndb

class StructuredProperty(ndb.StructuredProperty):
    def __init__(self, modelclass, name=None, **kwargs):
        ndb.StructuredProperty.__init__(self, modelclass, name, **kwargs)

class StringProperty(ndb.StringProperty):
    def __init__(self, **kwargs):
        ndb.StringProperty.__init__(self, **kwargs)

class EmailProperty(StringProperty):
    def __init__(self, **kwargs):
        StringProperty.__init__(self, **kwargs)

class DateTimeProperty(ndb.DateTimeProperty):
    def __init__(self, **kwargs):
        ndb.DateTimeProperty.__init__(self, **kwargs)
