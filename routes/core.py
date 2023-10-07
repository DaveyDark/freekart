from flask import Blueprint , render_template
from models import db, Product
from datetime import datetime
from flask import Blueprint, redirect , render_template, session, url_for
from routes.api import Calc_effective_price

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
        product.effective_price = Calc_effective_price(product.price, product.days)
    return render_template("landing.html" , products=products)

@core.route("/product-view/<int:id>/")
def product():
    product = db.session.query(Product).filter_by(id=id)
    product.days = (product.expiry - datetime.now()).days
    product.effective_price = Calc_effective_price(product.price, product.days)
    return render_template("product-view.html" , product=product)

@core.route("/logout/")
def logout():
    session.clear()
    return redirect('/')
@core.route("/dashboard/")
def dashboard():
    return render_template("dashboard.html")
@core.route("/dashboard/add/")
def add():
    return render_template("add.html")
