-- Not needed but makes testing easier
DROP TABLE IF EXISTS review         CASCADE;
DROP TABLE IF EXISTS booking        CASCADE;
DROP TABLE IF EXISTS room           CASCADE;
DROP TABLE IF EXISTS client_address CASCADE;
DROP TABLE IF EXISTS credit_card    CASCADE;
DROP TABLE IF EXISTS hotel          CASCADE;
DROP TABLE IF EXISTS address        CASCADE;
DROP TABLE IF EXISTS client         CASCADE;
DROP TABLE IF EXISTS manager        CASCADE;

-- Required for the booking overlap exclusion constraint
-- Not sure if prof went over this in lecture but this prevents us needing
-- to handle this in the application layer. Can be removed and delt with in application tho if required.
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Strong entities ------------------------------------------------------------------

-- Stores manager personal information. No relationships to other entities
-- ssn is stored WITHOUT dashes thus 9 long
CREATE TABLE manager (
    ssn   CHAR(9)      PRIMARY KEY,
    name  VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE
);

-- Stores client personal information
-- Note: clients must have >=1 address and >=1 credit card, we will handle this in the application layer
CREATE TABLE client (
    client_id SERIAL       PRIMARY KEY,
    name      VARCHAR(100) NOT NULL,
    email     VARCHAR(255) NOT NULL UNIQUE
);

-- Stores physical address details independently of any entity
CREATE TABLE address (
    address_id    SERIAL       PRIMARY KEY,
    street_name   VARCHAR(150) NOT NULL,
    street_number VARCHAR(20)  NOT NULL,
    city          VARCHAR(100) NOT NULL
);

-- Stores hotel information, every hotel has exactly one address
CREATE TABLE hotel (
    hotel_id   SERIAL       PRIMARY KEY,
    name       VARCHAR(150) NOT NULL,
    address_id INTEGER      NOT NULL UNIQUE
        REFERENCES address(address_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Stores client credit cards, each card has exactly one billing address
CREATE TABLE credit_card (
    card_number        VARCHAR(19) PRIMARY KEY,
    client_id          INTEGER     NOT NULL
        REFERENCES client(client_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    billing_address_id INTEGER     NOT NULL
        REFERENCES address(address_id)
        ON UPDATE CASCADE ON DELETE RESTRICT
);

-- Junction table for many to many relationship between client and address
CREATE TABLE client_address (
    client_id  INTEGER NOT NULL
        REFERENCES client(client_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    address_id INTEGER NOT NULL
        REFERENCES address(address_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    PRIMARY KEY (client_id, address_id)
);

-- Weak entities ----------------------------------------------------------------

-- Weak entity representing a room within a hotel, primary key includes hotel_id
CREATE TABLE room (
    hotel_id       INTEGER NOT NULL
        REFERENCES hotel(hotel_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    room_number    INTEGER NOT NULL,
    num_windows    INTEGER CHECK (num_windows >= 0),
    last_reno_year INTEGER CHECK (last_reno_year BETWEEN 1800 AND 2100),
    access_type    VARCHAR(10) NOT NULL CHECK (access_type IN ('elevator', 'stairs')),
    PRIMARY KEY (hotel_id, room_number)
);

-- Weak entity representing a review of a hotel by a client, primary key includes hotel_id
-- Note: a client can only review a hotel they have previously booked, handled in the application layer
CREATE TABLE review (
    hotel_id  INTEGER NOT NULL
        REFERENCES hotel(hotel_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    review_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL
        REFERENCES client(client_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    message   TEXT,
    rating    INTEGER CHECK (rating BETWEEN 0 AND 10),
    PRIMARY KEY (hotel_id, review_id)
);

-- Depends on room ----------------------------------------------------------------

-- Stores room reservations made by clients, no two bookings for the same room may overlap
CREATE TABLE booking (
    booking_id    SERIAL        PRIMARY KEY,
    client_id     INTEGER       NOT NULL
        REFERENCES client(client_id)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    hotel_id      INTEGER       NOT NULL,
    room_number   INTEGER       NOT NULL,
    start_date    DATE          NOT NULL,
    end_date      DATE          NOT NULL,
    price_per_day NUMERIC(10,2) NOT NULL CHECK (price_per_day >= 0),
    FOREIGN KEY (hotel_id, room_number)
        REFERENCES room(hotel_id, room_number)
        ON UPDATE CASCADE ON DELETE RESTRICT,

    -- Logic that handles overlapping, postgres will return an error if we try to 
    -- insert overlapping dates thus we need to handle all queries with try/catch
    -- which we should be doing anyway. just a reminder.
    CHECK (end_date > start_date),
    EXCLUDE USING gist (
        hotel_id    WITH =,
        room_number WITH =,
        daterange(start_date, end_date, '[]') WITH && -- spec says [x,y]
    )
);