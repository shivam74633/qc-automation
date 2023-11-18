from flask import Blueprint, jsonify, request
from app.init import db
from app.models import User

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/add', methods=['POST'])
def add_user():
    username = request.json.get('username', '')
    if username:
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            new_user = User(username=username)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User added successfully', 'user_id': new_user.id}), 201
        else:
            return jsonify({'message': 'Username already exists'}), 409
    else:
        return jsonify({'message': 'Username is required'}), 400
