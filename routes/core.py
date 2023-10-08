from flask import Blueprint , render_template , request
from models import Order, db, Product, Seller, Customer
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
        product.effective_price = Calc_effective_price(product.price, product.days, product.category)
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
    product.effective_price = Calc_effective_price(product.price, product.days,product.category)
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
    orders = Order.query.join(Product).filter(Product.seller_id == seller.id).all()
    for product in seller.products:
        product.time = product.expiry.strftime("%d-%m-%Y")
    for order in orders:
        order.product_name = Product.query.get(order.product_id).name
        order.customer_name = Customer.query.get(order.customer_id).name
        order.time = order.timestamp.strftime("%d-%m-%Y  %H:%M %p")
    return render_template("dashboard.html", seller=seller, orders=orders)

@core.route("/profile/")
def profile():
    if 'user_id' not in session or 'type' not in session or session['type'] != 'customer':
        return redirect(url_for('core.root'))
    customer = Customer.query.get(session['user_id'])
    orders = Order.query.filter_by(customer_id=session["user_id"]).all()
    for order in orders:
        order.product_name = Product.query.get(order.product_id).name
        order.timestamp = order.timestamp.strftime("%d-%m-%Y  %H:%M %p")
    return render_template("profile.html", customer=customer, orders=orders)
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

@core.route("/dashboard/accept/<int:id>")
def accept_order(id):
    seller = auth_seller()
    if not seller:
        return '',404
    order = Order.query.get(id)
    order.status = "Accepted"
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('core.dashboard'))

@core.route("/dashboard/refuse/<int:id>")
def refuse_order(id):
    seller = auth_seller()
    if not seller:
        return '',404
    order = Order.query.get(id)
    order.status = "Refused"
    db.session.add(order)
    db.session.commit()
    return redirect(url_for('core.dashboard'))


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
