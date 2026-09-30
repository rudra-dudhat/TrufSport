import unittest
from datetime import date

from app import app
from models import db, User, SportCategory, Venue, Slot, Booking


class BookingScopingTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            category = SportCategory(name='Football')
            venue = Venue(name='Test Venue', category=category, location='Test City', price_per_hour=500, description='Test')
            db.session.add(category)
            db.session.flush()
            venue.category_id = category.id
            slot1 = Slot(venue_id=venue.id, start_time='10:00:00', end_time='11:00:00')
            slot2 = Slot(venue_id=venue.id, start_time='11:00:00', end_time='12:00:00')
            db.session.add(venue)
            db.session.add(slot1)
            db.session.add(slot2)
            db.session.flush()

            user1 = User(username='alice', email='alice@example.com', password_hash='hash1')
            user2 = User(username='bob', email='bob@example.com', password_hash='hash2')
            db.session.add_all([user1, user2])
            db.session.flush()

            booking1 = Booking(user_id=user1.id, venue_id=venue.id, slot_id=slot1.id, booking_date=date(2026, 8, 1), total_amount=500, status='Confirmed')
            booking2 = Booking(user_id=user2.id, venue_id=venue.id, slot_id=slot2.id, booking_date=date(2026, 8, 2), total_amount=500, status='Confirmed')
            db.session.add_all([booking1, booking2])
            db.session.commit()

    def test_api_my_bookings_uses_email_to_scope_to_the_correct_user(self):
        response = self.client.get('/api/my-bookings?email=bob@example.com')
        self.assertEqual(response.status_code, 200)

        payload = response.get_json()
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]['date'], '2026-08-02')

    def test_book_route_uses_email_to_assign_booking_to_the_correct_user(self):
        response = self.client.post('/book', json={
            'venue_name': 'Test Venue',
            'slot_id': 2,
            'date': '2026-08-03',
            'email': 'bob@example.com'
        })

        self.assertEqual(response.status_code, 201)
        with app.app_context():
            booking = Booking.query.filter_by(booking_date=date(2026, 8, 3)).first()
            self.assertIsNotNone(booking)
            self.assertEqual(booking.user_id, User.query.filter_by(email='bob@example.com').first().id)


if __name__ == '__main__':
    unittest.main()
