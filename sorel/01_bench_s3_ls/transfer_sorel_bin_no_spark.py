# %% [markdown]
# # Transfer SOREL Binaries without Spark
# 
# Use ```pyarrow``` https://arrow.apache.org/docs/python/
# 
# Other python libraries:  https://stackoverflow.com/questions/32940416/methods-for-writing-parquet-files-using-python
# 
# 

# %%
import boto3
from typing import List
import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import os
import sys

# %%
# Source
BUCKET = 'sorel-20m'
PREFIX = '09-DEC-2020/binaries'
BUCKET_PATH = f's3://{BUCKET}'
SRC_PATH = f'{BUCKET_PATH}/{PREFIX}'

MB = 1024 * 1024

# %%
session = boto3.Session()
s3 = session.resource('s3')

def get_objects(filter_chars: str, bucket: str, prefix: str) -> List[str]:
    bucket = s3.Bucket(bucket)
    prefix = f'{prefix}/{filter_chars}'
    objects = bucket.objects.filter(Prefix=prefix)
    return objects

def get_num_objects(filter_chars):
    objects = get_objects(filter_chars, BUCKET, PREFIX)
    object_list = [o for o in objects]
    return len(object_list)

# TODO Use logger
def logmsg(msg):
    print(msg)

def logmsg01(msg):
    logmsg(f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S}:  {msg}')

# %%
#filter_chars = '0000'
filter_chars = sys.argv[1]
print(f'Filter={filter_chars}')

# %%
objects = get_objects(filter_chars, BUCKET, PREFIX)
num_objects = len([o for o in objects])

#max_size = 1024 * MB
max_size = 100 * MB
cur_size = 0
cur_num_rec = 0
tot_size = 0

delete_target = True

# TODO Add logmsg01
logmsg01('Begins')
start_time = datetime.datetime.now()
d = {'key': [],
        'last_modified': [],
        'size': [],
        'content': []}
for i, o in enumerate(objects):
    num_rec = i + 1
    cur_num_rec += 1
    # Read from S3
    o.load()
    response = o.get()
    content = response['Body'].read()
    #content = None
    d['key'].append(o.key)
    d['last_modified'].append(o.last_modified)
    d['size'].append(o.size)
    d['content'].append(content)
    if i and i % 10 == 0:
        logmsg01(f'i={i}, key={o.key}, cumulative size={cur_size}')
    cur_size += o.size 
    tot_size += o.size
    # if num_rec > 5:
    #     break

    # TODO Write file before size exceeds the limit.  However, if a single file is larger than the max, write it.
    if cur_size > max_size or num_rec == num_objects:
    # Write to parquet
        table = pa.Table.from_pydict(d)

        logmsg01(f'Writing {cur_num_rec} keys with content.  Size={cur_size}.')
        # https://stackoverflow.com/questions/58818227/how-to-write-pyarrow-parquet-data-to-s3-bucket
        pq.write_to_dataset(table, 
                            root_path=f's3://sorel-20m-demo/output_no_spark/{filter_chars}/', 
                            #filesystem=s3,
                            existing_data_behavior="delete_matching" if delete_target else "overwrite_or_ignore",
                            compression='snappy')
        delete_target = False
        cur_size = 0
        cur_num_rec = 0
        d = {'key': [],
                'last_modified': [],
                'size': [],
                'content': []}
end_time = datetime.datetime.now()        
logmsg01(f'Complete.  Processed {num_rec} files.  Total size={tot_size}.  Elapsed={end_time - start_time}')


