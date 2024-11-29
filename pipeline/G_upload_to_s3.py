import boto3
import os
from tqdm import tqdm
from boto3.s3.transfer import TransferConfig

# Initialize S3 client
s3 = boto3.client('s3')

try:
    response = s3.list_buckets()
    print("S3 Buckets:", [bucket['Name'] for bucket in response['Buckets']])
except Exception as e:
    print("Error:", e)

# Define the progress bar class
class ProgressPercentage:
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = tqdm.get_lock()

    def __call__(self, bytes_amount):
        # Updates the progress bar
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            tqdm.write(f"{self._filename}: {percentage:.2f}%")

def upload_file_with_progress(local_path, bucket_name, s3_object_key):
    """
    Upload a single file to S3 with a progress bar.

    :param local_path: Path to the local file
    :param bucket_name: S3 bucket name
    :param s3_object_key: S3 object key (path in S3)
    """
    config = TransferConfig(multipart_threshold=5 * 1024 * 1024,  # 5MB threshold for multipart
                            max_concurrency=10,  # Number of threads
                            multipart_chunksize=5 * 1024 * 1024)  # Chunk size 5MB

    try:
        # Upload with a progress callback
        s3.upload_file(local_path, bucket_name, s3_object_key,
                       Config=config,
                       Callback=ProgressPercentage(local_path))
        tqdm.write(f"Uploaded: {local_path} to s3://{bucket_name}/{s3_object_key}")
    except Exception as e:
        tqdm.write(f"Error uploading {local_path}: {e}")

def upload_folder_with_progress(local_folder, bucket_name, s3_folder=""):
    """
    Upload an entire folder to S3 with progress bars for each file.

    :param local_folder: Local folder path
    :param bucket_name: S3 bucket name
    :param s3_folder: Optional S3 folder (path in bucket)
    """
    files_to_upload = []
    for root, _, files in os.walk(local_folder):
        for filename in files:
            local_path = os.path.join(root, filename)
            relative_path = os.path.relpath(local_path, local_folder)
            s3_object_key = os.path.join(s3_folder, relative_path).replace("\\", "/")
            files_to_upload.append((local_path, bucket_name, s3_object_key))

    print(f"Found {len(files_to_upload)} files to upload. Starting uploads...")

    # Use a progress bar for the entire folder
    with tqdm(total=len(files_to_upload), desc="Uploading Files") as pbar:
        for local_path, bucket_name, s3_object_key in files_to_upload:
            upload_file_with_progress(local_path, bucket_name, s3_object_key)
            pbar.update(1)

    print("All uploads completed successfully!")

# Example usage
local_folder = "/data2/fyb/figurative/idiom"
bucket_name = "uot-ii-s3"
s3_folder = "output/google_image_search/idioms/crawled_images"  # Leave empty for root of bucket

upload_folder_with_progress(local_folder, bucket_name, s3_folder)