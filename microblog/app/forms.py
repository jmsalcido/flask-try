from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User
from sqlalchemy import or_


class LoginForm(Form):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember Me', default=False)

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is None or not user.verify_password(self.password.data):
            self.username.errors.append("Username of password is invalid, please try again.")
            return False
        return True


class RegisterForm(Form):
    username = StringField(label="Username", _name="username", validators=[DataRequired()])
    password = PasswordField(label="Password", _name="password",
                             validators=[DataRequired(), EqualTo('repeated_password', 'Passwords must match')])
    repeated_password = PasswordField(label="Repeat Password", _name="repeated_password", validators=[DataRequired()])
    email = StringField(label="Email", _name="email", validators=[DataRequired(), Email("Please enter a valid email")])

    def validate_on_submit(self):
        if not super().validate_on_submit():
            return False
        user = User.query.filter(or_(User.username == self.username.data, User.email == self.email.data)).first()
        if user is not None:
            if self.username.data == user.username:
                error = "The username: {0} already exists".format(user.username)
                self.username.errors.append(error)
            elif self.email.data == user.email:
                error = "The email: {0} is already registered for an user.".format(user.email)
                self.email.errors.append(error)
            return False
        return True


class EditForm(Form):
    username = StringField(label="Username", _name="username", validators=[DataRequired()])
    about_me = TextAreaField(label="About Me", _name="about_me")

    def __init__(self, original_username, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_username = original_username

    def validate_on_submit(self):
        if not Form.validate_on_submit(self):
            return False
        if self.username.data == self.original_username:
            return True
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            self.username.errors.append("This username is already in use. Please choose another one.")
            self.username.data = self.original_username
            return False
        return True
