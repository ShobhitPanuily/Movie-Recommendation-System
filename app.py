import streamlit as st
import pandas as pd
import pickle
import requests
import os

if not os.path.exists("movie_data.pkl"):
    url = "https://www.dropbox.com/scl/fi/jta3xmx29zl6suov311o3/movie_data.pkl?rlkey=rf937zyc9ho2snftbndgo631j&e=1&st=s4e9bhud&dl=0"  
    response = requests.get(url)
    with open("movie_data.pkl", "wb") as f:
        f.write(response.content)

with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

st.title("🎬 Movie Recommendation System")

selected_movie = st.selectbox("Select a movie:", movies['title'].values)

if st.button("Recommend"):
    recommendations = get_recommendations(selected_movie)
    st.write("### Top 10 Recommended Movies:")
    for i, title in enumerate(recommendations, start=1):
        st.write(f"{i}. {title}")
