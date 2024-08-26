import logging
import os

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
import azurefunctions.extensions.bindings.blob as blob

bp = func.Blueprint()

@bp.blob_trigger(
    arg_name="source_blob", path="bronze/weatherdata", connection="DATALAKE"
)
def process_blob_weather_data(source_blob: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob \n"
        f"Properties: {source_blob.get_blob_properties()}\n"
        f"Blob content head: {source_blob.download_blob().read(size=1)}"
    )
    account_url = os.environ['DATALAKE__blobServiceUri']
    default_credential = DefaultAzureCredential()
    dest_blob = BlobClient(account_url, credential=default_credential, container_name='silver', blob_name=f'weatherdata/{source_blob.name}')
    dest_blob.upload_blob(source_blob.read())
    logging.info(f"Blob {source_blob.name} copied to silver container")