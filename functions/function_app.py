import azure.functions as func
import json
import logging
import requests
from functions.blueprints.cron_extract_weather_data import bp as bp_cron_extract_weather_data
from functions.blueprints.http_hello_world import bp as bp_http_hello_world
from functions.blueprints.http_extract_weather_data import bp as bp_http_extract_weather_data

app = func.FunctionApp()

app.register_functions(bp_http_hello_world)
app.register_functions(bp_cron_extract_weather_data)
app.register_functions(bp_http_extract_weather_data)
