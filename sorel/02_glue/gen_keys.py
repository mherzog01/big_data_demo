import json
import boto3
from typing import List
import sys

# Source
BUCKET = 'sorel-20m'
PREFIX = '09-DEC-2020/binaries'
BUCKET_PATH = f's3://{BUCKET}'
SRC_PATH = f'{BUCKET_PATH}/{PREFIX}'

# Target
TARG_BUCKET = 'sorel-20m-demo'
TARG_BUCKET_PATH = f's3://{TARG_BUCKET}'
TARG_PREFIX = 'input'
TARG_PATH = f'{TARG_BUCKET_PATH}/{TARG_PREFIX}'

def logmsg(msg):
    print(msg)

def main(filter_chars):

    logmsg('Process begins')

    s3 = boto3.resource('s3')
    
    def get_objects(filter_chars: str, bucket: str, prefix: str) -> List[str]:
        bucket = s3.Bucket(bucket)
        prefix = f'{prefix}/{filter_chars}'
        objects = bucket.objects.filter(Prefix=prefix)
        return objects
    
    # Get keys
    objects = get_objects(filter_chars, BUCKET, PREFIX)
    object_list = [o for o in objects]
    
    # Write to S3
    content = ""
    for o in objects:
        content += o.key + '\n'
    s3.Object(TARG_BUCKET, f'{TARG_PREFIX}/keys_{filter_chars}.txt').put(Body=content)

    logmsg('Process ends')


if __name__ == '__main__':
    # https://stackoverflow.com/questions/4033723/how-do-i-access-command-line-arguments
    filter_chars = sys.argv[1]
    main(filter_chars)
