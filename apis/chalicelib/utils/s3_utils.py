import pathlib

import boto3
from botocore.exceptions import ClientError

from chalicelib.configuration import get_config
from chalicelib.utils.custom_logging import log

s3_client = boto3.client('s3', region_name=get_config("region"))

def create_presigned_url(bucket_name, object_name, expiration=3600,region="us-west-2"):
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        log(e)
        return None
    # The response contains the presigned URL
    return response

def ensure_directory_path_for_file(filepath):
    mpath = pathlib.Path(filepath)
    parent_directory = mpath.parent
    parent_directory.mkdir(parents=True, exist_ok=True)


def download_file(filepath, bucket_name, output_filepath,region="us-west-2"):
    ensure_directory_path_for_file(output_filepath)
    with open(output_filepath, 'wb') as f:
        s3_client.download_fileobj(bucket_name, filepath, f)
    return output_filepath