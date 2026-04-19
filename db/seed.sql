-- Managers 
INSERT INTO manager (ssn, name, email) VALUES
    ('111223333', 'Alice Manager',  'alice.mgr@example.com'),
    ('222334444', 'Bob Supervisor', 'bob.sup@example.com'),
    ('333445555', 'Carla Director', 'carla.dir@example.com');

-- Addresses
-- IDs 1-6: client primary addresses
-- IDs 7-12: credit card billing addresses (some shared, some different)
-- IDs 13-18: hotel addresses
INSERT INTO address (street_name, street_number, city) VALUES
    ('Michigan Ave',    '100',  'Chicago'),      -- 1 client 1 home
    ('State St',        '250',  'Chicago'),      -- 2 client 2 home
    ('Broadway',        '1500', 'New York'),     -- 3 client 3 home
    ('Market St',       '800',  'San Francisco'),-- 4 client 4 home
    ('Colfax Ave',      '3200', 'Denver'),       -- 5 client 5 home
    ('Peachtree St',    '450',  'Atlanta'),      -- 6 client 6 home

    ('Clark St',        '77',   'Chicago'),      -- 7  billing
    ('Wacker Dr',       '200',  'Chicago'),      -- 8  billing
    ('5th Ave',         '900',  'New York'),     -- 9  billing
    ('Mission St',      '410',  'San Francisco'),-- 10 billing
    ('17th St',         '1100', 'Denver'),       -- 11 billing
    ('Ponce De Leon',   '600',  'Atlanta'),      -- 12 billing

    ('Wabash Ave',      '1',    'Chicago'),      -- 13 hotel 1
    ('Dearborn St',     '55',   'Chicago'),      -- 14 hotel 2
    ('Madison Ave',     '700',  'New York'),     -- 15 hotel 3
    ('Powell St',       '45',   'San Francisco'),-- 16 hotel 4
    ('16th St',         '1000', 'Denver'),       -- 17 hotel 5
    ('West Peachtree',  '250',  'Atlanta');      -- 18 hotel 6

-- Clients
INSERT INTO client (name, email) VALUES
    ('Dan Grosch',     'dan@example.com'),       -- 1 Chicago
    ('James Nguyen',   'james@example.com'),     -- 2 Chicago
    ('Mandar Patel',   'mandar@example.com'),    -- 3 New York
    ('Kyle Gleason',   'kyle@example.com'),      -- 4 San Francisco
    ('Emma Wilson',    'emma@example.com'),      -- 5 Denver
    ('Frank Lopez',    'frank@example.com');     -- 6 Atlanta

-- Client (some clients have multiple addresses)
INSERT INTO client_address (client_id, address_id) VALUES
    (1, 1),   -- Dan: Chicago home
    (1, 5),   -- Dan also has a Denver address
    (2, 2),   -- James: Chicago home
    (3, 3),   -- Mandar: New York home
    (3, 4),   -- Mandar also has a San Francisco address
    (4, 4),   -- Kyle: San Francisco home
    (5, 5),   -- Emma: Denver home
    (6, 6);   -- Frank: Atlanta home

-- Credit cards (some billing addresses differ from home address)
INSERT INTO credit_card (card_number, client_id, billing_address_id) VALUES
    ('4111111111111001', 1, 7),    -- Dan: billed to a Chicago address
    ('4111111111111002', 1, 11),   -- Dan: a second card billed to Denver
    ('4111111111111003', 2, 8),    -- James: billed to Chicago
    ('4111111111111004', 3, 9),    -- Mandar: billed to New York
    ('4111111111111005', 4, 10),   -- Kyle: billed to San Francisco
    ('4111111111111006', 5, 11),   -- Emma: billed to Denver
    ('4111111111111007', 6, 12);   -- Frank: billed to Atlanta

-- Hotels
INSERT INTO hotel (name, address_id) VALUES
    ('Chicago Grand',      13),    -- 1
    ('Windy City Inn',     14),    -- 2 (Chicago, will become "problematic")
    ('Manhattan Plaza',    15),    -- 3
    ('Bay Area Suites',    16),    -- 4
    ('Mile High Lodge',    17),    -- 5
    ('Peachtree Hotel',    18);    -- 6

