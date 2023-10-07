from flask import Blueprint 

core = Blueprint('core', __name__)

@core.route("/")
def hello():
    return "Hello World!"
