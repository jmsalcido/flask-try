from datetime import datetime
from app import db, lm
from flask.ext.login import UserMixin
import hashlib
from passlib.apps import custom_app_context as pwd_context

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('users.user_id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('users.user_id')))


class SaveMixin(object):
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, UserMixin, SaveMixin):
    __tablename__ = 'users'
    id = db.Column(name='user_id', type_=db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    registered_on = db.Column('registered_on', db.DateTime)
    about_me = db.Column(db.String(140))
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.columns.follower_id == id),
                               secondaryjoin=(followers.columns.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.email = email
        self.registered_on = datetime.utcnow()
        self.hash_password(password)

    def avatar(self, size):
        gravatar_url = 'http://www.gravatar.com/avatar/{0}?d=mm&s={1}'
        return gravatar_url.format(hashlib.md5(self.email.encode('utf-8')).hexdigest(), size)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            self.save()
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            self.save()
            return self

    def is_following(self, user):
        return self.followed.filter(followers.columns.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def __repr__(self):
        return '<User {0}>'.format(self.username)

    @staticmethod
    def make_unique_username(username):
        def calculate_name(_str, _number):
            return _str + str(_number)

        if User.query.filter_by(username=username).first() is None:
            return username
        version = 2
        new_username = calculate_name(username, version)
        while True:
            new_username = calculate_name(username, version)
            if User.query.filter_by(username=new_username).first() is None:
                break
            version += 1
        return new_username


class Post(db.Model, SaveMixin):
    __tablename__ = "posts"
    id = db.Column(name="post_id", type_=db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    def __init__(self, body, timestamp=datetime.utcnow(), author=None):
        self.body = body
        self.timestamp = timestamp
        self.author = author

    def __repr__(self):
        return '<Post {0}:{1}>'.format(self.id, self.timestamp)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
