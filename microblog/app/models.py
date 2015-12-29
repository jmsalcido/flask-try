from datetime import datetime
from app import db, lm
from flask.ext.login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(name='user_id', type_=db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.registered_on = datetime.utcnow()
        self.hash_password(password)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return '<User {0}>'.format(self.username)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(name="post_id", type_=db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __repr__(self):
        return '<Post {0}:{1}>'.format(self.id, self.timestamp)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
