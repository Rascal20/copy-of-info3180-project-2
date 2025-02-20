from flask import Flask
from app.config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, static_folder='../dist/assets')
app.config.from_object(Config)

#db config
db = SQLAlchemy(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views
from app import models