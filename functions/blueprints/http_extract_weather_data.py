import logging
import json
import requests
import azure.functions as func
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
from blueprints.shared import generate_blob_path

bp = func.Blueprint()

@bp.route(route="TestWeatherAPI", auth_level=func.AuthLevel.ANONYMOUS)
# @bp.blob_output(arg_name='datalake', path=f'bronze/manual/{_blob_path}', connection='DATALAKE')
def TestWeatherAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        data = requests.get(
            'https://api.open-meteo.com/v1/forecast',
            params={'latitude': '52.374', 'longitude': '4.8897', 'hourly': 'temperature_2m', 'past_days': '1', 'forecast_days': '1'}
            ).json()
    except Exception as e:
        logging.error(e)
        return func.HttpResponse(
            f"Failed to get data from weather API with error {e}",
            status_code=500
        )
    write_to_datalake = req.params.get('writetodatalake')
    if write_to_datalake:
        account_url = os.environ['DATALAKE__blobServiceUri']
        default_credential = DefaultAzureCredential()
        _blob_path = generate_blob_path()
        blob = BlobClient(account_url, credential=default_credential, container_name='bronze', blob_name=f'weatherdata/{_blob_path}')
        try:
            blob.upload_blob(json.dumps(data))
        except Exception as e:
            logging.error(e)
            return func.HttpResponse(
                f"Failed to write to datalake with error {e}",
                status_code=500
            )
    
    return func.HttpResponse(
        json.dumps(data),
        status_code=200,
        mimetype='application/json'
    )