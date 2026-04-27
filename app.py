import tkinter as tk
from tkinter import ttk, messagebox

from src.preprocessing import load_data, preprocess_data
from src.recommender import (
    popularity_based_recommender,
    content_based_recommender
)

# Load data
movies, ratings = load_data("data/movies.csv", "data/ratings.csv")
data = preprocess_data(movies, ratings)

genres = sorted(data['genres'].unique())

# UI functions
def get_popular():
    try:
        genre = genre_var.get()
        min_r = int(min_entry.get())
        n = int(num_entry.get())

        result = popularity_based_recommender(data, genre, min_r, n)
        output.delete(1.0, tk.END)
        output.insert(tk.END, result.to_string())

    except:
        messagebox.showerror("Error", "Invalid input")


def get_content():
    try:
        title = title_entry.get()
        n = int(num_entry.get())

        result = content_based_recommender(movies, title, n)

        output.delete(1.0, tk.END)

        if isinstance(result, str):
            output.insert(tk.END, result)
        else:
            output.insert(tk.END, "\n".join(result))

    except:
        messagebox.showerror("Error", "Invalid input")


# UI layout
root = tk.Tk()
root.title("Movie Recommender")

ttk.Label(root, text="Genre").grid(row=0, column=0)
genre_var = tk.StringVar()
ttk.Combobox(root, textvariable=genre_var, values=genres).grid(row=0, column=1)

ttk.Label(root, text="Movie Title").grid(row=1, column=0)
title_entry = ttk.Entry(root)
title_entry.grid(row=1, column=1)

ttk.Label(root, text="Min Ratings").grid(row=2, column=0)
min_entry = ttk.Entry(root)
min_entry.grid(row=2, column=1)

ttk.Label(root, text="Top N").grid(row=3, column=0)
num_entry = ttk.Entry(root)
num_entry.grid(row=3, column=1)

ttk.Button(root, text="Popularity-Based", command=get_popular).grid(row=4, column=0)
ttk.Button(root, text="Content-Based", command=get_content).grid(row=4, column=1)

output = tk.Text(root, height=20, width=60)
output.grid(row=5, column=0, columnspan=2)

root.mainloop()