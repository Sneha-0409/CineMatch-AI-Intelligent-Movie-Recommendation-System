# 🎬 CineMatch AI: Intelligent Movie Recommendation System

## Overview

CineMatch AI is a machine learning-powered movie recommendation system that suggests similar movies based on their content and metadata. The system uses content-based filtering and cosine similarity to analyze genres, cast, directors, keywords, and plot descriptions to generate personalized recommendations.

The application is built using Python, Scikit-Learn, and Streamlit, and provides an interactive web interface where users can select a movie and instantly receive recommendations along with movie posters, ratings, and similarity scores.

---

## Features

* 🎥 Top 5 movie recommendations
* Movie posters fetched using TMDB API
* Movie ratings display
* Similarity score visualization
* Content-based recommendation engine

---

## Machine Learning Pipeline

1. Data Collection using the TMDB 5000 Movies Dataset
2. Data Preprocessing and Feature Engineering
3. Metadata Extraction

   * Genres
   * Keywords
   * Cast
   * Directors
   * Movie Overview
4. Text Vectorization using CountVectorizer
5. Similarity Computation using Cosine Similarity
6. Real-time Recommendation Generation

---

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* Streamlit
* TMDB API
* Pickle

---

## Dataset

TMDB 5000 Movies Dataset

The dataset contains information about more than 5,000 movies, including genres, cast, crew, keywords, ratings, and plot summaries.

---

## Project Structure

```text
CineMatch-AI
│
├── app.py
├── movie_list.pkl
├── requirements.txt
├── README.md
├── data
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
└── Movierecommend.ipynb
```

---

## Installation

```bash
git clone <repository-url>
cd CineMatch-AI
pip install -r requirements.txt
streamlit run app.py
```

---

## Future Enhancements

* Hybrid recommendation system
* Collaborative filtering
* User authentication
* Watchlist generation
* Personalized user profiles

---

## Author

Sneha

Built as a machine learning project to demonstrate recommendation systems, feature engineering, vectorization techniques, and deployment using Streamlit.
