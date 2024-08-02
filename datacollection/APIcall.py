import requests
import pandas as pd

def API_call(doi):
    prefix = "https://api.elsevier.com/content/object/doi/"

    postfix = '/ref/fx1/high?apiKey='

    api_key = 'd81d98cad3552d6739cda469edb54e97'

    end = '&httpAccept=*%2F*'

    url = prefix + doi + postfix + api_key + end

    response = requests.get(url)

    if response.status_code == 200:
        file_name = '/Users/stevensu/Desktop/SciSketch-Summer/Graphical Abstracts/' + doi+'.jpg'
        with open(file_name, 'wb') as file:
            file.write(response.content)
        return file_name
    else:
        return None
    
df = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Summer/Entries.csv')


df['Image'] = df['DOI'].apply(API_call)

