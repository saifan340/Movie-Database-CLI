import sqlite3

DB_NAME = "movies.db"

def connect():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        year INTEGER,
        rating REAL
    )
    """)
    conn.commit()
    conn.close()

def add_movie(title, year, rating):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO movies (title, year, rating) VALUES (?, ?, ?)", (title, year, rating))
    conn.commit()
    conn.close()

def get_movies():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    conn.close()
    return movies

def delete_movie(movie_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE id=?", (movie_id,))
    conn.commit()
    conn.close()

def delete_movie_by_title(title):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM movies WHERE title=?", (title,))
    conn.commit()
    conn.close()
    if cursor.rowcount > 0:
        print(f"Movie '{title}' deleted successfully.")
    else:
        print(f"Movie '{title}' not found.")

def search_movie_by_title(title):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM movies WHERE title=?", (title,))
    movie = cursor.fetchone()
    conn.close()
    return movie