import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os

from langchain.docstore.document import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import gradio as gr

load_dotenv()

# load datasets for posters and cleaned movies
posters = pd.read_csv('posters.csv')
movies_with_emotions = pd.read_csv("movies_with_emotions.csv")

# merge posters to main file
movies = pd.merge(movies_with_emotions, posters, on="id")

# increase the quality of the movie posters
movies["large_thumbnail"] = movies["link"] + "&fife=w800"
movies["large_thumbnail"] = np.where(
    movies["large_thumbnail"].isna(),
    "cover-not-found.jpg",
    movies["large_thumbnail"],
)

# build documents for vector DB using tagged descriptions
documents = [
    Document(page_content=f'{row["id"]} {row["tagged_description"]}')
    for _, row in movies.iterrows()
]

# set up embedding model and Chroma DB from vector-search.ipynb
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_movies = Chroma.from_documents(documents, embedding=embedding_model)


# Recommendation retrieval function
def retrieve_semantic_recommendations(
        query: str,
        category: str = None,
        tone: str = None,
        initial_top_k: int = 50,
        final_top_k: int = 16,
) -> pd.DataFrame:

    recs = db_movies.similarity_search(query, k=initial_top_k)
    movies_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
    movies_recs = movies[movies["id"].isin(movies_list)].head(initial_top_k)

    if category != "All":
        movies_recs = movies_recs[movies_recs["genre"].str.contains(category, na=False)].head(final_top_k)
    else:
        movies_recs = movies_recs.head(final_top_k)

    if tone == "Happy":
        movies_recs = movies_recs.sort_values(by="joy", ascending=False)
    elif tone == "Surprising":
        movies_recs = movies_recs.sort_values(by="surprise", ascending=False)
    elif tone == "Angry":
        movies_recs = movies_recs.sort_values(by="anger", ascending=False)
    elif tone == "Suspenseful":
        movies_recs = movies_recs.sort_values(by="fear", ascending=False)
    elif tone == "Sad":
        movies_recs = movies_recs.sort_values(by="sadness", ascending=False)

    return movies_recs


# Function to format output for Gradio
def recommend_movies(query, category, tone):
    # receive all semantic recommendations for the query
    recommendations = retrieve_semantic_recommendations(query, category, tone)
    results = []

    # get the description and poster for the results, then store
    for _, row in recommendations.iterrows():
        description = row["description"]
        truncated_description = " ".join(description.split()[:30]) + "..."

        caption = f"{row['name']}: {truncated_description}"
        results.append((row["large_thumbnail"], caption))

    return results


# UI category & tone options
all_genres = movies["genre"].dropna().str.split(",").explode().str.strip().unique()
categories = ["All"] + sorted(all_genres)
# categories = ["All"] + sorted(movies["simple_genres"].dropna().unique())
tones = ["All", "Happy", "Surprising", "Angry", "Suspenseful", "Sad"]

# gradio screen UI
with gr.Blocks(theme=gr.themes.Glass()) as dashboard:
    gr.Markdown("# 🎬 Semantic Movie Recommender")

    with gr.Row():
        user_query = gr.Textbox(label="What kind of movie are you in the mood for?",
                                placeholder="e.g., A heartwarming story about friendship")
        category_dropdown = gr.Dropdown(choices=categories, label="Select a genre:", value="All")
        tone_dropdown = gr.Dropdown(choices=tones, label="Select a mood/tone:", value="All")
        submit_button = gr.Button("🎥 Find Recommendations")

    gr.Markdown("## Recommended Movies")
    output = gr.Gallery(label="Results", columns=4, rows=4)

    # call function to pull up list of movies when button is clicked
    submit_button.click(fn=recommend_movies,
                        inputs=[user_query, category_dropdown, tone_dropdown],
                        outputs=output)

# main: running the dashboard
if __name__ == "__main__":
    dashboard.launch(share=True)
