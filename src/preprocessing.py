import pandas as pd

def load_data(movies_path, ratings_path):
    movies = pd.read_csv(movies_path)
    ratings = pd.read_csv(ratings_path)
    return movies, ratings


def preprocess_data(movies, ratings):
    # Merge datasets
    data = pd.merge(ratings, movies, on='movieId')

    # Convert timestamp
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

    # Extract year from title
    data['year'] = data['title'].str.extract(r'\((\d{4})\)', expand=False)
    data['title'] = data['title'].str.replace(r'\(\d{4}\)', '', regex=True).str.strip()

    # Split genres
    data = data.assign(genres=data['genres'].str.split('|')).explode('genres')

    return data