"""
Title: movies_update_and_delete.py
Description: Shows films, then inserts, updates, and deletes movies.
"""

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "Laurine88..",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}


def show_films(cursor, title):
    """
    Display film name, director, genre, and studio using joins.
    """
    query = """
        SELECT
            film.film_name   AS Name,
            film.film_director AS Director,
            genre.genre_name AS Genre,
            studio.studio_name AS Studio
        FROM film
        INNER JOIN genre
            ON film.genre_id = genre.genre_id
        INNER JOIN studio
            ON film.studio_id = studio.studio_id
        ORDER BY film.film_name;
    """

    cursor.execute(query)
    films = cursor.fetchall()

    print("-- {} --".format(title))
    for film in films:
        print("Film Name: {}".format(film[0]))
        print("Director: {}".format(film[1]))
        print("Genre: {}".format(film[2]))
        print("Studio: {}\n".format(film[3]))


def main():
    try:
        db = mysql.connector.connect(**config)
        cursor = db.cursor()

        # Initial display
        show_films(cursor, "DISPLAYING FILMS")

        # Insert a new film of your choice
        insert_film = """
            INSERT INTO film
                (film_name, film_releaseDate, film_runtime,
                 film_director, studio_id, genre_id)
            VALUES (%s, %s, %s, %s, %s, %s);
        """

        # Change these values if you want a different movie,
        # but keep studio_id and genre_id as valid ids in your tables.
        new_film_data = (
            "Inception",        # film_name
            "2010",             # film_releaseDate (keep it simple as a year)
            148,                # film_runtime in minutes
            "Christopher Nolan",# film_director
            1,                  # studio_id (must exist in studio table)
            1                   # genre_id (must exist in genre table)
        )

        cursor.execute(insert_film, new_film_data)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

        # Update Alien to be a Horror film
        update_alien = """
            UPDATE film
            SET genre_id = (
                SELECT genre_id
                FROM genre
                WHERE genre_name = 'Horror'
                LIMIT 1
            )
            WHERE film_name = 'Alien';
        """

        cursor.execute(update_alien)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER UPDATE - CHANGED ALIEN TO HORROR")

        # Delete Gladiator
        delete_gladiator = """
            DELETE FROM film
            WHERE film_name = 'Gladiator';
        """

        cursor.execute(delete_gladiator)
        db.commit()

        show_films(cursor, "DISPLAYING FILMS AFTER DELETE - REMOVED GLADIATOR")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Check your username or password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
        else:
            print("MySQL Error:", err)
    finally:
        try:
            cursor.close()
            db.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
