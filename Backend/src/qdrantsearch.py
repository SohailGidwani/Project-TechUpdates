import json
import uuid
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv("app.env"))

# Initialize Qdrant Client
client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
# print(client.get_collection(collection_name="tech_news"))
# # Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to search articles by query
def search_articles(query_text):
    query_vector = model.encode(query_text).tolist()  # Convert query text to vector
    search_results = client.search(
        collection_name="tech_news",
        query_vector=query_vector,
        score_threshold=0.25 # Adjust the number of results as needed
    )
    return search_results
def format_search_results(search_results):
    formatted_results = []
    for result in search_results:
        formatted_result = f"Title: {result.payload['title']}\n" \
                           f"Details: {result.payload['details'][:150]}... (more)\n" \
                           f"Category: {result.payload['category']}\n" \
                           f"Type: {result.payload['type']}\n" \
                           f"Source: {result.payload['source']}\n" \
                           f"URL: {result.payload['url']}\n" \
                           f"Score: {result.score:.4f}\n"
        formatted_results.append(formatted_result)
    return "\n".join(formatted_results)
# Example search
query_text = "What is the latest in AI technology?"
results = search_articles(query_text)
formatted_results = format_search_results(results)
print(formatted_results)
print("Search Results:", results)
