from flask import Blueprint, request, session
from sqlalchemy import or_
from models import Customer, Seller, db
import bcrypt

api = Blueprint('api', __name__)

@api.route('/register/seller', methods=['POST'])
def register_seller():
    required_keys = {'shop_name', 'lat', 'long', 'address', 'phone', 'email', 'gstin', 'name', 'password'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request', 400
    customer = Customer.query.filter_by(email=request.form['email']).first()
    if customer:
        return 'Email already in use', 409
    seller = Seller.query.filter(or_(Seller.email == request.form['email'], Seller.gstin == request.form['gstin'])).first()
    if seller:
        return 'Seller already exists', 409
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
    seller = Seller(
            shop_name=request.form.get('shop_name'),
            lat=request.form.get('lat'),
            long=request.form.get('long'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            gstin=request.form.get('gstin'),
            name=request.form.get('name'),
            password=hashed_password
            )
    db.session.add(Seller)
    db.session.commit()
    session['user_id'] = seller.id
    session['type'] = 'seller'
    return 'User Created',201

@api.route('/register/customer', methods=['POST'])
def register_customer():
    required_keys = {'name', 'lat', 'long', 'address', 'phone', 'email', 'password'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request', 400
    seller = Seller.query.filter_by(email=request.form['email']).first()
    if seller:
        return 'Email already in use', 409
    existing_customer = Customer.query.filter_by(email=request.form['email']).first()
    if existing_customer:
        return 'Customer already exists', 409
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
    new_customer = Customer(
        name=request.form.get('name'),
        lat=request.form.get('lat'),
        long=request.form.get('long'),
        address=request.form.get('address'),
        phone=request.form.get('phone'),
        email=request.form.get('email'),
        password=hashed_password
    )
    db.session.add(new_customer)
    db.session.commit()
    session['user_id'] = new_customer.id
    return 'Customer Created', 201

@api.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return 'Bad Request', 400

    seller = Seller.query.filter_by(email=email).first()

    if seller and bcrypt.checkpw(password.encode('utf-8'), seller.password.encode('utf-8')):
        session['user_id'] = seller.id
        session['type'] = 'seller'
        return 'Seller Logged In', 200

    customer = Customer.query.filter_by(email=email).first()

    if customer and bcrypt.checkpw(password.encode('utf-8'), customer.password.encode('utf-8')):
        session['user_id'] = customer.id
        session['type'] = 'customer'
        return 'Customer Logged In', 200

    return 'Login Failed', 401

@api.route('/products/add')
def add_product():
    required_keys = {'expiry', 'name', 'quantity', 'price'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request', 400
    if not 'pic' in request.files:
        return 'No pic attached', 400
    return ''
