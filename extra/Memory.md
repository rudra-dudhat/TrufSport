# Memory.md — Project Progress Log

> This file is empty on purpose. Do not fill it in now. Once the coding agent
> starts Phase 0, it should update this file **at the end of every phase**
> (per Rules.md #7) so that a new chat session can read this one file and
> know exactly where the project stands — instead of re-reading the whole
> codebase or guessing.

---

## How to use this file (instructions for the agent)

After finishing a phase, append a new entry below using this exact format:

```
## Phase N — <short title>  (Status: ✅ Done / ⚠️ Partial / ❌ Blocked)
**Date:** <date>
**What was built:** 1-3 sentences, plain language.
**Files added/changed:** list them.
**How to run/test it:** exact commands or steps.
**Decisions made:** anything the student and agent agreed on that isn't
already in PRD/Architecture/Design/Rules.
**Known issues / TODO:** anything left rough, to revisit later.
```

Keep entries short. This file is a status log, not a diary — the goal is
that reading it top to bottom takes under 2 minutes and gives full context.

---

## Current Status

**Last completed phase:** Phase 3 — MySQL Database Design.
**Next phase to build:** Phase 4 — Data Analytics Notebook (Standalone).

---

## Log

## Phase 0 — Project Setup  (Status: ✅ Done)
**Date:** 2026-07-21
**What was built:** Created the project folder structure (`static-pages`, `analytics`, `sqlite_admin_tool`), initialized a Python virtual environment, and set up a Git repository.
**Files added/changed:** `.git/`, `venv/`, `static-pages/css/`, `static-pages/js/`, `analytics/`, `sqlite_admin_tool/`.
**How to run/test it:** Run `.\venv\Scripts\activate` to activate the virtual environment. Verify folders exist in the workspace.
**Decisions made:** Django installation and DB connection are skipped for now per the prompt ("no Django yet, just Python/MySQL basics"). MySQL DB will be set up during Phase 3 since MySQL CLI is not currently available in PATH.
**Known issues / TODO:** Need to verify MySQL connection info in Phase 3.

## Phase 1 — Static Home Page  (Status: ✅ Done)
**Date:** 2026-07-21
**What was built:** Created a purely static `index.html` (LOP Practical 1) that lists all 12 sports as cards. Includes a Navbar, Hero section, and Footer. 
**Files added/changed:** `static-pages/index.html`.
**How to run/test it:** Open `static-pages/index.html` directly in any web browser.
**Decisions made:** Used internal CSS for the main layout and colors, and used inline CSS specifically on the Hero banner and the "Featured" badge on the first card to strictly satisfy the assignment rules (Rule 3). Simple emojis were used for sport icons to avoid extra dependencies for now.
**Known issues / TODO:** All links (e.g., `venue-detail.html`) currently lead nowhere or just reload the page; this will be wired up in Phase 2.

## Phase 2 — JavaScript Interactivity  (Status: ✅ Done)
**Date:** 2026-07-21
**What was built:** Added `venue-detail.html` with an image slider/carousel and a client-side form validation script (LOP Practical 2).
**Files added/changed:** `static-pages/venue-detail.html`, `static-pages/js/interactivity.js`.
**How to run/test it:** Open `static-pages/index.html` and click on any sport card to go to `venue-detail.html`. Test the image slider using the arrows or dots. Try submitting the booking form empty, with a bad phone number, or a past date to see the validation errors.
**Decisions made:** Wrote pure Vanilla JS to satisfy the project constraints, implementing a custom slider (with real Unsplash sports images instead of emojis) and form validation without external libraries. Added dynamic content loading via URL parameters so that clicking any sport on the homepage loads the correct title, location, and description on the venue detail page without duplicating HTML files. Cleaned up alerts to avoid referencing future phases (6/7) to keep the demo clean.
**Known issues / TODO:** The booking form doesn't save to the DB yet. Next step is to design the MySQL database.

## Phase 3 — MySQL Database Design  (Status: ✅ Done)
**Date:** 2026-07-21
**What was built:** Designed the raw MySQL database structure and wrote two SQL files: one to create the tables (`sport`, `venue`, `booking`) and insert seed data, and another providing 4 example SELECT queries showing JOINs and aggregations (LOP Practical 3).
**Files added/changed:** `schema_and_seed.sql`, `example_queries.sql`.
**How to run/test it:** If you have MySQL Server installed (like XAMPP or MySQL Workbench), you can run `source schema_and_seed.sql` and `source example_queries.sql` in your MySQL console, or open the files in your DB management tool and execute them.
**Decisions made:** Wrote the SQL manually into text files since `mysql` isn't in the terminal's PATH. Based on user feedback, expanded the DB seed data to ensure ALL 12 sports have at least one venue and sample bookings. Also created `login.html` and `my-bookings.html` as static mockups and wired them up in the navigation so all links work perfectly without errors.
**Known issues / TODO:** None. Next step is the standalone Analytics Notebook.

