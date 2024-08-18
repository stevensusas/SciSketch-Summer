import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class ScienceDirectAPI:
    def __init__(self, api_key, base_url='https://api.elsevier.com/content/search/sciencedirect'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Accept': 'application/json',
            'X-ELS-APIKey': self.api_key,
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def get_results(self, query):
        response = self.session.put(self.base_url, headers=self.headers, json=query)
        response.raise_for_status()
        return response.json()

    def retrieve_all_results(self, query, max_workers=5):
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

    def save_to_csv(self, df, filename='science_direct_results.csv'):
        df.to_csv(filename, index=False)
        print(f"Results saved to {filename}")

# Example usage
if __name__ == "__main__":
    API_KEY = '7f59af901d2d86f78a1fd60c1bf9426a'
    sd_api = ScienceDirectAPI(API_KEY)

    query = {
        "qs": "a OR b OR c OR d OR e OR f OR g OR h OR i OR j OR k OR l OR m OR n OR o OR p OR q OR r OR s OR t OR u OR v OR w OR x OR y OR z",
        "pub": "\"Cell\"",
        "filters": {
            "openAccess": False,
        },
        "display": {
            "offset": 0,
            "show": 100,
            "sortBy": "date"
        }
    }

    print("Starting data retrieval...")
    start_time = time.time()
    df = sd_api.retrieve_all_results(query)
    end_time = time.time()

    print(f"Data retrieval completed. Time taken: {end_time - start_time:.2f} seconds")

    print(f"\nDataFrame Summary:")
    print(f"Total rows: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}")
    print("\nFirst few rows:")
    print(df.head())

    sd_api.save_to_csv(df)