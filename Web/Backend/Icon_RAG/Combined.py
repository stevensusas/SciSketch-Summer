from huggingface_hub import HfApi
import requests
import icon_search

import os
from io import BytesIO
import warnings

# Ensure you are logged in using the CLI before running this script
# huggingface-cli login

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

repo_name = "FlanT5PhraseGeneration"  # Change this to your desired repository name
api = HfApi()
username = "stevensu123"  # This is the username of the person who owns the repository
repo_id = f"{username}/{repo_name}"

# Set your Hugging Face API token here
API_TOKEN = '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'  # Replace with your Hugging Face API token
API_URL = f"https://api-inference.huggingface.co/models/{repo_id}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)  # Print the status code to debug
    if response.status_code != 200:
        print("Error:", response.text)  # Print error message if not successful
    return response.json()

def call_flask_inference(input_data):
    url = 'http://127.0.0.1:5000/inference'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=input_data)
    
    if response.status_code == 200:
        print("Success:")
        print(response.json())
    else:
        print(f"Failed with status code: {response.status_code}")
        print(response.json())

# Example input for your Flan-T5 model
data = {
    "inputs": "generate key phrases: Neutrosophic sets provide greater versatility in dealing with a variety of uncertainties, including independent, partially independent, and entirely dependent scenarios, which q-ROF soft sets cannot handle. Indeterminacy, on the other hand, is ignored completely or partially by q-ROF soft sets. To address this issue, this study offers a unique novel concept as known as q-RONSS, which combines neutrosophic set with q-ROF soft set. This technique addresses vagueness using a set of truth, indeterminacy, and false membership degrees associated with the parametrization tool, with the condition that the sum of the qth power of the truth, indeterminacy, and false membership degrees be less than or equal to one. In addition, this study outlines operational laws for the suggested structure. The main purpose this article is to define some averaging and geometric operators based on the q-rung orthopair neutrosophic soft set. Furthermore, this article provides a step-by-step method and a mathematical model for the suggested techniques. To solve a MADM issue, this research article proposes a numerical example of people selection for a specific position in a real estate business based on a variety of criteria. Finally, to demonstrate the proposed model's superiority and authenticity, this article performs several analyses, including sensitivity analysis, to address the reliability and influence of various parameter 'q' values on the alternatives and the ultimate ranking outcomes using the averaging and geometric operators. A comparison of the proposed operators to current operators demonstrates the validity of the proposed structure. Furthermore, a comparison of the proposed structure to current theories demonstrates its superiority by overcoming their limits and offering a more flexible and adaptable framework. Finally, this study reviews the findings and consequences of our research."
}

print("Sending request to Hugging Face Inference API...")
result = query(data)
print("Result:", result)


generated_text = result[0]['generated_text']
items = [item.strip() for item in generated_text.split(',')]
# Result: [{'generated_text': 'q-RONSS, q-ROF soft set, q-RONSS'}]


# The name of your Google Cloud Storage bucket
bucket_name = "scisketch_icon_search"

# Directory in the bucket where icons are stored
icon_directory = "icons"

#icon search
query = ""

for phrase in items:
    query = phrase
    similar_icons = icon_search.search_similar_icons_by_text(query, 1)
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
call_flask_inference(data)