# Google Cloud Storage Operations Module
# This module provides functions for:
# - List all buckets
# - List all files in a bucket
# - Download a file from a bucket
# - Check bucket existence
# - Get file metadata

import os
import logging
from typing import List, Optional
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud.exceptions import NotFound
from dotenv import load_dotenv

class GCSClient:
    """Google Cloud Storage Client for read operations using service account authentication."""
    
    def __init__(self, log_level: int = logging.INFO):
        """
        Initialize GCS client using service account authentication.
        
        Args:
            log_level: Logging level for this instance (default: logging.INFO)
        """
        # Set up instance logger first (outside try block to ensure it's always available)
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.logger.setLevel(log_level)
        
        # Add handler if none exists
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        try:
            # Load environment variables
            load_dotenv()
            credentials = service_account.Credentials.from_service_account_file(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
            self.client = storage.Client(credentials=credentials)
            self.logger.info(f"GCS client initialized for project: {self.client.project}")
        except Exception as e:
            self.logger.error(f"Failed to initialize GCS client: {e}")
            raise
    
    def create_bucket(self, bucket_name):
        """Creates a bucket.
        Args:
            bucket_name: Name of the bucket to create
        
        Returns:
            bool: True if bucket created successfully, False otherwise
        """
        try:
            self.client.create_bucket(bucket_name)
        except Exception as e:
            self.logger.error(f"Failed to create bucket '{bucket_name}': {e}")
            return False
        return True

    def list_buckets(self) -> List[str]:
        """
        List all buckets in the project.
        
        Returns:
            List[str]: List of bucket names
        """
        try:
            buckets = list(self.client.list_buckets())
            bucket_names = [bucket.name for bucket in buckets]
            self.logger.info(f"Found {len(bucket_names)} buckets")
            return bucket_names
        except Exception as e:
            self.logger.error(f"Failed to list buckets: {e}")
            return []
    
    def bucket_exists(self, bucket_name: str) -> bool:
        """
        Check if a bucket exists.
        
        Args:
            bucket_name: Name of the bucket to check
            
        Returns:
            bool: True if bucket exists, False otherwise
        """
        try:
            bucket = self.client.bucket(bucket_name)
            return bucket.exists()
        except Exception as e:
            # Handle permission errors gracefully
            if "403" in str(e) or "Permission" in str(e):
                self.logger.warning(f"Permission denied checking bucket '{bucket_name}'. Assuming it doesn't exist or no access.")
                return False
            self.logger.error(f"Failed to check if bucket '{bucket_name}' exists: {e}")
            return False
    
    def list_files(self, bucket_name: str, prefix: str = "") -> List[str]:
        """
        List all files in a bucket.
        
        Args:
            bucket_name: Name of the bucket to list files from
            prefix: Optional prefix to filter files
            
        Returns:
            List[str]: List of file names in the bucket
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blobs = bucket.list_blobs(prefix=prefix)
            file_names = [blob.name for blob in blobs]
            self.logger.info(f"Found {len(file_names)} files in bucket '{bucket_name}'")
            return file_names
        except Exception as e:
            self.logger.error(f"Failed to list files in bucket '{bucket_name}': {e}")
            return []
    
    def upload_file(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket.
        Args:
            bucket_name: Name of the bucket to upload to
            source_file_name: Name of the file to upload
            destination_blob_name: Name of the file in the bucket
        
        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)

            print(f"File {source_file_name} uploaded to {destination_blob_name}.")
        except Exception as e:
            self.logger.error(f"Failed to upload file '{source_file_name}': {e}")
            return False
        return True
    
    def download_file(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket.
        Args:
            bucket_name: Name of the bucket to download from
            source_blob_name: Name of the file to download
            destination_file_name: Name of the file to download to
        
        Returns:
            bool: True if download successful, False otherwise
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)

            print(
                "Downloaded storage object {} from bucket {} to local file {}.".format(
                    source_blob_name, bucket_name, destination_file_name
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to download file '{source_blob_name}': {e}")
            return False
        return True
        
    
    def get_file_metadata(self, bucket_name: str, blob_name: str) -> Optional[dict]:
        """
        Get metadata for a file in a bucket.
        
        Args:
            bucket_name: Name of the bucket containing the file
            blob_name: Name of the file
            
        Returns:
            dict: File metadata or None if file not found
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.reload()
            
            metadata = {
                'name': blob.name,
                'size': blob.size,
                'content_type': blob.content_type,
                'created': blob.time_created,
                'updated': blob.updated,
                'md5_hash': blob.md5_hash
            }
            
            return metadata
        except NotFound:
            self.logger.warning(f"File '{blob_name}' not found in bucket '{bucket_name}'")
            return None
        except Exception as e:
            self.logger.error(f"Failed to get metadata for file '{blob_name}': {e}")
            return None
    
    def delete_file(self, bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
        except Exception as e:
            self.logger.error(f"Failed to delete blob '{blob_name}': {e}")
            return False
        return True

    def delete_bucket(self, bucket_name):
        """Deletes a bucket. The bucket must be empty."""
        try:
            self.client.delete_bucket(bucket_name)
        except Exception as e:
            self.logger.error(f"Failed to delete bucket '{bucket_name}': {e}")
            return False
        return True

        