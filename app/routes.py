# route for login

# route for forgotten password

# route for signup

# home/feed/index route

# route for view profile

# route for edit profile

# route for viewing a post

# route for creating/editing a post

# route to view my messages

# route to create a new message

# route for searching

from app import app, db
from flask import Flask, render_template, url_for, request, flash, redirect
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.models import User
from app.forms import LoginForm, RegistrationForm, EditProfile

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}

@app.route('/')
@app.route('/index')
@login_required
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, 
					email=form.email.data, 
					firstname=form.firstname.data,
					lastname=form.lastname.data,
					bio=form.bio.data,
					website=form.website.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Account Created!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route('/<username>', methods=['GET','POST'])
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	posts = [
		{'author': user, 'body': 'Test post #1'},
		{'author': user, 'body': 'Test post #2'}
	]
	return render_template('user.html', user=user, posts=posts, )

@app.route('/edit_profile', methods=["GET","POST"])
@login_required
def edit_profile():
	user = User.query.filter_by(username=current_user.username).first_or_404()
	form = EditProfile()
	if form.validate_on_submit():
		user = User.query.filter_by(username=current_user.username).first()
		if form.username.data != "":
			user.username = form.username.data
		if form.email.data != "":
			user.email = form.email.data
		if form.firstname.data != "":
			user.firstname = form.firstname.data
		if form.lastname.data != "":
			user.lastname = form.lastname.data
		if form.website.data != "":
			user.website = form.website.data
		if form.bio.data != "":
			user.bio = form.bio.data
		db.session.commit()
		flash('Profile Successfully Updated!')
		return redirect(url_for('user', username=current_user.username))
	elif request.method == "get":
		form.email.data = current_user.email 
		form.firstname.data = current_user.firstname
		form.lastname.data = current_user.lastname
		form.website.data = current_user.website
		form.bio.data = current_user.bio
	return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/messages')
@login_required
def messages():
	return render_template('messages.html')