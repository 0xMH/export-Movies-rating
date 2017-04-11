import requests,os,csv
import json,re
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
    '''Gets the Movie Name and Year from the filename and other meta
    data is removed.
    For Example:
    >>> Doctor.Strange.2016.720p.BrRip.mkv [INPUT]
    >>> Doctor Strange 2016 [RETURN]
    This function is made mostly from: https://github.com/RafayGhafoor/Subscene-Subtitle-Grabber
    '''
    nameslist = []
    for movies in medialst:
        yearRegex = re.compile(r'\d{4}')
        if yearRegex.search(movies):

            def get_year(filename):
                    searchItems = yearRegex.search(filename)
                    return searchItems.group()

            year = get_year(movies)
            # This is 2016 Movie --> This is | 2016 | Movie
            prev, found, removal = movies.partition(year)
            
            if prev[-1] == ' ':
                nameslist.append(prev.lower())
            else:
                nameslist.append(prev.lower()[:-1])

    print(nameslist)
    nameslist = [i.strip(' ') for i in nameslist]
    return nameslist

def identify_movies (x):
    ''' identifying the movies using omdbapi API '''

    url = "http://www.omdbapi.com/?t="
    u=[]
    for i in x:
        add = url + i
        u.append(add)
    return u

def scrap_info(x):
    ''' scrap movies' info'''
    u=[]
    for i in x:
        response = requests.get(i)
        python_dictionary_values = json.loads(response.text)
        u.append(python_dictionary_values)
    return u

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
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'movies.csv'), "w", newline='') as f:
        csvwriter = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(csv_fields)
        for row in csv_rows:
            csvwriter.writerow(row)


if __name__ == "__main__":  # pragma: no cover
    movies_names = name_grabber(os.listdir(os.path.dirname(os.path.abspath(__file__))))
    identifies = identify_movies(movies_names)
    info = scrap_info(identifies)
    csv_rows(info)


