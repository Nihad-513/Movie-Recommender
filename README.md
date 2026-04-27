# Movie Recommendation System

A machine learning-based movie recommendation system that provides personalized suggestions using **content-based** and **popularity-based filtering techniques**.

---

##  Features

*  Content-based recommendations using similarity between movie genres
*  Popularity-based recommendations based on user ratings
*  Simple graphical user interface using Tkinter
*  Modular code structure for better scalability and readability

---

##  Technologies Used

* Python
* Pandas, NumPy
* scikit-learn
* Tkinter (GUI)

---


##  How It Works

### 1. Data Preprocessing

* Merges movie and rating datasets
* Cleans and extracts features (e.g., genres, year)

### 2. Recommendation Techniques

* **Content-Based Filtering**
  Uses TF-IDF vectorization and cosine similarity to recommend similar movies

* **Popularity-Based Filtering**
  Recommends top-rated movies based on average ratings and minimum review threshold

---

##  How to Run

### 1. Clone the repository

```
git clone https://github.com/YOUR_USERNAME/movie-recommender.git
cd movie-recommender
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Add dataset

Create a `data/` folder and place:

* `movies.csv`
* `ratings.csv`

### 4. Run the application

```
python app.py
```

---

##  Dataset

This project uses a movie dataset (e.g., MovieLens).
Due to size constraints, the dataset is not included in this repository.

---

##  Future Improvements

* Convert GUI to web app using Streamlit
* Add collaborative filtering for better personalization
* Deploy the application online

---

