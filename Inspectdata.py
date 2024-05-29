import os
import requests
from PIL import Image
from io import BytesIO
import pandas as pd
from dask import delayed, compute
from dask.distributed import Client

def save_image_from_url(url):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        
        # Open the image from the response content
        image = Image.open(BytesIO(response.content))
        
        # Ensure the directory exists
        directory = "Training Data/Images"
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Generate a unique file name
        file_name = os.path.join(directory, os.path.basename(url))
        
        # Save the image to the specified file path
        image.save(file_name)
        
        print(f"Image saved at {file_name}.")
        
        return file_name
    except Exception as e:
        print(f"Failed to save image from {url}: {e}")
        return None

if __name__ == '__main__':
    # Load your DataFrame
    df = pd.read_csv('/Users/stevensu/Desktop/SciSketch-Newest/round12345678.csv')

    # Initialize a Dask client
    client = Client()

    # Create delayed tasks for each image download
    delayed_tasks = [delayed(save_image_from_url)(url) for url in df['Link_to_img']]

    # Compute the delayed tasks in parallel
    results = compute(*delayed_tasks)

    # Add the results to the DataFrame
    df['saved_image_path'] = results

    # Save the updated DataFrame to a CSV file
    df.to_csv('round12345678_with_images.csv', index=False)

    print("Updated DataFrame saved to 'round1_with_images.csv'")

    # Close the Dask client
    client.close()
