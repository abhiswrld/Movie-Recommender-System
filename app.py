import streamlit as st
import pickle
import pandas as pd
import requests
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for background, UI hiding, and button centering
page_bg_css = """
<style>
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); 
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

img {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.5);
}

/* Center the button */
div.stButton {
    text-align: center;
}

/* Optional: Make the button look a bit sleeker */
div.stButton > button {
    background-color: #2b5876;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 24px;
    font-weight: bold;
    transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #4e4376;
    color: white;
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
vectors = sparse.load_npz('vectors.npz')

def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}',
        params={'api_key': st.secrets["TMDB_API_KEY"], 'language': 'en-US'}
    )
    data = response.json()
    poster_path = data.get('poster_path')
    return 'https://image.tmdb.org/t/p/w500' + poster_path if poster_path else None

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = cosine_similarity(vectors[movie_index], vectors)[0]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

# 1. Centered HTML Title (Stays centered)
st.markdown("<h1 style='text-align: center; color: white; margin-bottom: 2rem;'>Movie Recommender System</h1>", unsafe_allow_html=True)

# 2. Left-aligned input section (removed the spacers)
selected_movie = st.selectbox(
    'Type or select a movie to get recommendations:',
    movies['title'].values
)

recommend_clicked = st.button('Recommend')

# 3. Display results full-width
if recommend_clicked:
    names, posters = recommend(selected_movie)
    
    st.markdown("<br>", unsafe_allow_html=True) 
    cols = st.columns(5)
    
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"<h5 style='text-align: center; color: white;'>{names[idx]}</h5>", unsafe_allow_html=True)
            st.image(posters[idx])