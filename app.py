from flask import Flask, escape, request, render_template
import json
import requests
import os

app = Flask(__name__)


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


@app.route('/favorites')
def favorites():
    """if query params are passed, write movie to json file."""
    return render_template('favorites.html')


@app.route('/search', methods=['POST'])
def search():
    """if POST, query movie api for data and return results."""

    query = request.form['title']

    key = os.environ['API_KEY']

    movieQueryResponse = requests.get(
        'http://www.omdbapi.com/?apikey=' + key + '&s='+query)

    return render_template('search_results.html', results=json.loads(movieQueryResponse.text)['Search'])


@app.route('/movie/<imdbID>')
def movie_detail(imdbID):
    """if fetch data from movie database by oid and display info."""
    #qs_name = request.args.get('name', '')

    query = escape(imdbID)

    key = os.environ['API_KEY']

    movieQueryResponse = requests.get(
        'http://www.omdbapi.com/?apikey=' + key + '&i='+query)

    print("response: ")

    print(movieQueryResponse.text)

    return render_template('movie.html', results=json.loads(movieQueryResponse.text))
