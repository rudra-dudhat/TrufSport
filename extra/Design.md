# Design.md — Visual Design System

## 1. Overall Feel

Energetic, clean, sporty — not corporate. Should feel like a modern booking
app (think: a clean utility site), not a gaming site. Prioritize readability
of the slot grid above everything else — that screen is the heart of the app.

## 2. Color Palette

| Role | Color | Hex |
|---|---|---|
| Primary (brand) | Navy | `#293681` |
| Primary accent | Royal Blue | `#4274d9` |
| Secondary (energy accent) | Sky Blue | `#95ccdd` |
| Background | Light Mint | `#d0e7e6` |
| Surface / cards | White | `#FFFFFF` |
| Text — primary | Charcoal | `#1F2933` |
| Text — muted | Slate Grey | `#6B7280` |
| **Slot: Free** | Royal Blue | `#4274d9` |
| **Slot: Booked/Past** | Grey | `#E5E7EB` |
| Success | Green | `#16A34A` |
| Error | Red | `#DC2626` |

Keep the slot-status colors consistent everywhere in the
app — never reuse these specific accent shades for anything else in the UI, or the grid becomes
confusing.

## 3. Typography

- Headings: **Poppins** (Google Fonts) — 600/700 weight
- Body text: **Inter** (Google Fonts) — 400/500 weight
- Base font size: 16px, scale up with `rem` units
- Headings scale: H1 32px, H2 24px, H3 20px, body 16px, small/labels 14px

## 4. Layout & Spacing

- Base spacing unit: 8px (use multiples: 8, 16, 24, 32...)
- Max content width: 1200px, centered
- Card border radius: 12px
- Buttons: border radius 8px, generous padding (12px 24px)
- Use Bootstrap's grid system from Phase 5 onward instead of hand-rolled
  flex/grid — stay consistent once Bootstrap is introduced.

## 5. Key Components

**Sport/Venue Card**
- White surface, subtle shadow, image on top, sport name + starting price
  below, rounded corners.

**Slot Grid**
- Grid of chips/cells, one per time slot.
- Free = royal blue border/text, white background, clickable. (Filled royal blue on hover)
- Booked = grey background, muted text, struck through, disabled/not clickable, small "Booked" badge.
- Selected (by the user, before confirming) = filled navy background and text.
- Always show a message to select a date if slots aren't loaded.

**Navbar**
- Logo/site name on left, sport categories or "Browse Sports" in the middle,
  Login/My Bookings on the right. Sticky on scroll once Bootstrap is in.

**Buttons**
- Primary action (Book Now, Confirm): filled royal blue (`#4274d9`), white text. Hover state switches to sky blue (`#95ccdd`) and navy text, floating up slightly.
- Secondary/cancel: outline style, grey border.
- Destructive (Cancel Booking): outline style, red text/border, changes to filled red on hover.

**Forms**
- Label above input, not placeholder-only (placeholders disappear and confuse
  users on longer forms like booking/signup).
- Inline error message directly under the field, in red, appears on invalid
  input.

## 6. Icons

Use Bootstrap Icons (comes free with Bootstrap 5, CDN) once Bootstrap is
introduced — do not add a separate icon library. Before that, in Phase 1–2,
plain emoji or simple inline SVGs are fine for sport icons.

## 7. Responsive Behavior

- Mobile-first once Bootstrap lands: sport cards stack to 1 column under
  576px, 2 columns under 768px, 3–4 columns above.
- Slot grid: shrink to a scrollable horizontal row on very small screens
  rather than squeezing cells unreadably small.

## 8. Homepage Layout (rough description for the agent)

1. Navbar (logo + nav links)
2. Hero section: short tagline ("Book your game, instantly.") + a search bar
   for sport/venue
3. Grid of sport cards (all 12 sports, each clickable → venue list for that
   sport)
4. Simple footer (site name, "College Project" note, links to nothing
   external is fine)

## 9. Booking Page Layout

1. Venue name + photo + basic info at top
2. Date picker
3. Legend (Free/Booked/Past)
4. Slot grid — the main focus of the page, largest visual element
5. Selected slot(s) + computed price shown clearly before confirming
6. "Confirm Booking" button (disabled until at least one free slot is picked)
