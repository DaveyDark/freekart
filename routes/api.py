from datetime import datetime
from flask import Blueprint, request, session
from sqlalchemy import or_
from models import Customer, Product, Order, Seller, db
import bcrypt
import os
import env
import pytz
#Initialisation
default_timezone = pytz.timezone('Asia/Kolkata')

api = Blueprint('api', __name__)

#Seller registeration 
@api.route('/register/seller', methods=['POST'])
def register_seller():
    #Check if all the necessity data has been entered
    required_keys = {'shop_name', 'lat', 'long', 'address', 'phone', 'email', 'gstin', 'name', 'password'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request', 400
    #Request info from the db to check if data already in use
    customer = Customer.query.filter_by(email=request.form['email']).first()
    if customer:
        return 'Email already in use', 409
    seller = Seller.query.filter(or_(Seller.email == request.form['email'], Seller.gstin == request.form['gstin'])).first()
    if seller:
        return 'Seller already exists', 409
    #Password encryption
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
    #Adding to the database
    seller = Seller(
            shop_name=request.form.get('shop_name'),
            lat=float(request.form.get('lat')),
            long=float(request.form.get('long')),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            gstin=request.form.get('gstin'),
            name=request.form.get('name'),
            password=hashed_password
            )
    db.session.add(seller)
    db.session.commit()
    session['user_id'] = seller.id
    session['type'] = 'seller'
    return 'User Created',201

#Registering customer 
@api.route('/register/customer', methods=['POST'])
def register_customer():
    #Check if all input required is present
    required_keys = {'name', 'lat', 'long', 'address', 'phone', 'email', 'password'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request', 400
    #Check whether seller has been registered before
    seller = Seller.query.filter_by(email=request.form['email']).first()
    if seller:
        return 'Email already in use', 409
    existing_customer = Customer.query.filter_by(email=request.form['email']).first()
    if existing_customer:
        return 'Customer already exists', 409
    #Password encryption 
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), salt)
    #Adding to the database
    new_customer = Customer(
        name=request.form.get('name'),
        lat=float(request.form.get('lat')),
        long=float(request.form.get('long')),
        address=request.form.get('address'),
        phone=request.form.get('phone'),
        email=request.form.get('email'),
        password=hashed_password
    )
    db.session.add(new_customer)
    db.session.commit()
    session['user_id'] = new_customer.id
    return 'Customer Created', 201
#Login for seller as well as customer
@api.route('/login', methods=['POST'])
def login():
    #Login using email 
    email = request.form.get('email')
    password = request.form.get('password')
    #Check if not registered
    if not email or not password:
        return 'Bad Request', 400
    #Fetch data from database 
    seller = Seller.query.filter_by(email=email).first()
    #Check password
    if seller and bcrypt.checkpw(password.encode('utf-8'), seller.password):
        session['user_id'] = seller.id
        session['type'] = 'seller'
        return 'Seller Logged In', 200

    customer = Customer.query.filter_by(email=email).first()

    if customer and bcrypt.checkpw(password.encode('utf-8'), customer.password):
        session['user_id'] = customer.id
        session['type'] = 'customer'
        return 'Customer Logged In', 200

    return 'Login Failed', 401

#Seller can add product for sale 
@api.route('/products/add', methods=['POST'])
def add_product():
    #Check if all the info is present 
    required_keys = {'expiry', 'name', 'quantity', 'price', 'category'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request: Missing required fields', 400
    #Check if the user is logged in
    if 'user_id' not in session or 'type' not in session or session['type'] != 'seller':
        return 'Unauthorized', 401

    if 'pic' not in request.files:
        return 'No picture attached', 400

    file = request.files['pic']
    if file.filename == '':
        return 'No selected file', 400

    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_extensions:
        return 'Invalid file extension. Allowed extensions are .jpg, .jpeg, .png, .gif', 400
    #Add product to the database  
    product = Product(
        expiry= datetime.strptime(request.form['expiry'], "%Y-%m-%d"),
        name=request.form['name'],
        quantity=request.form['quantity'],
        category=request.form['category'],
        price=request.form['price'],
        seller_id=session['user_id']
    )
    #Save file 
    filename = os.path.join(env.UPLOAD_FOLDER, f'{product.id}{file_extension}')
    try:
        file.save(filename)
    except Exception as e:
        return f'Error uploading file: {str(e)}', 500

    db.session.add(product)
    db.session.commit()

    return 'Product created', 201
#Customer can add order to the their cart
@api.route('/orders/add', methods=["POST"])
def add_order():
    #Check if all info is present 
    required_keys = {'quantity', 'amount', 'product_id'}
    if not required_keys.issubset(request.form.keys()):
        return 'Bad Request: Missing required fields', 400
    #Check if user is logged in 
    if 'user_id' not in session or 'type' not in session or session['type'] != 'customer':
        return 'Unauthorized', 401
    #Add order to the database 
    order = Order(
        quantity=request.form['quantity'],
        amount=request.form['amount'],
        timestamp=datetime.now(),
        product_id=request.form['product_id'],
        customer_id=session['user_id']
    )

    db.session.add(order)
    db.session.commit()

    return 'Order Created', 201

def Calc_effective_price(MRP, time):
    
    if time.days > 21:
        price = MRP * 0.90
    elif time.days > 14:
        price = MRP *0.75
    elif time.days > 7:
        price = MRP*0.50
    else: 
        if time.days == 7:
            price = MRP*75
        elif time.days == 6:
            price = MRP*80
        elif time.days == 5:
            price = MRP*84
        elif time.days == 4:
            price = MRP*87
        elif time.days == 3:
            price = MRP*89
        elif time.days == 2:
            price = MRP*90
        elif time.days == 1:
            price = MRP*91

    return price