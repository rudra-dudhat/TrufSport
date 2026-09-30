import unittest
from datetime import date, time

from app import app
from models import db, User, SportCategory, Venue, Slot, Booking


class AnalyticsEndpointTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI='sqlite:///:memory:')
        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            category = SportCategory(name='Cricket')
            db.session.add(category)
            db.session.flush()

            venue = Venue(
                name='Analytics Venue',
                category_id=category.id,
                location='Test Arena',
                price_per_hour=900,
                description='Analytics test venue'
            )
            db.session.add(venue)
            db.session.flush()

            slot1 = Slot(venue_id=venue.id, start_time=time(18, 0), end_time=time(19, 0))
            slot2 = Slot(venue_id=venue.id, start_time=time(19, 0), end_time=time(20, 0))
            db.session.add_all([slot1, slot2])
            db.session.flush()

            user = User(username='analytics_tester', email='analytics@example.com', password_hash='hash')
            db.session.add(user)
            db.session.flush()

            booking1 = Booking(
                user_id=user.id,
                venue_id=venue.id,
                slot_id=slot1.id,
                booking_date=date(2026, 8, 1),
                total_amount=venue.price_per_hour,
                status='Confirmed'
            )
            booking2 = Booking(
                user_id=user.id,
                venue_id=venue.id,
                slot_id=slot2.id,
                booking_date=date(2026, 8, 2),
                total_amount=venue.price_per_hour,
                status='Cancelled'
            )
            db.session.add_all([booking1, booking2])
            db.session.commit()

    def test_analytics_page_loads_successfully(self):
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Practical 4 Analytics', response.data)

    def test_api_analytics_returns_summary_and_series(self):
        response = self.client.get('/api/analytics')
        self.assertEqual(response.status_code, 200)

        payload = response.get_json()
        self.assertIn('summary', payload)
        self.assertEqual(payload['summary']['total_bookings'], 2)
        self.assertEqual(payload['summary']['confirmed_bookings'], 1)
        self.assertEqual(payload['summary']['cancelled_bookings'], 1)
        self.assertEqual(payload['summary']['revenue'], 900.0)
        self.assertTrue(isinstance(payload['venue_series'], list))
        self.assertTrue(isinstance(payload['date_series'], list))
        self.assertEqual(len(payload['venue_series']), 1)
        self.assertEqual(len(payload['date_series']), 2)


if __name__ == '__main__':
    unittest.main()
