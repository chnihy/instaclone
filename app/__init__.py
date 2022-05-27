from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import Config
from flask_sqlalchemy import SQLAlchemy

# create instance of app
app = Flask(__name__)

# import config
app.config.from_object(Config)

'''# initialize db
db = SQLAlchemy(app)
db.init_app(app)'''

# initialize bootstrap
bootstrap = Bootstrap(app)


from app import routes