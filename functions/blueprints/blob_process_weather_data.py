import logging
import os

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
import azurefunctions.extensions.bindings.blob as blob

bp = func.Blueprint()

@bp.function_name(name="sourceblob")
@bp.blob_trigger(
    arg_name="sourceblob", path="bronze/weatherdata/{name}.json", connection="DATALAKE"
)
def process_blob_weather_data(sourceblob: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob 2 \n"
        f"Properties: {sourceblob.get_blob_properties()}\n"
        f"Blob content head: {sourceblob.download_blob().read(size=1)}"
    )
    account_url = os.environ['DATALAKE__blobServiceUri']
    default_credential = DefaultAzureCredential()
    dest_blob = BlobClient(account_url, credential=default_credential, container_name='silver', blob_name=f'weatherdata/{sourceblob.name}')
    dest_blob.upload_blob(sourceblob.read())
    logging.info(f"Blob {sourceblob.name} copied to silver container")

@bp.function_name(name="sourceblob2")
@bp.blob_trigger(
    arg_name="sourceblob2", path="bronze/weatherdata/{name}", connection="DATALAKE"
)
def process_blob_weather_data2(sourceblob2: blob.BlobClient):
    logging.info(
        f"Python blob trigger function processed blob 2 \n"
        f"Properties: {sourceblob2.get_blob_properties()}\n"
        f"Blob content head: {sourceblob2.download_blob().read(size=1)}"
    )
    account_url = os.environ['DATALAKE__blobServiceUri']
    default_credential = DefaultAzureCredential()
    dest_blob = BlobClient(account_url, credential=default_credential, container_name='silver', blob_name=f'weatherdata2/{sourceblob2.name}')
    dest_blob.upload_blob(sourceblob2.read())
    logging.info(f"Blob {sourceblob2.name} copied to silver container")