from huggingface_hub import HfApi

#Before running this script for inference, please first run 'huggingface-cli login' in terminal.
#Go to HuggingFace and generate an API token, input upon request in cli. Replace 'your API token here' with your actual API token.

repo_name = "FlanT5PhraseGeneration"  # Change this to your desired repository name
api = HfApi()
username = api.whoami()["name"]
repo_id = f"{username}/{repo_name}"

# Step 6: Use the Hugging Face Inference API
import requests

API_TOKEN = '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'  # Replace with your Hugging Face API token
API_URL = f"https://api-inference.huggingface.co/models/{repo_id}"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)  # Print the status code to debug
    if response.status_code != 200:
        print("Error:", response.text)  # Print error message if not successful
    return response.json()

# Example input for your Flan-T5 model
data = {
    "inputs": "generate key phrases: Neutrosophic sets provide greater versatility in dealing with a variety of uncertainties, including independent, partially independent, and entirely dependent scenarios, which q-ROF soft sets cannot handle. Indeterminacy, on the other hand, is ignored completely or partially by q-ROF soft sets. To address this issue, this study offers a unique novel concept as known as q-RONSS, which combines neutrosophic set with q-ROF soft set. This technique addresses vagueness using a set of truth, indeterminacy, and false membership degrees associated with the parametrization tool, with the condition that the sum of the qth power of the truth, indeterminacy, and false membership degrees be less than or equal to one. In addition, this study outlines operational laws for the suggested structure. The main purpose this article is to define some averaging and geometric operators based on the q-rung orthopair neutrosophic soft set. Furthermore, this article provides a step-by-step method and a mathematical model for the suggested techniques. To solve a MADM issue, this research article proposes a numerical example of people selection for a specific position in a real estate business based on a variety of criteria. Finally, to demonstrate the proposed model's superiority and authenticity, this article performs several analyses, including sensitivity analysis, to address the reliability and influence of various parameter 'q' values on the alternatives and the ultimate ranking outcomes using the averaging and geometric operators. A comparison of the proposed operators to current operators demonstrates the validity of the proposed structure. Furthermore, a comparison of the proposed structure to current theories demonstrates its superiority by overcoming their limits and offering a more flexible and adaptable framework. Finally, this study reviews the findings and consequences of our research."
}

print("Sending request to Hugging Face Inference API...")
result = query(data)
print("Result:", result)

