# Integration tests for the Google Cloud Storage Python module.
# Run with: python -m pytest tests/integration_test.py

import unittest
import os
from google_cloud_storage_client import GoogleCloudStorageClient

class TestIntegrations(unittest.TestCase):
    """Integration tests for the Google Cloud Storage Python module."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.gcs = GoogleCloudStorageClient()
        self.test_bucket = f"test-bucket-integration-{os.environ.get('GOOGLE_CLOUD_PROJECT_ID')}"
        self.test_file = "env.example"

    def test_create_bucket(self):
        """Test creating a bucket."""
        create_result = self.gcs.create_bucket(self.test_bucket)
        self.assertTrue(create_result is not None, "create_bucket should return a boolean")

    def test_list_buckets(self):
        """Test listing buckets."""
        buckets = self.gcs.list_buckets()
        self.assertIsInstance(buckets, list)
        self.assertGreater(len(buckets), 0, "No buckets found to test with")

    def test_bucket_exists(self):
        """Test checking if a bucket exists."""
        self.assertTrue(self.gcs.bucket_exists(self.test_bucket))

    def test_upload_file(self):
        """Test uploading a file to a bucket."""
        upload_result = self.gcs.upload_file(self.test_bucket, self.test_file, self.test_file)
        self.assertTrue(upload_result is not None, "upload_file should return a boolean")

    def test_list_files(self):
        """Test listing files in a bucket."""
        files = self.gcs.list_files(self.test_bucket)
        self.assertIsInstance(files, list)
        self.assertGreater(len(files), 0, "No files found to test with")

    def test_download_file(self):
        """Test downloading a file from a bucket."""
        download_result = self.gcs.download_file(self.test_bucket, self.test_file, self.test_file)
        self.assertTrue(download_result is not None, "download_file should return a boolean")

    def test_get_file_metadata(self):
        """Test getting file metadata."""
        metadata = self.gcs.get_file_metadata(self.test_bucket, self.test_file)
        self.assertIsNotNone(metadata, "File metadata should not be None")
        if metadata is not None:  # Type guard to satisfy linter
            self.assertEqual(metadata['name'], self.test_file)
    
    def test_delete_file(self):
        """Test deleting a file from a bucket."""
        delete_result = self.gcs.delete_file(self.test_bucket, self.test_file)
        self.assertTrue(delete_result is not None, "delete_file should return a boolean")
    
    def test_delete_bucket(self):
        """Test deleting a bucket."""
        delete_result = self.gcs.delete_bucket(self.test_bucket)
        self.assertTrue(delete_result is not None, "delete_bucket should return a boolean")


if __name__ == '__main__':
    unittest.main()