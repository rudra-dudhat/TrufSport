# Architecture.md — Sports Facility Management & Turf Booking System

## 1. Tech Stack (final — do not swap without editing this file first)

| Layer | Technology |
|---|---|
| Structure | HTML5 |
| Styling | CSS3 — **mixed intentionally**: inline, internal, and external (see rule below) + Bootstrap 5 (CDN) for later pages |
| Client interactivity | Vanilla JavaScript (Phase 2) + jQuery (CDN, Phase 6) |
| Backend framework | Python + Flask |
| Main database | PostgreSQL (via Flask-SQLAlchemy) |
| Standalone CRUD utility | Python + `sqlite3` (separate small script, not part of Django) |
| Data analytics | Jupyter Notebook + Pandas + Matplotlib |
| Dev environment | Python virtual environment (`venv`), pip |

**CSS rule (per assignment requirement — all 3 CSS types must appear):**
- Home page (`index.html`, Phase 1): use **inline** CSS on a couple of elements
  (e.g. a hero banner `style="..."`) and **internal** CSS (`<style>` block in
  `<head>`) for the rest of that page's layout.
- Booking/venue detail page (Phase 2): also internal CSS for anything new,
  plus 1–2 inline styles where a one-off tweak is needed.
- From Phase 4 onward (Django templates), everything moves to **external**
  CSS files (`static/css/style.css`, `static/css/booking.css`, etc.) — this is
  the realistic, maintainable approach and mirrors how real Django apps work.

## 2. High-Level Flow

```
Browser (HTML/CSS/JS)
        |
        v
Flask Routes (app.py -> templates)
        |
        v
Flask-SQLAlchemy ORM Models (sports, venues, slots, bookings, users)
        |
        v
PostgreSQL Database
```

Separately, **not connected live to the website**:

```
MySQL bookings table
        |
   (export to CSV, or read directly with a DB connector)
        v
Jupyter Notebook (Pandas: clean/explore -> Matplotlib: charts)
        -> produces admin analytics report (screenshots/PNGs used in the
           admin analytics page, or shown as the notebook itself in the demo)
```

And a fully separate mini-tool:

```
standalone_admin_tool.py  <-->  local SQLite file (venues_local.db)
```
Used only to demonstrate practical #10 (Python + SQLite CRUD). It manages a
simple `Venue` table independently — it does NOT need to sync with the main
MySQL database. Keep it deliberately small and separate.

## 3. Folder Structure

```
sports-booking-system/
│
├── static-pages/                  # Phase 1-2 output (plain HTML/CSS/JS, before Django)
│   ├── index.html
│   ├── venue-detail.html
│   ├── css/
│   │   └── (empty until Phase 2 needs a shared file, prefer internal CSS here)
│   └── js/
│       └── interactivity.js
│
├── booking_project/                # Django project root (created in Phase 4)
│   ├── manage.py
│   ├── booking_project/            # Django settings package
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── core/                       # main Django app
│   │   ├── models.py               # Sport, Venue, Slot, Booking, (User via Django auth)
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   ├── style.css
│   │   │   │   ├── booking.css
│   │   │   │   └── admin.css
│   │   │   └── js/
│   │   │       ├── slot-grid.js    # jQuery DOM manipulation (Phase 6)
│   │   │       └── validation.js
│   │   └── templates/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── venue_detail.html
│   │       ├── booking_form.html
│   │       ├── booking_confirmation.html
│   │       ├── my_bookings.html
│   │       ├── login.html
│   │       └── signup.html
│   │
│   └── requirements.txt
│
├── analytics/                      # Phase 8 — Jupyter/Pandas/Matplotlib
│   ├── booking_analysis.ipynb
│   └── exported_bookings.csv
│
├── sqlite_admin_tool/               # Phase 9 — standalone practical #10
│   ├── admin_tool.py
│   └── venues_local.db              # generated at runtime
│
├── Memory.md
└── README.md
```

## 4. Core Data Models (Django ORM — used from Phase 4 onward)

- **Sport**: name, description, icon/image, category
- **Venue**: name, sport (FK), location, base_price, peak_price, image, is_active
- **Slot**: venue (FK), date, start_time, end_time — OR compute slots
  dynamically from fixed operating hours rather than storing every empty slot
  (simpler; recommended for a college project — store rows only for booked
  slots, and treat "no row = free" for everything else).
- **Booking**: user (FK), venue (FK), date, start_time, end_time, price_paid,
  status (confirmed/cancelled), created_at
- **User**: Django's built-in `auth.User` — do not build a custom auth system
  from scratch.

## 5. Page & API Routes (final)

1. Home / sport listing (`/`)
2. Venue detail page (`/venue?id=...`)
3. Slot booking API (`/api/slots`, `/book`)
4. My Bookings page (`/my-bookings` & `/api/my-bookings`, `/cancel-booking/<id>`)
5. Login page (`/login`)

Multiple pages are fine here — this project needs distinct URLs for each
screen above; do not try to cram everything into a single-page app.
