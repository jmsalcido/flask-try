from flask import render_template, flash, redirect, request, url_for, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from .forms import LoginForm, RegisterForm, EditForm
from .models import User
from datetime import datetime


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
def index():
    if g.user.is_authenticated:
        user = User.query.filter_by(username=g.user.username).first()
        posts = [
            {
                'author': {'username': 'One'},
                'body': 'Beautiful day in Los Mochis!',
                'date': datetime.utcnow()
            },
            {
                'author': {'username': 'Two'},
                'body': 'I hate everyone.',
                'date': datetime.utcnow()
            }
        ]
        return render_template('index.html', title="Home", user=user, posts=posts)
    return render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "GET" and not g.user.is_authenticated:
        return render_template('login.html', title='Sign In', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = find_user(request.form["username"])
            if user is None or not user.verify_password(request.form["password"]):
                flash("The username or password is invalid.")
                return render_template('login.html', title='Sign In', form=form)
            login_user(user, remember=form.remember_me.data)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "GET" and not g.user.is_authenticated:
        return render_template("register.html", form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]
            existing_user = User.query.filter_by(username=username).first()
            existing_email = User.query.filter_by(email=email).first()
            if existing_user is not None:
                flash('There is an user with the username: {0}'.format(username))
                return render_template("register.html", form=form)
            if existing_email is not None:
                flash('There is an user with the email: {0}'.format(email))
                return render_template("register.html", form=form)
            user = User(username, password, email)
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered')
            return redirect(url_for("login"))
        return render_template("register.html", form=form)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<username>', methods=['GET'])
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash("User with username: {0} was not found".format(username))
        return redirect(url_for('index'))
    posts = [
        {'id': 1, 'author': user, 'body': 'This is a test post #1'},
        {'id': 2, 'author': user, 'body': 'This is a test post #2'}
    ]
    title = "{0} Profile".format(username)
    return render_template('user/user.html', title=title, user=user, posts=posts)


@app.route('/user/edit/', methods=['GET', 'POST'])
@login_required
def user_edit_profile():
    user = g.user
    form = EditForm()
    if request.method == "POST" and form.validate_on_submit():
        username = form.username.data
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is not None and g.user.username != username:
            flash("User with username: " + username + " already exists.")
            return render_template('user/edit_user.html', user=user, form=form)
        g.user.username = username
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        return redirect(url_for("user_profile", username=username))
    elif request.method == "POST":

        return render_template('user/edit_user.html', user=user, form=form)
    elif request.method == "GET":
        form.username.data = user.username
        form.about_me.data = user.about_me
        return render_template('user/edit_user.html', user=user, form=form)
    else:
        return redirect(url_for("index"))


def find_user(username):
    return db.session.query(User).filter(User.username == username).first()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500
