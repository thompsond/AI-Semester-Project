import pandas as pd

df_movies = pd.read_csv('movies.csv') # Movie data: (movieId, title, genres)
df_ratings = pd.read_csv('ratings.csv', usecols=['movieId', 'rating']) # Rating data: (movieId, rating)

df_ratings = df_ratings.groupby('movieId').mean() # Group the rows in the ratings dataset by their movieId and the average rating for each movie
df_merged = df_movies.set_index('movieId').join(df_ratings).round(1)
df_merged = df_merged.dropna()

df_merged.to_csv('merged.csv')
