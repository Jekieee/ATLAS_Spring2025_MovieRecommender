from flask import Flask, request, jsonify,render_template
from flask_cors import CORS

import json
import os

import requests

from taste_quiz import rate_base_recommendations, story_base_recommendations, genre_base_recommendations
from explore import get_movies

app = Flask(__name__)
CORS(app)


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie = data.get('movie')
    reason = data.get('reason')  # Not used in logic yet, but available

    try:
        # Call the real recommendation function
        recommendations = []
        # Popular/Rate Based Recommendation
        if reason == "It is popular":
            recommendations = rate_base_recommendations().tolist()
        # Description Based Recommendation
        if reason == "Love the story":
            recommendations = story_base_recommendations(movie).tolist()

        # Genres Base Recommendation
        if reason == "Like the actors, director or the genre":
            recommendations = genre_base_recommendations(movie)

        return jsonify({"recommendations": recommendations})
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": "Could not generate recommendations"}), 500

@app.route('/api/questionnaire-movies', methods=['GET'])
def questionnaire_movies():
    try:
        with open('data/movies.json', encoding='utf-8') as f:
            movie_list = json.load(f)
        return jsonify(movie_list)
    except Exception as e:
        print(f"Error loading questionnaire movies: {e}")
        return jsonify({"error": "Failed to load movies"}), 500

# @app.route('/movies', methods=['GET'])
# def movies():
#     movies_list = get_movies()
#     return jsonify(movies_list)

@app.route('/fetch_movies', methods=['GET'])
def fetch_movies():
    try:
        # Log loading of the dataset
        print("Fetching movie data...")

        # Get the first 10 rows from the dataframe and convert to a dictionary
        movies_list = get_movies()

        return jsonify(movies_list)  # Return the movie data as JSON
    except Exception as e:
        print(f"Error fetching movies: {e}")  # Log error
        return jsonify({"error": "Something went wrong."}), 500

@app.route('/submit_rating', methods=['POST'])
def submit_rating():
    # Get the incoming JSON data
    data = request.json
    print('Received data:', data)  # Log it to the console

    imdb_id = data.get('imdbId')
    rating = data.get('rating')



    return jsonify(data), 200

if __name__ == '__main__':
    app.run(debug=True)
