'''
This file is where the recommendation logic happens. It retrieves data from the persistent directory
that embedding.py stored all the vector embeddings in. From there, it will load movies into a dataframe
with relevant movie information merged in.
def retrieve_semantic_recommendations():
    this function serves to find the most similar movies that fit the desired query of the user.
    this is where sentiment analysis occurs in the backend of the project.
'''

import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import pandas as pd
import os
# from embedding import db_movies 

# loading the saved vector store from Chroma's persistent directory
chroma_dir = "chroma_db"
client = chromadb.PersistentClient(path=chroma_dir)

# using the same embedding model that was used during saving
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# load the collection from the client
db_movies = Chroma(
    client=client, 
    embedding_function=embedding_model
)

# load the movies DataFrame
movies = pd.read_csv("movies_with_emotions.csv").merge(
    pd.read_csv("posters.csv"), on="id"
)

movies["large_thumbnail"] = movies["link"] + "&fife=w800"
movies["large_thumbnail"] = movies["large_thumbnail"].fillna("cover-not-found.jpg")
# load the movies dataframe
# posters = pd.read_csv(r'C:\Users\Owner\Desktop\class files\CS 6320\movies-recommender\NLP-Movies-Recommender\posters.csv')
# movies_with_emotions = pd.read_csv(r'C:\Users\Owner\Desktop\class files\CS 6320\movies-recommender\NLP-Movies-Recommender\movies_with_emotions.csv')
# movies = pd.merge(movies_with_emotions, posters, on="id")

# sentiment analysis logic for recommendations
def retrieve_semantic_recommendations(query, category="All", tone="All", initial_top_k=50, final_top_k=9):
    recs = db_movies.similarity_search(query, k=initial_top_k)
    movies_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
    movies_recs = movies[movies["id"].isin(movies_list)].head(initial_top_k)

    if category != "All":
        movies_recs = movies_recs[movies_recs["genre"].str.contains(category, na=False)].head(final_top_k)
    else:
        movies_recs = movies_recs.head(final_top_k)

    tone_map = {
        "Happy": "joy",
        "Surprising": "surprise",
        "Angry": "anger",
        "Suspenseful": "fear",
        "Sad": "sadness",
    }
    if tone in tone_map:
        movies_recs = movies_recs.sort_values(by=tone_map[tone], ascending=False)

    movies_recs = movies_recs.fillna({'tagline': 'No tagline available'})  # some taglines in the df are Nan, needs placeholder text

    return movies_recs.to_dict(orient="records")
