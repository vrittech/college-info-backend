import os
import boto3
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Retrieve credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")

# ✅ Debugging: Print variables to check if they are loaded
print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)
print("AWS_S3_ENDPOINT_URL:", AWS_S3_ENDPOINT_URL)
print("AWS_STORAGE_BUCKET_NAME:", AWS_STORAGE_BUCKET_NAME)

# ✅ Ensure credentials exist
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY:
    raise Exception("❌ AWS credentials are missing. Check your .env file!")

# ✅ Initialize Boto3 S3 Client with R2 Credentials
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=AWS_S3_ENDPOINT_URL
)

# ✅ Test Connection by Listing Buckets
try:
    response = s3_client.list_buckets()
    print("✅ Connection successful! Buckets:", response)
except Exception as e:
    print(f"❌ Error: {e}")
