-- Phase 3: Example MySQL Queries
-- These queries demonstrate basic DB operations required for the Practical

USE turfsport_db;

-- 1. List all venues along with their sport names
-- Shows the use of a JOIN
SELECT 
    v.name AS Venue_Name, 
    s.name AS Sport, 
    v.location AS Location, 
    v.base_price AS Price 
FROM venue v
JOIN sport s ON v.sport_id = s.id
ORDER BY s.name;

-- 2. Find all venues that cost less than ₹1000 per hour
-- Shows a basic WHERE filter
SELECT name, location, base_price 
FROM venue 
WHERE base_price < 1000.00
ORDER BY base_price ASC;

-- 3. Get all confirmed bookings for a specific sport (e.g., 'Box Cricket')
-- Shows multiple JOINs
SELECT 
    b.booking_date, 
    b.start_time, 
    b.customer_name, 
    v.name AS venue_name
FROM booking b
JOIN venue v ON b.venue_id = v.id
JOIN sport s ON v.sport_id = s.id
WHERE s.name = 'Box Cricket' AND b.status = 'confirmed'
ORDER BY b.booking_date, b.start_time;


SELECT 
    v.name AS Venue_Name, 
    COUNT(b.id) AS Total_Bookings, 
    SUM(b.price_paid) AS Total_Revenue
FROM venue v
LEFT JOIN booking b ON v.id = b.venue_id
GROUP BY v.id
ORDER BY Total_Revenue DESC;
