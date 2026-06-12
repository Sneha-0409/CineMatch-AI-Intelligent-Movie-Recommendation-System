import streamlit as st
import pickle
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


movies = pickle.load(
    open('movie_list.pkl','rb')
)

similarity = pickle.load(
    open('similarity.pkl','rb')
)



# Fetch Movie Poster
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data = requests.get(url).json()

    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500" + poster_path

    return None


# Fetch Movie Rating
def fetch_rating(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    data = requests.get(url).json()

    return round(data.get('vote_average', 0), 1)


# Recommendation Function
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


# Page Configuration
st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide"
)

# Title
st.title("🎬 CineMatch AI")

st.markdown("""
Discover movies similar to your favorites using **content-based filtering,
metadata feature engineering, and cosine similarity**.
""")

# Movie Dropdown
selected_movie = st.selectbox(
    "Choose a Movie",
    movies['title'].values
)

# Recommendation Button
if st.button("Recommend"):

    names, posters, ratings, scores = recommend(
        selected_movie
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    cols = [col1, col2, col3, col4, col5]

    for idx, col in enumerate(cols):

        with col:

            if posters[idx]:
                st.image(posters[idx])

            st.markdown(
                f"**{names[idx]}**"
            )

            st.write(
                f"⭐ {ratings[idx]}"
            )

            st.caption(
                f"Similarity Score: {scores[idx]}%"
            )