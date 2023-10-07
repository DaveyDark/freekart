from flask import Blueprint , render_template

core = Blueprint('core', __name__)

@core.route("/register/")
def login():
    return render_template("landing.html")
@core.route("/product-view")
def product():
    return render_template("product-view")
