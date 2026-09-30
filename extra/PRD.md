# PRD.md — Project Requirements Document
## Sports Facility Management & Turf Booking System

**Subject:** Open Source Technologies (3CS502ME24)
**Type:** College Semester Project (built with an AI coding agent, guided step-by-step)

---

## 1. Project Overview

A website where users can browse different sports facilities (turfs, courts, tables,
tracks), see available time slots for a chosen date, see the price for each slot,
and book a slot. Facility owners/admin can manage venues and view all bookings.

This is a **booking + slot-availability system**, not a social network or a
tournament manager. Keep every feature decision anchored to that one sentence.

## 2. Problem Statement

Right now, booking a box cricket ground, badminton court, or pool table usually
happens over a phone call or a WhatsApp message. There's no single place to see
what's free right now, what it costs, and to lock in a slot instantly. This
project solves that with one website covering many sports.

## 3. Target Users

| User type | What they do |
|---|---|
| **Player / Customer** | Browses sports & venues, checks slot availability, books a slot, views/cancels their own bookings |
| **Admin (facility manager)** | Adds/edits venues & sports, sets prices, blocks slots (maintenance), views all bookings |

No third user role needed for this project. Keep it to these two.

## 4. Scope for This Semester (MVP)

Build **one working, demo-ready website** covering the full booking flow for
multiple sports, with an admin side to manage it. Polish, extra integrations,
and "nice-to-have" ideas are explicitly **out of scope now** and listed in
Section 8 — they are for after the semester ends.

## 5. Sports / Facilities to Support

The system must be **generic** — a sport is a row in the database, not
hardcoded pages. Seed data should include at least:

Box Cricket, Pickleball Court, Football Box (5-a-side turf), 8-Ball Pool Table,
Bowling Alley, Badminton Court, Go-Karting, Golf, Tennis Court, Volleyball
Court, Basketball Court, Cricket Ground.

New sports must be addable from the admin panel without touching code.

## 6. Core Features (Functional Requirements)

### Customer-facing
1. Home page listing all sports/venues with a search/filter (by sport, price).
2. Venue detail page: description, images, price per slot, amenities.
3. **Slot booking page**: pick a date → see a grid of time slots for that venue,
   each slot clearly marked **Free** (green) or **Booked** (red) or **Past**
   (grey, disabled). Price shown per slot (peak/off-peak pricing).
4. Booking form: select slot(s), enter basic details, confirm booking.
5. Server-side check to prevent two people booking the same slot
   (no double-booking, even if two tabs are open).
6. Booking confirmation screen with a booking ID.
7. "My Bookings" page — logged-in user sees upcoming & past bookings, can
   cancel a future booking.
8. Simple login/signup (username, email, password). No social login needed.

### Admin-facing
9. Admin login (separate from customer login, or Django's built-in admin is fine).
10. Add / edit / delete a sport & venue, set base price and peak-hour price.
11. Block a slot manually (e.g., maintenance) so it shows as unavailable.
12. View all bookings across all venues, filterable by date/sport.
13. **Analytics view**: which sports are booked most, busiest hours/days,
    revenue trend — built from a Jupyter/Pandas/Matplotlib notebook (see
    Section 9), not required to be a live in-app dashboard.

## 7. Booking & Pricing Logic (must be explicit, agents get this wrong)

- A "slot" = one venue + one date + one time range (e.g., 6:00–7:00 PM).
- Each sport/venue has a **base price**, and optionally a **peak multiplier**
  for evening/weekend slots (keep it simple: e.g., peak = 1.5x base).
- A slot's status is always computed live from the bookings table:
  `Booked` if a confirmed booking exists for that exact venue+date+time,
  else `Free` (or `Past` if the date/time has already passed).
- Never let two confirmed bookings exist for the same venue+date+time. This
  check must happen on the server (in the view/model layer), not only in JS.
  - **Concurrency Constraint implemented**: Uses a SQLAlchemy `UniqueConstraint('venue_id', 'slot_id', 'booking_date', name='uq_active_booking')`.
  - **Transaction Safe**: The `/book` endpoint executes within a `db.session` block, catching `IntegrityError` to safely rollback and reject simultaneous double-booking attempts.

## 8. Out of Scope for This Semester (explicitly deferred)

- Real payment gateway (use a "Confirm Booking" button that just marks the
  booking as confirmed — no real money movement).
- Email/SMS notifications.
- Multi-city / multi-branch support.
- Ratings & reviews, loyalty points, coupons.
- Native mobile app.

These can be added **after** the semester, once the core is stable. Do not let
the coding agent add these early — it will bloat the project and introduce bugs.

## 9. How This Project Covers the Full LOP

| LOP Practical | Where it lives in this project |
|---|---|
| 1. HTML + CSS webpage | Home page (Phase 1) |
| 2. JS interactivity (slider/validation/mini game) | Venue image slider + booking form validation (Phase 2) |
| 3. MySQL (DB, CRUD, queries) | Core booking database (Phase 3) |
| 4. Jupyter + Matplotlib visualization | Admin analytics notebook (Phase 8) |
| 5. Django project + basic web app | Backend framework for the whole site (Phase 4) |
| 6. Bootstrap responsive layout | Booking pages + admin dashboard (Phase 5) |
| 7. jQuery DOM manipulation | Live slot grid highlighting (Phase 6) |
| 8. Pandas data manipulation | Same analytics notebook, data loading/cleaning step (Phase 8) |
| 9. EDA with Pandas + Matplotlib | Same notebook, insights step (Phase 8) |
| 10. Python + SQLite CRUD app | Standalone admin utility script, separate from the Django/MySQL app (Phase 9) |

## 10. Success Criteria (what "done" looks like for this semester)

- A user can open the site, pick any sport, see a real slot grid, book a free
  slot, and see it turn red immediately after.
- Admin can log in, add a new venue, and it appears on the site instantly.
- No crash on invalid input (empty form, past date, already-booked slot).
- The analytics notebook runs top-to-bottom without errors and produces at
  least 3 charts from real booking data.
- The standalone SQLite CRUD script runs from the terminal and can add/view/
  update/delete a venue record independently of the website.
- You (the student) can explain every file in the project in your own words.
