from config import PostgresAuth
import psycopg2
import psycopg2.extras

def connect_db():
    db = psycopg2.connect(
        host=PostgresAuth.DB_HOST,
        user=PostgresAuth.DB_USER,
        password=PostgresAuth.DB_PASSWORD,
        database=PostgresAuth.DB_NAME
    )
    return db.cursor(cursor_factory = psycopg2.extras.DictCursor)
    