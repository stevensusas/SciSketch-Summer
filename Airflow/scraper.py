import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class ScienceDirectAPI:
    def __init__(self, base_url='https://api.elsevier.com/content/search/sciencedirect'):
        self.base_url = base_url
        self.api_key ='7f59af901d2d86f78a1fd60c1bf9426a'
        self.headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': self.api_key,
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        
        self.journals = [
        "Cell",
        "Cancer Cell",
        "Cell Chemical Biology",
        "Cell Genomics",
        "Cell Host & Microbe",
        "Cell Metabolism",
        "Cell Reports",
        "Cell Reports Medicine",
        "Cell Stem Cell",
        "Cell Systems",
        "Current Biology",
        "Developmental Cell",
        "Immunity",
        "Med",
        "Molecular Cell",
        "Neuron",
        "Structure",
        "American Journal of Human Genetics",
        "Biophysical Journal",
        "Biophysical Reports",
        "Human Genetics and Genomics Advances",
        "Molecular Plant",
        "Molecular Therapy",
        "Molecular Therapy Methods & Clinical Development",
        "Molecular Therapy Nucleic Acids",
        "Molecular Therapy Oncology",
        "Plant Communications",
        "Stem Cell Reports",
        "Trends in Biochemical Sciences",
        "Trends in Cancer",
        "Trends in Cell Biology",
        "Trends in Ecology & Evolution",
        "Trends in Endocrinology & Metabolism",
        "Trends in Genetics",
        "Trends in Immunology",
        "Trends in Microbiology",
        "Trends in Molecular Medicine",
        "Trends in Neurosciences",
        "Trends in Parasitology",
        "Trends in Pharmacological Sciences",
        "Trends in Plant Science",
        "Cell Reports Physical Science",
        "Chem",
        "Chem Catalysis",
        "Device",
        "Joule",
        "Matter",
        "Newton",
        "Trends in Chemistry",
        "Cell Reports Methods",
        "Cell Reports Sustainability",
        "Heliyon",
        "iScience",
        "One Earth",
        "Patterns",
        "STAR Protocols",
        "Nexus",
        "The Innovation",
        "Trends in Biotechnology",
        "Trends in Cognitive Sciences"
    ]

    def get_results(self, query):
        response = self.session.put(self.base_url, headers=self.headers, json=query)
        response.raise_for_status()
        return response.json()

    def retrieve_all_results(self, query, max_workers=11):
        all_results = []
        total_results = None

        def fetch_batch(offset):
            query_copy = query.copy()
            query_copy['display']['offset'] = offset
            while True:
                try:
                    return self.get_results(query_copy)
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        print(f"Rate limit hit. Waiting for 60 seconds before retrying...")
                        time.sleep(60)
                    elif e.response.status_code == 400:
                        print(f"Reached the end of available results at offset {offset}.")
                        return None
                    else:
                        raise

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_offset = {}
            offset = 0
            page = 1

            while True:
                future = executor.submit(fetch_batch, offset)
                future_to_offset[future] = offset

                for completed_future in as_completed(future_to_offset):
                    data = completed_future.result()
                    current_offset = future_to_offset[completed_future]
                    
                    if data is None:
                        print(f"No more results available after offset {current_offset}.")
                        break

                    if 'resultsFound' not in data or 'results' not in data:
                        print(f"Unexpected API response structure. Full response: {data}")
                        return pd.DataFrame()

                    if total_results is None:
                        total_results = int(data['resultsFound'])

                    results = data['results']
                    if not results:
                        print(f"No more results available after offset {current_offset}.")
                        break

                    all_results.extend(results)

                    print(f"Page {page} completed (offset {current_offset}). Total results so far: {len(all_results)}/{total_results}")
                    page += 1

                    if len(all_results) >= total_results:
                        break

                if len(all_results) >= total_results or data is None or not results:
                    break

                offset += query['display']['show']
                time.sleep(1)  # Add a small delay between requests

        print(f"All available results retrieved. Total results: {len(all_results)}")

        df = pd.DataFrame(all_results)
        
        if 'authors' in df.columns:
            df['authors'] = df['authors'].apply(lambda x: ', '.join([author['name'] for author in x]) if isinstance(x, list) else x)
        
        if 'pages' in df.columns:
            df['pages'] = df['pages'].apply(lambda x: x.get('first', '') if isinstance(x, dict) else x)

        return df

    def scrape_all(self, max_workers=11):
        all_dfs = []
        for journal in self.journals:
            print(f"Starting data retrieval for {journal}...")
            query = {
                "qs": "a OR b OR c OR d OR e OR f OR g OR h OR i OR j OR k OR l OR m OR n OR o OR p OR q OR r OR s OR t OR u OR v OR w OR x OR y OR z",
                "pub": f'"{journal}"',
                "filters": {
                    "openAccess": False,
                },
                "display": {
                    "offset": 0,
                    "show": 100,
                    "sortBy": "date"
                }
            }
            df = self.retrieve_all_results(query)
            all_dfs.append(df)

        # Concatenate all dataframes into a single dataframe
        final_df = pd.concat(all_dfs, ignore_index=True)

        # Filter rows to keep only those with exact matches in sourceTitle
        final_df = final_df[final_df['sourceTitle'].isin(self.journals)]

        # Apply the DOI API calls in a multithreaded way
        final_df = self.apply_doi_api_multithreaded(final_df, max_workers=max_workers)

        return final_df

    def apply_doi_api_multithreaded(self, df, max_workers=11):
        def API_call(doi):
            prefix = "https://api.elsevier.com/content/object/doi/"
            postfix = '/ref/fx1/high?apiKey='
            end = '&httpAccept=*%2F*'
            url = prefix + doi + postfix + self.api_key + end

            response = requests.get(url)

            if response.status_code == 200:
                file_name = f'/Users/stevensu/Desktop/SciSketch-Summer/Graphical Abstracts/{doi}.jpg'
                with open(file_name, 'wb') as file:
                    file.write(response.content)
                return True  # Graphical Abstract found
            else:
                return False  # Graphical Abstract not found

        def process_row(row):
            doi = row['doi']
            row['GraphicalAbstract'] = API_call(doi)
            return row

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(process_row, row) for _, row in df.iterrows()]
            for future in as_completed(futures):
                row = future.result()
                df.loc[df['doi'] == row['doi'], 'GraphicalAbstract'] = row['GraphicalAbstract']

        return df

# Example usage:
if __name__ == "__main__":
    sd_api = ScienceDirectAPI()
    df = sd_api.scrape_all()
    
    # Count the number of rows where 'GraphicalAbstract' is True
    count_true = df['GraphicalAbstract'].sum()

    # Print the count
    print(f"Number of rows with 'GraphicalAbstract' = True: {count_true}")
