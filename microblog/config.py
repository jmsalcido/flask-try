import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

basedir = os.path.abspath(os.path.dirname(__file__))

databaseurl = os.environ.get("OPENSHIFT_POSTGRESQL_DB_URL")
logdir = os.environ.get("OPENSHIFT_LOG_DIR")

if logdir is None:
    logdir = "tmp/"

use_postgres = True
if use_postgres:
    if databaseurl is not None:
        SQLALCHEMY_DATABASE_URI = databaseurl
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/flaskmicroblog'
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# mail server settings
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_USE_TLS = False
MAIL_USE_SSL = True

# administrator list
ADMINS = ['eljose152@gmail.com']

POSTS_PER_PAGE = 10
