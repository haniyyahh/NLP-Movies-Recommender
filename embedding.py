'''
This file is where the embeddings are stored into a Chroma vector store. 
This file is run before api.py is, to ensure the embedding storage has been made once and modular i.e.
does not need to keep running each time changes occur in api.py during the debugging process.

To speed up the process, the embedding process is done in batches of 32 documents, which allows the entirety of the
computation to be done within 5 minutes. This can be optimized.
'''

import pandas as pd
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from tqdm import tqdm  # for progress bar
import os
from langchain_chroma import Chroma
import chromadb  # using PersistentClient method from ChromaDB

# load and merge datasets (these paths must be updated to fit repository paths)
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

# creating vector documents using tqdm for progress tracking
print("Creating vector documents...")
documents = []
for _, row in tqdm(movies.iterrows(), total=movies.shape[0], desc="Processing rows"):
    documents.append(Document(page_content=f'{row["id"]} {row["tagged_description"]}'))

# intializing the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# processing in batches due to memory space
batch_size = 32
num_batches = len(documents) // batch_size + (1 if len(documents) % batch_size != 0 else 0)


embeddings = []

# computation of embeddings
print("Computing embeddings...")
for i in tqdm(range(num_batches), desc="Embedding Documents"):
    start_idx = i * batch_size
    end_idx = min((i + 1) * batch_size, len(documents))
    
    # create a batch within this range of documents
    batch = documents[start_idx:end_idx]
    
    # generate embeddings within this range
    batch_embeddings = embedding_model.embed_documents([doc.page_content for doc in batch])
    embeddings.extend(batch_embeddings)

# using PersistentClient to store the embeddings and vector store
chroma_db_path = "chroma_db"  # Path where Chroma DB will persist
client = chromadb.PersistentClient(path=chroma_db_path)

print("Building Chroma vector store...")
db_movies = Chroma.from_documents(documents, embedding=embedding_model, client=client)

print("Embedding process complete and vector store is saved automatically in the chroma_db directory.")
