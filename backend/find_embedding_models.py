# find_embedding_models.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('NVIDIA_API_KEY')

def find_embedding_models():
    url = "https://integrate.api.nvidia.com/v1/models"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    models = response.json()['data']
    
    print("Looking for embedding models...")
    embedding_models = []
    
    for model in models:
        model_id = model['id'].lower()
        if 'embed' in model_id or 'bge' in model_id or 'e5' in model_id:
            embedding_models.append(model['id'])
            print(f" Found: {model['id']}")
    
    if not embedding_models:
        print(" No specific embedding models found.")
        print("We'll use a general model for embeddings.")
    
    return embedding_models

if __name__ == "__main__":
    find_embedding_models()