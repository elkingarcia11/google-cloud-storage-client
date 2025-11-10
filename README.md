# Google Cloud Storage Python Client

A lightweight helper around `google-cloud-storage` that focuses on authenticated bucket and object operations using service account credentials.

## Features

- ✅ Create and delete buckets
- ✅ List all buckets in a project
- ✅ Upload files to buckets
- ✅ Download files from buckets
- ✅ List files in buckets (with optional prefix)
- ✅ Delete files from buckets
- ✅ Check bucket existence
- ✅ Get file metadata (size, type, timestamps, MD5)
- ✅ Service account authentication
- ✅ Comprehensive error handling and logging
- ✅ Environment variable support via `.env`
- ✅ Type hints for better development experience

## Installation

### 1. Clone this repository:

```bash
git clone <repository-url>
cd google-cloud-storage-client
```

### 2. Create and activate virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install dependencies:

```bash
# Ensure pip is up to date
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 4. Set up Google Cloud service account:

- Go to Google Cloud Console > IAM & Admin > Service Accounts
- Create a new service account or select an existing one
- Create a new key (JSON format)
- Download the JSON key file to a secure location

### 5. Configure environment variables:

- Copy `.env.example` to `.env` and update the values:

  ```bash
  cp env.example .env
  ```

- Or export the variables directly:

  ```bash
  # Set your project ID
  export GOOGLE_CLOUD_PROJECT_ID="your-google-cloud-project-id"

  # Set the service account credentials
  export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
  ```

### 6. Add service account key to .gitignore:

```bash
echo "/path/to/your/service-account-key.json" >> .gitignore
```

## Quick Start

```python
from google_cloud_storage_client import GoogleCloudStorageClient

# Initialize client (loads variables from .env if present)
gcs = GoogleCloudStorageClient()

# List all buckets
buckets = gcs.list_buckets()
print(f"Available buckets: {buckets}")

# Upload a file
success = gcs.upload_file("my-bucket", "local-file.txt", "remote-file.txt")
print(f"Upload: {'Success' if success else 'Failed'}")

# List files in bucket
files = gcs.list_files("my-bucket")
print(f"Files in bucket: {files}")

# Download a file
success = gcs.download_file("my-bucket", "remote-file.txt", "downloaded-file.txt")
print(f"Download: {'Success' if success else 'Failed'}")
```

## Usage Examples

### Using the GoogleCloudStorageClient Class

```python
from google_cloud_storage_client import GoogleCloudStorageClient

# Initialize client (uses environment variables for authentication)
gcs = GoogleCloudStorageClient()

# Create a bucket
# (Requires Storage Admin permissions)
success = gcs.create_bucket("my-bucket")
print(f"Bucket creation: {'Success' if success else 'Failed'}")

# Upload a file
success = gcs.upload_file("my-bucket", "local-file.txt", "remote-file.txt")
print(f"Upload: {'Success' if success else 'Failed'}")

# Download a file
success = gcs.download_file("my-bucket", "remote-file.txt", "downloaded-file.txt")
print(f"Download: {'Success' if success else 'Failed'}")

# List files with prefix
files = gcs.list_files("my-bucket", prefix="data/")
print(f"Files with prefix 'data/': {files}")

# Get file metadata
metadata = gcs.get_file_metadata("my-bucket", "remote-file.txt")
if metadata:
    print(f"File size: {metadata['size']} bytes")
    print(f"Content type: {metadata['content_type']}")
    print(f"Created: {metadata['created']}")

# Check if bucket exists
exists = gcs.bucket_exists("my-bucket")
print(f"Bucket exists: {exists}")

# Delete a file
success = gcs.delete_file("my-bucket", "remote-file.txt")
print(f"File deletion: {'Success' if success else 'Failed'}")

# Delete bucket (must be empty)
success = gcs.delete_bucket("my-bucket")
print(f"Bucket deletion: {'Success' if success else 'Failed'}")
```

### Error Handling and Logging

```python
import logging
from google_cloud_storage_client import GoogleCloudStorageClient

logging.basicConfig(level=logging.INFO)

# Create client with debug logging
logging.getLogger().setLevel(logging.DEBUG)
gcs_debug = GoogleCloudStorageClient()

# Create client with only warnings and errors
logging.getLogger().setLevel(logging.WARNING)
gcs_quiet = GoogleCloudStorageClient()

