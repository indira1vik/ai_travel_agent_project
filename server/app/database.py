import psycopg2
from psycopg2.extras import Json
import hashlib
import os

DB_NAME = os.getenv("DB_NAME", "atap_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

def init_db():
    conn = get_connection()
    try:
        cur = conn.cursor()

        # users table
        cur.execute("DROP TABLE IF EXISTS users;")
        cur.execute(
            """
            CREATE TABLE users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            );
            """
        )
        
        # demo user added
        demo_hash = hash_password("demo123")
        cur.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s);
            """,
            ("Demouser", "demo_user@example.com", demo_hash),
        )

        # trips table
        cur.execute("DROP TABLE IF EXISTS trips;")
        cur.execute(
            """
            CREATE TABLE trips (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                people_count INTEGER NOT NULL,
                days INTEGER NOT NULL,
                total_budget DOUBLE PRECISION NOT NULL,
                raw_plan JSONB NOT NULL
            );
            """
        )
        
        conn.commit()
        cur.close()
    finally:
        conn.close()

def hash_password(plain: str) -> str:
    return hashlib.sha256(plain.encode("utf-8")).hexdigest()

def verify_password(plain: str, password_hash: str) -> bool:
    return hash_password(plain) == password_hash

def create_user(name: str, email: str, plain_password: str) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        password_hash = hash_password(plain_password)
        cur.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (name, email, password_hash),
        )
        (user_id,) = cur.fetchone()
        conn.commit()
        cur.close()
        return user_id
    finally:
        conn.close()

def get_user_by_email(email: str):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, name, email, password_hash
            FROM users
            WHERE email = %s;
            """,
            (email,),
        )
        row = cur.fetchone()
        cur.close()
    finally:
        conn.close()

    if row is None:
        return None

    user_id, name, email, password_hash = row
    return {
        "id": user_id,
        "name": name,
        "email": email,
        "password_hash": password_hash,
    }

def insert_trip_plan(
    user_id: int,
    source: str,
    destination: str,
    people_count: int,
    days: int,
    total_budget: float,
    raw_plan: dict,
) -> int:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO trips (user_id, source, destination, people_count, days, total_budget, raw_plan)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (user_id, source, destination, people_count, days, total_budget, Json(raw_plan)),
        )
        (trip_id,) = cur.fetchone()
        conn.commit()
        cur.close()
        return trip_id
    finally:
        conn.close()

def get_user_trips(user_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, raw_plan
            FROM trips
            WHERE user_id = %s;
            """,
            (user_id,),
        )
        rows = cur.fetchall()
        cur.close()
    finally:
        conn.close()

    trips = []
    for trip_id, raw_plan in rows:
        trip = dict(raw_plan)
        trip["id"] = trip_id
        trips.append(trip)

    return trips

def get_one_trip_by_id(user_id: int, trip_id: int):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id, raw_plan
            FROM trips
            WHERE id = %s AND user_id = %s;
            """,
            (trip_id, user_id),
        )
        row = cur.fetchone()
        cur.close()
    finally:
        conn.close()

    if row is None:
        return None

    trip_id, raw_plan = row
    trip = dict(raw_plan)
    trip["id"] = trip_id
    return trip

