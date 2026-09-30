# Phases.md — Build Order

Build strictly in this order. Do not start a phase until the previous one is
working and demoable. Each phase lists which LOP practical it satisfies.

---

## Phase 0 — Project Setup
- Create the folder structure from Architecture.md.
- Set up Python virtual environment, install Django, mysqlclient (or PyMySQL),
  Pandas, Matplotlib, Jupyter.
- Create a MySQL database for the project (empty, just created).
- Initialize a git repo (optional but recommended).
- **Deliverable:** empty project skeleton that runs (`python -m http.server`
  for now for static pages), README with setup steps.

## Phase 1 — Static Home Page *(LOP Practical 1: HTML + CSS)*
- Plain `index.html` (no Django yet) listing all sports as cards (Box
  Cricket, Pickleball, Football Box, 8-Ball Pool, Bowling, Badminton,
  Go-Karting, Golf, Tennis, Volleyball, Basketball, Cricket Ground).
- Use internal CSS (`<style>` in `<head>`) for layout, fonts, colors, grid of
  cards. Use inline CSS for 2–3 specific elements (e.g. hero banner
  background, a highlighted "featured sport" badge).
- No JS yet, no backend yet — pure HTML/CSS.
- **Deliverable:** a static page that looks good and lists every sport.

## Phase 2 — JavaScript Interactivity *(LOP Practical 2: JS)*
- Add a `venue-detail.html` static page for one sample venue.
- Add an image slider/carousel for venue photos (vanilla JS).
- Add client-side validation on a sample booking form (name required, valid
  phone number, date can't be in the past) — still static, no backend saves
  yet.
- Internal CSS for new styles, 1–2 inline where useful, separate `.js` file
  for the slider/validation logic.
- **Deliverable:** interactive slider + a form that blocks obviously invalid
  input, all still static HTML.

## Phase 3 — MySQL Database Design *(LOP Practical 3: MySQL)*
- Design and create the database by hand first (outside Django): tables for
  `sport`, `venue`, `booking`, with sensible columns and foreign keys.
- Practice raw SQL: create tables, insert seed data (the 12 sports + a few
  sample venues), write a few SELECT queries (e.g. "all bookings for
  Badminton", "venues under ₹500/hr").
- **Deliverable:** a populated MySQL database + a `.sql` file with the schema
  and seed data, plus a short file showing 3–5 example queries and results.

## Phase 4 — Django Project Setup *(LOP Practical 5: Django)*
- `django-admin startproject booking_project`, create the `core` app.
- Connect Django to the MySQL database from Phase 3 (via `settings.py`).
- Create Django models mirroring the schema (Sport, Venue, Booking) and run
  migrations against the existing MySQL DB (or let Django create it fresh,
  student's choice — pick the simpler path).
- Rebuild Phase 1's home page as a Django template (`home.html`) — now
  pulling sports/venues from the database instead of being hardcoded.
- From this phase onward, **all new CSS is external** (`static/css/style.css`).
- **Deliverable:** the home page now runs through Django and shows real DB
  data.

## Phase 5 — Bootstrap Responsive Layout *(LOP Practical 6: Bootstrap)*
- Rebuild the templates using Bootstrap 5 (CDN) — responsive grid for the
  sport cards, a proper navbar, responsive booking form.
- Make sure it looks correct on mobile width too (this is the whole point of
  the practical).
- **Deliverable:** the site is now responsive and uses Bootstrap components
  (navbar, cards, buttons, modal for confirmation, etc.).

## Phase 6 — Live Slot Grid with jQuery *(LOP Practical 7: jQuery)*
- Build the actual booking page: pick a date, see a grid of time slots for
  the chosen venue.
- Use jQuery to: highlight a slot on hover, mark it green/red/grey based on
  data from the server, disable clicking on booked/past slots, and update the
  grid instantly (without full page reload) when a booking is confirmed.
- Wire this up to real Django views/models — a booking must actually get
  created and immediately reflect as "Booked" in the grid.
- Implement the server-side double-booking check here (see Rules.md #5).
- **Deliverable:** the core feature of the whole project — a real, working
  slot booking flow.

## Phase 7 — Remaining Core Pages
- My Bookings page (list + cancel).
- Login / Signup using Django's built-in auth.
- Admin pages: manage venues (add/edit/delete), view all bookings.
- Booking confirmation page with a generated booking ID.
- **Deliverable:** the full customer + admin flow works end-to-end.

## Phase 8 — Data Analytics Notebook *(LOP Practicals 4, 8, 9: Matplotlib, Pandas, EDA)*
- Export bookings data from MySQL to a CSV (or connect directly with
  `pandas.read_sql`).
- In a Jupyter Notebook (`analytics/booking_analysis.ipynb`):
  - Load and clean the data with Pandas (handle missing/odd values).
  - Explore it: bookings per sport, bookings per day of week, peak hours,
    revenue over time.
  - Visualize with Matplotlib: at least a bar chart (bookings per sport), a
    line chart (revenue over time), and one more chart of the student's
    choice (e.g. histogram of booking times).
- **Deliverable:** a clean, well-commented notebook that runs top-to-bottom
  and tells a short "story" about the booking data — this is a standalone
  artifact, doesn't need to be embedded live in the website.

## Phase 9 — Standalone SQLite CRUD Tool *(LOP Practical 10: Python + SQLite)*
- A separate, small Python script (`sqlite_admin_tool/admin_tool.py`), not
  part of Django.
- Creates its own local SQLite database with one table (e.g. `Venue`: id,
  name, sport, price).
- Simple menu-driven terminal program (or a tiny Tkinter GUI if the student
  wants to push further) implementing full CRUD: Create, Read, Update,
  Delete.
- **Deliverable:** runs independently with `python admin_tool.py`, no
  dependency on the Django project.

## Phase 10 — Polish & Demo Prep
- Fix any UI rough edges, add basic seed data for a smooth demo (several
  sports, several venues, a mix of free/booked slots so the grid actually
  demonstrates both states).
- Write/update the README with setup + run instructions.
- Do one full walkthrough of the entire flow (student books a slot, admin
  sees it, cancel it, etc.) to catch any last bugs.
- **Deliverable:** a demo-ready project covering all 10 LOP practicals.

---

### After the semester (do not build now)
Real payment gateway, notifications, multi-branch support, reviews, coupons,
mobile app — see PRD.md Section 8.
