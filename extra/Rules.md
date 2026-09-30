# Rules.md — Boundaries for the AI Coding Agent

These rules apply to every phase. If a rule here conflicts with something in
Phases.md, **this file wins**.

## 1. Allowed technologies only

- HTML5, CSS3, vanilla JavaScript, jQuery (CDN), Bootstrap 5 (CDN)
- Python, Django, MySQL (via `mysqlclient` or `PyMySQL`)
- `sqlite3` (Python standard library) for the standalone practical #10 tool
- Pandas, Matplotlib, Jupyter Notebook

## 2. NOT allowed

- No React, Vue, Angular, Node.js/Express, or any other JS framework.
- No CSS framework other than Bootstrap 5.
- No NoSQL databases (MongoDB etc.) — MySQL only, SQLite only for the
  standalone tool.
- No paid or third-party APIs (payment gateways, SMS, maps APIs with billing).
- No authentication-as-a-service (Firebase Auth, Auth0, etc.) — use Django's
  built-in auth system.
- Do not silently add a library that isn't listed above. If a task seems to
  need one, stop and ask the student first.

## 3. CSS requirement (do not skip)

The project must visibly demonstrate all three CSS types:
- **Inline CSS**: a few elements on the home page and venue-detail page
  (Phase 1–2), used sparingly for one-off styling.
- **Internal CSS**: `<style>` blocks in the `<head>` of the Phase 1–2 static
  pages.
- **External CSS**: all Django template pages from Phase 4 onward use linked
  `.css` files in `static/css/`.

Do not convert the Phase 1–2 inline/internal CSS to external later — leave it
as-is; it's intentional, for the assignment requirement.

## 4. Code style & readability

- Comment every function and every non-obvious block. The student must be
  able to explain each file in a viva — code should read like a tutorial, not
  be clever or condensed.
- Python: follow PEP8, use clear variable names (`available_slots`, not `av`).
- JavaScript: no unexplained one-liners; prefer a few clear lines over a dense
  clever one.
- Keep each file focused — don't put views, forms, and business logic all in
  one giant file "for convenience."

## 5. Error handling — required, not optional

- Every form (login, signup, booking) must validate input on both the client
  (JS) and the server (Django forms/views) — never trust the client alone.
- Never let the app crash on bad input. Show a friendly message
  ("This slot was just booked, please pick another one") instead of a raw
  Python/Django error page.
- Wrap DB operations that can fail (booking creation, especially the
  double-booking check) in proper checks/transactions — two users must never
  be able to book the same slot. This is enforced via database-level `UniqueConstraint` and Flask-SQLAlchemy `db.session.rollback()` on `IntegrityError`.
- If MySQL connection fails, the app should show a clear error, not a blank
  page or stack trace, on the pages the student demos.

## 6. Security basics (keep it simple, but don't skip these)

- Use Django's ORM for all queries — never build raw SQL strings by
  concatenating user input (this is how SQL injection happens).
- Store passwords using Django's built-in hashing (`User.set_password`) —
  never store plain-text passwords.
- Use Django's CSRF protection on all forms (`{% csrf_token %}`) — do not
  disable it.

## 7. Agent working style

- Work **one phase at a time**, in the order given in Phases.md. Do not jump
  ahead to a later phase's code, even if it seems efficient to do it all now.
- At the end of each phase, summarize what was built and how to run/test it,
  in plain language a beginner can follow.
- Before any destructive action (deleting a file, dropping a DB table,
  rewriting a file that already works), stop and confirm with the student.
- After finishing a phase, update `Memory.md` with: what's done, what's next,
  and any decisions made or issues hit. Do this every single phase — it's how
  the student avoids re-explaining the whole project in a new chat.
- If a request from the student contradicts PRD.md/Architecture.md, point out
  the conflict instead of silently going along with it.
- Prefer the simplest working solution over the "impressive" one. This is a
  semester-length college project, not a production SaaS — simple, correct,
  and explainable beats clever every time.

## 8. Definition of "done" for any single phase

A phase is not complete until:
1. The code runs without errors.
2. The student can open it and see/interact with what was promised.
3. Memory.md has been updated.
4. The agent has explained, in a few plain sentences, what was added and why.
