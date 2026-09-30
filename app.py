"""
TurfSPort - Flask Application Entry Point
=========================================
Serves all frontend pages via Flask routes.
Data layer currently uses browser localStorage (JS-only).
Future: Replace localStorage calls with real API endpoints here.
"""
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, session, render_template_string
from models import db
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from google.oauth2 import id_token
from google.auth.transport import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "turfsport-secret-key-change-in-production")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


def get_request_user():
    from models import User

    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return user

    if request.is_json:
        data = request.get_json(silent=True) or {}
        email = data.get('email') or data.get('user_email')
        username = data.get('username')
    else:
        email = request.args.get('email') or request.args.get('user_email')
        username = request.args.get('username')

    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            return user

    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            return user

    return None

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://postgres:postgres@localhost:5432/truf_sport_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ---------------------------------------------------------------------------
# Page Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Homepage: Browse available sports."""
    return render_template("index.html")

@app.route('/google-login', methods=['POST'])
def google_login():
    # Google sends the token in a form field named 'credential'
    token = request.form.get('credential')
    
    try:
        # Verify the token securely with Google using your hidden Client ID
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
        
        # Extract the user's info
        user_email = idinfo['email']
        user_name = idinfo.get('name', 'Google User')
        
        # ---> ADD THIS LINE HERE <---
        from models import User 
        
        # Look up the user in your PostgreSQL Database
        user = User.query.filter_by(email=user_email).first()
        
        # If user doesn't exist, create a new account for them automatically
        if not user:
            user = User(username=user_name, email=user_email, password_hash='GOOGLE_AUTH')
            db.session.add(user)
            db.session.commit()
            
        # Log the user in by saving their ID in the Flask session
        session['user_id'] = user.id
        session['user_email'] = user.email

        # Return a small script that also sets browser sessionStorage so
        # the client-side code (which checks sessionStorage) immediately
        # recognises the signed-in user without requiring a manual login step.
        payload = {
            'username': user.username,
            'email': user.email
        }
        js = """
        <script>
            try {
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('currentUser', JSON.stringify({username: '%(username)s', email: '%(email)s'}));
            } catch(e) {
                console.warn('Could not set sessionStorage from server login:', e);
            }
            window.location = '/';
        </script>
        """ % payload

        return render_template_string(js)

    except ValueError:
        # Invalid token
        return "Invalid Google Login", 400

@app.route("/login")
def login():
    """Login / Sign-up page."""
    return render_template("login.html")


@app.route("/venue")
def venue_detail():
    """Venue detail page (sport id passed via query string: /venue?id=box-cricket)."""
    return render_template("venue-detail.html")


@app.route("/my-bookings")
def my_bookings():
    """My Bookings page — shows user's booking history."""
    return render_template("my-bookings.html")


