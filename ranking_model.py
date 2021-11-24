import pandas as pd
from typing import Dict, List, Any

class Movie:
  def __init__(self, title: str, year: int, rating: float, score: float) -> None:
    self.title = title
    self.year = year
    self.rating = rating
    self.score = score
  
  def get_info(self) -> Dict[str, Any]:
    return {
      'title': self.title,
      'year': self.year,
      'rating': self.rating,
      'score': self.score
    }


class MovieRankingModel:
  def __init__(self) -> None:
    self.df: pd.DataFrame = pd.read_csv('merged.csv')

    self.df['genres'] = self.df['genres'].apply(lambda x:x.split("|")) # Split the genres
    self.df['year'] = self.df.title.str.extract('(\(\d\d\d\d\))',expand=False) # Parse the date
    self.df['year'] = self.df.year.str.extract('(\d\d\d\d)',expand=False) # Parse the date
    self.df['title'] = self.df['title'].apply(lambda x: x.replace(x, x.lower())) # Convert all titles to lower case
    self.df['title'] = self.df.title.str.replace('\(\d\d\d\d\)', '', regex=True) # Remove the date from all titles
    self.df['title'] = self.df['title'].apply(lambda x: x.strip()) # Remove whitespace from all titles
    self.df = self.df.dropna() # Drop rows with missing values
    self.df['year'] = self.df['year'].astype(int) # Make the year column type integer

    genre_dummies = self.df['genres'].explode().str.get_dummies().sum(level=0).add_prefix('Genre_')
    self.df = self.df.drop('genres', 1).join(genre_dummies)
    self.df = self.df[self.df['Genre_(no genres listed)'] == 0]
    self.df = self.df.drop('Genre_(no genres listed)', 1)

    self.df['ranking_score'] = (0.9 * ( 1.0 - ((5.0 - self.df['rating']) / 4.5) ) ) + ( 0.1 * ( 1.0 - ((2016 - self.df['year']) / 142.0) ) )
    self.df['adjusted_ranking_score'] = 0.0

  def get_query_match_percentage(self, query: str, title: str) -> float:
    """Gets the percentage of query terms found in a movie title.
    
    Args:
      query: The search query.
      title: The movie title.
    """
    count = 0
    unique_title_words = set(title.split())
    for term in query.split():
      if term in unique_title_words:
        count += 1
    return round(float(count) / len(query.split()), 2)

  def get_top_results(self, query: str, genre: str, num_results: int) -> List[Movie]:
    """Gets the top results from the ranking model.

    Args:
      query: The search query.
      genre: The movie genre.
      num_results: The number of results to return.
    """
    # TODO(thompsond): Add a boolean flag for whether or not to filter by genre
    results = []
    filtered_rows = self.df[self.df[genre] == 1]
    for index, row in filtered_rows.iterrows():
      # Get the ranking_score
      ranking_score = row['ranking_score']
      # Get the query match percentage
      query_match_percent = self.get_query_match_percentage(query, row['title'])
      # Set the adjusted ranking score
      adjusted_ranking_score = ranking_score + query_match_percent
      filtered_rows.at[index, 'adjusted_ranking_score'] = adjusted_ranking_score
    # Sort by the adjusted ranking score
    sorted_rows = filtered_rows.sort_values(by=['adjusted_ranking_score'], ascending=False).head(num_results)
    # Return N results
    results = [Movie(row['title'], row['year'], row['rating'], row['adjusted_ranking_score']) for _, row in sorted_rows.iterrows()]
    return results
