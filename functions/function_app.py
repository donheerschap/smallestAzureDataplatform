import azure.functions as func
import datetime
import json
import logging
import requests
import datetime
import uuid
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient

app = func.FunctionApp()

def generate_blob_path():
    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime('%Y-%m-%d')
    unique_id = str(uuid.uuid4())
    blob_path = f'raw/{date_str}/{unique_id}.json'
    return blob_path

_blob_path = generate_blob_path()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.6",
             status_code=200
        )
    
@app.route(route="TestWeatherAPI", auth_level=func.AuthLevel.ANONYMOUS)
@app.blob_output(arg_name='datalake', path=_blob_path, connection='DATALAKE')
def TestWeatherAPI(req: func.HttpRequest, datalake: func.Out[str]) -> func.HttpResponse:
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
        try:
            datalake.set(json.dumps(data))
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

@app.function_name(name="mytimer")
@app.timer_trigger(schedule="0 0 9 * * *", 
              arg_name="mytimer",
              run_on_startup=True) 
def timedWeatherAPI(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.now(datetime.UTC).replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    account_url = os.environ['DATALAKE__blobServiceUri']
    default_credential = DefaultAzureCredential()
    blob = BlobClient(account_url, credential=default_credential, container_name='raw', blob_name=_blob_path)

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