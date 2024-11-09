from flask import Blueprint, request, jsonify
from models import db, Product

product_routes = Blueprint('product', __name__)

@product_routes.route('/addproduct', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(name=data['name'], description=data['description'],
                          price=data['price'], category=data['category'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(message="Product added", product_id=new_product.id)

@product_routes.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.name for product in products])