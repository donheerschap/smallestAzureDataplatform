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
    logging.info('Starting to process blob')
    logging.info(
        f"Python blob trigger function processed blob! Perms \n"
        f"Properties: {sourceblob.get_blob_properties()}\n"
        f"Blob content head: {sourceblob.download_blob().read(size=1)}"
    )
    try:
        account_url = os.environ['DATALAKE']
        logging.info(f"account_url: {account_url}")
    except Exception as e:
        logging.error(e)
    try:
        default_credential = DefaultAzureCredential()
        dest_blob = BlobClient(account_url, credential=default_credential, container_name='silver', blob_name=f'weatherdata/{sourceblob.name}')
        dest_blob.upload_blob(sourceblob.read())
        logging.info(f"Blob {sourceblob.name} copied to silver container")
    except Exception as e:
        logging.error(e)