-- Rooms
INSERT INTO room (hotel_id, room_number, num_windows, last_reno_year, access_type) VALUES
    -- Chicago Grand (1)
    (1, 101, 2, 2020, 'elevator'),
    (1, 102, 2, 2020, 'elevator'),
    (1, 201, 3, 2022, 'stairs'),

    -- Windy City Inn (2) - the problematic one, low ratings
    (2, 101, 1, 1995, 'stairs'),
    (2, 102, 1, 1995, 'stairs'),

    -- Manhattan Plaza (3)
    (3, 501, 4, 2023, 'elevator'),
    (3, 502, 4, 2023, 'elevator'),
    (3, 601, 5, 2024, 'elevator'),

    -- Bay Area Suites (4)
    (4, 10, 2, 2019, 'elevator'),
    (4, 11, 2, 2019, 'elevator'),

    -- Mile High Lodge (5)
    (5, 1, 3, 2021, 'stairs'),
    (5, 2, 3, 2021, 'stairs'),

    -- Peachtree Hotel (6)
    (6, 301, 2, 2018, 'elevator');

-- Bookings
-- Spread across 2025-2026 with varied counts per client so top-k has a clear order.
-- Dan (1): 4 bookings — top booker
-- Mandar (3): 3 bookings
-- Emma (5): 2 bookings, both at Windy City Inn (non-Chicago resident)
-- Kyle (4): 2 bookings, one at Windy City Inn (non-Chicago resident)
-- James (2): 1 booking
-- Frank (6): 1 booking

INSERT INTO booking (client_id, hotel_id, room_number, start_date, end_date, price_per_day) VALUES
    -- Dan's 4 bookings
    (1, 1, 101, '2025-06-01', '2025-06-05', 150.00),
    (1, 3, 501, '2025-08-10', '2025-08-15', 280.00),
    (1, 4, 10,  '2025-10-01', '2025-10-04', 220.00),
    (1, 5, 1,   '2026-01-05', '2026-01-10', 180.00),

    -- Mandar's 3 bookings (NY resident booking in Chicago at hotel 2 satisfies city-pair query)
    (3, 2, 101, '2025-07-10', '2025-07-14', 95.00),
    (3, 1, 102, '2025-09-01', '2025-09-05', 150.00),
    (3, 6, 301, '2025-12-20', '2025-12-27', 170.00),

    -- Emma's 2 bookings (Denver resident, both at Windy City Inn = problematic)
    (5, 2, 102, '2025-07-15', '2025-07-19', 95.00),
    (5, 4, 11,  '2025-11-01', '2025-11-05', 220.00),

    -- Kyle's 2 bookings (SF resident, one at Windy City Inn)
    (4, 2, 101, '2025-08-01', '2025-08-04', 95.00),
    (4, 3, 502, '2025-12-10', '2025-12-15', 280.00),

    -- James's 1 booking
    (2, 1, 201, '2025-07-01', '2025-07-03', 200.00),

    -- Frank's 1 booking
    (6, 5, 2,   '2026-02-14', '2026-02-18', 180.00);

-- Reviews
-- Windy City Inn gets bad reviews from non-Chicago residents (Emma + Kyle)
-- Other hotels get decent reviews.

INSERT INTO review (hotel_id, review_id, client_id, message, rating) VALUES
    -- Windy City Inn: avg rating 1.5 (< 2), reviewed by Emma (Denver) and Kyle (SF)
    (2, 1, 5, 'Dated rooms and poor service.',    1),
    (2, 2, 4, 'Would not stay again.',             2),

    -- Chicago Grand: solid reviews
    (1, 1, 1, 'Great location, very clean.',       9),
    (1, 2, 2, 'Nice rooms, helpful staff.',        8),

    -- Manhattan Plaza
    (3, 1, 1, 'Luxury experience, worth it.',      10),
    (3, 2, 4, 'Beautiful views.',                  9),

    -- Bay Area Suites
    (4, 1, 1, 'Comfortable and convenient.',       8),
    (4, 2, 5, 'Good for the price.',               7),

    -- Mile High Lodge
    (5, 1, 1, 'Cozy and warm.',                    8),

    -- Peachtree Hotel
    (6, 1, 3, 'Pleasant stay.',                    7);
