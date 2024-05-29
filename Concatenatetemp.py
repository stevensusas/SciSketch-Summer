import multiprocessing
import dask
from dask import delayed, compute
from dask.distributed import Client, LocalCluster
import pandas as pd
import ArticlePageScraping
from tqdm import tqdm

def process_link(link):
    # Use your function to get the summary and link
    result = ArticlePageScraping.getSummaryandLink(link)
    return result

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Initialize a Dask client
    client = Client()

    # Load only the first 5 rows of the CSV into a DataFrame
    df_first_5_rows = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/abstracts_data.csv', nrows=5)
    
    # Create delayed computations for each link in the first 5 rows
    delayed_computations = [delayed(process_link)(link) for link in df_first_5_rows['Link']]

    try:
        # Compute the delayed computations in parallel
        results = compute(*delayed_computations)

        # Create a new column in the DataFrame with the results
        df_first_5_rows['Link_to_img'] = results
    except Exception as e:
        print(f"Error occurred: {e}")
        # Save the processed DataFrame back to a separate CSV file
        df_first_5_rows.to_csv('abstracts_data_first_5_rows.csv', index=False)
        client.close()
        raise e

    # Save the processed DataFrame back to a separate CSV file
    df_first_5_rows.to_csv('abstracts_data_first_5_rows.csv', index=False)

    # Close the Dask client
    client.close()
