
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
  
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'])
BUCKET = 'sorel-20m'
PREFIX = '09-DEC-2020/binaries'
BUCKET_PATH = f's3://{BUCKET}'
import boto3
from typing import List

#filter_chars = '0000'
filter_chars = '0'

s3 = boto3.resource('s3')

def get_all_filepaths(filter_chars: str, bucket: str, prefix: str) -> List[str]:
    bucket = s3.Bucket(bucket)
    prefix = f'{prefix}/{filter_chars}'
    objects = bucket.objects.filter(Prefix=prefix)
    key_list = [f'{BUCKET_PATH}/{o.key}' for o in objects]
    return key_list

# File1_node = glueContext.create_dynamic_frame.from_options(
#    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
#    connection_type="s3",
#    format="binary",
#    connection_options={
#        "paths": get_all_filepaths(filter_chars, BUCKET, PREFIX)
#    }
# )

paths = get_all_filepaths(filter_chars, BUCKET, PREFIX)

#print(len(paths), paths[:10])
#df= File1_node.toDF()
#df= File1_node.toDF()
#df
df = spark.read.format("binaryFile").option("wholeFile","true").load(paths)
#print(df.count())
df_out = df.select('Path')
#df_out.show()
bucket = s3.Bucket('sorel-20m-demo')
objects = bucket.objects.filter(Prefix='tmp/app_output')

for o in objects:
    print(o.key)
    o.delete()

df_out.write.csv('s3://sorel-20m-demo/tmp/app_output')
job.commit()