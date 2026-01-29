from sqlalchemy import create_engine, text
import sqlite3
# Define the database URL
DB_URL = "sqlite:///movies.db"


DB_NAME = "movies.db"



# Create the engine
engine = create_engine(DB_URL)

# Create the movies table if it does not exist
def create_movies_table():
    with engine.connect() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL UNIQUE COLLATE NOCASE,
                year INTEGER NOT NULL,
                rating REAL NOT NULL
            )
        """))
        connection.commit()
#create_movies_table()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {
            "Inception": {"year": 2010, "rating": 8.8, "poster": "https://..."}
           }

def add_movie(title, year, rating, poster):
    """Add a new movie into the database."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO movies VALUES (?, ?, ?, ?)",
                       (title, year, rating, poster))
        conn.commit()
def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            connection.commit()
            if result.rowcount == 0:
                print(f"Movie '{title}' not found.")
            else:
                print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database (case-insensitive handled in Python)."""
    with engine.connect() as connection:
        # Get existing titles
        result = connection.execute(text("SELECT title FROM movies"))
        titles = [row[0] for row in result.fetchall()]

        matched_title = next((t for t in titles if t.lower() == title.lower()), None)

        if not matched_title:
            print(f"Movie '{title}' not found.")
            return

        try:
            result = connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": matched_title, "rating": rating}
            )
            connection.commit()
            print(f"Movie '{matched_title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

