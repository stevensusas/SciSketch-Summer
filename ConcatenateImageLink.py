import multiprocessing
import dask
from dask import delayed, compute
from dask.distributed import Client, LocalCluster
import pandas as pd
from selenium import webdriver
import ArticlePageScraping
from tqdm import tqdm

def process_link(link):
    try:
        # Use your function to get the summary and link
        result = ArticlePageScraping.getSummaryandLink(link)
    except Exception as e:
        print(f"Error processing link {link}: {e}")
        result = None
    return result

if __name__ == '__main__':
    multiprocessing.freeze_support()

    # Initialize a Dask client
    client = Client()

    # Load your data into a Dask DataFrame
    df = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/abstracts_data_missing_2.csv')
    ddf = dask.delayed(pd.DataFrame)(df)

    # Create delayed computations for each link
    delayed_computations = [delayed(process_link)(link) for link in df['Link']]

    try:
        # Compute the delayed computations in parallel
        results = compute(*delayed_computations)

        # Create a new column in the Dask DataFrame with the results
        ddf = ddf.assign(Link_to_img=results)
        df = ddf.compute()
        # Save the processed DataFrame back to a CSV file
        df.to_csv('abstracts_data_missing_2.csv', index=False)
    except Exception as e:
        print(f"Error occurred during computation: {e}")
    finally:
        # Convert the Dask DataFrame back to a Pandas DataFrame
        df = ddf.compute()
        # Save the processed DataFrame back to a CSV file
        df.to_csv('abstracts_data_missing_2.csv', index=False)
        client.close()
