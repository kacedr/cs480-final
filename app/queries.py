# All database queries for the application.
# Keep SQL in this file. Do not put queries in main.py.
from app.db import get_connection

def ping():
    # Just a test Returns the postgres version string
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT version();")
        return cur.fetchone()[0]
        
# Manager auth
def manager_login(ssn):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT ssn, name, email FROM manager WHERE ssn = %s;",
            (ssn,),
        )
        return cur.fetchone()

def register_manager(ssn, name, email):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO manager (ssn, name, email) VALUES (%s, %s, %s) "
            "RETURNING ssn, name, email;",
            (ssn, name, email),
        )
        row = cur.fetchone()
        conn.commit()
        return row
    
# Client auth
def client_login(email):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT client_id, name, email FROM client WHERE email = %s;",
            (email,),
        )
        return cur.fetchone()


def register_client(name, email, addresses, cards):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Insert client
            cur.execute(
                "INSERT INTO client (name, email) VALUES (%s, %s) "
                "RETURNING client_id, name, email;",
                (name, email),
            )
            client_row = cur.fetchone()
            client_id = client_row[0]

            # Insert each address and link to client
            for street_name, street_number, city in addresses:
                cur.execute(
                    "INSERT INTO address (street_name, street_number, city) "
                    "VALUES (%s, %s, %s) RETURNING address_id;",
                    (street_name, street_number, city),
                )
                address_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO client_address (client_id, address_id) "
                    "VALUES (%s, %s);",
                    (client_id, address_id),
                )

            # Insert each credit card with its billing address
            for card_number, b_street, b_number, b_city in cards:
                cur.execute(
                    "INSERT INTO address (street_name, street_number, city) "
                    "VALUES (%s, %s, %s) RETURNING address_id;",
                    (b_street, b_number, b_city),
                )
                billing_id = cur.fetchone()[0]
                cur.execute(
                    "INSERT INTO credit_card (card_number, client_id, billing_address_id) "
                    "VALUES (%s, %s, %s);",
                    (card_number, client_id, billing_id),
                )

            conn.commit()
            return client_row
    except Exception:
        conn.rollback()
        raise

# Manager hotels
def insert_hotel(name, street_name, street_number, city):
    """Insert an address, then a hotel pointing to it. Returns hotel_id."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO address (street_name, street_number, city) "
                "VALUES (%s, %s, %s) RETURNING address_id;",
                (street_name, street_number, city),
            )
            address_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO hotel (name, address_id) VALUES (%s, %s) "
                "RETURNING hotel_id;",
                (name, address_id),
            )
            hotel_id = cur.fetchone()[0]
            conn.commit()
            return hotel_id
    except Exception:
        conn.rollback()
        raise


def update_hotel(hotel_id, name, street_name, street_number, city):
    """Update hotel name and its address fields."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT address_id FROM hotel WHERE hotel_id = %s;",
                (hotel_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"hotel {hotel_id} not found")
            address_id = row[0]

            cur.execute(
                "UPDATE hotel SET name = %s WHERE hotel_id = %s;",
                (name, hotel_id),
            )
            cur.execute(
                "UPDATE address SET street_name = %s, street_number = %s, city = %s "
                "WHERE address_id = %s;",
                (street_name, street_number, city, address_id),
            )
            conn.commit()
    except Exception:
        conn.rollback()
        raise


def remove_hotel(hotel_id):
    """Delete a hotel. Rooms cascade, address is orphaned (kept)."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM hotel WHERE hotel_id = %s;",
                (hotel_id,),
            )
            if cur.rowcount == 0:
                raise ValueError(f"hotel {hotel_id} not found")
            conn.commit()
    except Exception:
        conn.rollback()
        raise


# Manager rooms
def insert_room(hotel_id, room_number, num_windows, last_reno_year, access_type):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO room (hotel_id, room_number, num_windows, "
                "last_reno_year, access_type) VALUES (%s, %s, %s, %s, %s);",
                (hotel_id, room_number, num_windows, last_reno_year, access_type),
            )
            conn.commit()
    except Exception:
        conn.rollback()
        raise


def update_room(hotel_id, room_number, num_windows, last_reno_year, access_type):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE room SET num_windows = %s, last_reno_year = %s, "
                "access_type = %s WHERE hotel_id = %s AND room_number = %s;",
                (num_windows, last_reno_year, access_type, hotel_id, room_number),
            )
            if cur.rowcount == 0:
                raise ValueError(f"room {room_number} in hotel {hotel_id} not found")
            conn.commit()
    except Exception:
        conn.rollback()
        raise


def remove_room(hotel_id, room_number):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM room WHERE hotel_id = %s AND room_number = %s;",
                (hotel_id, room_number),
            )
            if cur.rowcount == 0:
                raise ValueError(f"room {room_number} in hotel {hotel_id} not found")
            conn.commit()
    except Exception:
        conn.rollback()
        raise


# Manager clients
def remove_client(client_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM client WHERE client_id = %s;",
                (client_id,),
            )
            if cur.rowcount == 0:
                raise ValueError(f"client {client_id} not found")
            conn.commit()
    except Exception:
        conn.rollback()
        raise


# Manager reports
def top_k_clients_by_bookings(k):
    """Returns list of (name, email, booking_count) ordered by bookings desc."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT c.name, c.email, COUNT(b.booking_id) AS num_bookings "
            "FROM client c JOIN booking b ON c.client_id = b.client_id "
            "GROUP BY c.client_id, c.name, c.email "
            "ORDER BY num_bookings DESC "
            "LIMIT %s;",
            (k,),
        )
        return cur.fetchall()
    
