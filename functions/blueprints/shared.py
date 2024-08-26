import datetime
import uuid

def generate_blob_path():
    current_datetime = datetime.datetime.now()
    date_str = current_datetime.strftime('%Y-%m-%d')
    unique_id = str(uuid.uuid4())
    blob_path = f'{date_str}/{unique_id}.json'
    return blob_path