import pandas as pd

movies_df = pd.read_csv('data/movies_metadata.csv', usecols=['imdb_id', 'title','vote_count'])

def get_movies():
    # Return a limited number of movies (to keep it manageable)
    movies_df.sort_values('vote_count', ascending = False, inplace = True)
    movies_list = movies_df.head(10).to_dict(orient='records')  # Adjust as needed
    return movies_list

