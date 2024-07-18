import azure.functions as func
import datetime
import json
import logging
# import requests

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
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
    
# @app.route(route="TestWeatherAPI", auth_level=func.AuthLevel.ANONYMOUS)
# def TestWeatherAPI(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     data = requests.get(
#         'https://api.open-meteo.com/v1/forecast',
#         params={'latitude': '52.374', 'longitude': '4.8897', 'hourly': 'temperature_2m', 'past_days': '1', 'forecast_days': '1'}
#         ).json()
    
#     return func.HttpResponse(
#         json.dumps(data),
#         status_code=200,
#         mimetype='application/json'
#     )