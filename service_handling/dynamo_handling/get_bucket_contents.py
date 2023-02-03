from random import shuffle

import boto3
import os
from dotenv import load_dotenv

from helpers import get_filename
from metadata.file_metadata import Metadata


def get_bucket_contents():
    load_dotenv()
    s3_bucket_name = os.environ.get("S3_BUCKET_NAME")
    s3 = boto3.client("s3")
    bucket_name = s3_bucket_name
    bucket_objects = s3.list_objects(Bucket=bucket_name)["Contents"]
    shuffle(bucket_objects)
    for key in bucket_objects:
        yield key["Key"]


def main():
    res = {}
    contents = get_bucket_contents()

    for key in contents:
        filename = get_filename(key)

        metadata = Metadata(filename)

        res[metadata.emotion_1_id] = filename

    #     # item = {"filename": filename,
    #     #         "emotion_id": metadata.emotion_1_id}
    for key, val in res.items():
        print('"' + str(key) + '": "' + val + '",')



if __name__ == "__main__":
    main()
