# Search a large S3 bucket using parallel processing

# Partition the bucket by the first two characters in the prefix

# https://stackoverflow.com/questions/75759423/high-volume-read-of-many-keys-in-an-s3-bucket/75779792#75779792
import boto3
import ctypes
import multiprocessing
import datetime

def validate_hex_digits(s3, bucket, prefix):
    # Make sure the first character under the prefix is some hex digit
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix, MaxKeys=1)
    assert('0' <= resp['Contents'][0]['Key'][len(prefix)] <= 'f')
    # Make sure there's nothing after 'f'
    resp = s3.list_objects_v2(Bucket=bucket, Prefix=prefix + "g", MaxKeys=1, StartAfter=prefix+'g')
    assert('Contents' not in resp)

def worker(queue, queue_out, jobs):
    # A single worker, pull a job from 'queue', send results to 'queue_out'
    # Use jobs value to track the number of jobs in flight
    s3 = boto3.client('s3')
    while True:
        with jobs.get_lock():
            if jobs.value == 0:
                # Nothing left to do
                queue_out.put(None)
                break
            jobs.value -= 1
            bucket, prefix, token = queue.get()
        # Build up args for the call to list_objects
        args = {
            "Bucket": bucket,
            "Prefix": prefix,
        }
        if token is not None:
            args["ContinuationToken"] = token
        resp = s3.list_objects_v2(**args)
        if 'Contents' in resp:
            queue_out.put(resp['Contents'])
        if 'NextContinuationToken' in resp:
            # There's another page for this prefix, send it off
            # for the next available worker to pick up
            with jobs.get_lock():
                queue.put((bucket, prefix, resp['NextContinuationToken']))
                jobs.value += 1

def logmsg(msg):
    print(msg)

def logmsg01(msg):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logmsg(f'{timestamp}: {msg}')

def main():

    logmsg01('Process begins')

    bucket = 'sorel-20m'
    prefix = '09-DEC-2020/binaries/'

    s3 = boto3.client('s3')

    # Verify all of the objects are at least two digit hex digits under the prefix
    validate_hex_digits(s3, bucket, prefix)
    for i in range(16):
        validate_hex_digits(s3, bucket, prefix + f"{i:x}")

    # If we get here, all the keys follow the pattern we expect for at 
    # least two digits.  Go ahead and use multi processing to pull down 
    # the list of objects as fast as possible

    # A queue to store work items
    queue = multiprocessing.Queue()
    # A queue to get pages of results
    queue_out = multiprocessing.Queue()
    # How many jobs are left to process?
    jobs = multiprocessing.Value(ctypes.c_int, 0)
    # Place some seeds in the queue for the first two hex characters
    for i in range(256):
        queue.put((bucket, prefix + f"{i:02x}", None))
        jobs.value += 1
    # Create and start some worker threads, two per process 
    # to allow for network wait time
    workers = multiprocessing.cpu_count() * 2
    procs = []
    for _ in range(workers):
        proc = multiprocessing.Process(target=worker, args=(queue, queue_out, jobs))
        proc.start()
        procs.append(proc)

    # While the workers are working, pull down objects and process them
    num_found = 0
    tot_size = 0
    print(f'Listing contens of {bucket}/{prefix} with {workers} workers')
    while workers > 0:
        result = queue_out.get()
        if result is None:
            # Signal that a worker finished
            workers -= 1
        else:
            for cur in result:
                # Just show the results like the AWS CLI does
                #print(f"{cur['LastModified'].strftime('%Y-%m-%d %H:%M:%S')} {cur['Size']:10d} {cur['Key'][len(prefix):]}")
                num_found += 1
                tot_size += cur['Size']
                if num_found % (1000 * 1000) == 0:
                    logmsg01(f'Found {num_found}.  # workers = {workers}.')

    logmsg01('Process ends')
    return (num_found, tot_size)

    # Clean up
    for proc in procs:
        proc.join()

if __name__ == "__main__":
    main()
    # Number of files = 9,919,065
    # Size of data = 9,520,774,877,970
