import datetime
import uuid

def generate_blob_path():
    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime('%Y-%m-%d')
    year_str = current_datetime.strftime('%Y')
    month_str = current_datetime.strftime('%m')
    day_str = current_datetime.strftime('%d')
    unique_id = str(uuid.uuid4())
    blob_path = f'{year_str}/{month_str}/{day_str}/{unique_id}.json'
    return blob_path