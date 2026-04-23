import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    movies = pd.read_csv('data/movies.csv')
    ratings = pd.read_csv('data/ratings.csv')
    return movies, ratings

def build_matrix(ratings):
    #create a movie-user matrix
    matrix = ratings.pivot_table(
        index = 'movieId',
        columns = 'userId',
        values = 'rating'
    ).fillna(0)
    return matrix

def get_recommendations(movie_title, movies, matrix, n=10):
    #find the movie in our dataset
    movie_match = movies[movies['title'].str.contains(movie_title, case=False, na=False)]
    if movie_match.empty:
        return None, "movie not found. Try another title."
    
    #Get the first match
    movie_id = movie_match.iloc[0]['movieId']
    movie_title_clean = movie_match.iloc[0]['title']

    #Check movie is in our matrix
    if movie_id not in matrix.index:
        return None, "Not enough rating for this movie."
    
    #Compute cosine similarity between all movies
    similarity = cosine_similarity(matrix)
    similarity_df = pd.DataFrame(
        similarity,
        index=matrix.index,
        columns=matrix.index
    )

    #Get similar movies
    similar_movies = similarity_df[movie_id].sort_values(ascending=False)

    #Remove the movie itself
    similar_movies = similar_movies.drop(movie_id)

    #get top N
    top_ids = similar_movies.head(n).index.tolist()

    #Map back to titles
    recommendations = movies[movies['movieId'].isin(top_ids)][['title', 'genres']]

    return recommendations, movie_title_clean
    