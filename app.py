import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os

import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Load environment variables
load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

# Load model files
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------------
# Helper Functions
# ---------------------------

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data = requests.get(url).json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return None


def fetch_rating(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data = requests.get(url).json()

    return round(data.get('vote_average', 0), 1)


def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    similarity_scores = []

    for i in movie_list:

        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            fetch_poster(movie_id)
        )

        recommended_ratings.append(
            fetch_rating(movie_id)
        )

        similarity_scores.append(
            round(i[1] * 100)
        )

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        similarity_scores
    )

# ---------------------------
# Page Configuration
# ---------------------------

st.set_page_config(
    page_title="🎬 CineMatch AI",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------
# Custom CSS
# ---------------------------

st.markdown("""
<style>
li {
    color: #FF0000 !important;
}

.stSelectbox div[data-baseweb="select"] * {
    color: white !important;
}

/* Main Background */
.stApp {
    background-color: #CCE5FF;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #B3D9FF;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-size: 18px;
    background-color:#80BFFF;
    color: white;
    border: none;
    padding: 10px;
}

.stButton > button:hover {
    background-color: #2563EB;
    color: white;
}

/* Headings */
h1 {
    text-align: center;
    color: #4169E1 !important;
    font-size: 64px !important;
    font-weight: 700 !important;
}

h2 {
    color: #4169E1 !important;
    font-size: 24px !important;
    font-weight: 700 !important;
}

h3 {
    
    text-align: center;
    color: #4169E1 !important;
    font-size: 20px !important;
    font-weight: 700 !important;
}

/* Text */
p {
    text-align: center;
    color: #000000;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# Title
# ---------------------------

st.markdown("""
# 🎬 CineMatch AI

### Discover your next favorite movie using AI

Get personalized movie recommendations based on genres, cast, directors, keywords, and storyline similarities.
""")

# ---------------------------
# Sidebar
# ---------------------------

with st.sidebar:

    st.header("About CineMatch AI")

    st.write("""
    This recommendation system uses:

     1. Genres
     2. Cast
     3. Directors
     4. Keywords
     5. Movie Overview
    """)

    st.info(
        "Built using Python, Scikit-Learn, TMDB API and Streamlit"
    )

# ---------------------------
# Movie Selection
# ---------------------------

selected_movie = st.selectbox(
    "🎥 Choose a Movie",
    movies['title'].values
)

# ---------------------------
# Recommendation Button
# ---------------------------

if st.button("Recommend"):

    with st.spinner("Finding similar movies..."):

        names, posters, ratings, scores = recommend(
            selected_movie
        )

    st.subheader("🎯 Recommended Movies")

    # First Row
    row1 = st.columns(3)

    for idx in range(3):

        with row1[idx]:

            if posters[idx]:
                st.image(posters[idx])

            st.markdown(
                f"### {names[idx]}"
            )

            st.markdown(
                f"""
                <h4 style="color:black;text-align:center;background-color:#99CCFF;">
                    ⭐ Rating
                </h4>
                <h2 style="color:black;text-align:center;background-color:#99CCFF;">
                    {ratings[idx]}
                </h2>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                scores[idx] / 100
            )

            st.caption(
                f"Match Score: {scores[idx]}%"
            )

    # Second Row
    row2 = st.columns(2)

    for idx in range(3, 5):

        with row2[idx - 3]:

            if posters[idx]:
                st.image(posters[idx])

            st.markdown(
                f"### {names[idx]}"
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#99CCFF;
                    padding:10px;
                    border-radius:10px;
                    text-align:center;
                ">
                    <h4 style="color:#1E3A8A;">
                        ⭐ Rating
                    </h4>
                    <h2 style="color:black;">
                        {ratings[idx]}
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                scores[idx] / 100
            )

            st.caption(
                f"Match Score: {scores[idx]}%"
            )