@app.route("/analytics")
def analytics():
    """Booking analytics dashboard for Practical 4."""
    return render_template("analytics.html")


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.route("/api/analytics")
def api_analytics():
    from models import Booking, Venue, SportCategory
    from sqlalchemy import func, extract
    from datetime import date

    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)

    query_filter = []
    if month:
        query_filter.append(extract('month', Booking.booking_date) == month)
    if year:
        query_filter.append(extract('year', Booking.booking_date) == year)

    # Base query
    base_query = Booking.query.filter(*query_filter)

    total_bookings = base_query.count()
    confirmed_bookings = base_query.filter(func.lower(Booking.status) == 'confirmed').count()
    cancelled_bookings = base_query.filter(func.lower(Booking.status) == 'cancelled').count()
    
    revenue = float(db.session.query(func.coalesce(func.sum(Booking.total_amount), 0)).filter(
        func.lower(Booking.status) == 'confirmed',
        *query_filter
    ).scalar() or 0)
    
    average_booking_value = round(revenue / confirmed_bookings, 2) if confirmed_bookings else 0.0

    # Revenue by Sport
    sport_revenue_data = db.session.query(
        SportCategory.name, 
        func.coalesce(func.sum(Booking.total_amount), 0).label('revenue')
    ).select_from(Booking).join(Venue, Booking.venue_id == Venue.id)\
     .join(SportCategory, Venue.category_id == SportCategory.id)\
     .filter(func.lower(Booking.status) == 'confirmed', *query_filter)\
     .group_by(SportCategory.name).all()

    # Peak Booking Times (by Day of Week)
    # Using 'isodow' is postgres specific. Let's try it. If it fails, we can catch it or use something generic.
    dow_data = db.session.query(
        extract('isodow', Booking.booking_date).label('dow'), 
        func.count(Booking.id)
    ).filter(func.lower(Booking.status) == 'confirmed', *query_filter)\
     .group_by('dow').order_by('dow').all()

    # Date trend (Graph 1)
    date_data = db.session.query(
        Booking.booking_date, 
        func.count(Booking.id).label('count'),
        func.coalesce(func.sum(Booking.total_amount), 0).label('revenue')
    ).filter(func.lower(Booking.status) == 'confirmed', *query_filter)\
     .group_by(Booking.booking_date).order_by(Booking.booking_date.asc()).all()

    # For 'top_venue'
    venue_data = db.session.query(Venue.name, func.count(Booking.id).label('count'))\
        .join(Booking, Booking.venue_id == Venue.id)\
        .filter(func.lower(Booking.status) == 'confirmed', *query_filter)\
        .group_by(Venue.name).order_by(func.count(Booking.id).desc()).all()

    busiest_day = max(date_data, key=lambda item: item[1])[0] if date_data else None
    top_venue = venue_data[0][0] if venue_data else None

    dow_map = {1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat', 7: 'Sun'}
    peak_times_series = [
        {'label': dow_map.get(int(dow), str(dow)), 'value': int(count)} for dow, count in dow_data
    ]

    return jsonify({
        'summary': {
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'cancelled_bookings': cancelled_bookings,
            'revenue': round(revenue, 2),
            'average_booking_value': average_booking_value,
            'top_venue': top_venue,
            'busiest_day': busiest_day.strftime('%Y-%m-%d') if busiest_day else None
        },
        'trend_series': [
            {'date': d[0].strftime('%Y-%m-%d'), 'bookings': int(d[1]), 'revenue': float(d[2])} for d in date_data
        ],
        'revenue_by_sport': [
            {'label': name, 'value': float(rev)} for name, rev in sport_revenue_data
        ],
        'peak_times': peak_times_series
    })

@app.route("/api/analytics/filters")
def api_analytics_filters():
    from models import Booking
    from sqlalchemy import func, extract
    from datetime import date
    
    years = db.session.query(extract('year', Booking.booking_date)).distinct().order_by(extract('year', Booking.booking_date).desc()).all()
    years_list = [int(y[0]) for y in years if y[0]]
    if not years_list:
        years_list = [date.today().year]
    
    return jsonify({
        'years': years_list,
        'months': [
            {'value': '', 'label': 'All Months'},
            {'value': 1, 'label': 'January'},
            {'value': 2, 'label': 'February'},
            {'value': 3, 'label': 'March'},
            {'value': 4, 'label': 'April'},
            {'value': 5, 'label': 'May'},
            {'value': 6, 'label': 'June'},
            {'value': 7, 'label': 'July'},
            {'value': 8, 'label': 'August'},
            {'value': 9, 'label': 'September'},
            {'value': 10, 'label': 'October'},
            {'value': 11, 'label': 'November'},
            {'value': 12, 'label': 'December'}
        ]
    })


@app.route("/api/slots")
def api_slots():
    venue_name = request.args.get('venue_name')
    date_str = request.args.get('date')
    if not venue_name or not date_str:
        return jsonify({"error": "Missing parameters"}), 400

    from models import Venue, Slot, Booking
    from datetime import datetime
    from sqlalchemy import func

    # Flexible venue lookup: try exact ilike, substring match, and slug/id match
    venue = None
    slug = request.args.get('id') or request.args.get('venue_id')
    search_name = venue_name.strip() if venue_name else ''

    if search_name:
        venue = Venue.query.filter(Venue.name.ilike(search_name)).first()

    if not venue and search_name:
        venue = Venue.query.filter(Venue.name.ilike(f"%{search_name}%")).first()

    if not venue and slug:
        slug_name = slug.replace('-', ' ')
        venue = Venue.query.filter(Venue.name.ilike(slug_name)).first()

    if not venue:
        # final fallback: try lowercased search
        try:
            venue = Venue.query.filter(Venue.name.ilike(search_name.lower())).first()
        except Exception:
            venue = None

    if not venue:
        return jsonify([])

    try:
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    slots = Slot.query.filter_by(venue_id=venue.id).order_by(Slot.start_time).all()
    if not slots:
        print(f"[api/slots] venue_id={venue.id} name={venue.name!r} -> no slots rows found")
        return jsonify([])

    bookings = Booking.query.filter(
        Booking.venue_id == venue.id,
        Booking.booking_date == booking_date,
        func.lower(Booking.status) == 'confirmed'
    ).all()
    booked_slot_ids = {b.slot_id for b in bookings}

    # Diagnostic log to help client debugging
    try:
        print(f"[api/slots] called with venue_name={venue_name!r}, date={date_str!r}; matched venue_id={venue.id}, slots_found={len(slots)}, bookings_on_date={len(bookings)}")
    except Exception:
        pass

    result = []
    for slot in slots:
        start_t = slot.start_time.strftime('%H:%M') if hasattr(slot.start_time, 'strftime') else str(slot.start_time)[:5]
        end_t = slot.end_time.strftime('%H:%M') if hasattr(slot.end_time, 'strftime') else str(slot.end_time)[:5]

        result.append({
            "id": slot.id,
            "start_time": start_t,
            "end_time": end_t,
            "is_booked": slot.id in booked_slot_ids,
            "display_time": f"{start_t} - {end_t}"
        })

    return jsonify(result)

@app.route("/book", methods=["POST"])
def book_slot():
    from models import Venue, Slot, Booking, User, db
    from datetime import datetime
    from sqlalchemy.exc import IntegrityError

    data = request.json
    print(f"[book_slot] incoming request json: {data}")
    if not data:
        return jsonify({"error": "Missing data"}), 400

    venue_name = data.get('venue_name')
    slot_id_raw = data.get('slot_id')
    date_str = data.get('date')

    user = get_request_user()

    if not user:
        # If client provided email/username in payload, create or fetch a matching server-side User
        try:
            data = request.get_json(silent=True) or {}
            email = data.get('email') or data.get('user_email')
            username = data.get('username') or (email.split('@')[0] if email else None)
            if email:
                existing = User.query.filter_by(email=email).first()
                if existing:
                    user = existing
                else:
                    # create a lightweight server user so bookings can be linked
                    newu = User(username=username or f'user_{int(os.times().system_time() if hasattr(os, "times") else 0)}',
                                email=email,
                                password_hash='LOCAL_AUTH')
                    db.session.add(newu)
                    db.session.commit()
                    user = newu
        except Exception:
            user = None

    if not user:
        return jsonify({"error": "Please log in to book a slot."}), 401

    # Convert slot_id safely
    try:
        slot_id = int(slot_id_raw) if slot_id_raw is not None else None
    except (ValueError, TypeError):
        slot_id = None

    if not venue_name or slot_id is None or not date_str:
        return jsonify({"error": "Missing required fields"}), 400

    venue = Venue.query.filter(Venue.name.ilike(venue_name)).first()
    if not venue:
        return jsonify({"error": "Venue not found"}), 404

    try:
        booking_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    # --- SMART BOOKING LOGIC ---
    existing_booking = Booking.query.filter_by(
        venue_id=venue.id, 
        slot_id=slot_id, 
        booking_date=booking_date
    ).first()
    
    if existing_booking:
        if existing_booking.status == 'Confirmed':
            return jsonify({"error": "This slot is already booked for this date!"}), 409
        else:
            # Overwrite the cancelled slot for the new user
            existing_booking.user_id = user.id
            existing_booking.status = 'Confirmed'
            existing_booking.total_amount = getattr(venue, 'price_per_hour', 1200)
            db.session.commit()
            return jsonify({"message": "Booking confirmed successfully"}), 201
            
    # If no row exists at all, safely insert a new one
    try:
        new_booking = Booking(
            user_id=user.id,
            venue_id=venue.id,
            slot_id=slot_id,
            booking_date=booking_date,
            total_amount=getattr(venue, 'price_per_hour', 1200),
            status='Confirmed'
        )
        db.session.add(new_booking)
        db.session.commit()
        return jsonify({"message": "Booking confirmed successfully"}), 201
        
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity conflict."}), 409


@app.route("/api/my-bookings")
def api_my_bookings():
    from models import Booking, Venue, Slot, User
    
    user = get_request_user()

    if not user:
        return jsonify([])
        
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.booking_date.desc(), Booking.id.desc()).all()
    
    result = []
    for b in bookings:
        venue = Venue.query.get(b.venue_id)
        slot = Slot.query.get(b.slot_id)
        
        time_str = ""
        if slot:
            start_t = slot.start_time.strftime('%H:%M') if hasattr(slot.start_time, 'strftime') else str(slot.start_time)[:5]
            end_t = slot.end_time.strftime('%H:%M') if hasattr(slot.end_time, 'strftime') else str(slot.end_time)[:5]
            time_str = f"{start_t} - {end_t}"

        db_status = b.status or "Confirmed"
        display_status = "CANCELLED" if db_status.upper() == "CANCELLED" else "Confirmed"

        result.append({
            "id": b.id,
            "venueName": venue.name if venue else "Unknown Venue",
            "sport": getattr(venue, 'sport_type', 'Sport'),
            "date": b.booking_date.strftime('%Y-%m-%d') if b.booking_date else '',
            "time": time_str,
            "price": f"₹{b.total_amount}" if b.total_amount else "₹500",
            "status": display_status
        })
        
    return jsonify(result)

@app.route("/cancel-booking/<int:id>", methods=["POST"])
def cancel_booking(id):
    from models import Booking, db
    
    booking = Booking.query.get_or_404(id)
    booking.status = 'CANCELLED'  # Ensure it matches uppercase
    db.session.commit()
    
    return jsonify({"message": "Booking cancelled successfully"})


@app.errorhandler(404)
def log_404(error):
    try:
        print(f"[404] {request.method} {request.path} args={dict(request.args)}")
    except Exception:
        print("[404] (could not log request details)")
    # Return JSON for easier debugging from the client network tab
    return jsonify({"error": "Not Found", "path": request.path}), 404


@app.route('/api/whoami')
def api_whoami():
    from models import User
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({
                'username': user.username,
                'email': user.email
            })
    return jsonify({})


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("  TurfSPort Flask Server")
    print("  Open: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
