from flask import Blueprint , render_template
from models import db, Product
from datetime import datetime

core = Blueprint('core', __name__)

@core.route("/register/")
def login():
    return render_template("register.html")
@core.route("/")
def root():
    products = db.session.query(Product).all()
    
    for product in products :
        product.days = (product.expiry - datetime.now()).days
    return render_template("landing.html" , products=products)
@core.route("/product-view")
def product():
    return render_template("product-view")
