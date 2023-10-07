from flask import Flask, redirect, render_template, session, url_for
from routes.api import api
from routes.core import core
from models import db
import env
#Initialising the app
app = Flask(__name__)
app.secret_key = env.SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///freekart.db"
app.config['UPLOAD_FOLDER'] = env.UPLOAD_FOLDER

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(core, url_prefix='/')
