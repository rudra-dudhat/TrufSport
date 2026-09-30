-- Phase 3: MySQL Database Design
-- LOP Practical 3

-- Create the database (if not exists)
CREATE DATABASE IF NOT EXISTS turfsport_db;
USE turfsport_db;

-- ==========================================
-- 1. Table Definitions
-- ==========================================

-- Table: sport
-- Stores the different types of sports/facilities available.
CREATE TABLE IF NOT EXISTS sport (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    category VARCHAR(50)
);

-- Table: venue
-- Stores the actual venues where sports are played.
-- Links to sport via a foreign key.
CREATE TABLE IF NOT EXISTS venue (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sport_id INT NOT NULL,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(255) NOT NULL,
    base_price DECIMAL(10, 2) NOT NULL,
    peak_price DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (sport_id) REFERENCES sport(id) ON DELETE CASCADE
);

-- Table: booking
-- Stores customer bookings for specific venues and time slots.
-- In a full Django app this would link to a User table, but for this pure DB design phase we include a customer name.
CREATE TABLE IF NOT EXISTS booking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    venue_id INT NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    booking_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    price_paid DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed', -- confirmed, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (venue_id) REFERENCES venue(id) ON DELETE CASCADE
);

-- ==========================================
-- 2. Seed Data Insertion
-- ==========================================

-- Clear existing data (if running script multiple times)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE booking;
TRUNCATE TABLE venue;
TRUNCATE TABLE sport;
SET FOREIGN_KEY_CHECKS = 1;

-- Insert 12 core sports
INSERT INTO sport (name, icon, category) VALUES
('Box Cricket', '🏏', 'Team Sports'),
('Pickleball', '🏓', 'Racquet Sports'),
('Football Box', '⚽', 'Team Sports'),
('8-Ball Pool', '🎱', 'Indoor Sports'),
('Bowling', '🎳', 'Indoor Sports'),
('Badminton', '🏸', 'Racquet Sports'),
('Go-Karting', '🏎️', 'Racing'),
('Golf', '⛳', 'Outdoor Sports'),
('Tennis', '🎾', 'Racquet Sports'),
('Volleyball', '🏐', 'Team Sports'),
('Basketball', '🏀', 'Team Sports'),
('Cricket Ground', '🏏', 'Outdoor Sports');

-- Insert sample venues for ALL 12 sports
INSERT INTO venue (sport_id, name, location, base_price, peak_price) VALUES
((SELECT id FROM sport WHERE name = 'Box Cricket'), 'Greenfield Box Cricket', 'Sector 14', 800.00, 1200.00),
((SELECT id FROM sport WHERE name = 'Pickleball'), 'Smash Pickleball Court', 'Downtown', 600.00, 800.00),
((SELECT id FROM sport WHERE name = 'Football Box'), 'GoalArena 5v5', 'North City Mall', 1200.00, 1800.00),
((SELECT id FROM sport WHERE name = '8-Ball Pool'), 'Cue Masters Lounge', 'City Center', 300.00, 450.00),
((SELECT id FROM sport WHERE name = 'Bowling'), 'Strike Zone Alley', 'Westend Mall', 400.00, 500.00),
((SELECT id FROM sport WHERE name = 'Badminton'), 'Feather Shuttle Club', 'East End', 500.00, 750.00),
((SELECT id FROM sport WHERE name = 'Go-Karting'), 'Speedway Tracks', 'Highway 51', 900.00, 1100.00),
((SELECT id FROM sport WHERE name = 'Golf'), 'Elite Greens Country Club', 'Hillside', 1500.00, 2000.00),
((SELECT id FROM sport WHERE name = 'Tennis'), 'Grand Slam Tennis Academy', 'Sports Complex', 700.00, 900.00),
((SELECT id FROM sport WHERE name = 'Volleyball'), 'Spikers Beach Court', 'Lake View', 600.00, 800.00),
((SELECT id FROM sport WHERE name = 'Basketball'), 'Hoops Indoor Arena', 'Downtown YMCA', 800.00, 1000.00),
((SELECT id FROM sport WHERE name = 'Cricket Ground'), 'Lords Local Ground', 'Outskirts', 2500.00, 3500.00);

-- Insert sample bookings across multiple venues to ensure analytics have good variety
DELIMITER $$
CREATE PROCEDURE generate_dummy_bookings()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE v_id INT;
    DECLARE rand_days INT;
    DECLARE b_date DATE;
    DECLARE b_status VARCHAR(20);
    DECLARE v_price DECIMAL(10,2);
    
    WHILE i < 1500 DO
        -- Random venue 1 to 12
        SET v_id = FLOOR(1 + (RAND() * 12));
        
        -- Get venue base price
        SELECT base_price INTO v_price FROM venue WHERE id = v_id LIMIT 1;
        
        -- Random days within the last 730 days
        SET rand_days = FLOOR(RAND() * 730);
        SET b_date = DATE_SUB(CURDATE(), INTERVAL rand_days DAY);
        
        -- Random status: 85% confirmed, 15% cancelled
        IF RAND() < 0.85 THEN
            SET b_status = 'Confirmed';
        ELSE
            SET b_status = 'Cancelled';
        END IF;

        INSERT INTO booking (venue_id, customer_name, booking_date, start_time, end_time, price_paid, status)
        VALUES (
            v_id,
            CONCAT('Customer_', i),
            b_date,
            '18:00:00',
            '19:00:00',
            v_price,
            b_status
        );
        
        SET i = i + 1;
    END WHILE;
END$$
DELIMITER ;

CALL generate_dummy_bookings();
DROP PROCEDURE generate_dummy_bookings;
