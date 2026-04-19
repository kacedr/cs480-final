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