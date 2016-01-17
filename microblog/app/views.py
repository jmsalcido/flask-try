from flask import render_template, flash, redirect, request, url_for, g, abort
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db
from .forms import LoginForm, RegisterForm, EditForm, PostForm
from .models import User, Post
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
    form = PostForm()
    if g.user.is_authenticated:
        user = User.query.filter_by(username=g.user.username).first()
        posts = g.user.followed_posts().all()
        return render_template('index.html', title="Home", form=form, user=user, posts=posts)
    return render_template('index.html', title="Home")


@app.route("/post", methods=["POST"])
@login_required
def post():
    if request.method == "POST":
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=g.user)
            post.save()
            flash("Your post is now live!")
            return redirect(url_for("index"))
    else:
        abort(405)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "GET" and not g.user.is_authenticated:
        return render_template('login.html', title='Sign In', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            user = find_user(request.form["username"])
            followself = user.follow(user)
            if followself is not None:
                user.save()
            login_user(user, remember=form.remember_me.data)
        else:
            return render_template('login.html', title='Sign In', form=form)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
@login_required
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
            user = User(request.form["username"], request.form["password"], request.form["email"])
            user.follow(user)
            user.save()
            flash('User successfully registered')
            return redirect(url_for("login"))
        return render_template("register.html", form=form)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/user/<username>', methods=['GET'])
def user_profile(username):
    user = find_user(username)
    if user is None:
        flash("User with username: {0} was not found".format(username))
        return redirect(url_for('index'))
    posts = user.posts.all()
    title = "{0} Profile".format(username)
    return render_template('user/user.html', title=title, user=user, posts=posts)


@app.route('/user/edit/', methods=['GET', 'POST'])
@login_required
def user_edit_profile():
    user = g.user
    form = EditForm(user.username)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            g.user.username = username
            g.user.about_me = form.about_me.data
            g.user.save()
            return redirect(url_for("user_profile", username=username))
    elif request.method == "GET":
        form.username.data = user.username
        form.about_me.data = user.about_me
    return render_template('user/edit_user.html', user=user, form=form)


@app.route("/follow/<username>")
@login_required
def follow(username):
    user = find_user(username)
    if user is None:
        flash("User: {0} was not found.".format(username))
        return redirect(url_for("index"))
    if user == g.user:
        flash("You cant follow yourself.")
        return redirect(url_for("user_profile", username=username))
    u = g.user.follow(user)
    if u is None:
        flash("Can't follow {0}".format(username))
        return redirect(url_for("user_profile", username=username))
    u.save()
    flash("You are now following: {0}".format(username))
    return redirect(url_for("user_profile", username=username))


@app.route("/unfollow/<username>")
@login_required
def unfollow(username):
    user = find_user(username)
    if user is None:
        flash("User: {0} was not found.".format(username))
        return redirect(url_for("index"))
    if user == g.user:
        flash("You can't unfollow yourself.")
        return redirect(url_for("user_profile", username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash("Can't unfollow {0}".format(username))
        return redirect(url_for("user_profile", username=username))
    u.save()
    flash("You no longer follow: {0}".format(username))
    return redirect(url_for("user_profile", username=username))


def find_user(username):
    return User.query.filter_by(username=username).first()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404


@app.errorhandler(500)
def not_found_error(error):
    db.session.rollback()
    return render_template('error/500.html'), 500