def room_booking_counts():
    """Returns list of (hotel_name, room_number, num_bookings) for every room."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT h.name, r.room_number, "
            "(SELECT COUNT(*) FROM booking b "
            " WHERE b.hotel_id = r.hotel_id AND b.room_number = r.room_number) AS num_bookings "
            "FROM room r "
            "JOIN hotel h ON r.hotel_id = h.hotel_id "
            "ORDER BY r.hotel_id, r.room_number;"
        )
        return cur.fetchall()


def hotel_statistics():
    """Returns list of (hotel_name, total_bookings, avg_rating) for every hotel."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT h.name, "
            "(SELECT COUNT(*) FROM booking b WHERE b.hotel_id = h.hotel_id) AS total_bookings, "
            "(SELECT ROUND(AVG(rv.rating), 2) FROM review rv WHERE rv.hotel_id = h.hotel_id) AS avg_rating "
            "FROM hotel h "
            "ORDER BY h.hotel_id;"
        )
        return cur.fetchall()


def clients_by_city_pair(c1, c2):
    """Returns list of (name, email) for clients with an address in c1 who booked a hotel in c2."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT DISTINCT c.name, c.email "
            "FROM client c "
            "JOIN client_address ca ON c.client_id = ca.client_id "
            "JOIN address a ON ca.address_id = a.address_id "
            "JOIN booking b ON c.client_id = b.client_id "
            "JOIN hotel h ON b.hotel_id = h.hotel_id "
            "JOIN address ha ON h.address_id = ha.address_id "
            "WHERE a.city = %s AND ha.city = %s;",
            (c1, c2),
        )
        return cur.fetchall()


def problematic_hotels():
    """Returns hotel names in Chicago with avg rating < 2, booked by >= 2 clients with no Chicago address."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT h.name "
            "FROM hotel h "
            "JOIN address ha ON h.address_id = ha.address_id "
            "WHERE ha.city = 'Chicago' "
            "AND (SELECT AVG(rv.rating) FROM review rv WHERE rv.hotel_id = h.hotel_id) < 2 "
            "AND (SELECT COUNT(DISTINCT b.client_id) "
            "     FROM booking b "
            "     WHERE b.hotel_id = h.hotel_id "
            "     AND b.client_id NOT IN ( "
            "         SELECT ca.client_id "
            "         FROM client_address ca "
            "         JOIN address a ON ca.address_id = a.address_id "
            "         WHERE a.city = 'Chicago' "
            "     )) >= 2;"
        )
        return cur.fetchall()


def client_spending_report():
    """Returns list of (client_name, total_spent) ordered by total spent descending."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT c.name, SUM(b.price_per_day * (b.end_date - b.start_date + 1)) AS total_spent "
            "FROM client c "
            "JOIN booking b ON c.client_id = b.client_id "
            "GROUP BY c.client_id, c.name "
            "ORDER BY total_spent DESC;"
        )
        return cur.fetchall()
    
# Manager list / lookup helpers
def list_hotels():
    """Returns list of (hotel_id, name, street_number, street_name, city)."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT h.hotel_id, h.name, a.street_number, a.street_name, a.city "
            "FROM hotel h JOIN address a ON h.address_id = a.address_id "
            "ORDER BY h.hotel_id;"
        )
        return cur.fetchall()


def list_rooms(hotel_id=None):
    """
    Returns list of (hotel_id, hotel_name, room_number, num_windows,
    last_reno_year, access_type). Optionally filtered by hotel.
    """
    conn = get_connection()
    with conn.cursor() as cur:
        if hotel_id is None:
            cur.execute(
                "SELECT r.hotel_id, h.name, r.room_number, r.num_windows, "
                "r.last_reno_year, r.access_type "
                "FROM room r JOIN hotel h ON r.hotel_id = h.hotel_id "
                "ORDER BY r.hotel_id, r.room_number;"
            )
        else:
            cur.execute(
                "SELECT r.hotel_id, h.name, r.room_number, r.num_windows, "
                "r.last_reno_year, r.access_type "
                "FROM room r JOIN hotel h ON r.hotel_id = h.hotel_id "
                "WHERE r.hotel_id = %s "
                "ORDER BY r.room_number;",
                (hotel_id,),
            )
        return cur.fetchall()


def list_clients():
    """Returns one row per (client, address) pair: 
    (client_id, name, email, street_number, street_name, city)."""
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT c.client_id, c.name, c.email, "
            "a.street_number, a.street_name, a.city "
            "FROM client c "
            "JOIN client_address ca ON c.client_id = ca.client_id "
            "JOIN address a ON ca.address_id = a.address_id "
            "ORDER BY c.client_id, a.address_id;"
        )
        return cur.fetchall()