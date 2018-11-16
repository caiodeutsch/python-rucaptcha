from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from WebRucaptcha.config import Config

app = Flask(__name__)
app.config.from_object(Config)

# DB
db = SQLAlchemy(app)
@app.before_first_request
def insert_initial_values():
    from WebRucaptcha.dbconnect import Database
    # создаём таблицу в БД, если ещё не создана
    Database().creating_tables()

from WebRucaptcha import routes
