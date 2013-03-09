'''
Created on Feb 24, 2013

@author: siebz0r
'''
import jinja2
from model.common import Person
from model.common import RegistrationActivationToken
import webapp2
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.form import Form
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

class RegistrationHandler(webapp2.RequestHandler):
    class RegistrationForm(Form):
        user_name = StringField("User name", [DataRequired(), Length(3, message="Must be at least %(min)d characters long.")])
        password = PasswordField("Password", [DataRequired(), EqualTo('password_verify', "Passwords must match.")])
        password_verify = PasswordField("Verify password", [EqualTo('password', "")])
        email_address = StringField("Email address", [DataRequired(), Email()])

    def get(self):
        form = self.RegistrationForm()
        template_values = { "form" : form }
        self.render(template_values)

    def post(self):
        form = self.RegistrationForm(self.request.params)
        if form.validate():
            person = Person()
            person.user_name = form.user_name.data
            person.email_address = form.email_address.data
            Person.register(person, form.password.data)
            self.render({"success": True,
                         "email_address": person.email_address})
        else:
            template_values = { "form" : form }
            self.render(template_values)

    def render(self, template_values):
        template = jinja2.env.get_template("register.html")
        self.response.out.write(template.render(template_values))

class LoginHandler(webapp2.RequestHandler):
    class LoginForm(Form):
        user_name = StringField("User name", [DataRequired()])
        password = PasswordField("Password", [DataRequired()])

    def get(self):
        form = self.LoginForm()
        template_values = { 'form' : form }
        self.render(template_values)

    def post(self):
        form = self.LoginForm(self.request.params)
        if form.validate():
            p = Person.authenticate(form.user_name.data, form.password.data)
            if p:
                pass
                #TODO: redirect to home or something.
            else:
                form.errors['credentials'] = "User name or password incorrect."
                self.render({ 'form' : form })
        else:
            self.render({ 'form' : form })

    def render(self, template_values):
        template = jinja2.env.get_template("login.html")
        self.response.out.write(template.render(template_values))


class ActivationHandler(webapp2.RequestHandler):
    def get(self, token):
        token = RegistrationActivationToken.query(
                              RegistrationActivationToken.token == token).get()
        if token:
            token.activate()
            self.render(True)
        self.render(False)

    def render(self, success):
        template = jinja2.env.get_template("activate.html")
        self.response.out.write(template.render({ 'success' : success }))
