from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import session
from flask_migrate import Migrate

# create instance of app
app = Flask(__name__)

# import config
app.config.from_object(Config)

# initialize db
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# initialize bootstrap
bootstrap = Bootstrap(app)

# Initialize Flask Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



from app import routes, models, forms