from flask import Flask
from flask_login import LoginManager
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite+pysqlite:///microblog.db"
app.config['SECRET_KEY'] = 'PD3608'

login = LoginManager(app)

db = SQLAlchemy()
db.init_app(app)

from app import routes, models, alquimias

with app.app_context():
    db.create_all()


