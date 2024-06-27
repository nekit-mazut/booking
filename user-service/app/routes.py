from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
import re
from flask import Blueprint, request, jsonify
from .models import User, db
import requests
import random
import string

bp = Blueprint('users', __name__)


def generate_confirmation_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


@bp.route('/users/<int:user_id>/change_email', methods=['PUT'])
@jwt_required()
def change_user_email(user_id):
    data = request.get_json()
    new_email = data.get('email')

    if not new_email:
        return jsonify({'message': 'New email is required'}), 400

    user = User.query.get_or_404(user_id)
    user.email = new_email
    db.session.commit()

    return jsonify({
        'message': 'Email updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200


@bp.route('/users/<int:user_id>/change_password', methods=['PUT'])
@jwt_required()
def change_user_password(user_id):
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')

    if not current_password or not new_password:
        return jsonify({'message': 'Current and new passwords are required'}), 400

    user = User.query.get_or_404(user_id)

    if not user.check_password(current_password):
        return jsonify({'message': 'Current password is incorrect'}), 401

    user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully'}), 200


@bp.route('/users/change_username/<int:user_id>', methods=['PUT'])
@jwt_required()
def change_user_username(user_id):
    current_user = get_jwt_identity()
    if current_user['id'] != user_id:
        return jsonify({'message': 'Access forbidden'}), 403

    data = request.get_json()
    new_username = data.get('username')

    if not new_username:
        return jsonify({'message': 'New username is required'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.username = new_username
    db.session.commit()

    return jsonify({'message': 'Username updated successfully'}), 200


@bp.route('/users/send_confirmation', methods=['POST'])
def send_confirmation():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({'message': 'Email, username, and password are required'}), 400

    confirmation_code = generate_confirmation_code()
    subject = "Confirm your account"
    body = f"Your confirmation code is {confirmation_code}"

    email_response = requests.post('http://localhost:5002/email/send', json={
        'to': email,
        'subject': subject,
        'body': body
    })

    if email_response.status_code != 200:
        return jsonify({'message': 'Failed to send confirmation email'}), 500

    return jsonify({'message': 'Confirmation email sent', 'confirmation_code': confirmation_code}), 200


@bp.route('/confirm', methods=['POST'])
def confirm_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    entered_code = data.get('confirmation_code')
    original_code = data.get('original_code')

    if entered_code != original_code:
        return jsonify({'message': 'Invalid confirmation code'}), 400

    new_user = User(
        username=username,
        email=email
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id, expires_delta=datetime.timedelta(days=1))

    return jsonify({
        'access_token': access_token,
        'user': {
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
            'created_at': new_user.created_at
        }
    }), 201


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


@bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user['id'])

    if not user.is_admin and user.id != user_id:
        return jsonify({"msg": "Access forbidden"}), 403

    data = request.get_json()
    user_to_update = User.query.get_or_404(user_id)
    user_to_update.username = data.get('username', user_to_update.username)
    user_to_update.email = data.get('email', user_to_update.email)
    user_to_update.email_notifications = data.get('email_notifications', user_to_update.email_notifications)
    if 'password' in data:
        user_to_update.set_password(data['password'])
    db.session.commit()
    return jsonify({
        'id': user_to_update.id,
        'username': user_to_update.username,
        'email': user_to_update.email,
        'email_notifications': user_to_update.email_notifications,
        'created_at': user_to_update.created_at
    }), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    user = User.query.get_or_404(current_user['id'])

    if not user.is_admin and user.id != user_id:
        return jsonify({"msg": "Access forbidden"}), 403

    user_to_delete = User.query.get_or_404(user_id)
    db.session.delete(user_to_delete)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200


@bp.route('/login', methods=['POST'])
@bp.route('/authenticate', methods=['POST'])
def login_or_authenticate():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data['password']

    user = None
    if username:
        user = User.query.filter_by(username=username).first()
    elif email:
        user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity={'id': user.id, 'username': user.username})
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_user():
    return jsonify({"msg": "Successfully logged out"}), 200


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
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
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


@bp.route('/users/check_auth', methods=['GET'])
@jwt_required()
def check_auth():
    current_user = get_jwt_identity()
    user_id = current_user.get('id') if isinstance(current_user, dict) else current_user

    user = User.query.get(user_id)

    if user:
        return jsonify({
            'isAuthenticated': True,
            'isAdmin': user.is_admin
        }), 200
    else:
        return jsonify({
            'isAuthenticated': False,
            'isAdmin': False
        }), 401
