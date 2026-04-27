import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import tkinter as tk
from tkinter import ttk, messagebox

# Load the data
movies = pd.read_csv('movies.csv')
ratings = pd.read_csv('ratings.csv')

# Merge movies and ratings dataframes on movieId
data = pd.merge(ratings, movies, on='movieId')

# Convert timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

# Extract year from the title
data['year'] = data['title'].str.extract(r'\((\d{4})\)', expand=False)
data['title'] = data['title'].str.replace(r'\(\d{4}\)', '').str.strip()

# Split genres into individual rows
data = data.assign(genres=data['genres'].str.split('|')).explode('genres')

# Get unique genres
unique_genres = sorted(data['genres'].unique())


def popularity_based_recommender(genre, min_ratings, num_recommendations):
    genre_data = data[data['genres'] == genre]
    movie_stats = genre_data.groupby('title').agg({'rating': ['mean', 'count']})
    movie_stats.columns = ['average_rating', 'num_ratings']
    popular_movies = movie_stats[movie_stats['num_ratings'] >= min_ratings]
    top_movies = popular_movies.sort_values(by='average_rating', ascending=False).head(num_recommendations)
    return top_movies


def content_based_recommender(movie_title, num_recommendations):
    movie_title = movie_title.strip()
    matching_movies = movies[movies['title'].str.lower() == movie_title.lower()]

    if len(matching_movies) == 0:
        return f"Movie '{movie_title}' not found in the dataset."

    movie_index = matching_movies.index[0]
    count_vect = CountVectorizer(tokenizer=lambda x: x.split('|'))
    genre_matrix = count_vect.fit_transform(movies['genres'])
    cosine_sim = cosine_similarity(genre_matrix, genre_matrix)
    sim_scores = list(enumerate(cosine_sim[movie_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:num_recommendations + 1]
    similar_movies = [movies['title'].iloc[i[0]] for i in sim_scores]
    return similar_movies


def display_popularity_based_recommendations():
    genre = genre_var.get().strip()
    min_ratings = min_ratings_entry.get().strip()
    num_recommendations = num_recommendations_entry.get().strip()

    if not min_ratings.isdigit() or not num_recommendations.isdigit():
        messagebox.showerror("Input Error",
                             "Please enter valid integers for minimum ratings threshold and number of recommendations.")
        return

    min_ratings = int(min_ratings)
    num_recommendations = int(num_recommendations)

    recommendations = popularity_based_recommender(genre, min_ratings, num_recommendations)
    result_text = recommendations.to_string()
    recommendations_text.delete(1.0, tk.END)
    recommendations_text.insert(tk.END, result_text)


def display_content_based_recommendations():
    movie_title = movie_title_entry.get().strip()
    num_recommendations = num_recommendations_entry.get().strip()

    if not num_recommendations.isdigit():
        messagebox.showerror("Input Error", "Please enter a valid integer for number of recommendations.")
        return

    num_recommendations = int(num_recommendations)
    recommendations = content_based_recommender(movie_title, num_recommendations)

    if isinstance(recommendations, str):
        result_text = recommendations
    else:
        result_text = '\n'.join(recommendations)

    recommendations_text.delete(1.0, tk.END)
    recommendations_text.insert(tk.END, result_text)


def show_main_menu():
    popularity_frame.grid_forget()
    content_frame.grid_forget()
    main_frame.grid(row=0, column=0, padx=10, pady=10)


def show_popularity_frame():
    main_frame.grid_forget()
    content_frame.grid_forget()
    popularity_frame.grid(row=0, column=0, padx=10, pady=10)


def show_content_frame():
    main_frame.grid_forget()
    popularity_frame.grid_forget()
    content_frame.grid(row=0, column=0, padx=10, pady=10)


# Create the main window
root = tk.Tk()
root.title("Movie Recommendation System")

# Main frame
main_frame = ttk.Frame(root)
ttk.Label(main_frame, text="Choose Recommendation Type").grid(row=0, column=0, columnspan=2, pady=10)
ttk.Button(main_frame, text="Popularity-based Recommendation", command=show_popularity_frame).grid(row=1, column=0,
                                                                                                   pady=10, padx=10)
ttk.Button(main_frame, text="Content-based Recommendation", command=show_content_frame).grid(row=1, column=1, pady=10,
                                                                                             padx=10)
main_frame.grid(row=0, column=0, padx=10, pady=10)

# Popularity frame
popularity_frame = ttk.Frame(root)
ttk.Label(popularity_frame, text="Popularity-based Recommendations").grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(popularity_frame, text="Genre:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

# Dropdown menu for genres
genre_var = tk.StringVar()
genre_menu = ttk.Combobox(popularity_frame, textvariable=genre_var, values=unique_genres)
genre_menu.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(popularity_frame, text="Minimum Reviews:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
min_ratings_entry = ttk.Entry(popularity_frame)
min_ratings_entry.grid(row=2, column=1, padx=5, pady=5)
ttk.Label(popularity_frame, text="Number of Recommendations:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
num_recommendations_entry = ttk.Entry(popularity_frame)
num_recommendations_entry.grid(row=3, column=1, padx=5, pady=5)
ttk.Button(popularity_frame, text="Get Popularity-based Recommendations",
           command=display_popularity_based_recommendations).grid(row=4, column=0, columnspan=2, pady=10)
ttk.Button(popularity_frame, text="Back", command=show_main_menu).grid(row=5, column=0, columnspan=2, pady=10)

# Content frame
content_frame = ttk.Frame(root)
ttk.Label(content_frame, text="Content-based Recommendations").grid(row=0, column=0, columnspan=2, pady=10)
ttk.Label(content_frame, text="Movie Title:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
movie_title_entry = ttk.Entry(content_frame)
movie_title_entry.grid(row=1, column=1, padx=5, pady=5)
ttk.Label(content_frame, text="Number of Recommendations:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
num_recommendations_entry = ttk.Entry(content_frame)
num_recommendations_entry.grid(row=2, column=1, padx=5, pady=5)
ttk.Button(content_frame, text="Get Content-based Recommendations", command=display_content_based_recommendations).grid(
    row=3, column=0, columnspan=2, pady=10)
ttk.Button(content_frame, text="Back", command=show_main_menu).grid(row=4, column=0, columnspan=2, pady=10)

# Recommendations text widget
recommendations_text = tk.Text(root, wrap=tk.WORD, height=20, width=60)
recommendations_text.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
