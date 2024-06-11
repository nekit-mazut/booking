from . import db


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, default=False)
    booking_start_date = db.Column(db.DateTime)
    booking_end_date = db.Column(db.DateTime)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    room = db.relationship('Room', backref=db.backref('bookings', lazy=True))

    def __repr__(self):
        return f'<Booking {self.id} - Room {self.room_id} - User {self.user_id}>'
