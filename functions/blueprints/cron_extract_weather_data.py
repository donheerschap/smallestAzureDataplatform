import logging
import datetime
import os
import json
import requests
import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
from shared import generate_blob_path

bp = func.Blueprint()

_blob_path = generate_blob_path()

@bp.function_name(name="mytimer")
@bp.timer_trigger(schedule="0 0 9 * * *", 
              arg_name="mytimer",
              run_on_startup=True) 
def timedWeatherAPI(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now(datetime.UTC).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    account_url = os.environ['DATALAKE__blobServiceUri']
    default_credential = DefaultAzureCredential()
    blob = BlobClient(account_url, credential=default_credential, container_name='raw', blob_name=f'weatherdata/{_blob_path}')

    if mytimer.past_due:
        logging.info('The timer is past due!')

    try:
        data = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={'latitude': '52.374', 'longitude': '4.8897', 'hourly': 'temperature_2m', 'past_days': '2', 'forecast_days': '2'}
            ).json()
    except Exception as e:
        logging.error(e)
    try:
        blob.upload_blob(json.dumps(data))
    except Exception as e:
        logging.error(e)
    
    logging.info('Python timer trigger function ran at %s', utc_timestamp)