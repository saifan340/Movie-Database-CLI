import movie_storage_sql as storage
from movies import input_movie_rating, input_movie_title, input_movie_year


def menu():
    print("\n--- Movie Database ---")
    print("1. Show movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Search film")
    print("5. Rating average")
    print("6. Exit")

def show_movies():
    movies = storage.get_movies()
    for m in movies:
        print(f"[ID: {m[0]}] {m[1]} ({m[2]}) | Rating: {m[3]}")

def add_movie():
    title = input_movie_title()
    year = input_movie_year()
    rating = input_movie_rating()
    storage.add_movie(title, year, rating)

def delete_movie():
    show_movies()
    title = input_movie_title()
    storage.delete_movie_by_title(title)

def search_film():
    title = input_movie_title()
    movie = storage.search_movie_by_title(title)
    if movie:
        print(f"[ID: {movie[0]}] {movie[1]} ({movie[2]}) | Rating: {movie[3]}")
    else:
        print(f"Movie '{title}' not found.")

def rating_average():
    movies = storage.get_movies()
    if not movies:
        print("No movies in database.")
        return
    avg_rating = sum(m[3] for m in movies) / len(movies)
    print(f"Average rating: {avg_rating:.2f}")

def main():
    storage.create_table()

    while True:
        menu()
        choice = input("Choose: ")

        if choice == "1":
            show_movies()
        elif choice == "2":
            add_movie()
        elif choice == "3":
            delete_movie()
        elif choice == "4":
            search_film()
        elif choice == "5":
            rating_average()
        elif choice == "6":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()