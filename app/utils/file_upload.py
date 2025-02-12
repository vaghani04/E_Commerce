import uuid
from google.cloud import storage
from fastapi import UploadFile

async def upload_file_to_gcs(file: UploadFile, folder: str, bucket_name: str, service_account_json: str):
    print(service_account_json)
    client = storage.Client.from_service_account_json(service_account_json)
    bucket = client.bucket(bucket_name)
    filename = f"{folder}/{uuid.uuid4()}_{file.filename}"
    blob = bucket.blob(filename)
    blob.upload_from_file(file.file)
    return blob.public_url
