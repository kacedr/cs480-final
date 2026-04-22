# Input validators for schema constraints.

def ssn(val):
    v = val.strip()
    if len(v) != 9 or not v.isdigit():
        raise ValueError("SSN MUST BE EXACTLY 9 DIGITS")
    return v


def non_empty(val, label, max_len):
    v = val.strip()
    if not v:
        raise ValueError(f"{label} CANNOT BE EMPTY")
    if len(v) > max_len:
        raise ValueError(f"{label} EXCEEDS {max_len} CHARACTERS")
    return v


def email(val):
    v = val.strip()
    if not v:
        raise ValueError("EMAIL CANNOT BE EMPTY")
    if len(v) > 255:
        raise ValueError("EMAIL EXCEEDS 255 CHARACTERS")
    return v


def card_number(val):
    v = val.strip()
    if not v:
        raise ValueError("CARD NUMBER CANNOT BE EMPTY")
    if len(v) > 19:
        raise ValueError("CARD NUMBER EXCEEDS 19 CHARACTERS")
    return v


def positive_int(val, label):
    v = val.strip()
    try:
        n = int(v)
    except ValueError:
        raise ValueError(f"{label} MUST BE AN INTEGER")
    if n <= 0:
        raise ValueError(f"{label} MUST BE POSITIVE")
    return n


def non_negative_int(val, label):
    v = val.strip()
    try:
        n = int(v)
    except ValueError:
        raise ValueError(f"{label} MUST BE AN INTEGER")
    if n < 0:
        raise ValueError(f"{label} CANNOT BE NEGATIVE")
    return n


def reno_year(val):
    v = val.strip()
    try:
        n = int(v)
    except ValueError:
        raise ValueError("RENO YEAR MUST BE AN INTEGER")
    if n < 1800 or n > 2100:
        raise ValueError("RENO YEAR MUST BE BETWEEN 1800 AND 2100")
    return n


def access_type(val):
    v = val.strip().lower()
    if v not in ("elevator", "stairs"):
        raise ValueError("ACCESS MUST BE 'elevator' OR 'stairs'")
    return v


def booking_date(val):
    from datetime import date as _date
    v = val.strip()
    try:
        return _date.fromisoformat(v)
    except ValueError:
        raise ValueError("DATE MUST BE YYYY-MM-DD")


def price(val):
    v = val.strip()
    try:
        n = float(v)
    except ValueError:
        raise ValueError("PRICE MUST BE A NUMBER")
    if n < 0:
        raise ValueError("PRICE CANNOT BE NEGATIVE")
    return round(n, 2)