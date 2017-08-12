from pprint import pprint

import requests
import os
import csv
import json
import re
from imdbpie import Imdb

"""
export-Movies-rating.py
Mohamed Hamza
Exports IMDB's information for your movies to CSV file.
"""

# def list_movies():
#     '''
#     identifies movies in the current directory
#     movies' names should be in a specific form which is 'name of the movie (year)'
#     for the script to work.
#     you can use "filebot" to do that.
#     https://www.filebot.net/forums/viewtopic.php?f=4&t=215

#     or you can make your own Regex
#     '''

#     u=[]

#     Regex = re.compile(r'(.+) \(\d+\)')
#     print()
#     for x in os.listdir(os.path.dirname(os.path.abspath(__file__))):
#         if Regex.search(x):
#             z = Regex.search(x).group(1)
#             print('this is z  ', z)
#             u.append(z)
#     # print(u)
#     return u


def name_grabber(medialst):
    """Gets the Movie Name and Year from the filename and other meta
    data is removed.
    For Example:
    - Doctor.Strange.2016.720p.BrRip.mkv [INPUT]
    - Doctor Strange 2016 [RETURN]
    This function is made mostly from: https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber
    """

    nameslist = {}
    for movies in medialst:
        yearRegex = re.compile(r'\d{4}')
        if yearRegex.search(movies):

            def get_year(filename):
                    searchitems = yearRegex.search(filename)
                    return searchitems.group()

            year = get_year(movies)
            # This is 2016 Movie --> This is | 2016 | Movie
            prev, found, removal = movies.partition(year)
            
            if prev[-1] == ' ':
                nameslist[found] = prev.lower()
            else:
                nameslist[found] = prev.lower()[:-1]

    nameslist = {key: val.strip(' ') for key, val in nameslist.items()}
    print('found these movies', nameslist)
    return nameslist

def identify_movies (movies):
    """ identifying the movies from IMDB """
    imdb = Imdb()

    ids = []
    for key, val in movies.items():
        for info in imdb.search_for_title(val):
            if key == info.get('year') and val == info.get('title').lower():
                ids.append(info.get('imdb_id'))
            # if val == info.get('title'):
            #     print(val)
    return [imdb.get_title_by_id(id) for id in ids]
"""
info.title
info.year
info.rating
info.certification
info.runtime
info.genres
info.plot_outline
"""


def csv_rows(x):
    ''' get CSV's rows'''
    csv_rows = []
    for i in x:
        csv_rows.append([getattr(i, z) for z in ['title','year','rating','certification','runtime','genres','plot_outline']])
    write_csv(csv_rows)

def write_csv(csv_rows):
    """write csv using csv module."""

    # csv setting
    csv_fields = ['Title', 'Year', 'imdbRating', 'Rated', 'Runtime','Genre','Plot']
    delimiter = ','

    # write csv using csv module
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'movies.csv'), "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_fields)
        for row in csv_rows:
            csvwriter.writerow(row)


if __name__ == "__main__":  # pragma: no cover
    movies_names = name_grabber(os.listdir(os.path.dirname(os.path.abspath(__file__))))
    identifies = identify_movies(movies_names)
    csv_rows(identifies)


