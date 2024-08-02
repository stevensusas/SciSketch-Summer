import re
import os
import pandas as pd

# Define the path to your folder
folder_path = '/Users/stevensu/Desktop/SciSketch-Summer/Article Links'

# Initialize an empty list to store the results
all_entries = []

# Define the regex pattern to match abstracts
pattern_abstract = r'Abstract: Summary([\s\S]*?)(?=\n\n|\Z)|Abstract:([\s\S]*?)(?=\n\n|\Z)'

# Define the regex pattern to match DOI URLs
doi_pattern = r'https://doi\.org/[^\s]+'

# Iterate through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the content of each text file
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Find all DOI matches in the content
        doi_matches = re.findall(doi_pattern, content)
        
        # Find all abstract matches in the content
        abstract_matches = re.findall(pattern_abstract, content)
        
        # Combine DOIs and abstracts into pairs and add to the list
        for doi, abstract_tuple in zip(doi_matches, abstract_matches):
            # Extract the abstract text from the tuple
            abstract_text = abstract_tuple[0] if abstract_tuple[0] else abstract_tuple[1]
            all_entries.append({
                'File Name': filename,
                'DOI_urls': doi,
                'Abstract': abstract_text.strip()
            })

# Create a dataframe with the collected entries
df = pd.DataFrame(all_entries)

def process_doi(doi_url, substring='https://doi.org/'):
    """
    Removes the specified substring and the last occurrence of '.' from the DOI URL.
    
    Args:
        doi_url (str): The DOI URL string to be processed.
        substring (str): The substring to be removed from the DOI URL. Default is 'https://doi.org/'.
        
    Returns:
        str: The processed string with the specified substring and the last occurrence of '.' removed.
    """
    # Remove the specified substring
    processed_doi = doi_url.replace(substring, '')
    # Remove the last occurrence of '.'
    last_dot_index = processed_doi.rfind('.')
    if last_dot_index != -1:
        processed_doi = processed_doi[:last_dot_index] + processed_doi[last_dot_index + 1:]
    return processed_doi


df['DOI'] = df['DOI_urls'].apply(process_doi)

df.to_csv('/Users/stevensu/Desktop/SciSketch-Summer/Entries.csv', index=False)