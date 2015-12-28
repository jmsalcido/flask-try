from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(Form):
    user = StringField('User', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)


class RegisterForm(Form):
    username = StringField(label="Username", _name="username", validators=[DataRequired()])
    password = PasswordField(label="Password", _name="password", validators=[DataRequired()])
    repeated_password = PasswordField(label="Repeat Password", _name="repeated_password", validators=[DataRequired()])
    email = StringField(label="Email", _name="email", validators=[DataRequired(), Email()])
