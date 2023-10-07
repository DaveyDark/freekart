from flask import Blueprint , render_template
from models import db, Product
from datetime import datetime
from flask import Blueprint, redirect , render_template, session, url_for

core = Blueprint('core', __name__)

@core.route("/register/")
def register():
    if 'user_id' in session:
        return redirect(url_for('core.root'))
    return render_template("register.html")
@core.route("/login/")
def login():
    if 'user_id' in session:
        return redirect(url_for('core.root'))
    return render_template("login.html")
@core.route("/")
def root():
    products = db.session.query(Product).all()
    
    for product in products :
        product.days = (product.expiry - datetime.now()).days
    return render_template("landing.html" , products=products)
@core.route("/product-view/")
def product():
    return render_template("product-view.html")
@core.route("/logout/")
def logout():
    session.clear()
    return redirect('/')
