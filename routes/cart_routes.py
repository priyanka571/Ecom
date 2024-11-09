from flask import Blueprint, request, jsonify
from models import db, Cart

cart_routes = Blueprint('cart_routes', __name__)

@cart_routes.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    cart_item = Cart(user_id=data['user_id'], product_id=data['product_id'], quantity=data['quantity'])
    db.session.add(cart_item)
    db.session.commit()
    return jsonify(message="Product added to cart"), 201

@cart_routes.route('/cart', methods=['GET'])
def get_cart():
    user_id = request.args.get('user_id')
    cart_items = Cart.query.filter_by(user_id=user_id).all()
    cart_list = [{"product_id": c.product_id, "quantity": c.quantity} for c in cart_items]
    return jsonify(cart=cart_list), 200
