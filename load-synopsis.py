from bs4 import BeautifulSoup
import requests
import csv

BASE_URL = "https://www.imdb.com/title/tt"


def create_synopsis(movie_imdb_ids, new_file):
    """
    Creates a csv file with movie id and synopsis column.
    Synopsis is taken from IMDB

    ARGS:
        movie_imdb_ids (dict): map of movie ids to imdb ids

    """

    with open(new_file, "w") as csv_file:

        writer = csv.DictWriter(csv_file, fieldnames=["movieId", "synopsis"])
        writer.writeheader()

        for key in movie_imdb_ids.keys():
            print("Writing synopsis for movie id: {}".format(key))
            writer.writerow({'movieId': key, 'synopsis': get_synopsys(movie_imdb_ids[key])})


def movie_to_imdb(path):
    """
    Returns a dictionary of movie id to IMDB id extracted from the links.csv file provided by
    the MovieLens small dataset

    ARGS:
        path (str): path to the links.csv file provided by the MovieLens small dataset

    RERTURNS:
        dict: a dictionary containing movie id to IMDB id
    """

    movie_imdb_ids = dict()

    with open(path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")

        first_row = True
        for row in csv_reader:
            if first_row:
                first_row = False
            else:
                movie_imdb_ids[row[0]] = row[1]

    return movie_imdb_ids


def get_synopsys(imdb_id):
    """
    Returns synopsis for a movie with the provided IDMB id

    ARGS:
        imdb_id (str): IMDB id of the movie to return the synopsys for

    RETURNS:
        str: synopsis of of the movie with the provided IMDB id
    """

    url = BASE_URL + imdb_id
    synopsis = ""

    try:
        content = requests.get(url).content
    except Exception as err:
        print("Failed to retrieve page contents for {}".format(url))
        print("The error was: {}".format(str(err)))
        return synopsis

    try:
        soup = BeautifulSoup(content, features="html.parser")
        synopsis = soup.findAll("div", {"class": "summary_text"})[0].next.strip()
    except Exception as err:
        print("Failed to extract synopsis for the movie with IMDB id {}".format(imdb_id))
        print("The error was: {}".format(str(err)))

    return synopsis


def main():
    movie_imdb_ids = movie_to_imdb("links.csv")
    create_synopsis(movie_imdb_ids, "synopsis.csv")


if __name__ == "__main__":
    main()
