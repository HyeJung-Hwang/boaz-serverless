import uuid
from typing import Any, Dict
from urllib.parse import unquote_plus

import boto3
from PIL import Image

s3_client = boto3.client("s3")

def resize_image(image_path: str, resized_path: str) -> None:
    with Image.open(image_path) as image:
        image.thumbnail(tuple(x / 4 for x in image.size))
        image.save(resized_path)

def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    for record in event['Records']:
        bucket: str = record['s3']['bucket']['name']
        key: str = unquote_plus(record['s3']['object']['key'])
        tmpkey: str = key.replace('/', '')
        download_path: str = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path: str = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(
            upload_path,
            '{}-resized'.format(bucket), 
            'resized-{}'.format(key)
        )
