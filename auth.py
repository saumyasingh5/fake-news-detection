
import sqlite3
import hashlib
import hmac
import secrets
import re

DB_NAME = "users.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                email TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL
            )
        """)


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        600000
    ).hex()

    return password_hash, salt


def create_user(username, email, password):
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3:
        return False, "Username must have at least 3 characters."

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return False, "Enter a valid email address."

    if len(password) < 8:
        return False, "Password must have at least 8 characters."

    password_hash, salt = hash_password(password)

    try:
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO users
                   (username, email, password_hash, salt)
                   VALUES (?, ?, ?, ?)""",
                (username, email, password_hash, salt)
            )
        return True, "Account created successfully!"
    except sqlite3.IntegrityError:
        return False, "Username or email already exists."


def authenticate_user(identifier, password):
    identifier = identifier.strip()

    with get_connection() as conn:
        user = conn.execute(
            """SELECT id, username, email, password_hash, salt
               FROM users
               WHERE username = ? COLLATE NOCASE
                  OR email = ? COLLATE NOCASE""",
            (identifier, identifier)
        ).fetchone()

    if not user:
        return None

    stored_hash, salt = user[3], user[4]
    entered_hash, _ = hash_password(password, salt)

    if hmac.compare_digest(stored_hash, entered_hash):
        return {
            "id": user[0],
            "username": user[1],
            "email": user[2]
        }

    return None
