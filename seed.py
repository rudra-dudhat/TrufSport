import argparse
from datetime import time, date, timedelta
from app import app
from models import db, User, SportCategory, Venue, Slot, Booking


def seed_database(reset=False):
    with app.app_context():
        print("Ensuring database tables exist...")
        db.create_all()

        if reset:
            print("Reset mode requested: dropping existing tables...")
            db.drop_all()
            db.create_all()

        print("Seeding Users...")
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@example.com',
                password_hash='dummy_hash_for_now',
                role='user'
            )
            db.session.add(test_user)
            db.session.flush()

        print("Seeding Sport Categories and Venues...")
        venues_data = [
            {'cat': 'Box Cricket', 'icon': 'cricket', 'name': 'Greenfield Box Cricket', 'location': 'Sector 14, Main Road, City Center', 'desc': 'Welcome to Greenfield Box Cricket, the premier location for 6-a-side matches. Equipped with high-intensity floodlights, professional-grade turf, and dugout areas.', 'price': 800, 'img': '/static/images/box-cricket1.jpg'},
            {'cat': 'Pickleball', 'icon': 'pickleball', 'name': 'Smash Pickleball Court', 'location': 'Downtown', 'desc': 'Top quality indoor pickleball courts with synthetic flooring.', 'price': 600, 'img': '/static/images/pickleball1.jpg'},
            {'cat': 'Football', 'icon': 'football', 'name': 'GoalArena 5v5', 'location': 'North City Mall', 'desc': 'High-intensity 5-a-side football turf with floodlights.', 'price': 1200, 'img': '/static/images/football1.jpg'},
            {'cat': 'Pool', 'icon': 'pool', 'name': 'Cue Masters Lounge', 'location': 'City Center', 'desc': 'Professional 8-ball pool tables in a relaxed lounge setting.', 'price': 300, 'img': '/static/images/pool1.jpg'},
            {'cat': 'Bowling', 'icon': 'bowling', 'name': 'Strike Zone Alley', 'location': 'Westend Mall', 'desc': '10-lane bowling alley with automated scoring and cafe.', 'price': 400, 'img': '/static/images/bowling1.jpg'},
            {'cat': 'Badminton', 'icon': 'badminton', 'name': 'Feather Shuttle Club', 'location': 'East End', 'desc': 'Wooden courts designed for professional badminton play.', 'price': 500, 'img': '/static/images/badminton1.jpg'},
            {'cat': 'Go-Karting', 'icon': 'gokarting', 'name': 'Speedway Tracks', 'location': 'Highway 51', 'desc': 'Outdoor 800m go-karting track with professional karts.', 'price': 900, 'img': '/static/images/gokarting1.jpg'},
            {'cat': 'Golf', 'icon': 'golf', 'name': 'Elite Greens Country Club', 'location': 'Hillside', 'desc': '18-hole lush green golf course with caddy service.', 'price': 1500, 'img': '/static/images/golf1.jpg'},
            {'cat': 'Tennis', 'icon': 'tennis', 'name': 'Grand Slam Tennis Academy', 'location': 'Sports Complex', 'desc': 'Synthetic hard courts for standard tennis matches.', 'price': 700, 'img': '/static/images/tennis1.jpg'},
            {'cat': 'Volleyball', 'icon': 'volleyball', 'name': 'Spikers Beach Court', 'location': 'Lake View', 'desc': 'Outdoor sand volleyball court by the lake.', 'price': 600, 'img': '/static/images/volleyball1.jpg'},
            {'cat': 'Basketball', 'icon': 'basketball', 'name': 'Hoops Indoor Arena', 'location': 'Downtown YMCA', 'desc': 'Full-court indoor basketball with hardwood floors.', 'price': 800, 'img': '/static/images/basketball1.jpg'},
            {'cat': 'Cricket Ground', 'icon': 'cricket', 'name': 'Lords Local Ground', 'location': 'Outskirts', 'desc': 'Full-size leather ball cricket ground with grass outfield and match-ready pitch.', 'price': 2500, 'img': '/static/images/default1.jpg'}
        ]

        venues = []
        for vd in venues_data:
            cat = SportCategory.query.filter_by(name=vd['cat']).first()
            if not cat:
                cat = SportCategory(name=vd['cat'], icon_name=vd['icon'])
                db.session.add(cat)
                db.session.flush()

            venue = Venue.query.filter_by(name=vd['name']).first()
            if not venue:
                venue = Venue(
                    category_id=cat.id,
                    name=vd['name'],
                    description=vd['desc'],
                    location=vd['location'],
                    price_per_hour=vd['price'],
                    image_url=vd['img']
                )
                db.session.add(venue)
            else:
                venue.category_id = cat.id
                venue.description = vd['desc']
                venue.location = vd['location']
                venue.price_per_hour = vd['price']
                venue.image_url = vd['img']

            venues.append(venue)

        db.session.commit()

        print("Seeding Slots (06:00 to 23:00)...")
        for venue in venues:
            for hour in range(6, 23):
                existing_slot = Slot.query.filter_by(venue_id=venue.id, start_time=time(hour, 0)).first()
                if not existing_slot:
                    slot = Slot(
                        venue_id=venue.id,
                        start_time=time(hour, 0),
                        end_time=time(hour + 1, 0)
                    )
                    db.session.add(slot)

        db.session.commit()

        print("Seeding Sample Bookings (Historical Data)...")
        import random
        from datetime import timedelta, date

        end_date = date.today() + timedelta(days=30)
        start_date = end_date - timedelta(days=730)
        delta_days = (end_date - start_date).days

        # Pre-fetch slots for faster randomized booking
        all_slots_by_venue = {}
        for venue in venues:
            all_slots_by_venue[venue.id] = Slot.query.filter_by(venue_id=venue.id).all()

        total_bookings_to_create = 2500  # Generate ~2500 bookings
        
        for _ in range(total_bookings_to_create):
            random_days = random.randint(0, delta_days)
            booking_date = start_date + timedelta(days=random_days)
            
            venue = random.choice(venues)
            slots = all_slots_by_venue.get(venue.id)
            if not slots:
                continue
                
            slot = random.choice(slots)
            
            existing_booking = Booking.query.filter_by(
                venue_id=venue.id,
                slot_id=slot.id,
                booking_date=booking_date
            ).first()
            
            if not existing_booking:
                # 85% confirmed, 15% cancelled
                status = 'Confirmed' if random.random() < 0.85 else 'Cancelled'
                booking = Booking(
                    user_id=test_user.id,
                    venue_id=venue.id,
                    slot_id=slot.id,
                    booking_date=booking_date,
                    total_amount=venue.price_per_hour,
                    status=status
                )
                db.session.add(booking)

        try:
            db.session.commit()
            print("Database seeded successfully with historical data!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding bookings: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Seed TurfSPort database.')
    parser.add_argument('--reset', action='store_true', help='Drop and recreate all tables before seeding.')
    args = parser.parse_args()
    seed_database(reset=args.reset)
