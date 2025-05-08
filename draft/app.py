from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# login system
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os

import requests

from data import rate_base_recommendations, story_base_recommendations, genre_base_recommendations
from pprint import pprint

from datetime import datetime, timedelta

app = Flask(__name__)
app.permanent_session_lifetime = timedelta(hours=12)

app.secret_key = os.urandom(24)
USER_DB_FILE = 'users.json'

# Load users if file exists
if os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, 'r') as f:
        user_db = json.load(f)
else:
    user_db = {}

# Save users to file
def save_users():
    with open(USER_DB_FILE, 'w') as f:
        json.dump(user_db, f)


CORS(app, supports_credentials=True)


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


SERPAPI_KEY = '2805f62cad5c41428c65a956d4af98645d6854f0271b8a70d1e09a3460ab56ba'


@app.route('/showtimes', methods=['GET'])
def fetch_showtimes():
    location = request.args.get('location')
    q = request.args.get('q', f"movies in {location}")
    if not location:
        return jsonify({"error": "Location is required"}), 400

    params = {
        "q": q,
        "location": f"{location}, United States",
        "hl": "en",
        "gl": "us",
        "api_key": SERPAPI_KEY
    }

    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        data = response.json()
        print(f"🧪 {len(data.get('showtimes', []))} showtime entries found.")
        pprint(data.get('showtimes', [])[0])
        return jsonify(data.get("showtimes") or data.get("movies") or [])
    except Exception as e:
        print(f"❌ Error fetching showtimes: {e}")
        return jsonify({"error": "Failed to fetch showtimes"}), 500

@app.route("/session", methods=["GET", "POST"])
def session_handler():
    session.permanent = True

    if request.method == "GET":
        if "user" in session:
            return jsonify({"loggedIn": True, "name": session["user"]["name"]})
        return jsonify({"loggedIn": False})

    if request.method == "POST":
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        # Handle Registration
        if "name" in data:
            name = data["name"]
            if email in user_db:
                return jsonify({"success": False, "message": "Email already registered."})

            hashed_pw = generate_password_hash(password)
            user_db[email] = {"name": name, "password": hashed_pw}
            session["user"] = {"name": name, "email": email}
            save_users()
            return jsonify({"success": True})

        # Handle Login
        if email in user_db and check_password_hash(user_db[email]["password"], password):
            session["user"] = {"name": user_db[email]["name"], "email": email}
            return jsonify({"success": True, "name": user_db[email]["name"]})
        return jsonify({"success": False, "message": "Invalid email or password."})

@app.route('/logout', methods=["GET"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True})

@app.route("/debug/users")
def debug_users():
    return jsonify(user_db)

if __name__ == '__main__':
    app.run(debug=True)