# All methods return appropriate values on failure
buckets = gcs_debug.list_buckets()  # Returns empty list if failed
success = gcs_debug.upload_file("bucket", "file.txt", "remote.txt")  # Returns False if failed
metadata = gcs_debug.get_file_metadata("bucket", "file.txt")  # Returns None if file not found
```

## API Reference

### GoogleCloudStorageClient Class

#### Constructor

```python
GoogleCloudStorageClient()
```

#### Methods

- `create_bucket(bucket_name: str) -> bool` - Creates a new bucket
- `delete_bucket(bucket_name: str) -> bool` - Deletes a bucket (must be empty)
- `list_buckets() -> List[str]` - Lists all buckets in the project
- `bucket_exists(bucket_name: str) -> bool` - Checks if a bucket exists
- `upload_file(bucket_name: str, source_file_name: str, destination_blob_name: str) -> bool` - Uploads a file
- `download_file(bucket_name: str, source_blob_name: str, destination_file_name: str) -> bool` - Downloads a file
- `list_files(bucket_name: str, prefix: str = "") -> List[str]` - Lists files in a bucket
- `delete_file(bucket_name: str, blob_name: str) -> bool` - Deletes a file
- `get_file_metadata(bucket_name: str, blob_name: str) -> Optional[dict]` - Gets file metadata

#### Return Values

- **Boolean methods** (`create_bucket`, `delete_bucket`, `upload_file`, `download_file`, `delete_file`): Return `True` on success, `False` on failure
- **List methods** (`list_buckets`, `list_files`): Return list of items on success, empty list `[]` on failure
- **Metadata method** (`get_file_metadata`): Returns dictionary with file info on success, `None` if file not found
- **Existence check** (`bucket_exists`): Returns `True` if bucket exists, `False` otherwise

## Environment Variables

Set the following environment variables:

```bash
# Google Cloud Project ID (REQUIRED)
export GOOGLE_CLOUD_PROJECT_ID="your-google-cloud-project-id"

# Path to your Google Cloud service account key file (REQUIRED)
# Download this from Google Cloud Console > IAM & Admin > Service Accounts
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

**Note**: The `GoogleCloudStorageClient` uses service account authentication and requires both environment variables to be set.

## Service Account Setup

1. **Create a Service Account:**

   - Go to Google Cloud Console
   - Navigate to IAM & Admin > Service Accounts
   - Click "Create Service Account"
   - Give it a name and description

2. **Assign Permissions:**

   - Add the following roles:
     - Storage Admin (for full access)
     - Storage Object Admin (for object operations only)
     - Storage Object Viewer (for read-only access)

3. **Create and Download Key:**

   - Click on the service account
   - Go to Keys tab
   - Click "Add Key" > "Create new key"
   - Choose JSON format
   - Download the key file

4. **Set Environment Variable:**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

## Testing

### Running Integration Tests

The project includes comprehensive integration tests that interact with actual Google Cloud Storage buckets. See the [tests/README.md](tests/README.md) for detailed instructions on:

- Setting up the test environment
- Running individual tests
- Understanding what each test does
- Troubleshooting common issues

### Quick Test Run

```bash
# Activate virtual environment
source venv/bin/activate

# Set environment variables
export GOOGLE_CLOUD_PROJECT_ID="your-project-id"
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"

# Run all integration tests
python -m pytest tests/integration_test.py -v

# Run a specific test
python -m pytest tests/integration_test.py::TestIntegrations::test_create_bucket -v
```

## Advanced Features

### Logging

Each `GoogleCloudStorageClient` instance attaches a logger named after the module and class. Configure logging globally or add handlers on the returned logger to suit your needs:

```python
import logging
from google_cloud_storage_client import GoogleCloudStorageClient

logging.basicConfig(level=logging.INFO)
client = GoogleCloudStorageClient()

# Override level for this client only
client.logger.setLevel(logging.DEBUG)
```

### Error Handling

All methods return appropriate values on failure and log errors for debugging:

- **Boolean methods**: Return `False` on failure
- **List methods**: Return empty list `[]` on failure
- **Metadata method**: Returns `None` if file not found
- **All methods**: Log errors with detailed information

### Permissions

Some operations require specific permissions for your service account:

- **Storage Admin**: For creating/deleting buckets
- **Storage Object Admin**: For uploading/deleting files
- **Storage Object Viewer**: For listing and downloading files

If your service account lacks permissions, the module will log warnings and return appropriate failure values.

---

For more details, see the code and docstrings in `google_cloud_storage_client.py`.
