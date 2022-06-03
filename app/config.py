import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = ['pdf', 'png', 'jpg', 'jpeg', 'gif', 'svg']
    
    UPLOAD_FOLDER = '/static/images/'
    AVATAR_UPLOAD_FOLDER = '/static/images/avatars/'
    DEFAULT_AVATAR_URL = '/static/images/avatars/placeholder_small.png'

