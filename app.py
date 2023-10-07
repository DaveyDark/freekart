from flask import Flask, redirect, render_template, session, url_for
from routes.api import api
from routes.core import core
from models import db

app = Flask(__name__)
app.secret_key = "apex_secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///utype.db"

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(core, url_prefix='/')
