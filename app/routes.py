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

from app import app
from flask import Flask, render_template, url_for, request
#from app.models import User

'''@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student}'''

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/login', methods=["GET","POST"])
def login():
	if request.method =="POST":
		# TODO Verify login credentials
		return render_template('index.html')
	return render_template('login.html')


