import streamlit as st
from recommender import load_data, build_matrix, get_recommendations

#Page config
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

#Load data
@st.cache_data
def setup():
    movies, ratings = load_data()
    matrix = build_matrix(ratings)
    return movies, matrix

movies, matrix = setup()

#UI

st.title("🎬 Movie Recommender System")
st.write("Enter a movie you like and we'll recommend 10 similar ones.")

movie_input = st.text_input("Movie Title:", placeholder="e.g. The Matrix")

if movie_input:
    recommendations, matched_title = get_recommendations(movie_input, movies, matrix)

    if recommendations is None:
        st.error(matched_title)
    else:
        st.success(f"Becuase you liked **{matched_title}**, you might enjoy:")
        st.dataframe(
            recommendations.reset_index(drop=True),
            use_container_width=True
        )

