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

# Define and create the collection if it doesn't exist
try:
    collection_name = "tech_news"
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # Adjust size according to your model's output
    )
except Exception as e:
    print(e)
try:
    # Load data from the JSON file
    with open('categorized_data.json', 'r') as file:
        articles = json.load(file)

    # Load the model for vectorization
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Upload each article as a point
    for article in articles:
        # Generate a unique identifier for each article
        point_id = str(uuid.uuid4())
        vector = model.encode(article['Details']).tolist()  # Vectorize the 'Details' for search
        payload = {
            "title": article['Title'],
            "details": article['Details'],
            "type": article['Type'],
            "url": article['URL'],
            "source": article['Source'],
            "category": article['Category']
        }
        client.upsert(
            collection_name=collection_name,
            points=[{
                "id": point_id,
                "vector": vector,
                "payload": payload
            }]
        )
except Exception as e:
    print(e)