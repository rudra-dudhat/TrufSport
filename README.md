# TurfSPort

TurfSPort is a Flask-based sports venue booking and analytics application backed by PostgreSQL. It provides sports browsing, venue details, booking history, Google Sign-In integration, and a booking analytics dashboard.

## Features

- Browse sports and venues
- Venue detail pages
- Booking and booking-history workflow
- Google Sign-In integration
- PostgreSQL database with SQLAlchemy ORM
- Booking analytics dashboard
- Revenue, booking trends, sport-wise revenue, peak-day analysis, and top-venue statistics
- Database seeding with sample sports, venues, slots, users, and historical bookings
- Automated endpoint and booking-scope tests

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- SQLAlchemy
- Google OAuth / Google Identity token verification
- HTML, CSS, JavaScript
- Pytest

## Project Structure

```text
TurfSPort/
├── app.py
├── models.py
├── seed.py
├── requirements.txt
├── .env.example
├── schema_and_seed.sql
├── example_queries.sql
├── templates/
├── static/
├── extra/
├── test_analytics.py
├── test_booking_scoping.py
└── test_endpoints.py
```

## Prerequisites

Install:

1. Python 3.11+ (Python 3.13 is also supported if the dependencies install successfully)
2. PostgreSQL
3. Git (only needed for GitHub)
4. A Google OAuth Client ID if Google Sign-In is required

## Local Setup on Windows

### 1. Create and activate a virtual environment

PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
py -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

Open **pgAdmin** or `psql` and create:

```sql
CREATE DATABASE truf_sport_db;
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and replace the placeholders with your local values. For the original computer, use the same PostgreSQL username, password, host, port, and database name that were configured in the original project:

```env
DATABASE_URL=postgresql://postgres:YOUR_POSTGRES_PASSWORD@localhost:5432/truf_sport_db
FLASK_SECRET_KEY=your-secret-key
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
FLASK_DEBUG=1
PORT=5000
```

**Never commit `.env` to GitHub.** Only `.env.example` belongs in the repository. The original project contained a real PostgreSQL password, so it is intentionally not copied into the repository template. Put that value into your local `.env` file only.

### 5. Create and seed the database

```bash
python seed.py
```

To completely reset and reseed the tables:

```bash
python seed.py --reset
```

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Tests

Run:

```bash
pytest -q
```

## GitHub

The repository should contain the source code, templates, static assets, SQL files, tests, documentation, `requirements.txt`, and `.env.example`.

Do **not** upload:

- `.env`
- `venv/`
- `__pycache__/`
- `.pytest_cache/`
- local passwords, API secrets, or private credentials

## Database Files

- `schema_and_seed.sql` contains the SQL schema/seed material.
- `example_queries.sql` contains example database queries.
- `seed.py` creates the SQLAlchemy tables and generates sample data programmatically.

## Author

TurfSPort project developed as an academic software project.
