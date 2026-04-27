from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def popularity_based_recommender(data, genre, min_ratings, n):
    genre_data = data[data['genres'] == genre]

    movie_stats = genre_data.groupby('title').agg({
        'rating': ['mean', 'count']
    })

    movie_stats.columns = ['avg_rating', 'num_ratings']

    popular = movie_stats[movie_stats['num_ratings'] >= min_ratings]
    top_movies = popular.sort_values(by='avg_rating', ascending=False).head(n)

    return top_movies


def content_based_recommender(movies, title, n):
    title = title.strip()

    if title.lower() not in movies['title'].str.lower().values:
        return f"Movie '{title}' not found."

    idx = movies[movies['title'].str.lower() == title.lower()].index[0]

    tfidf = TfidfVectorizer(tokenizer=lambda x: x.split('|'))
    tfidf_matrix = tfidf.fit_transform(movies['genres'])

    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    scores = list(enumerate(cosine_sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:n+1]

    return [movies['title'].iloc[i[0]] for i in scores]