from flask import Blueprint, request, jsonify
from . import db
from .models import Room, Booking
from sqlalchemy import or_

bp = Blueprint('bookings', __name__)


@bp.route('/rooms', methods=['GET'])
def get_available_rooms():
    check_in = request.args.get('check_in')
    check_out = request.args.get('check_out')
    capacity = request.args.get('capacity')

    if not check_in or not check_out or not capacity:
        return jsonify({'error': 'Check-in, check-out date, and capacity are required parameters.'}), 400

    available_rooms = Room.query.filter(Room.capacity >= capacity) \
        .filter(or_(Room.is_booked == False, Room.is_booked == None)) \
        .filter(or_(Room.booking_start_date == None, Room.booking_start_date <= check_out)) \
        .filter(or_(Room.booking_end_date == None, Room.booking_end_date >= check_in)) \
        .all()

    rooms_data = []
    for room in available_rooms:
        rooms_data.append({
            'id': room.id,
            'name': room.name,
            'room_type': room.room_type,
            'price': room.price,
            'capacity': room.capacity,
            'is_booked': room.is_booked,
            'booking_start_date': room.booking_start_date,
            'booking_end_date': room.booking_end_date
        })

    return jsonify({'rooms': rooms_data}), 200


@bp.route('/rooms', methods=['POST'])
def create_room():
    data = request.get_json()
    new_room = Room(name=data['name'], room_type=data['room_type'], price=data['price'], capacity=data['capacity'],
                    is_booked=False, booking_start_date=None, booking_end_date=None)
    db.session.add(new_room)
    db.session.commit()
    return jsonify(
        {'id': new_room.id, 'name': new_room.name, 'room_type': new_room.room_type, 'price': new_room.price,
         'capacity': new_room.capacity, 'is_booked': new_room.is_booked,
         'booking_start_date': new_room.booking_start_date, 'booking_end_date': new_room.booking_end_date}), 201


@bp.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    new_booking = Booking(room_id=data['room_id'], user_id=data['user_id'], check_in=data['check_in'],
                          check_out=data['check_out'], total_price=data['total_price'])
    db.session.add(new_booking)
    db.session.commit()
    return jsonify({'id': new_booking.id, 'room_id': new_booking.room_id, 'user_id': new_booking.user_id,
                    'check_in': new_booking.check_in, 'check_out': new_booking.check_out,
                    'total_price': new_booking.total_price}), 201


@bp.route('/bookings/user/<int:user_id>', methods=['GET'])
def get_user_bookings(user_id):
    user_bookings = Booking.query.filter_by(user_id=user_id).all()
    if not user_bookings:
        return jsonify({'message': 'No bookings found for user with id {}'.format(user_id)}), 404
    bookings_data = [{'id': booking.id, 'room_id': booking.room_id, 'check_in': booking.check_in,
                      'check_out': booking.check_out, 'total_price': booking.total_price} for booking in user_bookings]
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
