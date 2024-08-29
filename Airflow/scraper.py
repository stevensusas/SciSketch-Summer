import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from tqdm import tqdm
import os
from MySQLDatabase import MySQLConnector
from datetime import date

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScienceDirectAPI:
    def __init__(self, base_url='https://api.elsevier.com/content/search/sciencedirect'):
        self.base_url = base_url
        self.api_key = 'd81d98cad3552d6739cda469edb54e97'
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
        self.db = MySQLConnector()
        self.date = '2024-08-27'

    def get_results(self, query):
        response = self.session.put(self.base_url, headers=self.headers, json=query)
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After', 60)
            logging.warning(f"Rate limit hit. Retrying after {retry_after} seconds...")
            time.sleep(int(retry_after))
            response = self.session.put(self.base_url, headers=self.headers, json=query)
        response.raise_for_status()
        return response.json()

    def retrieve_all_results(self, query):
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
                        logging.warning("Rate limit hit. Waiting for 60 seconds before retrying...")
                        time.sleep(60)
                    elif e.response.status_code == 400:
                        logging.info(f"Reached the end of available results at offset {offset}.")
                        return None
                    else:
                        logging.error(f"HTTP error occurred: {e}")
                        raise

        num_cpus = os.cpu_count() or 1
        max_workers = min(num_cpus * 2, 20)
        logging.info(f"Using {max_workers} workers based on CPU count of {num_cpus}.")

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
                        logging.info(f"No more results available after offset {current_offset}.")
                        break

                    if 'resultsFound' not in data or 'results' not in data:
                        logging.error(f"Unexpected API response structure. Full response: {data}")
                        return pd.DataFrame()

                    if total_results is None:
                        total_results = int(data['resultsFound'])

                    results = data['results']
                    if not results:
                        logging.info(f"No more results available after offset {current_offset}.")
                        break

                    all_results.extend(results)

                    logging.info(f"Page {page} completed (offset {current_offset}). Total results so far: {len(all_results)}/{total_results}")
                    page += 1

                    if len(all_results) >= total_results:
                        break

                if len(all_results) >= total_results or data is None or not results:
                    break

                offset += query['display']['show']
                time.sleep(1)

        logging.info(f"All available results retrieved. Total results: {len(all_results)}")

        df = pd.DataFrame(all_results)

        if 'authors' in df.columns:
            df['authors'] = df['authors'].apply(lambda x: ', '.join([author['name'] for author in x]) if isinstance(x, list) else x)

        if 'pages' in df.columns:
            df['pages'] = df['pages'].apply(lambda x: x.get('first', '') if isinstance(x, dict) else x)

        return df

    def scrape_all(self):
        for journal in self.journals:
            table_name = f"{journal.replace(' ', '_')}_{self.date.replace('-', '_')}"
            
            # Check if the table already exists
            if self.db.table_exists(table_name):
                logging.info(f"Table {table_name} already exists. Skipping scraping for {journal}.")
                continue
            
            logging.info(f"Starting data retrieval for {journal}...")
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
            df = df[df['sourceTitle'] == journal]  # Ensure we only have results for this journal
            self.db.upload_dataframe(df, table_name)
            logging.info(f"Uploaded data for {journal} to table {table_name}")

    def get_graphical_abstract(self):
        tables = self.db.list_tables()
        today_tables = [table for table in tables if self.date.replace('-', '_') in table]

        for table in today_tables:
            logging.info(f"Processing graphical abstracts for table: {table}")
            df = self.db.fetch_table(table)

            def API_call(doi):
                prefix = "https://api.elsevier.com/content/object/doi/"
                postfix = '/ref/fx1/high?apiKey='
                end = '&httpAccept=*%2F*'
                url = prefix + doi + postfix + self.api_key + end
                backoff_time = 5

                while True:
                    try:
                        response = self.session.get(url)
                        if response.status_code == 200:
                            return (doi, True)  # Graphical Abstract found
                        elif response.status_code == 429:
                            retry_after = response.headers.get('Retry-After', backoff_time)
                            logging.warning(f"Rate limit hit. Backing off for {retry_after} seconds...")
                            time.sleep(int(retry_after))  # Use Retry-After header if available
                            backoff_time = min(backoff_time * 2, 3600)  # Exponential backoff with max cap of 1 hour
                        else:
                            return (doi, False)  # Graphical Abstract not found
                    except requests.exceptions.RequestException as e:
                        logging.error(f"Failed to fetch graphical abstract for DOI {doi}: {e}")
                        return (doi, False)  # Mark as failed

            max_workers = 10  # Set maximum number of workers to 10
            logging.info(f"Using {max_workers} workers for processing.")

            results = {}
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_doi = {executor.submit(API_call, row['doi']): row['doi'] for _, row in df.iterrows()}

                with tqdm(total=len(df), desc=f"Processing DOIs for {table}", unit="doi") as pbar:
                    for future in as_completed(future_to_doi):
                        doi, result = future.result()
                        results[doi] = result
                        pbar.update(1)

            df['GraphicalAbstract'] = df['doi'].map(results)
            self.db.upload_dataframe(df, table)
            logging.info(f"Updated table {table} with graphical abstract information")

            # Count and log the number of rows where 'GraphicalAbstract' is True
            count_true = df['GraphicalAbstract'].eq(True).sum()
            logging.info(f"Number of rows with 'GraphicalAbstract' = True in {table}: {count_true}")

        return "Graphical abstract processing completed for all tables."


# Example usage:
if __name__ == "__main__":
    sd_api = ScienceDirectAPI()
    result = sd_api.get_graphical_abstract()
    print(result)