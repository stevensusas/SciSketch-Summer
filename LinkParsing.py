import pandas as pd
import re
import os

data = []

folder_path = 'Training Data/Article Links/'

for file_name in os.listdir(folder_path):
    if file_name.endswith('.txt'):
        with open(os.path.join(folder_path, file_name), 'r') as file:
            content = file.read()
            link_matches = re.findall(r'https://www\.sciencedirect\.com/science/article/pii/[A-Za-z0-9]{17}', content)
            abstract_matches = re.finditer(r'Abstract(?:\s*:\s*\w+\s*)?\n(.*?)\n\n', content, re.DOTALL)
            for link_match, abstract_match in zip(link_matches, abstract_matches):
                link = link_match
                abstract = abstract_match.group(1)
                data.append({'Link': link, 'Abstract': abstract})

df = pd.DataFrame(data)
df.to_csv('abstracts_data.csv', index=False)
