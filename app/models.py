from datetime import datetime
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	password_hash = db.Column(db.String(128))
	email = db.Column(db.String(120), unique=True, nullable=False)
	firstname = db.Column(db.String(20), unique=False, nullable=False)
	lastname = db.Column(db.String(20), unique=False, nullable=False)
	bio = db.Column(db.String(80), unique=False, nullable=True)
	website = db.Column(db.String(80), unique=False, nullable=True)

	posts = db.relationship('Post', backref='author', lazy='dynamic')


	def __repr__(self):
		return '<User %r>' % self.username

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)