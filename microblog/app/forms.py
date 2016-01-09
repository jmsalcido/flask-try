from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(Form):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me', default=False)


class RegisterForm(Form):
    username = StringField(label="Username", _name="username", validators=[DataRequired()])
    password = PasswordField(label="Password", _name="password",
                             validators=[DataRequired(), EqualTo('repeated_password', 'Passwords must match')])
    repeated_password = PasswordField(label="Repeat Password", _name="repeated_password", validators=[DataRequired()])
    email = StringField(label="Email", _name="email", validators=[DataRequired(), Email("Please enter a valid email")])


class EditForm(Form):
    username = StringField(label="Username", _name="username", validators=[DataRequired()])
    about_me = TextAreaField(label="About Me", _name="about_me")
