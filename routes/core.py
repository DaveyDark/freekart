from flask import Blueprint , render_template , request
from models import db, Product, Seller
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

@core.route("/search/")
def search():
    search_key = request.args["search_key"]
    products = db.session.query(Product).filter(Product.name.ilike(f"%{search_key}%")).all()
    print(products)
    return render_template("search.html", products=products)

@core.route("/product-view/<int:id>/")
def product(id):
    product = db.session.query(Product).filter_by(id=id).first()
    product.days = (product.expiry - datetime.now()).days
    product.effective_price = Calc_effective_price(product.price, product.days)
    return render_template("product-view.html" , product=product)

@core.route("/logout/")
def logout():
    session.clear()
    return redirect('/')
@core.route("/dashboard/")
def dashboard():
    seller = auth_seller()
    if not seller:
        return redirect(url_for('core.root'))
    return render_template("dashboard.html", seller=seller)
@core.route("/dashboard/add/")
def add():
    return render_template("add.html")

@core.route("/dashboard/edit/<int:id>")
def edit_product(id):
    seller = auth_seller()
    if not seller:
        return '',404
    product = Product.query.get(id)
    return render_template("edit.html", seller=seller, product=product)

@core.route("/dashboard/delete/<int:id>")
def delete_product(id):
    seller = auth_seller()
    if not seller:
        return '',404
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('core.dashboard'))

def auth_seller():
    if 'user_id' not in session or 'type' not in session or session['type'] != 'seller':
        return None
    seller = Seller.query.get(session['user_id'])
    if not seller:
        return None
    return seller
