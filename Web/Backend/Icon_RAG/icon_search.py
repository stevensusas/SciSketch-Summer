import clip
import torch
from PIL import Image
import numpy as np
import os
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import cairosvg
from io import BytesIO
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category = FutureWarning)

# Load the CLIP pre-trained model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# SentenceTransformer model for text embedding
text_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Extract features from an image using CLIP
def extract_image_features(image_path):
    # Handle SVG files
    if image_path.lower().endswith('.svg'):
        with open(image_path, 'rb') as svg_file:
            svg_data = svg_file.read()
        png_data = cairosvg.svg2png(bytestring=svg_data)
        image = Image.open(BytesIO(png_data))
    else:
        image = Image.open(image_path)
    image = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        features = model.encode_image(image).cpu().numpy()
    return features

# Extract text embedding using SentenceTransformer
def extract_text_embedding(text):
    return text_model.encode(text)

# Initialize ChromaDB client with PersistentClient
client = chromadb.PersistentClient(path="./db")

# Attempt to create the collection, or get it if it already exists
try:
    collection = client.create_collection(name="icon_collection")
except Exception as e:
    if 'already exists' in str(e):
        collection = client.get_collection(name="icon_collection")
    else:
        raise e

# Function to process files and add to the database
def process_and_add_files(icon_directory):
    # Extract features and store them in lists
    icon_paths = []
    image_features = []
    filename_embeddings = []

    # Retrieve the set of processed files
    processed_files = set()
    # Fetch all ids in the collection to know which files have been processed
    collection_data = collection.get(include=["metadatas"])
    if collection_data and "ids" in collection_data:
        for id in collection_data["ids"]:
            processed_files.add(id)

    # Traverse the directory and its subdirectories
    for root, dirs, files in os.walk(icon_directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')):
                image_path = os.path.join(root, filename)
                if image_path in processed_files:
                    print(f"Skipping already processed file: {image_path}")
                    continue
                try:
                    # Extract image features using CLIP
                    features = extract_image_features(image_path)
                    
                    # Convert filename to embeddings
                    filename_embedding = extract_text_embedding(filename)
                    
                    icon_paths.append(image_path)
                    image_features.append(features)
                    filename_embeddings.append(filename_embedding)
                    print(f"Processed {image_path}")
                except Exception as e:
                    print(f"Failed to process {image_path}: {e}")

    # Check if lists are not empty before concatenation
    if image_features and filename_embeddings:
        # Convert lists to numpy arrays
        image_features_np = np.vstack(image_features)
        filename_embeddings_np = np.vstack(filename_embeddings)

        # Combine all features into one array
        combined_features = np.hstack((image_features_np, filename_embeddings_np))

        # Add embeddings to the collection
        collection.add(
            ids=icon_paths,  # IDs
            embeddings=combined_features.tolist(),  # Embeddings
            metadatas=[{"path": path} for path in icon_paths]  # Metadata
        )

        print("All embeddings have been stored in the vector database.")
    else:
        print("Error: No features extracted. Please check the icon directory and the extraction functions.")

# Function to search for similar icons based on a text query using the combined embeddings, return top k
def search_similar_icons_by_text(query, k):
    # Check if there are embeddings in the collection
    collection_data = collection.get(include=["embeddings", "metadatas"])
    if not collection_data or not collection_data.get("ids"):
        print("No embeddings found in the collection.")
        return []

    # Fetch an example embedding to determine the image feature dimension
    example_id = collection_data["ids"][0]
    example_embedding_data = collection.get(ids=[example_id], include=["embeddings"])
    if not example_embedding_data or not example_embedding_data.get("embeddings"):
        print("No embeddings found for the example ID.")
        return []

    example_embedding = example_embedding_data["embeddings"][0]
    total_feature_dim = len(example_embedding)
    text_embedding_dim = len(extract_text_embedding("example").tolist())
    image_feature_dim = total_feature_dim - text_embedding_dim

    query_embedding = extract_text_embedding(query).tolist()
    
    # Create dummy image embedding (zeros) to align with the dimensions
    dummy_image_embedding = np.zeros(image_feature_dim).tolist()
    
    # Combine dummy image embedding with query embedding
    query_combined_embedding = dummy_image_embedding + query_embedding
    
    results = collection.query(
        query_embeddings=[query_combined_embedding],  # Query embeddings
        n_results=k,
        include=["metadatas", "distances"]
    )
    
    return results


import os
import requests

# Function to generate the absolute URL for an icon in Google Cloud Storage
def generate_gcs_url(bucket_name, icon_path):
    return f"https://storage.googleapis.com/{bucket_name}/{icon_path}"

# Function to check if a URL is accessible
def check_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return False

if __name__ == "__main__":
    # The name of your Google Cloud Storage bucket
    bucket_name = "scisketch_icon_search"

    # Directory in the bucket where icons are stored
    icon_directory = "icons"

    # Perform a search (this is a placeholder, replace with actual search function)
    query = "elder woman"
    similar_icons = search_similar_icons_by_text(query, 5)  # Replace with actual search function
    
    if similar_icons and "ids" in similar_icons:
        for idx, metadata in zip(similar_icons['ids'][0], similar_icons['metadatas'][0]):
            icon_path = metadata['path']
            absolute_url = generate_gcs_url(bucket_name, os.path.join(icon_directory, os.path.basename(icon_path)))
            distance = similar_icons['distances'][0][similar_icons['ids'][0].index(idx)]
            if check_url(absolute_url):
                print(f"Valid URL: {absolute_url}, Distance: {distance}")
            else:
                print(f"Invalid URL: {absolute_url}, Distance: {distance}")
    else:
        print("No results found in the search query.")


# # Example usage
# if __name__ == "__main__":
#     icon_directory = "all_icon"

#     # Uncomment the following line to process files and add them to the database
#     # process_and_add_files(icon_directory)

#     # Perform a search
#     query = "elder woman"
#     similar_icons = search_similar_icons_by_text(query, 5)
#     if similar_icons and "ids" in similar_icons:
#         for idx, metadata in zip(similar_icons['ids'][0], similar_icons['metadatas'][0]):
#             print(f"Image Path: {metadata['path']}, Distance: {similar_icons['distances'][0][similar_icons['ids'][0].index(idx)]}")
#     else:
#         print("No results found in the search query.")
