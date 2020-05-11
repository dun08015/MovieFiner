from flask import Flask, escape, request, render_template
import json
import requests
import os

app = Flask(__name__)

key = os.environ['API_KEY']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/favorites')
def favorites():
    # Read out favorited movies.
    filename = os.path.join('data.json')
    with open(filename) as data_file:
        data = json.load(data_file)
        favorites = json.dumps(data)
        print("sending: "+favorites)
        return render_template('favorites.html', results=favorites['Movies'])


@app.route('/favorites', methods=['POST'])
def favoritesPost():
    """if query params are passed, write movie to json file."""

    movieID = request.form['movieID']
    movieTitle = request.form['movieTitle']
    isFavorite = request.form['isFavorite']

    movie = {
        'movieID': movieID,
        'movieTitle': movieTitle
    }

    filename = os.path.join('data.json')

    with open(filename, 'r+') as outfile:
        data = json.load(outfile)
        if isFavorite == 'true':
            data['Movies'].append(movie)
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
            return json.dumps({
                "result": "favorite added!"
                })
        else:
            try:
                data['Movies'].remove(movie)
            except ValueError:
                return json.dumps({
            "result": "value error on removing favorite!"})
            outfile.seek(0)
            json.dump(data, outfile)
            outfile.truncate()
            return json.dumps({
                "result": "favorite removed!"
                })


@app.route('/search', methods=['POST'])
def search():
    """if POST, query movie api for data and return results."""

    query = request.form['title']

    strippedQuery = query.strip()

    wildCardQuery = "*" + strippedQuery + "*"

    movieParams = {'s': wildCardQuery, 'apikey': key}

    movieQueryResponse = requests.get(
        'http://www.omdbapi.com', params=movieParams)

    resp = json.loads(movieQueryResponse.text)

    # handle condition where no movies are returned from query
    if "Error" in resp:
        return render_template('index.html', errorQuery=query)
    else:
        return render_template('search_results.html', results=resp['Search'])


@app.route('/movie/<imdbID>')
def movie_detail(imdbID):
    """if fetch data from movie database by imdbID and display info."""

    query = escape(imdbID)

    movieParams = {'i': query, 'apikey': key}

    movieQueryResponse = requests.get(
        'http://www.omdbapi.com', params=movieParams)

    return render_template('movie.html', results=json.loads(movieQueryResponse.text))
