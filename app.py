from flask import Flask, escape, request, render_template
import json
import requests
import os

app = Flask(__name__)

key = os.environ['API_KEY']


@app.route('/')
def index():
    return render_template('index.html')

# @app.route('favorites')
# def favorites():
#    Read out favorited movies.
#    filename = os.path.join('data.json')
#    with open(filename) as data_file:
#        data = json.load(data_file)
#        return data


@app.route('/favorites', methods=['POST'])
def favorites():
    """if query params are passed, write movie to json file."""
    #return render_template('favorites.html')
    return json.dumps({
        "favorite": "added"
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

    resp =json.loads(movieQueryResponse.text)
    
    #handle condition where no movies are returned from query
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
