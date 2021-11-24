from ranking_model import MovieRankingModel

model = MovieRankingModel()

for row in model.get_top_results('toy', 'Genre_Children', 10):
  movie_data = row.get_info()
  print(f"{movie_data['title']} ({movie_data['year']}) -- Rating: {movie_data['rating']} -- Score: {movie_data['score']}")
