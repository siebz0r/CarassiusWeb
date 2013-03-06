'''
Created on Feb 25, 2013

@author: siebz0r
'''
from google.appengine.ext import ndb
import hashlib
from model.properties import EmailProperty
from model.properties import StringProperty
from model.properties import StructuredProperty
import random
import string

class Password(ndb.Model):
    hash = ndb.StringProperty(required=True)
    hash_method = ndb.StringProperty(required=True)
    salt = ndb.StringProperty(required=True)
    
    def hash_password(self, password, hash_method=None):
        self.hash_method = hash_method or self.hash_method
        h = hashlib.new(self.hash_method)
        h.update(''.join([self._update_salt(), password]))
        self.hash = h.hexdigest()

    def _update_salt(self, hash_method=None):
        self.hash_method = hash_method or self.hash_method
        h = hashlib.new(self.hash_method)
        h.update(''.join(random.choice(string.printable) for x in range(10)))
        self.salt = h.hexdigest()
        return self.salt
    
    def test(self, password):
        h = hashlib.new(self.hash_method)
        h.update(''.join([self.salt, password]))
        return self.hash == h.hexdigest()

class Person(ndb.Model):
    first_name = StringProperty()
    last_name = StringProperty()
    insertion = StringProperty()
    email_address = EmailProperty()
    
    user_name = StringProperty(required=True)
    password = StructuredProperty(Password)
    
    @classmethod
    @ndb.transactional
    def register(cls, person, password):
        person.password = Password()
        person.password.hash_password(password, "sha256")
        person.put()
        # TODO: Send e-mail
        
    @classmethod
    def authenticate(cls, user_name, password):
        person = Person.query(Person.user_name == user_name).get()
        if person != None and person.password.test(password):
            return person