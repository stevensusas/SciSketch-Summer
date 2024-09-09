import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv
import os

load_dotenv()

class S3_uploader:
    def __init__(self):
        # Initialize an S3 client with credentials
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name='us-east-1'  # e.g., 'us-east-1'
        )

    def upload_image_response(self, image_data, object_name):
        """Uploads binary image data from an API response to the S3 bucket in a thread-safe way."""
        try:
            # Upload the binary image data directly to the S3 bucket
            self.s3.put_object(
                Bucket='scisketch-airflow',
                Key=object_name + '.jpg',
                Body=image_data,
                ContentType='image/jpeg'  # Adjust this based on the image type (e.g., image/png)
            )
            print(f"Image uploaded successfully to {'scisketch-airflow'}/{object_name}")
        except NoCredentialsError:
            print("Error: AWS credentials are not available.")