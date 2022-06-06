from app import app, db
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from app.models import User, Post, Comment
from app.forms import LoginForm, RegistrationForm, EditProfile, EmptyForm
import os

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'User': User, "Post": Post, "Comment": Comment}

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
@login_required
def index():
	form = EmptyForm()
	all_users = User.query.all()
	all_posts_all_users = []
	for user in all_users:
		user_posts_query = user.posts
		for post in user_posts_query:
			all_posts_all_users.append(post)
	'''
	for post in all_posts_all_users:
		print("post id {}".format(post.id))
		print("post image_url {}".format(post.image_url))
		print("post author {}".format(post.author))
		print("post timestamp {}".format(post.timestamp))'''

	return render_template('index.html', all_posts_all_users=all_posts_all_users, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password', category="error")
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
		return redirect(url_for('upload_avatar'))
	return render_template('register.html', title='Register', form=form)

@app.route('/upload_avatar', methods=['GET','POST'])
@login_required
def upload_avatar():
	if request.method == 'post':
		return redirect('avatar_upload', )
	return render_template('upload_avatar.html')

@app.route('/newpost', methods=['POST'])
@login_required
def newpost():
	#--- Image Upload ---#
	def allowed_file(filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	# check if the post request has the file part
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	
	# If the user does not select a file, the browser submits an
	# empty file without a filename.
	if file.filename == '':
		flash('No selected file')
		return redirect(request.url)
	
	# Upload file to static
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(basedir + app.config['UPLOAD_FOLDER']) + filename)

		# Add post to db
		caption_text = request.form['caption_text']
		image_url = "./static/images/" + filename
		new_post = Post(image_url=image_url, caption=caption_text, author=current_user)
		db.session.add(new_post)
		db.session.commit()
		
		# Add tags to db
		flash('You Post Has Been Created! ')
		#return redirect(url_for('new_post_caption'), image_url=image_url)
		username=current_user.username
		return redirect(url_for('user', username=username))
	
	else:
		flash('There was a problem with your upload - please try again')
		return redirect(url_for('index'))

@app.route('/new_comment', methods=["POST"])
@login_required
def new_comment():
	form = request.form
	comment_text = form['comment_text']
	post_id = form['post_id']
	#print('POST ID: {}'.format(post_id))
	post = Post.query.get(post_id)

	new_comment = Comment(body=comment_text, user_id=current_user.id, post_id=post_id)
	db.session.add(new_comment)
	db.session.commit()
	flash('Your comment has been added! ')
	return redirect(url_for('index'))

@app.route('/<username>')
@login_required
def user(username):
	form = EmptyForm()
	user = User.query.filter_by(username=username).first_or_404()
	posts = user.posts
	
	num_followers = len(user.followers.all())
	num_following = len(user.following.all())
	num_posts = len(user.posts.all())

	followers = user.followers.all()
	following = user.following.all()
	
	return render_template('user.html', user=user, posts=user.posts, form=form, 
		num_followers=num_followers, num_following=num_following, num_posts=num_posts,
		followers=followers, following=following)

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

@app.route('/avatar_upload', methods=['POST'])
@login_required
def avatar_upload():
	def allowed_file(filename):
		return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
	
	basedir = os.path.abspath(os.path.dirname(__file__))
	
	# check if the post request has the file part
	if 'file' not in request.files:
		flash('No file part')
		return redirect(url_for('user', username=current_user.username))
	file = request.files['file']
	
	# If the user does not select a file, the browser submits an
	# empty file without a filename.
	if file.filename == '':
		flash('No selected file')
		return redirect(url_for('user', username=current_user.username))
	
	# Upload file to static
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(basedir + app.config['AVATAR_UPLOAD_FOLDER']) + filename)

		# Add post to db
		image_url = app.config['AVATAR_UPLOAD_FOLDER'] + filename
		current_user.avatar_url = image_url
		db.session.add(current_user)
		db.session.commit()
		
		flash('Your profile photo has been updated!' )
		return redirect(url_for('user', username=current_user.username))
	
	else:
		flash('There was a problem with your upload - please try again')
		return redirect(url_for('index'))

@app.route('/delete_avatar', methods=["POST"])
@login_required
def delete_avatar():
	flash('Your profile photo has been deleted!')
	default_avatar_url = app.config['DEFAULT_AVATAR_URL']
	# TODO delete old avatar
	current_user.avatar_url = default_avatar_url
	db.session.add(current_user)
	db.session.commit()
	return redirect(url_for('user', username=current_user.username))

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash('User {} not found.'.format(username))
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot follow yourself!')
			return redirect(url_for(username))
		current_user.follow(user)
		db.session.commit()
		flash('You are following {}!'.format(username))
		return redirect(url_for('user', username=user.username))
	else:
		return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		if user is None:
			flash('User {} not found.'.format(username))
			return redirect(url_for('index'))
		if user == current_user:
			flash('You cannot unfollow yourself!')
			return redirect(url_for(username))
		current_user.unfollow(user)
		db.session.commit()
		flash('You are not following {}.'.format(username))
		return redirect(url_for('user', username=user.username))
	else:
		return redirect(url_for('index'))


@app.route('/delete_post', methods=["POST"])
@login_required
def delete_post():
	# TODO
	print("Post ID: {}".format(request.form["post_id"]))
	post_id = request.form['post_id']
	# TODO this will need much more work
	post = Post.query.filter_by(id=post_id).first()
	#print("Post: {}".format(post))
	db.session.delete(post)
	db.session.commit()
	flash('Post successfully deleted! ')
	return redirect(url_for('index'))


@app.route('/messages')
@login_required
def messages():
	return render_template('messages.html')