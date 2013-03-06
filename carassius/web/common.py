'''
Created on Feb 24, 2013

@author: siebz0r
'''
import webapp2
import jinja2
from wtforms.form import Form
from wtforms.fields.simple import PasswordField
from wtforms.validators import Length, DataRequired, EqualTo, Email
from model.common import Person
from wtforms.fields.core import StringField

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
            # TODO: Render registration success page
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
