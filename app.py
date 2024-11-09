from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from config import Config
from bcrypt import hashpw, gensalt, checkpw
from datetime import datetime
from extensions import db

# Initialize the app and configuration
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', secondary='cart_items', backref='carts')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return render_template('index.html')
  

# Route to render the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form
        hashed_password = hashpw(data['password'].encode(), gensalt())
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('signin'))
    return render_template('signup.html')

# Route to render the signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and checkpw(data['password'].encode(), user.password):
            access_token = create_access_token(identity=user.id)
            return jsonify(message="Login successful", token=access_token)
        return jsonify(message="Invalid credentials"), 401
    return render_template('signin.html')

# Add product route for admin
@app.route('/addproduct', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        data = request.form
        new_product = Product(name=data['name'], description=data['description'],
                              price=float(data['price']), category=data['category'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify(message="Product added successfully", product_id=new_product.id)
    return render_template('add_product.html')

# Update product route
@app.route('/updateproduct/<int:product_id>', methods=['POST'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        data = request.form
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.category = data.get('category', product.category)
        db.session.commit()
        return jsonify(message="Product updated successfully")
    return jsonify(message="Product not found"), 404

# Delete product route
@app.route('/deleteproduct/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify(message="Product deleted successfully")
    return jsonify(message="Product not found"), 404

# Get all products route
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'category': p.category} for p in products]
    return render_template('products.html', products=product_list)

# Add product to cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    # Implementation of adding to cart logic
    return jsonify(message="Product added to cart successfully")

# Get cart details
@app.route('/cart', methods=['GET'])
def get_cart():
    # Implementation of cart retrieval logic
    return render_template('cart.html')

# Place order
@app.route('/placeorder', methods=['POST'])
def place_order():
    # Implementation of order placement logic
    return jsonify(message="Order placed successfully")

# View orders
@app.route('/orders', methods=['GET'])
def get_orders():
    # Implementation of orders retrieval logic
    return render_template('orders.html')

# Database setup - create tables if not exist
with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)