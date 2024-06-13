import requests
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from .models import User
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
import re

bp = Blueprint('users', __name__)


def is_valid_email(email):
    return re.match(r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b$', email)


def is_valid_password(password):
    return len(password) >= 8


@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(key in data for key in ('username', 'email', 'password')):
        return jsonify({'message': 'Missing required fields'}), 400

    if not is_valid_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400

    if not is_valid_password(data['password']):
        return jsonify({'message': 'Password must be at least 8 characters long'}), 400

    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'User with this username or email already exists'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        email_notifications=data.get('email_notifications', True)
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'email_notifications': new_user.email_notifications,
        'created_at': new_user.created_at
    }), 201


@bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user)

    if not user.is_admin and user.id != user_id:
        return jsonify({"msg": "Access forbidden"}), 403

    target_user = User.query.get_or_404(user_id)
    return jsonify({
        'id': target_user.id,
        'username': target_user.username,
        'email': target_user.email,
        'email_notifications': target_user.email_notifications,
        'is_admin': target_user.is_admin,
        'created_at': target_user.created_at
    })


@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user)

    if not user.is_admin and user.id != user_id:
        return jsonify({"msg": "Access forbidden"}), 403

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.email_notifications = data.get('email_notifications', user.email_notifications)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'email_notifications': user.email_notifications,
        'created_at': user.created_at
    }), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user)

    if not user.is_admin and user.id != user_id:
        return jsonify({"msg": "Access forbidden"}), 403

    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@bp.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity={'id': user.id, 'is_admin': user.is_admin},
                                    expires_delta=datetime.timedelta(hours=24))
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401


@bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify(access_token=access_token), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    # Клиент должен удалить токен
    return jsonify({"msg": "Successfully logged out"}), 200


@bp.route('/users/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({'message': 'Invalid email address'}), 400
    token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
    user.set_reset_token(token)
    db.session.commit()
    # send email with token (integration with email service)
    return jsonify({'message': 'Password reset token sent'}), 200


@bp.route('/users/<int:user_id>/notification-preferences', methods=['PUT'])
@jwt_required()
def set_notification_preferences(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.email_notifications = data.get('email_notifications', user.email_notifications)
    db.session.commit()
    return jsonify({
        'id': user.id,
        'email_notifications': user.email_notifications
    }), 200


@bp.route('/users/<int:user_id>/bookings', methods=['GET'])
@jwt_required()
def getuser_bookings(user_id):
    user = User.query.get_or_404(user_id)
    response = requests.get(f'http://localhost:5000/bookings/user/{user_id}')
    if response.status_code != 200:
        return jsonify({'error': 'Could not fetch bookings from booking-service'}), 500
    bookings = response.json()
    return jsonify(bookings), 200


@bp.route('/users/admin', methods=['POST'])
@jwt_required()
def create_admin():
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user)

    if not user.is_admin:
        return jsonify({"msg": "Admin access required"}), 403

    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        email_notifications=data.get('email_notifications', True),
        is_admin=True
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email,
        'email_notifications': new_user.email_notifications,
        'is_admin': new_user.is_admin,
        'created_at': new_user.created_at
    }), 201
