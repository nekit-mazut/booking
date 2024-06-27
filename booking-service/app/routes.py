from flask import Blueprint, request, jsonify
from . import db
from .models import Room, Booking
from sqlalchemy import and_

bp = Blueprint('bookings', __name__)


@bp.route('/room_types', methods=['GET'])
def get_room_types():
    room_types = Room.query.with_entities(Room.room_type).distinct().all()
    room_types_list = [row[0] for row in room_types]
    return jsonify({'room_types': room_types_list}), 200


@bp.route('/rooms/search', methods=['POST'])
def search_available_rooms():
    data = request.get_json()
    check_in = data.get('check_in')
    check_out = data.get('check_out')
    capacity = data.get('capacity')
    room_types = data.get('room_types', [])
    price_min = data.get('price_min')
    price_max = data.get('price_max')

    if not check_in or not check_out or not capacity:
        return jsonify({'error': 'Check-in, check-out date, and capacity are required parameters.'}), 400

    query = Room.query.filter(Room.capacity >= capacity)

    if room_types:
        query = query.filter(Room.room_type.in_(room_types))

    if price_min is not None:
        query = query.filter(Room.price >= price_min)

    if price_max is not None:
        query = query.filter(Room.price <= price_max)

    rooms = query.all()
    available_rooms = []
    for room in rooms:
        overlapping_bookings = Booking.query.filter(
            Booking.room_id == room.id,
            and_(
                Booking.check_in < check_out,
                Booking.check_out > check_in
            )
        ).all()

        if not overlapping_bookings:
            available_rooms.append({
                'id': room.id,
                'name': room.name,
                'room_type': room.room_type,
                'price': room.price,
                'capacity': room.capacity
            })

    response_data = {'rooms': available_rooms}

    return jsonify(response_data), 200


@bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    if not data or not all(key in data for key in ('name', 'roomType', 'price', 'capacity')):
        return jsonify({'message': 'Missing required fields'}), 400

    new_room = Room(
        name=data['name'],
        room_type=data['roomType'],
        price=data['price'],
        capacity=data['capacity']
    )

    db.session.add(new_room)
    db.session.commit()

    return jsonify({
        'id': new_room.id,
        'name': new_room.name,
        'room_type': new_room.room_type,
        'price': new_room.price,
        'capacity': new_room.capacity,
    }), 201


@bp.route('/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json()

        check_in = data['check_in']
        check_out = data['check_out']
        room_id = data['room_id']
        user_id = data['user_id']
        total_price = data['total_price']

        new_booking = Booking(
            room_id=room_id,
            user_id=user_id,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price
        )

        db.session.add(new_booking)
        db.session.commit()

        return jsonify({'message': 'Booking created successfully'}), 201

    except KeyError as e:
        return jsonify({'error': f'Missing key: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': 'An error occurred while creating the booking.'}), 500


@bp.route('/bookings/user/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    user_bookings = Booking.query.filter_by(user_id=user_id).all()
    if not user_bookings:
        return jsonify({'message': f'No bookings found for user with id {user_id}'}), 404
    bookings_data = [{
        'id': booking.id,
        'room_id': booking.room_id,
        'check_in': booking.check_in,
        'check_out': booking.check_out,
        'total_price': booking.total_price
    } for booking in user_bookings]
    return jsonify({'bookings': bookings_data}), 200


@bp.route('/rooms/<int:room_id>', methods=['PUT'])
def update_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({'message': 'Room with id {} does not exist'.format(room_id)}), 404
    data = request.get_json()
    room.name = data.get('name', room.name)
    room.room_type = data.get('room_type', room.room_type)
    room.price = data.get('price', room.price)
    db.session.commit()
    return jsonify({'message': 'Room with id {} has been updated'.format(room_id)}), 200


@bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return jsonify({'message': 'Booking with id {} does not exist'.format(booking_id)}), 404
    db.session.delete(booking)
    db.session.commit()
    return jsonify({'message': 'Booking with id {} has been cancelled'.format(booking_id)}), 200
