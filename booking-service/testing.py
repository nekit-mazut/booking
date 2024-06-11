import unittest
from app import create_app, db
from app.models import Room, Booking


class TestRoomEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_available_rooms(self):
        room1 = Room(name="Room1", room_type="Single", price=100.0, capacity=1)
        room2 = Room(name="Room2", room_type="Double", price=150.0, capacity=2)
        room3 = Room(name="Room3", room_type="Suite", price=200.0, capacity=4)
        room4 = Room(name="Room4", room_type="Single", price=120.0, capacity=1, is_booked=True)
        db.session.add_all([room1, room2, room3, room4])
        db.session.commit()

        response = self.client.get('/rooms?check_in=2024-06-12&check_out=2024-06-12&capacity=1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['rooms']), 3)

    def test_create_room(self):
        response = self.client.post('/rooms',
                                    json={"name": "New Room", "room_type": "Single", "price": 100.0, "capacity": 1})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue('id' in data)

    def test_create_booking(self):
        room = Room(name="Room1", room_type="Single", price=100.0, capacity=1)
        db.session.add(room)
        db.session.commit()
        response = self.client.post('/bookings', json={"room_id": room.id, "user_id": 1, "check_in": "2024-06-12",
                                                       "check_out": "2024-06-14", "total_price": 200.0})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertTrue('id' in data)

    def test_get_user_bookings(self):
        room = Room(name="Room1", room_type="Single", price=100.0, capacity=1)
        db.session.add(room)
        db.session.commit()
        booking1 = Booking(room_id=room.id, user_id=1, check_in="2024-06-12", check_out="2024-06-14",
                           total_price=200.0)
        booking2 = Booking(room_id=room.id, user_id=1, check_in="2024-06-15", check_out="2024-06-17",
                           total_price=200.0)
        db.session.add_all([booking1, booking2])
        db.session.commit()

        response = self.client.get('/bookings/user/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['bookings']), 2)

    def test_update_room(self):
        room = Room(name="Room1", room_type="Single", price=100.0, capacity=1)
        db.session.add(room)
        db.session.commit()

        response = self.client.put(f'/rooms/{room.id}', json={"name": "Updated Room"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], f'Room with id {room.id} has been updated')

    def test_cancel_booking(self):
        room = Room(name="Room1", room_type="Single", price=100.0, capacity=1)
        db.session.add(room)
        db.session.commit()
        booking = Booking(room_id=room.id, user_id=1, check_in="2024-06-12", check_out="2024-06-14",
                          total_price=200.0)
        db.session.add(booking)
        db.session.commit()

        response = self.client.delete(f'/bookings/{booking.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], f'Booking with id {booking.id} has been cancelled')

    if __name__ == '__main__':
        unittest.main()
