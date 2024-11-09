from flask import Blueprint, request, jsonify
from models import db, Order

order_routes = Blueprint('order_routes', __name__)

@order_routes.route('/placeorder', methods=['POST'])
def place_order():
    data = request.get_json()
    order = Order(user_id=data['user_id'], shipping_details=data['shipping_details'])
    db.session.add(order)
    db.session.commit()
    return jsonify(message="Order placed successfully", orderId=order.id), 201

@order_routes.route('/orders/customer/<int:customer_id>', methods=['GET'])
def get_orders_by_customer(customer_id):
    orders = Order.query.filter_by(user_id=customer_id).all()
    order_list = [{"id": o.id, "created_at": o.created_at, "status": o.status} for o in orders]
    return jsonify(orders=order_list), 200
