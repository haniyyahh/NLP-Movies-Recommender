import pandas as pd
import numpy as np
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from tqdm import tqdm  # for progress bar

# load and merge datasets
print("Loading datasets...")
posters = pd.read_csv(r'C:\Users\Owner\Desktop\class files\CS 6320\movies-recommender\NLP-Movies-Recommender\posters.csv')
movies_with_emotions = pd.read_csv(r'C:\Users\Owner\Desktop\class files\CS 6320\movies-recommender\NLP-Movies-Recommender\movies_with_emotions.csv')
movies = pd.merge(movies_with_emotions, posters, on="id")

# enhance image quality
print("Enhancing image quality...")
movies["large_thumbnail"] = movies["link"] + "&fife=w800"
movies["large_thumbnail"] = np.where(
    movies["large_thumbnail"].isna(),
    "cover-not-found.jpg",
    movies["large_thumbnail"],
)

# create vector documents using tqdm for progress tracking
print("Creating vector documents...")
documents = []
for _, row in tqdm(movies.iterrows(), total=movies.shape[0], desc="Processing rows"):
    documents.append(Document(page_content=f'{row["id"]} {row["tagged_description"]}'))

# Build vector database with progress tracking
print("Building vector database...")

# Initialize the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# processing in batches do to memory space (will speed up the process)
batch_size = 32
num_batches = len(documents) // batch_size + (1 if len(documents) % batch_size != 0 else 0)

# begin processing: it will run through about 763 times
batch_embeddings = []
for i in tqdm(range(num_batches), desc="Embedding Documents"):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, len(documents))
    
    # create a batch of documents
    batch = documents[start_idx:end_idx]
    
    # generate embeddings for this batch
    batch_embeddings.extend(embedding_model.embed_documents([doc.page_content for doc in batch]))

# create the Chroma vector store with the batched embeddings
db_movies = Chroma.from_documents(documents, embedding=embedding_model)


# Main function for recommendations
def retrieve_semantic_recommendations(query, category="All", tone="All", initial_top_k=50, final_top_k=16):
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

    return movies_recs
