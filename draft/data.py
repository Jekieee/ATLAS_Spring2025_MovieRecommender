import pandas as pd
import numpy as np

# Import Data
df1 = pd.read_csv('tmdb_5000_credits.csv')
df2 = pd.read_csv('tmdb_5000_movies.csv')

df1.columns = ['id', 'tittle', 'cast', 'crew']
df2 = df2.merge(df1, on='id')

# Create Parameters
C = df2['vote_average'].mean()

m = df2['vote_count'].quantile(0.9)

q_movies = df2.copy().loc[df2['vote_count'] >= m]


def weighted_rating(x, m=m, C=C):
    v = x['vote_count']
    R = x['vote_average']
    return (v / (v + m) * R) + (m / (m + v) * C)


q_movies['score'] = q_movies.apply(weighted_rating, axis=1)

q_movies = q_movies.sort_values('score', ascending=False)

# Import TfIdfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer

# Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

# Replace NaN with an empty string
df2['overview'] = df2['overview'].fillna('')

# Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(df2['overview'])

# Output the shape of tfidf_matrix
tfidf_matrix.shape

# Import linear_kernel
from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Construct a reverse map of indices and movie titles
indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

# Function that return high rate and popular movies:
def rate_base_recommendations():
    return q_movies['title'].head(10)

# Function that takes in movie title as input and outputs most similar movies
def story_base_recommendations(title, cosine_sim=cosine_sim):
    # Get the index of the movie that matches the title
    idx = indices[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df2['title'].iloc[movie_indices]

# Genres Base Recommender System
from ast import literal_eval

features = ['cast', 'crew', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(literal_eval)

def get_director(x):
    for i in x:
        if i['job'] == 'Director':
            return i['name']
    return np.nan

def get_list(x):
    if isinstance(x, list):
        names = [i['name'] for i in x]
        #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
        if len(names) > 3:
            names = names[:3]
        return names

    #Return empty list in case of missing/malformed data
    return []

# Define new director, cast, genres and keywords features that are in a suitable form.
df2['director'] = df2['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feature in features:
    df2[feature] = df2[feature].apply(get_list)

df3 = df2.copy()

# Convert stringified lists to actual lists (if needed)
def clean_list_column(col):
    return col.apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Apply to relevant columns
for col in ['keywords', 'cast', 'genres']:
    df3[col] = clean_list_column(df2[col])

def clean_text_list(text_list):
    return [str(item).replace(" ", "").lower() for item in text_list]

# Apply cleaning
for col in ['keywords', 'cast', 'genres']:
    df3[col] = df3[col].apply(clean_text_list)

# Also clean director
df3['director'] = df3['director'].apply(lambda x: str(x).replace(" ", "").lower())

def compute_similarity(movie1, movie2):
    score = 0

    # Compare keywords
    score += len(set(movie1['keywords']) & set(movie2['keywords']))

    # Compare cast
    score += len(set(movie1['cast']) & set(movie2['cast']))

    # Compare genres
    score += len(set(movie1['genres']) & set(movie2['genres']))

    # Compare director
    if movie1['director'] == movie2['director']:
        score += 1

    return score / 10  # Normalize to [0,1]

def genre_base_recommendations(movie_title, df = df3, top_n=10):
    # Get the movie we want to compare others to
    movie = df[df['title'] == movie_title].iloc[0]

    # Compute similarity with all other movies
    scores = []
    for idx, other in df.iterrows():
        if other['title'] != movie_title:
            sim = compute_similarity(movie, other)
            scores.append((other['title'], sim))

    # Sort by score, descending
    scores.sort(key=lambda x: x[1], reverse=True)

    # Return top_n recommendations
    return scores[:top_n]
