import requests,os,csv
import json,re
"""
export-Movies-rating.py
Mohamed Hamza
Exports IMDB's informations for your movies to CSV file.
"""

def list_movies():
    '''
    identifies movies in the current directory
    movies' names should be in a specific form which is 'name of the movie (year)'
    for the script to work.
    you can use "filebot" to do that.
    https://www.filebot.net/forums/viewtopic.php?f=4&t=215

    or you can make your own Regex
    '''

    u=[]
    #regex = re.compile(r'(\w+\s)+')

    Regex = re.compile(r'.+[^ \(\d+\)]')
    for x in os.listdir(os.path.dirname(os.path.abspath(__file__))):
        z=Regex.search(x).group()
        u.append(z)
    identify_movies(u)


def identify_movies (x):
    ''' identifying the movies using omdbapi API '''
    url = "http://www.omdbapi.com/?t="
    u=[]
    for i in x:
        add = url + i
        u.append(add)
    scrap_info(u)

def scrap_info(x):
    ''' scrap movies' info'''
    u=[]
    for i in x:
        response = requests.get(i)
        python_dictionary_values = json.loads(response.text)
        u.append(python_dictionary_values)
    csv_rows(u)

def csv_rows(x):
    ''' get CSV's rows'''
    csv_rows = []
    for i in x:
        csv_rows .append([i.get(z) for z in ['Title','Year','imdbRating','Rated','Runtime','Genre','Plot']])
    write_csv(csv_rows)

def write_csv(csv_rows):
    """write csv using csv module."""

    # csv setting
    csv_fields = ['Title', 'Year', 'imdbRating', 'Rated', 'Runtime','Genre','Plot']
    delimiter = ','

    # write csv using csv module
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__),'movies.csv'), "w", newline='')) as f:
        csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_fields)
        for row in csv_rows:
            csvwriter.writerow(row)


if __name__ == "__main__":  # pragma: no cover
    list_movies()
