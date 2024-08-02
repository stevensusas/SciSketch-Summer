import requests

def get_article_by_doi(doi, api_key):
    url = f"https://api.elsevier.com/content/object/doi/10.1016/j.cell.2024.05.022/ref/fx1/high?apiKey=7f59af901d2d86f78a1fd60c1bf9426a&httpAccept=*%2F*"
    
    print(f"Requesting URL: {url}")
    
    response = requests.get(url)
    
    print(f"Response Status Code: {response.status_code}")
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 300:
        print("Multiple Choices available. Details:")
        return response.json()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Replace 'your_doi_here' with the actual DOI and 'your_api_key_here' with your Elsevier API key
doi = '10.1016/j.cell.2024.05.013'
api_key = '3bba2ed26462be857a872db83ddb5e98'

article_data = get_article_by_doi(doi, api_key)
print(article_data)
