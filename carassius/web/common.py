'''
Created on Feb 24, 2013

@author: siebz0r
'''
from argparse import ArgumentError
from model.common import Person
from model.common import RegistrationActivationToken
import webapp2
from webapp2_extras import jinja2
from wtforms.fields.core import StringField
from wtforms.fields.simple import PasswordField
from wtforms.form import Form
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length

class TemplateHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2()

    def render_response(self, template=None, **context):
        template = template or self.template
        if not template:
            raise ArgumentError(
                        "A template must supplied as property or as argument.")
        self.response.write(self.jinja2.render_template(template, **context))

class RegistrationHandler(TemplateHandler):
    template = "register.html"

    class RegistrationForm(Form):
        user_name = StringField("User name", [DataRequired(), Length(3, message="Must be at least %(min)d characters long.")])
        password = PasswordField("Password", [DataRequired(), EqualTo('password_verify', "Passwords must match.")])
        password_verify = PasswordField("Verify password", [EqualTo('password', "")])
        email_address = StringField("Email address", [DataRequired(), Email()])

    def get(self):
        form = self.RegistrationForm()
        self.render_response(form=form)

    def post(self):
        form = self.RegistrationForm(self.request.params)
        if form.validate():
            person = Person()
            person.user_name = form.user_name.data
            person.email_address = form.email_address.data
            Person.register(person, form.password.data)
            self.render_response(success=True,
                                 email_address=person.email_address)
        else:
            self.render_response(form=form)

class LoginHandler(TemplateHandler):
    template = "login.html"

    class LoginForm(Form):
        user_name = StringField("User name", [DataRequired()])
        password = PasswordField("Password", [DataRequired()])

    def get(self):
        form = self.LoginForm()
        self.render_response(form=form)

    def post(self):
        form = self.LoginForm(self.request.params)
        if form.validate():
            p = Person.authenticate(form.user_name.data, form.password.data)
            if p:
                pass
                #TODO: redirect to home or something.
            else:
                form.errors['credentials'] = "User name or password incorrect."
                self.render_response(form=form)
        else:
            self.render_response(form=form)


class ActivationHandler(TemplateHandler):
    template = "activate.html"
    def get(self, token):
        token = RegistrationActivationToken.query(
                              RegistrationActivationToken.token == token).get()
        if token:
            token.activate()
            self.render_response(success=True)
        else:
            self.render_response(success=False)
