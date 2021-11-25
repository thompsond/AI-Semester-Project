import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from ranking_model import MovieRankingModel


app_title = 'Movie RankFinder'
genres = [
  'Action',
  'Adventure',
  'Animation',
  'Children',
  'Comedy',
  'Crime',
  'Documentary',
  'Drama',
  'Fantasy',
  'Film-Noir',
  'Horror',
  'IMAX',
  'Musical',
  'Mystery',
  'Romance',
  'Sci-Fi',
  'Thriller',
  'War',
  'Western'
]
num_results_options = ['5', '10', '15', '20', '30']
model = MovieRankingModel()


def on_search():
  """Event handler for search button."""
  global model, search_var, selected_genre, selected_num_results, search_results

  search_results.config(state=NORMAL)
  search_results.delete('1.0', tk.END)
  query = search_var.get()
  genre = 'Genre_' + selected_genre.get()
  num_results = int(selected_num_results.get())
  results = model.get_top_results(query, genre, num_results)
  result_text = ''
  for index, row in enumerate(results):
    movie_data = row.get_info()
    result_text += f"  {index + 1}. {movie_data['title']} ({movie_data['year']})\n\n"
  search_results.insert(tk.END, result_text)
  search_results.config(state=DISABLED)


# Set up root window
root = tk.Tk()
root.geometry('600x485')
root.title(app_title)
root.resizable(False, False)

# Set up grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

# Title
app_title_label = ttk.Label(root, text=app_title, font=('Helvetica 16'))
app_title_label.grid(column=0, row=0, columnspan=3, pady=10)

####### Search Widgets #######
# Search label
search_label = ttk.Label(root, text='Enter movie title or keywords', font=('Arial 11 bold'))
search_label.grid(column=0, row=1, sticky=tk.W, padx=5)

# Search box
search_var = tk.StringVar()
search_box = ttk.Entry(root, textvariable=search_var)
search_box.grid(column=0, row=2, sticky=tk.W+tk.E, padx=5)

# Search button
search_btn = tk.Button(root, text='Search', command=on_search)
search_btn.grid(column=0, row=3, sticky=tk.E, padx=5, pady=10)

####### Genre Widgets #######
# Genre label
genre_label = ttk.Label(root, text='Genre', font=('Arial 11 bold'))
genre_label.grid(column=1, row=1)

# Genre dropdown
selected_genre = tk.StringVar(root)
genre_dropdown = ttk.OptionMenu(root, selected_genre, genres[0], *genres)
genre_dropdown.grid(column=1, row=2)

####### Number of Results Widgets #######
# Num of results label
num_results_label = ttk.Label(root, text='# of Results', font=('Arial 11 bold'))
num_results_label.grid(column=2, row=1)

# Num of results dropdown
selected_num_results = tk.StringVar(root)
num_results_picker = ttk.OptionMenu(root, selected_num_results, num_results_options[0], *num_results_options)
num_results_picker.grid(column=2, row=2)


# Movie results
search_results = scrolledtext.ScrolledText(root, cursor='arrow', font=('Helvetica 15 bold'), height=15)
search_results.grid(column=0, columnspan=3)

root.mainloop()
