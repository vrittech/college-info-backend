from django.core.files.storage import Storage
import boto3
from botocore.exceptions import ClientError
from django.conf import settings


class R2Storage(Storage):
    """Custom Django Storage Backend for Cloudflare R2"""

    def __init__(self, *args, **kwargs):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            endpoint_url=settings.R2_ENDPOINT_URL
        )
        self.bucket_name = settings.R2_BUCKET_NAME
        super().__init__(*args, **kwargs)

    def _open(self, name, mode="rb"):
        """Retrieve file from R2"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=name)
            return response["Body"]
        except ClientError as e:
            raise IOError(f"Error retrieving file: {e}")

    def _save(self, name, content):
        """Upload file to R2"""
        try:
            self.s3_client.upload_fileobj(content, self.bucket_name, name)
            return name
        except ClientError as e:
            raise IOError(f"Error saving file: {e}")

    def exists(self, name):
        """Check if file exists in R2"""
        try:
            self.s3_client.head_object(Bucket=self.bucket_name, Key=name)
            return True
        except ClientError:
            return False

    def url(self, name):
        """Generate a presigned URL for accessing the file"""
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket_name, "Key": name},
            ExpiresIn=3600,  # 1 hour
        )
