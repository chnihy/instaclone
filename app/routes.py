from app import app, db
from flask import Flask, render_template, url_for
from app.models import Student

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Student': Student}

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


