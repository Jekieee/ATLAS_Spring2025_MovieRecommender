# ATLAS_Spring2025_MovieRecommender
ATLAS ML/AI Internship, 2025 Spring, Movie Recommender System

## Introduction
This is a web application that can test a user's preference of movies.
There are 4 different movie recommender systems behind.
 - Demographic Filtering
 - Content Based Filtering, base on:
   - Movie's Description
   - Movie's Metadata
     - Director
     - Crew
     - Genres
     - Keywords    
 - Collaborative Filtering With

There are three features in this web application:
 - [Complete] Taste Test: A questionnaire test recommend movies base on user's choice of movie and the reason they love the movie
 - [In_Progress] Explore Movies: A page that user can rating on different movies, the collaborative filtering can make recommendation based on user's ratings.
 - [Complete] Nearby Cinema: Fetch nearby cinema.

You may find more information about the project in the project report.

## Warning
Some tasks are not complete
Some tasks not connected together, draft and useful code that are not connected to the frontend are in 'draft' file.
 - In explore movie:
   - There is not a way to collect the rating data
   - No connection between the collaborative filtering and the frontend
 - In Nearby Cinema:
   - The Showtime API is not connected to it.

## How to start
1. Download all the code.
2. Start the local web server:  
   Open your terminal and run:  
   python -m http.server 8000
3. Start the Flask server:  
   Run the following command in a separate terminal window/tab:  
   python backend/app.py  
4. Open the website:  
   In your browser, go to:  
   http://localhost:8000/path-to-your-local-file/entry.html

## Contact
If you have any questions or suggestions, feel free to get in touch!  
email: jiaqizeng642@gmail.com
