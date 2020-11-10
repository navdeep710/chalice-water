from datetime import datetime

import boto3
from chalice import Chalice

from chalicelib.configuration import get_config
from chalicelib.utils.file_utils import read_file_from_line
from chalicelib.utils.s3_utils import create_presigned_url, download_file

app = Chalice(app_name='apis')

def dummy():
    """
    Collection of all s3.client() functions.
    The sole purpose is to force Chalice to generate the right permissions in the policy.
    Does nothing and returns nothing.
    """
    s3 = boto3.client('s3')
    s3.put_object()
    s3.download_file()
    s3.get_object()
    s3.list_objects_v2()
    s3.get_bucket_location()
    s3.generate_presigned_url()


@app.route('/')
def index():
    if False:
        dummy()
    return {'bit': 'chainalysis'}


@app.route('/get-analytics-api')
def get_analytics_file():
    if app.current_request.query_params != None:
        date = app.current_request.query_params.get('date')
    else:
        date = datetime.now().strftime("%Y-%m-%d")
    url = create_presigned_url(get_config("bucket"),f"daily_data/{date}/daily.csv")
    return url


@app.route('/get-file-content',api_key_required=True)
def get_analytics_file_paginated():
    if app.current_request.query_params != None:
        date = app.current_request.query_params.get('date') or datetime.now().strftime("%Y-%m-%d")
        offset = int(app.current_request.query_params.get('offset')) or 0
        limit = int(app.current_request.query_params.get('limit')) or 1000
        data = read_file_from_line(download_file(f'daily_data/{date}/daily.csv',get_config("bucket"),f'/tmp/{date}/daily.csv'),offset,limit)
        return data
    return {"message":"inadequate_params"}
