from flask import Blueprint, request, jsonify
from models import db, User
from bcrypt import hashpw, gensalt, checkpw

auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = hashpw(data['password'].encode(), gensalt())
    new_user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User created successfully", user_id=new_user.id)

@auth_routes.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and checkpw(data['password'].encode(), user.password):
        return jsonify(message="Login successful", user_id=user.id)
    return jsonify(message="Invalid credentials"), 401