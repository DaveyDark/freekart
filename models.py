from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Seller(db.Model):
    __tablename__ = "sellers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shop_name = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    gstin = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    products = db.relationship('Product', backref='seller', lazy=True)

    def __init__(self, shop_name, name, lat, long, address, phone, email, gstin, password):
        self.shop_name = shop_name
        self.name = name
        self.lat = lat
        self.long = long
        self.address = address
        self.phone = phone
        self.email = email
        self.gstin = gstin
        self.password = password

    def __repr__(self):
        return f"<Seller {self.shop_name}>"

class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    expiry = db.Column(db.DateTime, nullable=False)
    pic = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('sellers.id'), nullable=False)

    def __init__(self, expiry, pic, name, quantity, price, seller_id):
        self.expiry = expiry
        self.pic = pic
        self.name = name
        self.quantity = quantity
        self.price = price
        self.seller_id = seller_id

    def __repr__(self):
        return f"<Product {self.name}>"

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    orders = db.relationship('Order', backref='customer', lazy=True)

    def __init__(self, name, lat, long, address, phone, email, password):
        self.name = name
        self.lat = lat
        self.long = long
        self.address = address
        self.phone = phone
        self.password = password

    def __repr__(self):
        return f"<Customer {self.name}>"

class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    def __init__(self, quantity, amount, timestamp, customer_id, product_id):
        self.quantity = quantity
        self.amount = amount
        self.timestamp = timestamp
        self.customer_id = customer_id
        self.product_id = product_id

    def __repr__(self):
        return f"<Order {self.id}>"
