from datetime import datetime
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('following_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, index=True, nullable=False)
	avatar_url = db.Column(db.String(140))
	password_hash = db.Column(db.String(128))
	email = db.Column(db.String(120), unique=True, index=True, nullable=False)
	firstname = db.Column(db.String(20), unique=False)
	lastname = db.Column(db.String(20), unique=False)
	bio = db.Column(db.String(80), unique=False)
	website = db.Column(db.String(80), unique=False)

	posts = db.relationship('Post', backref='author', lazy='dynamic')
	comments = db.relationship('Comment', backref='author', lazy='dynamic')
	following = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.following_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

	def follow(self, user):
		if not self.is_following(user):
			self.following.append(user)

	def unfollow(self, user):
		if self.is_following(user):
			self.following.remove(user)

	def is_following(self, user):
		return self.following.filter(
			followers.c.following_id == user.id).count() > 0
			
	def following_posts(self):
		following = Post.query.join(
			followers, (followers.c.following_id == Post.user_id)).filter(
				followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		return following.union(own).order_by(Post.timestamp.desc()) 

	def __repr__(self):
		return '<User {}> <password {}>'.format(self.username, self.password_hash)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)



class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	image_url = db.Column(db.String(140))
	caption = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	comments = db.relationship('Comment', backref='post', lazy='dynamic')

	def __repr__(self):
		return '<Post img_url: {}> <Caption: {}'.format(self.image_url, self.caption)



class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
	post_id = db.Column(db.Integer, db.ForeignKey('post.id'), index=True, nullable=False)

	def __repr__(self):
		return '<Comment: {}><Post: {}><User: {}>'.format(self.body, self.post_id, self.user_id)