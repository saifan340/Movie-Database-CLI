import random
import movie_storage_sql as storage
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("API_KEY")
OMDB_API_URL = "http://www.omdbapi.com/"


def fetch_movie_from_omdb(title):
    params = {"t": title, "apikey": API_KEY}
    response = requests.get(OMDB_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data["Title"],
                "year": int(data["Year"].split("–")[0]),
                "rating": float(data["imdbRating"]) if data["imdbRating"] != "N/A" else None,
                "poster": data["Poster"] if data["Poster"] != "N/A" else None
            }
    return None
def input_movie_title():
    movie_title = input("Please enter the movie name:").strip().lower()
    if movie_title:
        return movie_title
    else:
        print("Movie title cannot be empty. Please try again.")


def input_movie_rating():
    min_rating = 1
    max_rating = 10
    while True:
        try:
            rating = float(input("Please enter a rating 1 to 10: "))
            if min_rating <= rating <= max_rating:
                return rating
            else:
                print("Rating must be between 1 and 10")
        except ValueError:
            print("Please enter a valid number.")


def input_movie_year():
    movie_year = int(input(f"Please enter the year of the movie: "))
    return movie_year

def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for title, data in movies.items():
        print(f"{title} ({data['year']}) - ⭐ {data['rating']} | Poster: {data['poster']}")


def command_add_movie():
    """Add movie by fetching details from OMDb API."""
    while True:
        title_input = input_movie_title()
        movies = storage.list_movies()
        if title_input.lower() in (t.lower() for t in movies.keys()):
            print(f"The movie '{title_input}' already exists.")
            continue

        movie_data = fetch_movie_from_omdb(title_input)
        if not movie_data:
            print("Movie not found in OMDb. Please try another title.")
            continue

        storage.add_movie(
            movie_data["title"],
            movie_data["year"],
            movie_data["rating"],
            movie_data["poster"]
        )
        print(f"Added {movie_data['title']} ({movie_data['year']}) - Rating: {movie_data['rating']}")
        break


def command_delete_movie():
    movies = storage.list_movies()
    title_input = input_movie_title()
    for title ,details in movies.items():
        if title_input == title.lower():
           storage.delete_movie(title)
           break
    else:
       print(f"Movie {title} doesn't exist!")


def command_update_movie():
    movies = storage.list_movies()
    title_input = input_movie_title()
    for title, details in movies.items():
        if title_input == title.lower():
            rating = input_movie_rating()
            storage.update_movie(title, rating)  # Use original title for DB
            break
    else:
        print(f"Movie '{title_input}' not found.")



def stats():
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    ratings = [details["rating"] for details in movies.values()]
    average = sum(ratings) / len(ratings)
    sorted_ratings = sorted(ratings)
    n = len(sorted_ratings)
    if n % 2 == 0:
        median = (sorted_ratings[n // 2 - 1] + sorted_ratings[n // 2]) / 2
    else:
        median = sorted_ratings[n // 2]
    max_rating = max(ratings)
    min_rating = min(ratings)
    best = [title for title, details in movies.items() if details["rating"] == max_rating]
    worst = [title for title, details in movies.items() if details["rating"] == min_rating]
    print("\n📊 Movie Stats:")
    print(f"• Average rating: {average:.2f}")
    print(f"• Median rating: {median:.2f}")
    print(f"• Best movie(s) ({max_rating}): {', '.join(best)}")
    print(f"• Worst movie(s) ({min_rating}): {', '.join(worst)}")


def random_movie():
    movies = storage.list_movies()
    if movies:
        title = random.choice(list(movies.keys()))
        details = movies[title]
        print(f"Your movie for tonight: {title} ({details['year']}) - Rating: {details['rating']}")
    else:
        print("No movies in the database.")


def search_movie():
    """search for movies in the data base when found print the movies name,year and rating"""
    movies = storage.list_movies()
    title_input = input("Enter a keyword to search for a movie: ").lower()
    found = False
    for title, details in movies.items():
        if title_input in title.lower():
            print(f"{title} ({details['year']}) - Rating: {details['rating']}")
            found = True
    if not found:
        print("No matching movies found.")


def movies_sorted_by_rating():
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    print("\nMovies sorted by rating:")
    for title, details in sorted_movies:
        print(f"{title} ({details['year']}): {details['rating']}")


def menu():
    while True:
        print("")
        print("********** My Movies Database **********")
        print("\nMenu:")
        print("0. Exit")
        print("1. List movies")
        print("2. Add movie")
        print("3. Delete movie")
        print("4. Update movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        choice = input("Enter choice (0-8):")
        print("")
        if choice == "0":
            print("Bye")
            break
        if choice == '1':
            command_list_movies()
        elif choice == '2':
            command_add_movie()
        elif choice == '3':
            command_delete_movie()
        elif choice == '4':
            command_update_movie()
        elif choice == '5':
            stats()
        elif choice == '6':
            random_movie()
        elif choice == '7':
            search_movie()
        elif choice == '8':
            movies_sorted_by_rating()
        else:
            print("\nInvalid choice. Please try again.")


def main():

    menu()


if __name__ == "__main__":
    main()


