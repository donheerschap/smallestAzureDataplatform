import logging

import azure.functions as func

bp = func.Blueprint()

@bp.function_name(name="blobTriggerWeatherData")
@bp.blob_trigger(
    arg_name="blob", path="raw/weatherdata", connection="DATALAKE"
)
def process_blob_weather_data(myblob: func.InputStream):
   logging.info(f"Python blob trigger function processed blob \n"
                f"Name: {myblob.name}\n"
                f"Blob Size: {myblob.length} bytes")