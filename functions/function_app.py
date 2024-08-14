import azure.functions as func
import datetime
import json
import logging
import requests

app = func.FunctionApp()

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
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.3",
             status_code=200
        )
    
def generate_blob_path():
    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime('%Y-%m-%d')
    unique_id = str(uuid.uuid4())
    blob_path = f'raw/{date_str}/{unique_id}.json'
    return blob_path

_blob_path = generate_blob_path()
    
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