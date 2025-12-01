"""
Title: movies_queries.py
Description: Queries the movies database and displays results.
"""

import mysql.connector
from mysql.connector import errorcode

# Your database config
config = {
    "user": "root",
    "password": "Laurine88..",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}


def show_studios(cursor):
    cursor.execute("SELECT studio_id, studio_name FROM studio")
    studios = cursor.fetchall()

    print("-- DISPLAYING Studio RECORDS --")
    for studio in studios:
        print("Studio ID: {}".format(studio[0]))
        print("Studio Name: {}\n".format(studio[1]))


def show_genres(cursor):
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()

    print("-- DISPLAYING Genre RECORDS --")
    for genre in genres:
        print("Genre ID: {}".format(genre[0]))
        print("Genre Name: {}\n".format(genre[1]))


def show_short_films(cursor):
    cursor.execute("""
        SELECT film_name, film_runtime
        FROM film
        WHERE film_runtime < 120
        ORDER BY film_runtime
    """)
    films = cursor.fetchall()

    print("-- DISPLAYING Short Film RECORDS (runtime < 120) --")
    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Runtime (minutes): {}\n".format(film[1]))


def show_films_grouped_by_director(cursor):
    cursor.execute("""
        SELECT film_director, film_name
        FROM film
        ORDER BY film_director, film_name
    """)
    films = cursor.fetchall()

    print("-- DISPLAYING Film RECORDS Grouped by Director --")
    for film in films:
        print("Director: {}".format(film[0]))
        print("Film Name: {}\n".format(film[1]))


def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        show_studios(cursor)
        show_genres(cursor)
        show_short_films(cursor)
        show_films_grouped_by_director(cursor)

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

    finally:
        try:
            cursor.close()
            db.close()
        except:
            pass


if __name__ == "__main__":
    main()
