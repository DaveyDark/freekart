from flask import Blueprint , render_template

core = Blueprint('core', __name__)

@core.route("/")
def hello():
    return render_template("landing.html")
