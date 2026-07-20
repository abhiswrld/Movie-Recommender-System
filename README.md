# CineSync Match: Movie Recommender System

**Live Demo:** [https://cinesyncmatch.streamlit.app/](https://cinesyncmatch.streamlit.app/)

This is a content-based movie recommendation engine. You select a movie, and the system analyzes its genres, plot keywords, cast, and crew to recommend the five most similar films. 

## Key Features
* **Content-Based Filtering:** Uses a Bag-of-Words model and Cosine Similarity to find movies with similar tags.
* **Cloud Optimized:** Uses Compressed Sparse Row (CSR) matrices to reduce memory usage and bypass GitHub's large file limits.
* **Dynamic Posters:** Pulls real-time, high-resolution posters from the TMDB API for every recommendation.
* **Custom UI:** A clean, dark-mode interface built with Streamlit and custom CSS.

## The Machine Learning Pipeline
1. **Data Ingestion:** Merges the TMDB 5000 Movies and Credits datasets.
2. **Feature Extraction:** Pulls the top 3 actors, director, genres, and plot keywords from the raw JSON data.
3. **Data Cleaning:** Removes spaces from names and tags so multi-word entities (like "Science Fiction") are treated as single, unique tokens.
4. **Stemming:** Uses NLTK to reduce words to their root form (e.g., "actions" becomes "action").
5. **Vectorization:** Combines all tags and uses CountVectorizer to map movies into a 3000-dimensional mathematical space.
6. **Similarity Calculation:** Measures the angles between movie vectors using Cosine Similarity to identify the closest matches.

## Built With
* **Frontend:** Streamlit, HTML/CSS
* **Data Processing:** Pandas, NumPy
* **Machine Learning & NLP:** Scikit-Learn, NLTK, SciPy
* **API Integration:** TMDB API, Python `requests`