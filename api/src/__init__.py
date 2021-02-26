from flask import Flask
from src.config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

config_name = os.getenv('APP_ENV')

app = Flask(__name__)
app.config.from_object(app_config[config_name])
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src import routes, models